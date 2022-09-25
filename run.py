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
    C1_R1 = C1_R2 = C1_R3 = C1_R4 = C1_R5 = C2_R1 = C2_R2 = C2_R3 = C2_R4 = C2_R5 = C3_R1 = C3_R2 = C3_R3 = C3_R4 = C3_R5 = C4_R1 = C4_R2 = C4_R3 = C4_R4 = C4_R5 = C5_R1 = C5_R2 = C5_R3 = C5_R4 = C5_R5 ='-'

    print(f"\n  5 {C1_R5} {C2_R5} {C3_R5} {C4_R5} {C5_R5} \n  4 {C1_R4} {C2_R4} {C3_R4} {C4_R4} {C5_R4} \nR 3 {C1_R3} {C2_R3} {C3_R3} {C4_R3} {C5_R3} \n  2 {C1_R2} {C2_R2} {C3_R2} {C4_R2} {C5_R2} \n  1 {C1_R1} {C2_R1} {C3_R1} {C4_R1} {C5_R1} \n    1 2 3 4 5 \n        C\n")

    print('Make your move')
    move = input("Please enter your move here, with column then row seperated by a ',':\n")

def main():
    """
    Runs all functions
    """
    user = login_choice()
    print(user)
    play_battleship()
    

print('Welcome lets play Battleships!')
main()