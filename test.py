import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import cv2


def get_rock_positions(image_path):
    """
    Given a path to the standard sheet overview (image_path) as a string, returns a
    pandas DataFrame with all rock positions in terms of pixel positions in
    the image, and the rock color (Red or Yellow), and the size of the rock
    (useful for removing the unthrown ones without a position cut that could
    prove problematic in the extreme edge case of a rock that isn't fully past the hog
    line but is still in play because it collided  with a rock past the hog line.

    NB: The output requires further post-processing to flip the rocks to the correct
    coordinate system (origin at the center of the button) and extract the
    direction of play, as well as remove the rocks that are out of play or yet
    to be thrown.
    """

    # The discussion here indicates that assembling a list of dicts for each row
    # is a pretty fast way of getting a structure we can easily convert to a
    # DataFrame.  So set that up now:
    # https://stackoverflow.com/questions/10715965/add-one-row-to-pandas-dataframe
    row_list = []

    # Dictionary keys will be ["color", "x", "y", "size"]

    # Start by reading in the image.
    img = cv2.imread(image_path)

    # Convert this to a binary image for each stone color.
    # (White where the stones are, black everywhere else).
    # Red stones are just solid red circles
    red_bin = cv2.inRange(img, (0, 0, 255), (0, 0, 255))

    # Yellow stones that have been thrown already are yellow circles that also
    # have an X in them that is part blue and part greyish-yellow.  So that the
    # contour finding works properly, we need to OR all these binary images
    # together so that played rock contours are detected as circles.
    # In most cases yellow is (B,G,R) = (0,255,255).  It looks like when the
    # house is yellow-ish sometimes it is darker.  So expand the range to allow
    # (0,193,255).  Should still be specific enough not to trigger on the house.
    # In this case, blue takes on a little bit of green too.
    # Also need to expand greyish-yellow out to allow (0, 178, 239)
    yellow_bin = cv2.inRange(img, (0, 192, 255), (0, 255, 255))
    blue_bin = cv2.inRange(img, (255, 0, 0), (255, 63, 0))

    # Greyish-yellow appears to employ two shades in some instances.  Use them
    # as the bounds of the range.
    # Original before the "off yellow" expansion:
    # (32,207,207), (32,223,223)
    # Increse G by 1 for another shade of grey found (sometimes (rarely) a black X is
    # used through the yellow stones.  Adding black is problematic for this
    # algorithm though (triggers on all the lines), so will not do that.
    greyish_yellow_bin = cv2.inRange(img, (0, 164, 207), (32, 224, 239))

    yellow_rocks = cv2.bitwise_or(yellow_bin, cv2.bitwise_or(blue_bin,
                                                             greyish_yellow_bin))

    # Loop over red and yellow, and fill the row_list, one rock position per
    # row.
    rock_bin_dict = {"red": red_bin, "yellow": yellow_rocks}.items()
    for color, rock_bin in rock_bin_dict:

        # Get the contours, using RETR_TREE so can use hierarchy to remove contours within
        # contours (unfilled circles denoting positions of rocks that were
        # moved)
        contours, hierarchy = cv2.findContours(rock_bin, cv2.RETR_TREE,
                                               cv2.CHAIN_APPROX_NONE)

        # We want to remove all contours that have contours within them or are
        # within contours, as these are former positions of rocks, which we
        # don't need to store.
        # Such contours have parents or children (the last 2 entries in the
        # hierarchy for the contour), so we need to only keep contours whose
        # last 2 hierarchy numbers are both -1.
        only_rocks = np.array(contours)[np.all(hierarchy[0, :, 2:4] == -1,
                                               axis=1)]

        # Finally, loop over the remaining contours in only_rocks and get the
        # centroids to get the rock positions, appending them with their color
        # to row_list.
        # Note: In the case of partial rock previous positions, the area, M['m00'],
        # comes up as zero.  To guard against division by zero, divide by the
        # maximum of M['m00'] and 1.
        for cnt in only_rocks:
            M = cv2.moments(cnt)
            cx = M['m10'] / max(M['m00'], 1)
            cy = M['m01'] / max(M['m00'], 1)

            row_list.append({"color": color, "x": cx, "y": cy, "size": M['m00']})

    # Now that we've looped over both colors and all rocks with those colors,
    # turn the row_list to a DataFrame and return it.