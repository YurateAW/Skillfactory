# Sea battle game
# Yurate Wolf 09/09/2022

from random import randint
import time


# GAME
# DEFINITION OF DIFFERENT EXCLUSION CLASSES
class BoardException(Exception):
    pass


# 1. Definition of exclusion out of the Board range (outside the 6x6 grid)
class BoardOutException(BoardException):
    def __str__(self):
        return "Your attempt is out of the board range!"


# 2. Definition of exclusion for repetitive attempt
class BoardAttemptException(BoardException):
    def __str__(self):
        return "You have already given this value"


# 3. Definition of exclusion for misplaced ship
class BoardMisplacedException(BoardException):
    pass


# DEFINITION OF CLASS DOT
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 1. Comparison method using _eq_, checking if the values are equal to each other
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # 2. Return of the dots for check
    def __repr__(self):
        return f"({self.x}, {self.y})"


# DEFINITION OF CLASS SHIP
class Ship:
    def __init__(self, shlength, shnose, shorient):
        self.shlength = shlength  # length of the ship
        self.shnose = shnose  # ship nose
        self.shorient = shorient  # ship orientation
        self.shlives = shlength  # number of ship lives

# Dots- method, thant returns a list of all ship points
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.shlength):
            cur_x = self.shnose.x
            cur_y = self.shnose.y

            if self.shorient == 0: 
                cur_x += i

            elif self.shorient == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))  # Fill the list ship_dots

        return ship_dots

    # Shoten- method, thant returns shot in the coordinates
    def shoten(self, shot):
        return shot in self.dots


# DEFINITION OF CLASS BOARD
# 1. Defined hid (type bool) - opened or not the board,
# 2. Size: defines the size of the board grid (6x6)
# 3. Ships: is the definition of the list of ships on the board
# 4. Busy: cells that are busy by a ship or already been shot
class Board:
    def __init__(self, hid=True, size=6):

        self.hid = hid
        self.size = size
        self.ships = []
        self.busy = []
        self.count = 0
        self.field = [['-'] * 6 for i in range(6)]


    # Method add_ship: adds the ship on class board and if it can not place then calls the exclusion
    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardMisplacedException()
        for d in ship.dots:
            self.field[d.x][d.y] = "O"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    # Method contour: defines the points around the contour where the ships can not be placed
    def contour(self, ship, mission=False):  # mission - point of hitting the ship
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]  # Ship coordinate is (0, 0)
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if mission:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    # Definition of the Grid print of our board
    def __str__(self):
        grid = ""
        print(f"  | 1  2  3  4  5  6 |")
        print('-- --- --- --- --- --- ---')
        for i, row in enumerate(self.field):
            grid = f"{i + 1} | {' | '.join(row)} |"
            print(grid)
            print("-- --- --- --- --- --- ---")

        if self.hid:
            grid.replace("O", ".")
        return ''

    # Method out: defined for the class Dot
    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Method shot: does the shots on the ships
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardAttemptException()

        self.busy.append(d)

        # Calculating the number of lives
        for ship in self.ships:
            if ship.shoten(d):
                ship.shlives -= 1
                self.field[d.x][d.y] = "X"
                if ship.shlives == 0:
                    self.count += 1
                    self.contour(ship, mission=True)
                    print("Congratulations, ship is fully destroyed.")
                    return False
                else:
                    print("Ship is partially destroyed.")
                    return True

        self.field[d.x][d.y] = "."
        print("You missed")
        return False

    def begin(self):
        self.busy = []


# DEFINITION OF GENERAL CLASS PLAYER WITH ASK AND MOVE METHOD
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:  # Calling exception
                print(e)

# DEFINITION CLASS ARTIFICIAL INTELLIGENCE
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Your opponent move: {d.x + 1} {d.y + 1}")
        return d


# DEFINITION CLASS USER
class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn: ").split()

            if len(cords) != 2:  #
                print(" Please enter 2 values from 1to 6 using space in between.")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Please enter numbers only. ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


# DEFINITION CLASS GAME
class Game:
    def __init__(self, size=6):
        self.size = size
        playerb = self.random_board()  # Player board randomly generated
        compb = self.random_board()  # Computer board randomly generated
        compb.hid = True  # Computer board hidden

        self.ai = AI(compb, playerb)
        self.user = User(playerb, compb)

    # Definition of random_board method
    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

# DEFINITION OF GREET FUNCTION
    def greet(self):

        print("               Welcome to Sea battle game!", end='\n\n')

        time.sleep(2)

        print(" ! In order to start, please read the rules carefully !"
              """

    RULES:
    1. A 6x6 grid will have 7 ships of length of 1x3, 2x2 and 4x1 randomly placed about
    2. You will have 50 bullets to take down the ships that are placed down
    3. You can choose a row and column using space to indicate where to shoot
    4. For every shot that hits or misses it will show up in the grid
    5. A ship cannot be placed diagonally, so if a shot hits the rest of
        the ship is in one of 4 directions, left, right, up, and down
    6. If all ships are unearthed before using up all bullets, you win
        else, you lose
    Legend:
    1. "O"  = Ship positions
    2. "-" = empty space
    3. "X" = part of ship that was hit with bullet
    4. "." = water that was shot with bullet, a miss because it hit no ship
"""

              " \n\n GAME STARTS, GOOD LUCK!\n")

    # Randomly places ships on board
    def random_place(self):
        length = [3, 2, 2, 1, 1, 1, 1]  # Condition on number of ships on the board
        board = Board(size=self.size)
        attempts = 0
        for shlength in length:
            while True:
                attempts += 1
                if attempts > 5000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), shlength, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardMisplacedException:
                    pass
        board.begin()
        return board

    # Definition of the loop method
    def loop(self):
        num = 0  # number of turns
        while True:
            print("-" * 50)
            print("Player board:")
            print(self.user.board)
            print("-" * 50)
            print("Computer board:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 50)
                print("Player turn")
                repeat = self.user.move()
            else:
                print("-" * 50)
                print("Computer turn")

                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 50)
                print("PLAYER WON!!!")
                break

            if self.user.board.count == 7:
                print("-" * 50)
                print("COMPUTER WON!!!")
                break
            num += 1

    # Game start method
    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()



