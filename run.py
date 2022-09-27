import gspread
from google.oauth2.service_account import Credentials 

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('battleships')

def login_choice():
    """
    Allows the user to choose the appropriate login for them
    """
    x=0 
    while x == 0:
        print('Please select a loggin option\n')
        print('Login [L]')
        print('Create an account [C]')
        print('Log in as a guess [G]\n')

        option = input('Please enter your option here:\n')

        if option == 'L':
            user = log_in()
            x += 1

        elif option == 'C':
            user = create_login()
            x += 1
        elif option == 'G':
            x += 1
            user = 'Guess'
        else:
            print(f"Please check as the input you have supplied is not a valid option you have enter: {option}, please try again.\n")

        return user


def log_in():
    """
    For users with an existing account will enter there details here 
    """
    x = 0 

    login = SHEET.worksheet('login')

    username_data = login.col_values(1)
    password_data = login.col_values(2)

    while x == 0:
        username = input('Please enter your username here:\n')

        if username in username_data:
            x += 1
        else:
            print(f"Username: '{username}', is not recognised please try again\n")

    username_place = username_data.index(username)

    y = 0
    while y == 0:
        password = input('Please enter your password here:\n')

        if password == password_data[username_place]:
            print(f"welcome back {username}")
            y += 1
        else:
            print(f"Password: {password}, is not recognised please try again")

    return username


def create_login():
    """
    This function will check if a username is already in use and if not will save the username and password to the spreadsheet
    """

    print('Thank you for creating an account')

    login = SHEET.worksheet('login')

    username_data = login.col_values(1)

    x = 0

    while x == 0:
        username = input('Please enter your username here:\n')
        x += 1
        if username in username_data:
            print(f"Please select another username as '{username}' has already been selected.\n")
            x -= 1

    password = input('Please enter your password here:\n')

    new_user = [username, password]

    login.append_row(new_user)

    return username

def play_battleship():
    print('Lets play battleships!')
    X1_Y1 = X1_Y2 = X1_Y3 = X1_Y4 = X1_Y5 = X2_Y1 = X2_Y2 = X2_Y3 = X2_Y4 = X2_Y5 = X3_Y1 = X3_Y2 = X3_Y3 = X3_Y4 = X3_Y5 = X4_Y1 = X4_Y2 = X4_Y3 = X4_Y4 = X4_Y5 = X5_Y1 = X5_Y2 = X5_Y3 = X5_Y4 = X5_Y5 = '-'

    print(f"\n  5 {X1_Y5} {X2_Y5} {X3_Y5} {X4_Y5} {X5_Y5} \n  4 {X1_Y4} {X2_Y4} {X3_Y4} {X4_Y4} {X5_Y4} \ny 3 {X1_Y3} {X2_Y3} {X3_Y3} {X4_Y3} {X5_Y3} \n  2 {X1_Y2} {X2_Y2} {X3_Y2} {X4_Y2} {X5_Y2} \n  1 {X1_Y1} {X2_Y1} {X3_Y1} {X4_Y1} {X5_Y1} \n    1 2 3 4 5 \n        x\n")

    print('Make your move')
    print('To quit [Q]')
    move = input("Please enter your move here, with column (x) then row (y) seperated by a ',' (x,y):\n")

def main():
    """
    Runs all functions
    """
    user = login_choice()
    print(user)
    play_battleship()
    

print('Welcome lets play Battleships!')
main()