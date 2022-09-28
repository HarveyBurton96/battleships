import gspread
import random
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
    """Create new game and resets the board"""
    print('Lets play battleships!\n')

    board5 = ['  5', '-', '-', '-', '-', '-']
    board4 = ['  4', '-', '-', '-', '-', '-']
    board3 = ['y 3','-', '-', '-', '-', '-']
    board2 = ['  2','-', '-', '-', '-', '-']
    board1 = ['  1','-', '-', '-', '-', '-']
    xcolumn = ['   ', '1', '2', '3', '4', '5']
    xcolumn2 = ['   ', ' ', ' ', 'x', ' ', ' ']

    board_layout = [xcolumn, board1, board2, board3, board4, board5, xcolumn2]

    print(*board5, sep = ' ')
    print(*board4, sep = ' ')
    print(*board3, sep = ' ')
    print(*board2, sep = ' ')
    print(*board1, sep = ' ')
    print(*xcolumn, sep = ' ')
    print(*xcolumn2, sep = ' ')

    computer_ships = []
    player_ships = []
    player_move = []
    computer_move = []

    i = 0
    while i < 6:
        player_ships.append(str(random.randint(1,5)) + ',' + str(random.randint(1,5)))
        computer_ships.append(str(random.randint(1,5)) + ',' + str(random.randint(1,5)))
        i += 1
    
    return player_ships, computer_ships, player_move, computer_move


def score_checker(player, computer):
    """Function takes the player and computer ship lists and counts the list and while the both have greater than 0 ships left the game continues""" 
    while len(player) > 0 and len(computer) > 0:
        print(f"Player has {player} ships left\n")
        print(f"Computer has {computer} ships left")

    
def hit(data, board_data):
    """ Take the users input and edit the board data to chnage a - to H """
    xandy = data.split(',')
    print(xandy)
    x = int(xandy[0])
    y = int(xandy[1])

    print(x)
    print(y)

    board_data[y][x] = 'H'

    print(*board_data[5], sep = ' ')
    print(*board_data[4], sep = ' ')
    print(*board_data[3], sep = ' ')
    print(*board_data[2], sep = ' ')
    print(*board_data[1], sep = ' ')
    print(*board_data[0], sep = ' ')
    print(*board_data[6], sep = ' ')

    print(board_data[y][x])


def player_move():
    """takes the user moves and assignes it a hit or miss """
    print('Make your move')
    print('To quit [Q]')
    move = input("Please enter your move here, with column (x) then row (y) seperated by a ',' (x,y):\n")


def main():
    """
    Runs all functions
    """
    user = login_choice()
    print(user)
    ship_location = play_battleship()
    score_checker(ship_location[0], ship_location[1])



print('Welcome lets play Battleships!')
main()