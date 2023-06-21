# NextShotCurling
Landing page for an upcoming project combining computer-vision and machine learning regression to determine a "next shot" in the sport of curling.

## Scope of this project
This project aims to be a showcase of computer vision and machine learning skills. Data collected will be at the championship level, though across different events.
For those new to curling (described as 'chess on ice'), player's main objectives are to maximize points won in an end and minimize points lost. In short, you chuck a 20 kilo stone across a sheet of ice and score based on where your stones are relative to the button (center) of the house (the big colored rings) and to the opponent's stones. A primer on curling and the terminologies can be found online, but to scale back the project scope a bit a knowledge of these terms won't be neccisary.

## What this is, and what it isn't

As some one who curls at the college level, I wanted to develop a tool that could help me make stronger decisions of what my next shot should be. Granted, I wouldnt have acsess to such a program when I'm on the ice... but as a learning tool and experiment, I think NextShotCurling could be an interesting aid. This project aims to answer the question **can I determine what shot I should make, depending on the posistion of all the other stones in play?**

This isn't (yet!) a replacement for skill or knowledge of the game, and predictions of shots don't factor in your level of play, your own accuracy, or ability of sweepers. For this early iteration, there are also some conceptiual leaps that users will be expected to do inorder to interpret predicted shots; depending on context, you might need to come in with some extra weight (curling jargon for power / speed, in a sense) to knock another stone out, or you might want to gently rest your stone ontop of another. For such predictions, I'll have to consider another method of data collection that can estimate a weight paramter (such as tracking the frames of a curling match video), though this ability is out of my current skillset. 

# Project Outline
Here's a rough outline for what I'll do for this project

## I. Collect data
Worldcurling.org provides shot-by-shot diagrams for their matches, an incredibly valueable resource that I'll be using as data.
Each image will be read into an OpenCV function that extracts stone posistions for that play, with the shot with a bold outline being the stone thrown.
This "shot made" stone will be the feature that I'll want to derive, based on ~~all other stones posistions~~ zone location. The stones will be stored in the format

**Other stone** n_x, **Other stone** n_y with n ranging from 1-15 with the stone that we'll be determine being **Made shot**x, **Made shot**y.

### Issues with collecting the data
Since the order in which inputs come in matters for regression models, I think this might be the biggest obsticle for this project. That is, thinking of a way to make the model _ _permuation-invarient_ _ or atleast fairly. 
It shouldn't matter what order the stone's coordinates come in; stones exist in a space regardless of the previous stones posistion. [This](https://github.com/off99555/superkeras/blob/master/README.md) repo seems like it could be helpful in keeping this property.
Alternatively, maybe sorting by largest / smallest could help? 

UPDATE:
Instead of tracking the absolute posistion of the stones, it might be easier to track how many stones are in certain areas? This does track relative posistion, which could be useful data. It also doesn't matter which stone is where, but rather having some sort of count.

![ZoneDiagram](https://github.com/areid04/NextShotCurling/assets/114508072/b421f611-d06d-42fb-b0af-93ff2f955cf6)

I also updated the CV data retreveal process to ignore the thrown stone's posistion from the count (obviously I shouldnt include the thrown stone's posistion when determining the thrown stone!!). I have an idea to re-do this check by instead shifting stone X,y actual values up a row (for example, the "predicted" stone thrown for E1S1 would be the detected stone found at E1S2, and so on.)

I'm wondering how feasible it would be to store data baased on the stone's color (such as g1r/y...)

I'm also using some pretty poor data; I'm including the "ghost" posistions of stones that I really shouldn't be.


## II. Train

Trough a first round of tests, I was able to get an r^2 score of 0.222 when using lasso regression. I'll include more masks to improve this.
Update: I'm no longer using r^2 as a metric to score, instead using MAE. 
Also, my attempt to create a regression model with tensorflow NN yeilds larger MAE than that of the Random Forest Regressor. Probably going to continue with this route rather than work with two models at the same time and choose a winner. As I get acsess to more shots, I'll try again in a later attempt.

## III. UI

Helpful UI to help input data to be predicted and visualize this data. Probably going to do something like stamp/send.

