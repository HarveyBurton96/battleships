import gspread
import random
import time
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

        if option == 'L' or option == 'l':
            user = log_in()
            valid_login = True
        elif option == 'C' or option == 'c':
            user = create_login()
            valid_login = True
        elif option == 'G' or option == 'g':
            valid_login = True
            user = 'Guest'
        elif option == 'Q' or option == 'q':
            print(f"You have entered {option} to quit the game. Hope you come back soon!")
            return 'Q'
        else:
            print(
                f"Please check as the input you have supplied is not a valid option you have enter: {option}, please try again.\n"
            )

    return user


def log_in():
    """
    For users with an existing account will enter their details here
    """
    x = 0

    login = SHEET.worksheet('login')

    username_data = login.col_values(1)
    password_data = login.col_values(2)

    while x == 0:
        username = input('Please enter your username here:\n')

        if username in username_data:
            x += 1
        elif username == 'q' or username == 'Q':
            print(f"You have entered {username} to quit the game. Hope you come back soon!")
            return 'Q'
        else:
            print(f"Username: '{username}', is not recognised please try again\n")

    username_place = username_data.index(username)

    y = 0
    while y == 0:
        password = input('Please enter your password here:\n')

        if password == password_data[username_place]:
            print(f"Welcome back {username}")
            y += 1
        elif password == 'q' or password == 'Q':
            print(f"You have entered {password} to quit the game. Hope you come back soon!")
            return 'Q'
        else:
            print(f"Password: {password}, is not recognised please try again")

    return username


def create_login():
    """
    This function will check if a username is already in use and if not
    will save the username and password to the spreadsheet as well as
    adding thier scores
    """
    print('Thank you for creating an account')
    time.sleep(1)

    login = SHEET.worksheet('login')
    score = SHEET.worksheet('score')

    username_data = login.col_values(1)

    x = 0

    while x == 0:
        username = input('Please enter your username here:\n')
        x += 1
        if username in username_data:
            print(
                f"Please select another username as '{username}' has already been selected.\n"
                )
            x -= 1
        elif username.count(' ') >= 1 or username == '':
            print(
                f"Please select another username as '{username}' is not valid.\n"
                )
            x -= 1
        elif username == 'q' or username == 'Q':
            print(f"You have entered {username} to quit the game. Hope you come back soon!")
            return 'Q'
    p = 0

    while p == 0:
        password = input('Please enter your password here:\n')
        p += 1
        
        if password.count(' ') >= 1 or password == '':
            print(
                f"Please select another password as '{password}' is not valid.\n"
                )
            x -= 1
        elif password == 'q' or password == 'Q':
            print(f"You have entered {password} to quit the game. Hope you come back soon!")
            return 'Q'
    

    new_user = [username, password]
    new_user_score = [username, 0, 0, 0]

    login.append_row(new_user)
    score.append_row(new_user_score)

    return username


def play_battleship(user):
    """
    Create new game and resets the board
    """
    print('Lets play battleships!\n')
    time.sleep(1)

    player_row5 = ['  5', '-', '-', '-', '-', '-']
    player_row4 = ['  4', '-', '-', '-', '-', '-']
    player_row3 = ['y 3', '-', '-', '-', '-', '-']
    player_row2 = ['  2', '-', '-', '-', '-', '-']
    player_row1 = ['  1', '-', '-', '-', '-', '-']
    player_xcolumn_numbers = ['   ', '1', '2', '3', '4', '5']
    player_xcolumn = ['   ', ' ', ' ', 'x', ' ', ' ']

    player_board = [
        player_xcolumn_numbers, player_row1, player_row2, player_row3,
        player_row4, player_row5, player_xcolumn
        ]

    print('--------------------------------------')
    print("Computer's ships locations\n")

    print(*player_row5, sep=' ')
    print(*player_row4, sep=' ')
    print(*player_row3, sep=' ')
    print(*player_row2, sep=' ')
    print(*player_row1, sep=' ')
    print(*player_xcolumn_numbers, sep=' ')
    print(*player_xcolumn, sep=' ')

    print(' ')
    print('--------------------------------------')
    time.sleep(1)

    computer_row5 = ['  5', '-', '-', '-', '-', '-']
    computer_row4 = ['  4', '-', '-', '-', '-', '-']
    computer_row3 = ['y 3', '-', '-', '-', '-', '-']
    computer_row2 = ['  2', '-', '-', '-', '-', '-']
    computer_row1 = ['  1', '-', '-', '-', '-', '-']
    computer_xcolumn_numbers = ['   ', '1', '2', '3', '4', '5']
    computer_xcolumn = ['   ', ' ', ' ', 'x', ' ', ' ']

    computer_board = [
        computer_xcolumn_numbers, computer_row1, computer_row2,
        computer_row3, computer_row4, computer_row5, computer_xcolumn
        ]

    print('--------------------------------------')
    print(f"{user}'s ships locations\n")

    print(*computer_row5, sep=' ')
    print(*computer_row4, sep=' ')
    print(*computer_row3, sep=' ')
    print(*computer_row2, sep=' ')
    print(*computer_row1, sep=' ')
    print(*computer_xcolumn_numbers, sep=' ')
    print(*computer_xcolumn, sep=' ')

    print(' ')
    print('--------------------------------------\n')
    time.sleep(1)

    computer_ships_locations = []
    player_ships_locations = []
    players_input_moves = []
    computer_potential_moves = [
        '1,5', '3,4', '1,1', '2,3', '1,4',
        '5,1', '3,3', '5,5', '3,1', '2,2',
        '4,3', '3,5', '4,1', '4,4', '5,3',
        '2,1', '4,5', '4,2', '2,4', '3,2',
        '1,2', '5,4', '2,5', '1,3', '5,2'
        ]

    while len(player_ships_locations) < 5:
        num1 = str(random.randint(1, 5)) + ',' + str(random.randint(1, 5))
        if num1 not in player_ships_locations:
            player_ships_locations.append(num1)

    while len(computer_ships_locations) < 5:
        num2 = str(random.randint(1, 5)) + ',' + str(random.randint(1, 5))
        if num2 not in computer_ships_locations:
            computer_ships_locations.append(num2)

    return player_ships_locations, computer_ships_locations, players_input_moves, computer_potential_moves, player_board, computer_board


def score_checker(player_ships_locations, computer_ships_locations, players_input_moves, computer_potential_moves, player_board, computer_board, user):
    """
    Function takes the player and computer ship lists and counts the list,
    and while both have a length greater than no ships left the game
    continues. Unless the player has entered Q to quit the game
    """
    while len(player_ships_locations) > 0 and len(computer_ships_locations) > 0:
        print(' ')
        print(f"{user} has {len(player_ships_locations)} ships left")
        print(f"Computer has {len(computer_ships_locations)} ships left\n")
        time.sleep(1)

        if coordinates_entered(
            player_ships_locations, computer_ships_locations,
            players_input_moves, computer_potential_moves, player_board,
            computer_board, user
            ) == 'Q':
            print(
                f"Your remaining ships were located at: {player_ships_locations}\nThe computers remaining ships were located at: {computer_ships_locations}\n"
                )
            return 'Q'
    
    if len(player_ships_locations) != 0 and len(computer_ships_locations) == 0:
        print(f"Your remaining ships were located at: {player_ships_locations}\n")
        return 'W'
    elif len(computer_ships_locations) != 0 and len(player_ships_locations) == 0:
        print(f"The computers remaining ships were located at: {computer_ships_locations}\n")
        return 'L'
    elif len(player_ships_locations) == 0 and len(computer_ships_locations) == 0:
        return 'D'


def coordinates_entered(player_ships_locations, computer_ships_locations, players_input_moves, computer_potential_moves, player_board, computer_board, user):
    """
    Takes players and computers moves for each turn
    """ 
    coordinates_not_valid = True
    while coordinates_not_valid is True:
        move = input("Please enter your move here, with column (x) then row (y) \nseparated by a ',' i.e. x,y:\n")

        if move == 'Q' or move == 'q':
            return 'Q'

        coordinates_not_valid = move_checker(move, players_input_moves)

    com_move = computer_potential_moves.pop(random.randrange(len(computer_potential_moves)))
    computer = 'Computer'

    hit_or_miss(move, computer_ships_locations, player_board, user, computer)
    hit_or_miss(com_move, player_ships_locations, computer_board, computer, user)


def move_checker(move, players_input_moves):
    """
    Checks the players input moves for input being a number and within 
    the range of the board and have only entered 2 coordinates
    """
    ranges = range(1, 6)
    moves = move.split(',')

    try:
        if len(moves) != 2:
            print(f"\nIncorrect amount of coordinates have been entered, you have entered: {len(moves)} coordinates. Please only enter 2 coordinates\n")
        elif moves[0].isnumeric() is False:
            print(f"\nx coordinate is not a number you have entered: {moves[0]}\n")
        elif moves[1].isnumeric() is False:
            print(f"\ny coordinate is not a number you have entered: {moves[1]}\n")
        elif int(moves[0]) not in ranges:
            print(f"\nx coordinate is not a number on the board, you have entered: {moves[0]}\n")
        elif int(moves[1]) not in ranges:
            print(f"\ny coordinate is not a number on the board, you have entered: {moves[1]}\n")
        elif move in players_input_moves:
            print(f"\nYou have already fired upon these coordinates: {moves}\n")
        else:
            players_input_moves.append(move)
            return False
    except ValueError:
        print(f"\nPlease check as your input was not a valid coordinates, you entered: {moves}\n")

    return True


def hit_or_miss(move, enemy_ships_locations, board_layout, name, oppositons_name):
    """
    Takes the move and checks if it's the same as a enemy ship
    coordinates if so will send a H if not O
    """
    if move in enemy_ships_locations:
        hit = 'H'
        enemy_ships_locations.remove(move)
    else:
        hit = 'O'
    outcome(move, board_layout, hit, name, oppositons_name)


def outcome(move, board_layout, hit, name, oppositons_name):
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
    print(F"{oppositons_name}'s ships locations\n")

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
        print(f"\nwins: {win}\nLoses: {lose}\nDraws: {draw}")

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
        
        if decision == 'P' or decision == 'p':
            return True
        elif decision == 'Q' or decision == 'q':
            print('Thank you for playing!')
            return False
        else:
            print(f"The input has not been recognised you have entered: {decision}, Please try again.\n")       


def main():
    """
    Runs all functions
    """
    user = login_choice()
    if user != 'q' and user != 'Q':
        play = True
        while play is True:
            ship_location = play_battleship(user)
            result = score_checker(ship_location[0], ship_location[1], ship_location[2], ship_location[3], ship_location[4], ship_location[5], user)
            results(result, user)
            play = still_playing()


print('Welcome lets play Battleships!')
main()
