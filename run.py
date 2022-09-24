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

def login_choice():
    """
    Allows the user to choose the appropriate login for them
    """
    print('Login [L]')
    print('Create an account [C]')
    print('Log in as a guess [G]\n')

    option = input('Please enter your option here:')

    if option == 'L':
        print('login()')
    elif option == 'C':
        print('create_login()')
    elif option == 'G':
        print('start_battleships()')
    else:
        raise ValueError(
            f"Please check as the input you have supplied is not an option you enter: {option}"
        )


def main():
    """
    Runs all functions
    """
    login_choice()

print('Welcome lets play Battleships!')
main()