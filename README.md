# Workout Tracker

Workout Tracker is a command-line Python program which enables users to record the amount of time they spend doing different types of exercise.  Users can set themselves weekly targets for each type of exercise and view how much progress they have made towards meeting the current week's target.  The app also enables them to view how much time they spent on each exercise over the preceeding four weeks.

It is displayed to the user in a web browser using Code Institute's mock terminal Heroku template.

The live version of the app is here: https://cr-workout-tracker.herokuapp.com/

## Users and their goals

## What it does

## Features

### Existing features

### Design

### Features that would be added for real-world deployment

### Future features

## Testing

(Testing done)

### Bugs (fixed/remaining)

(Needing to format Google Sheet to be number rather than automatic data type?)

### Validator testing

The code was passed through Code Institute's Python Linter https://pep8ci.herokuapp.com/ with no remaining issues. (screenshot?)

## Deployment process

## Technologies used

Python 3
Heroku
(plus HTML, CSS and Javascript within the Heroku template provided by Code Institute)

## Credits

Heroku template provided by Code Institute
Instructions on connecting Google Sheets to VSCode taken from Code Institute's 'Love Sandwiches' walkthrough project

![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome Charley Roberts,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!