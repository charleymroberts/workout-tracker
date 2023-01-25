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


#Option One: Add minutes

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
            print(f"Minutes added successfully!\n") 
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


#Option Two: view this week's progress against targets

def view_progress_this_week():
    '''
    Calculates how many minutes the user has entered for each exercise during the current week and compares the total with their targets
    '''
    minutes_data = minutes.get_values(value_render_option=ValueRenderOption.unformatted)

    this_week = datetime.now().isocalendar()[1] 
    cardio_this_week = []
    weights_this_week = []
    swimming_this_week = []

    for row in minutes_data:
        if row[5] == this_week:
            cardio_this_week.append(row[0])
            weights_this_week.append(row[1])
            swimming_this_week.append(row[2])

    cardio_this_week = (sum(cardio_this_week))
    weights_this_week = (sum(weights_this_week))
    swimming_this_week = (sum(swimming_this_week))

    targets = SHEET.worksheet("weekly_targets").get_values(value_render_option=ValueRenderOption.unformatted)
    most_recent_targets = targets[-1]
    cardio_target = most_recent_targets[0]
    weights_target = most_recent_targets[1]
    swimming_target = most_recent_targets[2]

    cardio_minutes_to_go = cardio_target - cardio_this_week

    if cardio_target > cardio_this_week:
        print(f"You have done {cardio_this_week} minutes of cardio so far this week. Your target is {cardio_target} minutes. You have {cardio_minutes_to_go} minutes to go. Keep it up!")
    else:
        print(f"You have done {cardio_this_week} minutes of cardio so far this week. Your target was {cardio_target} minutes. Well done!")


    weights_minutes_to_go = weights_target - weights_this_week

    if weights_target > weights_this_week:
        print(f"You have done {weights_this_week} minutes of weight training so far this week. Your target is {weights_target} minutes. You have {weights_minutes_to_go} minutes to go. Keep it up!")
    else:
        print(f"You have done {weights_this_week} minutes of weight training this week. Your target was {weights_target} minutes. Well done!")


    swimming_minutes_to_go = swimming_target - swimming_this_week

    if swimming_target > swimming_this_week:
        print(f"You have done {swimming_this_week} minutes of swimming so far this week. Your target is {swimming_target} minutes. You have {swimming_minutes_to_go} minutes to go. Keep it up!\n")
    else:
        print(f"You have done {swimming_this_week} minutes of swimming this week. Your target was {swimming_target} minutes. Well done!\n")


#Option Three: Add new targets

def print_current_targets():
    '''
    Displays user's current weekly targets
    '''
    targets = SHEET.worksheet("weekly_targets").get_values()
    headings = targets[0]
    most_recent_targets = targets[-1]
    
    targets_list = zip(headings, most_recent_targets)
    print(f"Your current weekly targets are: ") 

    print(targets[0][0].capitalize() + ": " + targets[-1][0] + " minutes per week") #cardio
    print(targets[0][1].capitalize() + ": " + targets[-1][1] + " minutes per week") #weights 
    print(targets[0][2].capitalize() + ": " + targets[-1][2] + " minutes per week") #swimming 


def edit_targets():
    """
    Takes user input for new targets, adds them to a list and appends them to the 'targets' spreadsheet
    """
    print_current_targets()
    print("Please enter your new weekly targets for each exercise: \n")
    #put something here to make sure the user enters a number
    while True:
        try: 
            new_cardio_target = int(input("New cardio target (minutes per week): "))
            new_weights_target = int(input("New weights target (minutes per week): ")) 
            new_swimming_target = int(input("New swimming target (minutes per week): "))
            break 
        except ValueError:
            print("Please enter a number") #this sends it back to the top of the try statement

    updated_targets = []
    updated_targets.append(new_cardio_target)
    updated_targets.append(new_weights_target)
    updated_targets.append(new_swimming_target)

    targets.append_row(updated_targets)
    print("Targets updated!")


#Option Four: view minutes completed for each exercise over the last four weeks

def view_previous_weeks():
    """
    Calculates and displays average times for each exercise for the last four whole weeks
    """
    #Currently just cardio, add options for weights and swimming
    #Add an option to ask the user which exercise they want to view
    #also refactor the code to just use the exercise name instead of writing out similar code three times

    minutes_data = minutes.get_values(value_render_option=ValueRenderOption.unformatted)

    this_week = datetime.now().isocalendar()[1]

    cardio_one_week_ago = []
    cardio_two_weeks_ago = []
    cardio_three_weeks_ago = []
    cardio_four_weeks_ago = []

    for row in minutes_data:
        if row[5] == this_week - 1:
            cardio_one_week_ago.append(row[0])
        elif row[5] == this_week - 2:
            cardio_two_weeks_ago.append(row[0])
        elif row[5] == this_week - 3:
            cardio_three_weeks_ago.append(row[0])
        elif row[5] == this_week - 4:
            cardio_four_weeks_ago.append(row[0])
        else:
            pass
        
    cardio_one_sum = sum(cardio_one_week_ago)
    cardio_two_sum = sum(cardio_two_weeks_ago)
    cardio_three_sum = sum(cardio_three_weeks_ago)
    cardio_four_sum = sum(cardio_four_weeks_ago)

    print(f"Last week you did {cardio_one_sum} minutes of cardio")
    print(f"Two weeks ago you did {cardio_two_sum} minutes of cardio")
    print(f"Three weeks ago you did {cardio_three_sum} minutes of cardio")
    print(f"Four weeks ago you did {cardio_four_sum} minutes of cardio")


#Option Five: Exit program

def close_program():
    '''
    Ends program
    '''
    print(f"Exiting workout tracker. See you soon!") #why can't it see the username from here


#User menu:

def show_options():
    '''
    Presents a menu for user to select which part of the program they want to run
    '''
    while True:
        print("What would you like to do today? Please select a number:")
        option = input("1. Enter minutes / 2. View progress this week / 3. Update targets / 4. View last four weeks / 5. Exit ")

        if option == "1":
            enter_exercise_data()
        elif option == "2":
            view_progress_this_week()
        elif option == "3":
            edit_targets()
        elif option == "4":
            view_previous_weeks()
        elif option == "5":
            close_program()
            break
        else:
            print("Please enter a number 1-5")

#Main function to run program:

def main():
    username = greet_user()
    show_options()

main()