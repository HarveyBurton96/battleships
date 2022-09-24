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

login = SHEET.worksheet('login')

data = login.get_all_values()

print(data)

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
            log_in()
            x += 1
        elif option == 'C':
            print('create_login()')
            x += 1
        elif option == 'G':
            print('start_battleships()')
            x += 1
        else:
            print(f"Please check as the input you have supplied is not a valid option you have enter: {option}, please try again.\n")


def log_in():
    """
    For users with an existing account will enter there details here 
    """
    username = input('Please enter your username here:\n')
    password = input('Please enter your password here:\n')

    


def main():
    """
    Runs all functions
    """
    login_choice()

print('Welcome lets play Battleships!')
main()