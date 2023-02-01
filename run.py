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
    global username #this is set to global so that the close_program function can access it
    username = input("Please enter your name: \n")
    print(f"Hi, {username}, good to see you today!\n")


#Option One: Add minutes

def enter_exercise_type():
    '''
    Collect input from user about which type of exercise they want to add minutes to
    '''
    while True:
        exercise = input("Which exercise did you do today? (cardio/weights/swimming): \n").lower()
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
            minutes = float(input("How many minutes did you do?: \n"))
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
    minutes_data = SHEET.worksheet("minutes").get_values(value_render_option=ValueRenderOption.unformatted)

    this_week = datetime.now().isocalendar()[1] 

    exercise_types = minutes_data[0][0:3] #fetches the exercise names from the headings of the 'minutes' Google sheet

    ex_0_minutes_this_week = [] #list for all the minutes entries for the current week for exercise 0
    ex_1_minutes_this_week = [] #list for all the minutes entries for the current week for exercise 1
    ex_2_minutes_this_week = [] #list for all the minutes entries for the current week for exercise 2

    for row in minutes_data:
        if row[5] == this_week:
            ex_0_minutes_this_week.append(row[0]) 
            ex_1_minutes_this_week.append(row[1])
            ex_2_minutes_this_week.append(row[2])

    ex_0_total_this_week = (sum(ex_0_minutes_this_week)) #calculates and stores total minutes this week for each exercise
    ex_1_total_this_week = (sum(ex_1_minutes_this_week))
    ex_2_total_this_week = (sum(ex_2_minutes_this_week))

    minutes_this_week_list = [ex_0_total_this_week, ex_1_total_this_week, ex_2_total_this_week]

    targets = SHEET.worksheet("weekly_targets").get_values(value_render_option=ValueRenderOption.unformatted)
    most_recent_targets = targets[-1]

    for exercise, minutes, target in zip(exercise_types, minutes_this_week_list, most_recent_targets):
        minutes_to_go = target - minutes
        if target > minutes:
            print(f"You have done {minutes} minutes of {exercise} this week. \nYour target is {target}. You have {minutes_to_go} minutes to go. Keep it up! \n")
        else:
            print(f"You have done {minutes} minutes of {exercise} this week. \nYour target was {target}. Well done! \n")


#Option Three: Add new targets

def print_current_targets():
    '''
    Displays user's current weekly targets
    '''
    targets = SHEET.worksheet("weekly_targets").get_values()
    headings = targets[0]
    most_recent_targets = targets[-1]

    print("Your current weekly targets are: ") 
    for heading, target in zip(headings, most_recent_targets):
        print(f"{(heading.capitalize())}: {target} minutes per week")

        
def edit_targets():
    """
    Takes user input for new targets, adds them to a list and appends them to the 'targets' spreadsheet
    """
    print_current_targets()
    print("Please enter your new weekly targets for each exercise: \n")

    while True:
        try: 
            new_cardio_target = int(input("New cardio target (minutes per week): \n"))
            break 
        except ValueError:
            print("Please enter a number") 

    while True:
        try: 
            new_weights_target = int(input("New weights target (minutes per week): \n")) 
            break 
        except ValueError:
            print("Please enter a number")

    while True:
        try: 
            new_swimming_target = int(input("New swimming target (minutes per week): \n"))
            break 
        except ValueError:
            print("Please enter a number") 

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

    exercise = input("Which exercise would you like to view? (cardio/weights/swimming) \n").lower()

    while True:
        if exercise == "cardio": 
            column_number = 0
            break
        elif exercise == "weights":
            column_number = 1
            break
        elif exercise == "swimming":
            column_number = 2
            break
        else:
            print("Please enter cardio, weights or swimming")

    minutes_data = minutes.get_values(value_render_option=ValueRenderOption.unformatted)

    this_week = datetime.now().isocalendar()[1]

    one_week_ago = []
    two_weeks_ago = []
    three_weeks_ago = []
    four_weeks_ago = [] #also what to do when four weeks ago was last year

    for row in minutes_data:
        if row[5] == this_week - 1:
            one_week_ago.append(row[column_number])
        elif row[5] == this_week - 2:
            two_weeks_ago.append(row[column_number])
        elif row[5] == this_week - 3:
            three_weeks_ago.append(row[column_number])
        elif row[5] == this_week - 4:
            four_weeks_ago.append(row[column_number])

    one_sum = sum(one_week_ago)
    two_sum = sum(two_weeks_ago)
    three_sum = sum(three_weeks_ago)
    four_sum = sum(four_weeks_ago)

    print(f"Last week you did {one_sum} minutes of {exercise}")
    print(f"Two weeks ago you did {two_sum} minutes of {exercise}")
    print(f"Three weeks ago you did {three_sum} minutes of {exercise}")
    print(f"Four weeks ago you did {four_sum} minutes of {exercise}")


#Option Five: Exit program

def close_program():
    '''
    Ends program
    '''
    print(f"Exiting workout tracker. See you soon, {username}!") 


#User menu:

def show_options():
    '''
    Presents a menu for user to select which part of the program they want to run
    '''
    while True:
        print("What would you like to do today? Please select a number:")
        option = input("1. Enter minutes \n 2. View progress this week \n 3. Update targets \n 4. View last four weeks \n 5. Exit \n")

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