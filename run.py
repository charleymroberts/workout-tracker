import gspread
from gspread.utils import ValueRenderOption

from google.oauth2.service_account import Credentials

from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('workout_tracker')

minutes = SHEET.worksheet('minutes')
targets = SHEET.worksheet('weekly_targets')

entry = {'cardio': 0, 'weights': 0, 'swimming': 0, 'todays_date': 0, 'day_of_week': '', 'week_number': 0}
'''
Dictionary to hold number of minutes inputted by user, which is converted to a list and pushed to Google sheet by the add_data_to_worksheet function
'''

def greet_user():
'''
Collects the user's name and displays personalised greeting
'''
    username = input("Please enter your name: ")
    print(f"Hi, {username}, good to see you today!\n")
    return username


def enter_exercise_type():
'''
Collect input from user about which type of exercise they want to add minutes to
'''
    while True:
        exercise = input("Which exercise did you do today? (cardio/weights/swimming): ").lower()
        if exercise == "cardio" or exercise == "weights" or exercise == "swimming":
            return exercise
        else:
            print("Please choose either cardio, weights or swimming")


def enter_minutes():
'''
Collects user input for how many minutes they did, and displays a message depending on the number of minutes
'''
    while True:
        try:
            minutes = float(input("How many minutes did you do?: "))
            break
        except ValueError:
            print("Please enter a number")

    if minutes > 0 and minutes <= 15:
        print("Good job, every little helps!\n")
    elif minutes > 15:
        print("Well done! You rock!\n")
    elif minutes == 0:
        print("Ok, no worries\n")
    else:
        print("Error\n")

    return minutes


def add_data(exercise, minutes):
'''
Adds the number of minutes to the correct exercise in the 'entry' dictionary
'''
    if exercise == "cardio":
        entry['cardio'] = minutes
    elif exercise == "weights":
        entry['weights'] = minutes
    elif exercise == "swimming":
        entry['swimming'] = minutes
    else:
        print("Error, please try again")


def enter_exercise_data():
'''
Asks the user if they want to add more data, and keeps offering this option until the user confirms they have finished
'''
    while True: 
        exercise = enter_exercise_type()
        minutes = enter_minutes()
        add_data(exercise, minutes)
        print("Are you done for today?")
        restart = input("Press y to finish or press any key to enter more exercise \n").lower()
        if restart == "y":
            add_datetime()
            add_data_to_worksheet()
            print(f"Minutes added successfully. See you tomorrow, {username}!")
            break


def add_datetime():
'''
Adds today's date, day of the week and week number to the entry dictionary
'''
    the_date = datetime.now().date()
    the_day = datetime.now().weekday() 
    this_week = datetime.now().isocalendar()[1]

    entry['todays_date'] = str(the_date) 
    entry['day_of_week'] = the_day
    entry['week_number'] = this_week


def add_data_to_worksheet():
'''
Converts the dictionary values to a list and pushes this to the Google sheet 'minutes' as the most recently added row
'''
    new_data = list(entry.values())
    minutes.append_row(new_data)
