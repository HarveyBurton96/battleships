import random
import time

# The code from line 9 to 21 is not my own and is from the code institute
# Love sandwiches project. The video is located here:
# https://learn.codeinstitute.net/courses/course-v1:CodeInstitute+LS101+2021_T1/courseware/293ee9d8ff3542d3b877137ed81b9a5b/c92755338ef548f28cc31a7c3d5bfb46/
# The code is also available in a repository I created as I followed along
# the guide located here: https://github.com/HarveyBurton96/love-sandwiches
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
    valid_login = False
    while valid_login is False:
        print('Please select a login option\n')
        print('Login [L]')
        print('Create an account [C]')
        print('Log in as a guest [G]\n')
        print('If you would like to quit the game at any time please enter [Q].\n')

        option = input('Please enter your option here:\n')

        if option in ('L', 'l'):
            user = log_in()
            valid_login = True
        elif option in ('C', 'c'):
            user = create_login()
            valid_login = True
        elif option in ('G', 'g'):
            valid_login = True
            user = 'Guest'
        elif option in ('Q', 'q'):
            print(f"You have entered {option} to quit the game.")
            print("Hope you come back soon!")
            return 'Q'
        else:
            print("Please check as the input you have supplied is not a valid")
            print(f"option you have enter: {option}, please try again.\n")

    return user


def log_in():
    """
    For users with an existing account will enter their details here
    """
    acceptable_username = True

    login = SHEET.worksheet('login')

    username_data = login.col_values(1)
    password_data = login.col_values(2)

    print("Please note for your username and password that they are case sensitive")

    while acceptable_username is True:
        username = input('Please enter your username here:\n')

        if username in username_data:
            acceptable_username = False
        elif username in ('q', 'Q'):
            print(f"You have entered {username} to quit the game.")
            print("Hope you come back soon!")
            return 'Q'
        else:
            print(f"Username: '{username}', is not recognised please try again\n")

    username_place = username_data.index(username)

    acceptable_password = True
    while acceptable_password is True:
        password = input('Please enter your password here:\n')

        if password == password_data[username_place]:
            print(f"Welcome back {username}")
            acceptable_password = False
        elif password == 'q' or password == 'Q':
            print(f"You have entered {password} to quit the game.")
            print("Hope you come back soon!")
            return 'Q'
        else:
            print(f"Password: {password}, is not recognised please try again")

    return username


def create_login():
    """
    This function will check if a username is already in use and if not
    will save the username and password to the spreadsheet as well as
    creating their scores
    """
    time.sleep(1)

    login = SHEET.worksheet('login')
    score = SHEET.worksheet('score')

    username_data = login.col_values(1)

    acceptable_username = True

    while acceptable_username is True:
        username = input('Please enter your username here:\n')
        acceptable_username = False
        if username in username_data:
            print(
                f"Please select another username as '{username}' has already been selected.\n"
                )
            acceptable_username = True
        elif username.count(' ') >= 1 or username == '':
            print(
                f"Please select another username as '{username}' is not valid.\n"
                )
            acceptable_username = True
        elif username in ('q', 'Q'):
            print(f"You have entered {username} to quit the game.")
            print("Hope you come back soon!")
            return 'Q'

    print('Thank you for creating an account')
    time.sleep(1)

    acceptable_password = True

    while acceptable_password is True:
        password = input('Please enter your password here:\n')
        acceptable_password = False
        if password.count(' ') >= 1 or password == '':
            print(
                f"Please select another password as '{password}' is not valid.\n"
                )
            acceptable_password = True
        elif password in ('q', 'Q'):
            print(f"You have entered {password} to quit the game.")
            print("Hope you come back soon!")
            return 'Q'

    new_user = [username, password]
    new_user_score = [username, 0, 0, 0]

    login.append_row(new_user)
    score.append_row(new_user_score)

    return username


def play_battleship(user):
    """
    Create new game and removes the previous games data
    """
    print('Lets play battleships!\n')
    print('A hit is displayed as a H')
    print('A miss is displayed as a O\n')
    time.sleep(1)

    player_board = build_board()
    computer_board = build_board()

    print('--------------------------------------')
    print(f"{user}'s ships locations\n")

    print(*computer_board[5], sep=' ')
    print(*computer_board[4], sep=' ')
    print(*computer_board[3], sep=' ')
    print(*computer_board[2], sep=' ')
    print(*computer_board[1], sep=' ')
    print(*computer_board[0], sep=' ')
    print(*computer_board[6], sep=' ')

    print(' ')
    print('--------------------------------------')
    time.sleep(1)

    print('--------------------------------------')
    print("Computer's ships locations\n")

    print(*player_board[5], sep=' ')
    print(*player_board[4], sep=' ')
    print(*player_board[3], sep=' ')
    print(*player_board[2], sep=' ')
    print(*player_board[1], sep=' ')
    print(*player_board[0], sep=' ')
    print(*player_board[6], sep=' ')

    print(' ')
    print('--------------------------------------\n')
    time.sleep(1)

    players_input_moves = []
    computer_potential_moves = [
        '1,5', '3,4', '1,1', '2,3', '1,4',
        '5,1', '3,3', '5,5', '3,1', '2,2',
        '4,3', '3,5', '4,1', '4,4', '5,3',
        '2,1', '4,5', '4,2', '2,4', '3,2',
        '1,2', '5,4', '2,5', '1,3', '5,2'
        ]

    player_ships_locations = ship_generator()
    computer_ships_locations = ship_generator()

    return player_ships_locations, computer_ships_locations, players_input_moves, computer_potential_moves, player_board, computer_board


def build_board():
    """Generates the starting board which is blank"""
    board = [
        ['   ', '1', '2', '3', '4', '5'],
        ['  1', '-', '-', '-', '-', '-'],
        ['  2', '-', '-', '-', '-', '-'],
        ['y 3', '-', '-', '-', '-', '-'],
        ['  4', '-', '-', '-', '-', '-'],
        ['  5', '-', '-', '-', '-', '-'],
        ['   ', ' ', ' ', 'x', ' ', ' ']]
    return board


def ship_generator():
    """Generates random locations for ships"""
    ships = []
    while len(ships) < 5:
        num1 = str(random.randint(1, 5)) + ',' + str(random.randint(1, 5))
        if num1 not in ships:
            ships.append(num1)
    return ships


def score_checker(ship_data, user):
    """
    Function takes the player and computer ship lists and counts the list,
    and while both have a length greater than 0 ships left the game
    continues. Unless the player has entered Q to quit the game. If the game
    ends without the player quitting it will also calculate if the player
    won, lost, or drew
    """
    while len(ship_data[0]) > 0 and len(ship_data[1]) > 0:
        print(' ')
        print(f"{user} has {len(ship_data[0])} ships left")
        print(f"Computer has {len(ship_data[1])} ships left\n")
        time.sleep(1)

        if coordinates_entered(ship_data, user) == 'Q':
            print(f"Your remaining ships were located at: {ship_data[0]}")
            print(f"The computers remaining ships were located at: {ship_data[1]}\n")
            return 'Q'

    if len(ship_data[0]) != 0 and len(ship_data[1]) == 0:
        print(f"Your remaining ships were located at: {ship_data[0]}\n")
        return 'W'
    if len(ship_data[1]) != 0 and len(ship_data[0]) == 0:
        print(f"The computers remaining ships were located at: {ship_data[1]}\n")
        return 'L'
    if len(ship_data[0]) == 0 and len(ship_data[1]) == 0:
        return 'D'


def coordinates_entered(ship_data, user):
    """
    Takes the players input and generates the computers moves for each turn
    """
    coordinates_not_valid = True
    while coordinates_not_valid is True:
        move = input("Please enter your move here, with column (x) then row (y) \nseparated by a ',' i.e. x,y:\n")

        if move == 'Q' or move == 'q':
            return 'Q'

        coordinates_not_valid = move_checker(move, ship_data[2])

    com_move = ship_data[3].pop(random.randrange(len(ship_data[3])))
    computer = 'Computer'

    hit_or_miss(com_move, ship_data[0], ship_data[5], computer, user)
    hit_or_miss(move, ship_data[1], ship_data[4], user, computer)


def move_checker(move, players_input_moves):
    """
    Checks the players input moves for input being a number, within
    the range of the board, have only entered 2 coordinates, and not
    already been entered
    """
    ranges = range(1, 6)
    moves = move.split(',')

    try:
        if len(moves) != 2:
            print("\nIncorrect amount of coordinates have been entered,")
            print(f"you have entered: {len(moves)} coordinates. Please only")
            print("enter 2 coordinates\n")
        elif moves[0].isnumeric() is False:
            print(f"\nx coordinate is not a number you have entered: {moves[0]}\n")
        elif moves[1].isnumeric() is False:
            print(f"\ny coordinate is not a number you have entered: {moves[1]}\n")
        elif int(moves[0]) not in ranges:
            print("\nx coordinate is not a number on the board,")
            print(f"you have entered: {moves[0]}\n")
        elif int(moves[1]) not in ranges:
            print("\ny coordinate is not a number on the board,")
            print(f"you have entered: {moves[1]}\n")
        elif move in players_input_moves:
            print(f"\nYou have already fired upon these coordinates: {moves}\n")
        else:
            players_input_moves.append(move)
            return False
    except ValueError:
        print("\nPlease check as your input was not a valid coordinates,")
        print(f"you entered: {moves}\n")

    return True


def hit_or_miss(move, enemy_ships_locations, board_layout, name, oppositions_name):
    """
    Takes the move and checks if it's the same as a enemy ship
    coordinates if so will send a H if not O
    """
    if move in enemy_ships_locations:
        hit = 'H'
        enemy_ships_locations.remove(move)
    else:
        hit = 'O'
    outcome(move, board_layout, hit, name, oppositions_name)


def outcome(move, board_layout, hit, name, oppositions_name):
    """
    Take the users input and edit the board data to change a - to
    H or O depending if it's a hit or miss
    """
    xandy = move.split(',')
    x = int(xandy[0])
    y = int(xandy[1])

    if hit == 'H':
        board_layout[y][x] = 'H'
        move_outcome = 'Hit!'
    else:
        board_layout[y][x] = 'O'
        move_outcome = 'Miss'

    time.sleep(1)

    print('--------------------------------------')
    print(F"{oppositions_name}'s ships locations\n")

    print(*board_layout[5], sep=' ')
    print(*board_layout[4], sep=' ')
    print(*board_layout[3], sep=' ')
    print(*board_layout[2], sep=' ')
    print(*board_layout[1], sep=' ')
    print(*board_layout[0], sep=' ')
    print(*board_layout[6], sep=' ')

    print(' ')
    print(f"{name} has fired upon: {move} its a {move_outcome}")
    print('--------------------------------------')
    time.sleep(1)


def results(result, user):
    """
    Displays the result of the game and if the player has an
    account will display their total win/lose/draw
    """
    score = SHEET.worksheet('score')

    if user != 'Guest':
        username_place = score.col_values(1).index(user)
        win = score.col_values(2)[username_place]
        lose = score.col_values(3)[username_place]
        draw = score.col_values(4)[username_place]

    if result == 'W':
        print(f"Congratulations {user} you won!")
        if user != 'Guest':
            win = int(win) + 1
    elif result == 'L':
        print(f"Better luck next time {user} you lost :(")
        if user != 'Guest':
            lose = int(lose) + 1
    elif result == 'D':
        print(f"So close {user} you drew!")
        if user != 'Guest':
            draw = int(draw) + 1

    if user != 'Guest' and result != 'Q':
        print(f"\nWins: {win}\nLoses: {lose}\nDraws: {draw}")

        score.update('B' + str(username_place+1), win)
        score.update('C' + str(username_place+1), lose)
        score.update('D' + str(username_place+1), draw)


def still_playing():
    """
    To determine if the payer would like to play another round of battleships
    """
    playing = True
    while playing is True:
        decision = input("Would you like to play another game? \nEnter [P] to play another\nEnter [Q] to quite to the game\n")

        if decision in ('P', 'p'):
            return True
        if decision in ('Q', 'q'):
            print('Thank you for playing!')
            return False

        print(f"The input has not been recognised, you have entered: {decision},")
        print("Please try again.\n")


def main():
    """
    Runs all functions
    """
    user = login_choice()
    if user != 'q' and user != 'Q':
        play = True
        while play is True:
            ship_data = play_battleship(user)
            result = score_checker(ship_data, user)
            results(result, user)
            play = still_playing()


print('Welcome lets play Battleships!')
main()
