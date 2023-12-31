# NextShotCurling
Landing page for an upcoming project combining computer vision and machine learning regression to determine a "next shot" in the sport of curling.

## Scope of this project
This project aims to showcase computer vision and machine learning skills. Data collected will be at the championship level, though across different events.
For those new to curling (described as 'chess on ice'), the player's main objectives are to maximize points won in the end and minimize points lost. In short, you chuck a 20-kilo stone across a sheet of ice and score based on where your stones are relative to the button (center) of the house (the big colored rings) and to the opponent's stones. A primer on curling and the terminologies can be found online, but a knowledge of these terms won't be necessary.

## What this is, and what it isn't

As someone who curls at the college level, I wanted to develop a tool that could help me make stronger decisions about what my next shot should be. Granted, I wouldn't have access to such a program when I'm on the ice... but as a learning tool and experiment, NextShotCurling could be an interesting aid. This project aims to answer the question **can I determine what shot I should make, depending on the position of all the other stones in play?**

This isn't (yet!) a replacement for skill or knowledge of the game, and predictions of shots don't factor in your level of play, your own accuracy, or the ability of sweepers. For this early iteration, there are also some conceptual leaps that users will be expected to do in order to interpret predicted shots; depending on the context, you might need to come in with some extra weight (curling jargon for power/speed, in a sense) to knock another stone out, or you might want to gently rest your stone on top of another. For such predictions, I'll have to consider another method of data collection that can estimate a weight parameter (such as tracking the frames of a curling match video), though this ability is out of my current skill set. 

# Project Outline
Here's a rough outline of what I'll do for this project

## I. Collect data
Worldcurling.org provides shot-by-shot diagrams for their matches, an incredibly valuable resource that I'll be using as data.
Each image will be read into an OpenCV function that extracts stone positions for that play, with the shot with a bold outline being the stone thrown.
This "shot made" stone will be the feature that I'll want to derive, based on ~~all other stones' positions ~~ zone location. When a stone is in the mask region, I'll add one to the region.

### Issues with collecting the data
Since the order in which inputs come in matters for regression models, I think this might be the biggest obstacle for this project. That is, thinking of a way to make the model _ _permuation-invarient_ _ or at least fairly. 
It shouldn't matter what order the stone's coordinates come in; stones exist in space regardless of the previous stones' position. [This](https://github.com/off99555/superkeras/blob/master/README.md) repo seems like it could be helpful in keeping this property.
Alternatively, maybe sorting by largest / smallest could help. 

UPDATE:
Instead of tracking the absolute position of the stones, it might be easier to track how many stones are in certain areas. This does track relative position, which could be useful data. It also doesn't matter which stone is where, but rather having some sort of count.

![ZoneDiagram](https://github.com/areid04/NextShotCurling/assets/114508072/b421f611-d06d-42fb-b0af-93ff2f955cf6)

Below is the "more mask" version, following the same label principle (without text, they're just too small.)

![AOIpng](https://github.com/areid04/NextShotCurling/assets/114508072/0fc49bb5-ae1a-4c21-b986-7b2e3af58bf6)

I also updated the CV data retrieval process to ignore the thrown stone's position from the count (obviously I shouldn't include the thrown stone's position when determining the thrown stone!!). I have an idea to re-do this check by instead shifting stone X,y actual values up a row (for example, the "predicted" stone thrown for E1S1 would be the detected stone found at E1S2, and so on.)

I'm wondering how feasible it would be to store data based on the stone's color (such as g1r/g1y...)

I'm also using some pretty poor data; I'm including the "ghost" positions of stones that I really shouldn't be.

6/20/23 10:13 Update:
I figured out how to ignore the ghost stones (indicated by a hollow circle). I now have a more accurate representation of the stones on the board. I almost went back on this though when I realized that I shouldn't predict the x,y thrown stone cords from the board AFTER the stone was thrown in the first place!
Reason is: since I'm using shot-by-shot data, I'm really just looking at the stone's positions AFTER the stone was thrown when I really want to have them BEFORE the stone was thrown. Hits, bumps, etc. didn't exist until the stone was thrown.

Solution:
Since I capture the response to the board on the NEXT end, I can shift the X and Y columns up one.
```
              =>            
info x y              info x1 y1
info x1 y1              info x2 y2
info x2 y2              info x3 y3
info x3 y3              info null null
```
This will result in the final shot of the final end not having a predicted best shot (which kind of makes sense, the game ended.)
I'll have to add a white space row for this deletion.

## II. Train

Through the first round of tests, I was able to get an r^2 score of 0.222 when using lasso regression. I'll include more masks to improve this.
Update: I'm no longer using r^2 as a metric to score, instead using MAE. 
Also, my attempt to create a regression model with TensorFlow NN yields a larger MAE than that of the Random Forest Regressor. Probably going to continue with this route rather than work with two models at the same time and choose a winner. As I get access to more shots, I'll try again in a later attempt.

Update 6/21/23 11:48 PM:
It seems like my training has hit a plateau; MAE is 30 for x dimensions and 60 for y dimensions. I think this is a good starting place for the project, especially for developing a UI.

## III. UI

Helpful UI to help input data to be predicted and visualize this data.

![image](https://github.com/areid04/NextShotCurling/assets/114508072/b04371a9-0532-4a5f-a2af-2c7c4cc91168)


I'd like to keep things as simple and intuitive as possible; left click for red stones, right-click for yellow stones (though the difference doesn't reflect in the model, might do that in a future update..), and enter to run the mask/retrieval function, to give a zone estimating where you should place your stone.

Some next steps would be including takeouts and hits as part of the data set!


