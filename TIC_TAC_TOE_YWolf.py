# Tic-tac-toe
# Yurate Wolf 24/08/2022

# INTRODUCTION
import time

print("               Welcome to TIC-TAC-TOE!", end='\n\n')

time.sleep(2)

print(" ! In order to start, please read the rules carefully !")

# RULES
# name variable for the rules itself
print_rules = (" \n RULES:\n"
               "Tic-tac-toe is played on a three-by-three grid by two players, who alternately\nplace "
               "the marks X and O in one of the nine spaces in the grid. In this\n"
               "particular case the player who plays for X starts first. During the game you\nwould "
               "need to use only Numpad (numbers to be used are from 1 to 9)."
               " \n\n GAME STARTS, GOOD LUCK!\n")

# create variable option to skip the rules
skip_rules = None
while skip_rules not in ("yes", "no"):
    skip_rules = input(" If you want to skip the rules please enter yes or no:")
    if skip_rules == "yes":
        print(" \n\n GAME STARTS, GOOD LUCK!\n")
    elif skip_rules == "no":
        print(print_rules)
    else:
        print(" Wrong input. Please try again,check for spelling mistakes (no space).")

# GAME
game_active = True
current_player = ' X '
game_board = ["  ",
              " 1 ", " 2 ", " 3 ",
              " 4 ", " 5 ", " 6 ",
              " 7 ", " 8 ", " 9 "]


def game_board_print():
    print(game_board[1] + game_board[2] + game_board[3])
    print(game_board[4] + game_board[5] + game_board[6])
    print(game_board[7] + game_board[8] + game_board[9])


# Game input and check of the input
def player_definition():
    global game_active
    while True:
        move = input(" Please select number on the board above where to put your " + current_player + ":")
        # Game ends earlier for players
        if move == 'q':
            game_active = False
            return
        try:
            move = int(move)
        except ValueError:
            print(" Please give number from 1 to 9.")
        else:
            if 1 <= move <= 9:
                return move
            else:
                print("The value must be equal or more than 1 and equal or less than 9.")


def player_change():
    global current_player
    if current_player == ' X ':
        current_player = ' O '
    else:
        current_player = ' X '


# Check of the winning situations:
def win_check():
    # check on rows
    if game_board[1] == game_board[2] == game_board[3]:
        return game_board[1]
    if game_board[4] == game_board[5] == game_board[6]:
        return game_board[4]
    if game_board[7] == game_board[8] == game_board[9]:
        return game_board[7]
    # check on columns
    if game_board[1] == game_board[4] == game_board[7]:
        return game_board[1]
    if game_board[2] == game_board[5] == game_board[8]:
        return game_board[2]
    if game_board[3] == game_board[6] == game_board[9]:
        return game_board[3]
    # check on diagonals
    if game_board[1] == game_board[5] == game_board[9]:
        return game_board[5]
    if game_board[7] == game_board[5] == game_board[3]:
        return game_board[5]


# Check of undetermined situations:
def check_undeterm():
    if (game_board[1] == 'X' or game_board[1] == 'O') \
            and (game_board[2] == 'X' or game_board[2] == 'O') \
            and (game_board[3] == 'X' or game_board[3] == 'O') \
            and (game_board[4] == 'X' or game_board[4] == 'O') \
            and (game_board[5] == 'X' or game_board[5] == 'O') \
            and (game_board[6] == 'X' or game_board[6] == 'O') \
            and (game_board[7] == 'X' or game_board[7] == 'O') \
            and (game_board[8] == 'X' or game_board[8] == 'O') \
            and (game_board[9] == 'X' or game_board[9] == 'O'):
        return "UNDETERMINED"


# Output current game board
game_board_print()
while game_active:
    # Input active players
    print()
    print(" It is the turn of:" + current_player + " player")
    move = player_definition()
    if move:
        game_board[move] = current_player
        # Print actual board game
        game_board_print()
        # Check if someone won
        won = win_check()
        if won:
            print(" CONGRATULATIONS, PLAYER" + won + "WON!")
            game_active = False
            break
        # Check whether it is undetermined
        undetermined = check_undeterm()
        if undetermined:
            print(" GAME ENDED IN A DRAW")
            game_active = False
            # Change the player
        player_change()
print("  \n\n THANK YOU FOR THE GAME!")
