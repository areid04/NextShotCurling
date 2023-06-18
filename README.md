# NextShotCurling
Landing page for an upcoming project combining computer-vision and machine learning regression to determine a "next shot" in the sport of curling.

## Scope of this project
This project aims to be a showcase of computer vision and machine learning skills. Data collected will be at the championship level, though across different events.
For those new to curling (described as 'chess on ice'), player's main objectives are to maximize points won in an end and minimize points lost. In short, you chuck a 20 kilo stone across a sheet of ice and score based on where your stones are relative to the button (center) of the house (the big colored rings) and to the opponent's stones. A primer on curling and the terminologies can be found online, but to scale back the project scope a bit a knowledge of these terms won't be neccisary.

## What this is, and what it isn't

As some one who curls at the college level, I wanted to develop a tool that could help me make stronger decisions of what my next shot should be. Granted, I wouldnt have acsess to such a program when I'm on the ice... but as a learning tool and experiment, I think NextShotCurling could be an interesting aid. This project aims to answer the question *** can I determine what shot I should make, depending on the posistion of all the other stones in play? ***

This isn't (yet!) a replacement for skill or knowledge of the game, and predictions of shots don't factor in your level of play, your own accuracy, or ability of sweepers. For this early iteration, there are also some conceptiual leaps that users will be expected to do inorder to interpret predicted shots; depending on context, you might need to come in with some extra weight (curling jargon for power / speed, in a sense) to knock another stone out, or you might want to gently rest your stone ontop of another. For such predictions, I'll have to consider another method of data collection that can estimate a weight paramter (such as tracking the frames of a curling match video), though this ability is out of my current skillset. 

# Project Outline
Here's a rough outline for what I'll do for this project

## I. Collect data
Worldcurling.org provides shot-by-shot diagrams for their matches, an incredibly valueable resource that I'll be using as data.
Each image will be read into an OpenCV function that extracts stone posistions for that play, with the shot with a bold outline being the stone thrown.
This "shot made" stone will be the feature that I'll want to derive, based on all other stones posistions. The stones will be stored in the format

**Other stone** n_x, **Other stone** n_y with n ranging from 1-15 with the stone that we'll be determine being **Made shot**x, **Made shot**y.

### Issues with collecting the data
Since the order in which inputs come in matters for regression models, I think this might be the biggest obsticle for this project. That is, thinking of a way to make the model _ _permuation-invarient_ _ or atleast fairly. 
It shouldn't matter what order the stone's coordinates come in; stones exist in a space regardless of the previous stones posistion. [This](https://github.com/off99555/superkeras/blob/master/README.md) repo seems like it could be helpful in keeping this property.
Alternatively, maybe sorting by largest / smallest could help? 

## II. Train

Train with TensorFlow or sklearn. 

## III. UI

Helpful UI to help input data to be predicted and visualize this data.

