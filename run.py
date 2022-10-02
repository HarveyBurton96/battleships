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
        print('Please select a login option\n')
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
        else:
            print(f"Username: '{username}', is not recognised please try again\n")

    username_place = username_data.index(username)

    y = 0
    while y == 0:
        password = input('Please enter your password here:\n')

        if password == password_data[username_place]:
            print(f"Welcome back {username}")
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
    score = SHEET.worksheet('score')

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
    new_user_score = [username, 0, 0, 0]

    login.append_row(new_user)
    score.append_row(new_user_score)

    return username


def play_battleship(user):
    """
    Create new game and resets the board
    """
    print('Lets play battleships!\n')

    player_board5 = ['  5', '-', '-', '-', '-', '-']
    player_board4 = ['  4', '-', '-', '-', '-', '-']
    player_board3 = ['y 3','-', '-', '-', '-', '-']
    player_board2 = ['  2','-', '-', '-', '-', '-']
    player_board1 = ['  1','-', '-', '-', '-', '-']
    player_xcolumn = ['   ', '1', '2', '3', '4', '5']
    player_xcolumn2 = ['   ', ' ', ' ', 'x', ' ', ' ']

    player_board_layout = [player_xcolumn, player_board1, player_board2, player_board3, player_board4, player_board5, player_xcolumn2]

    print('--------------------------------------')
    print("Computer's ships locations\n")

    print(*player_board5, sep = ' ')
    print(*player_board4, sep = ' ')
    print(*player_board3, sep = ' ')
    print(*player_board2, sep = ' ')
    print(*player_board1, sep = ' ')
    print(*player_xcolumn, sep = ' ')
    print(*player_xcolumn2, sep = ' ')

    print(' ')
    print('--------------------------------------')

    computer_board5 = ['  5', '-', '-', '-', '-', '-']
    computer_board4 = ['  4', '-', '-', '-', '-', '-']
    computer_board3 = ['y 3','-', '-', '-', '-', '-']
    computer_board2 = ['  2','-', '-', '-', '-', '-']
    computer_board1 = ['  1','-', '-', '-', '-', '-']
    computer_xcolumn = ['   ', '1', '2', '3', '4', '5']
    computer_xcolumn2 = ['   ', ' ', ' ', 'x', ' ', ' ']

    computer_board_layout = [computer_xcolumn, computer_board1, computer_board2, computer_board3, computer_board4, computer_board5, computer_xcolumn2]

    print('--------------------------------------')
    print(f"{user}'s ships locations\n")

    print(*computer_board5, sep = ' ')
    print(*computer_board4, sep = ' ')
    print(*computer_board3, sep = ' ')
    print(*computer_board2, sep = ' ')
    print(*computer_board1, sep = ' ')
    print(*computer_xcolumn, sep = ' ')
    print(*computer_xcolumn2, sep = ' ')

    print(' ')
    print('--------------------------------------')

    computer_ships = []
    player_ships = []
    player_move = []
    computer_move = ['1,5', '3,4', '1,1', '2,3', '1,4', '5,1', '3,3', '5,5', '3,1', '2,2', '4,3', '3,5', '4,1', '4,4', '5,3', '2,1', '4,5', '4,2', '2,4', '3,2', '1,2', '5,4', '2,5', '1,3', '5,2']

    while len(player_ships) < 5:
        num1 = str(random.randint(1,5)) + ',' + str(random.randint(1,5))
        if num1 not in player_ships:
            player_ships.append(num1)

    while len(computer_ships) < 5:
        num2 = str(random.randint(1,5)) + ',' + str(random.randint(1,5))
        if num2 not in computer_ships:
            computer_ships.append(num2)
    
    return player_ships, computer_ships, player_move, computer_move, player_board_layout, computer_board_layout


def score_checker(player, computer, players_move, computer_move, player_board_layout, computer_board_layout, user):
    """
    Function takes the player and computer ship lists and counts the list, and while both have a length greater than no ships left the game continues. Unless the player has entered Q to quit the game
    """ 
    while len(player) > 0 and len(computer) > 0:
        print(' ')
        print(f"{user} has {len(player)} ships left")
        print(f"Computer has {len(computer)} ships left\n")

        if coordinates_entered(player, computer, players_move, computer_move, player_board_layout, computer_board_layout, user) == 'Q':
            print(f"Your remaining ships were located at: {player}\nThe computers remaining ships were located at: {computer}\n")
            return 'Q'
    
    if len(player) != 0 and len(computer) == 0:
        print(f"Your remaining ships were located at: {player}\n")
        return 'W'
    elif len(computer) != 0 and len(player) == 0:
        print(f"The computers remaining ships were located at: {computer}\n")
        return 'L'
    elif len(player) == 0 and len(computer) == 0:
        return 'D'


def coordinates_entered(player_ships, computer_ships, players_move, computer_move, player_board_layout, computer_board_layout, user):
    """
    Takes players and computers moves for each turn
    """ 
    j = 'True'
    while j == 'True':
        move = input("Please enter your move here, with column (x) then row (y) separated by a ',' i.e. x,y:\nIf you would like to quit the game please enter [Q].\n")

        if move == 'Q':
            return 'Q'

        j = move_checker(move, players_move, j)

    com_move = computer_move.pop(random.randrange(len(computer_move)))
    computer = 'Computer'

    hit_or_miss(move, computer_ships, player_board_layout, user, computer)
    hit_or_miss(com_move, player_ships, computer_board_layout, computer, user)


def move_checker(move, players_moves, j):
    """
    Checks the players input moves for input being a number and within the range of the board and have only entered 2 coordinates
    """
    r = range(1,6)
    moves = move.split( ',')

    try:
        if len(moves) != 2:
            print(f"Incorrect amount of coordinates have been entered, you have entered: {len(moves)} coordinates. Please only enter 2 coordinates")
        elif moves[0].isnumeric() == 'false':
            print(f"x coordinate is not a number you have entered: {moves[0]}\n")
        elif moves[1].isnumeric() == 'false':
            print(f"y coordinate is not a number you have entered: {moves[1]}\n")
        elif int(moves[0]) not in r:
            print(f"x coordinate is not a number on the board, you have entered: {moves[0]}\n")
        elif int(moves[1]) not in r:
            print(f"y coordinate is not a number on the board, you have entered: {moves[1]}\n")
        elif move in players_moves:
            print(f"You have already fired upon these coordinates: {moves}")
        else:
            players_moves.append(move)
            return 'False'
    except ValueError:
        print(f"Please check as your input was not a valid coordinates, you entered: {moves}")

    return 'True'


def hit_or_miss(move, enemy_ships, board_layout, name, oppositons_name):
    """
    Takes the move and checks if it's the same as a enemy ship coordinates if so will send a H if not O
    """
    if move in enemy_ships:
        hit = 'H'
        enemy_ships.remove(move)
    else:
        hit = 'O'
    outcome(move, board_layout, hit, name, oppositons_name)
        


def outcome(data, board_data, HM, name, oppositons_name):
    """
    Take the users input and edit the board data to change a - to H or O depending if it's a hit or miss
    """
    xandy = data.split(',')
    x = int(xandy[0])
    y = int(xandy[1])

    if HM == 'H':
        board_data[y][x] = 'H'
        HorM = 'Hit!'
    else:
        board_data[y][x] = 'O'
        HorM = 'Miss'

    print('--------------------------------------')
    print(F"{oppositons_name}'s ships locations\n")

    print(*board_data[5], sep = ' ')
    print(*board_data[4], sep = ' ')
    print(*board_data[3], sep = ' ')
    print(*board_data[2], sep = ' ')
    print(*board_data[1], sep = ' ')
    print(*board_data[0], sep = ' ')
    print(*board_data[6], sep = ' ')

    print(' ')
    print(f"{name} has fired upon: {data} its a {HorM}")
    print('--------------------------------------')


def results(result, user):
    """
    Displays the result of the game and if the player has an account will display their total win/lose/draw
    """
    score = SHEET.worksheet('score')

    if user != 'Guess':
        username_place = score.col_values(1).index(user)
        win = score.col_values(2)[username_place]
        lose = score.col_values(3)[username_place]
        draw = score.col_values(4)[username_place]

    if result == 'W':
        print(f"Congratulations {user} you won!")
        if user != 'Guess':
            win = int(win) + 1
    elif result == 'L':
        print(f"Better luck next time {user} you lost :(")
        if user != 'Guess':
            lose = int(lose) + 1
    elif result == 'D':
        print(f"So close {user} you drew!")
        if user != 'Guess':
            draw = int(draw) + 1

    if user != 'Guess' and result != 'Q':
        print(f"\nwins: {win}\nLoses: {lose}\nDraws: {draw}")

        score.update('B' + str(username_place+1), win)
        score.update('C' + str(username_place+1), lose)
        score.update('D' + str(username_place+1), draw)


def still_playing(user):
    """
    To determine if the payer would like to play another round of battleships
    """
    t = 0
    while t == 0:
        decision = input(f"Would you like to play another game? \nEnter [P] to play another\nEnter [Q] to quite to the game\n")
        
        if decision == 'P':
            return True
        elif decision == 'Q':
            print('Thank you for playing!')
            return False
        else:
            print(f"The input has not been recognised you have entered: {decision}, Please try again.\n")       


def main():
    """
    Runs all functions
    """
    user = login_choice()
    play = True
    while play == True:
        ship_location = play_battleship(user)
        result = score_checker(ship_location[0], ship_location[1], ship_location[2], ship_location[3], ship_location[4], ship_location[5], user)
        results(result, user)
        play = still_playing(user)


print('Welcome lets play Battleships!')
main()