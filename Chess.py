"""
Hello Doc String
"""

import os
clear = lambda: os.system('cls')

def add_c(char, i):
    """ ("A", 1) -> "B" """
    return chr(ord(char) + i)

def add_pos(pos, col, row):
    """ (E6, 1, -2) -> F4 """
    return add_c(pos[0], col) + add_c(pos[1], row)

def direction_gen(pos, direction, board, team):
    """ raytracing for possible moves """
    next_pos = add_pos(pos, direction[0], direction[1])
    if can_go(next_pos, board, team):
        yield next_pos
        if next_pos not in board.piece_hash:
            yield from direction_gen(next_pos, direction, board, team)

def can_go(pos, board, team):
    """ Can I move there? Killing the other team is okay. """
    if pos not in board.squares:
        return False
    piece_at = board.piece_hash.get(pos, None)
    if not piece_at or piece_at.team != team:
        # take enemy piece
        return True
    return False

def around_dir_gen(pos, board, team):
    """ Generate the moves for the king """
    directions = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
    for direction in directions:
        next_pos = add_pos(pos, direction[0], direction[1])
        if can_go(next_pos, board, team):
            yield next_pos

def knight_gen(pos, board, team):
    """ Generate the moves for the knight """
    directions = [(-1, 2), (1, 2), (-2, 1), (2, 1), (-2, -1), (2, -1), (-1, -2), (1, -2)]
    for direction in directions:
        next_pos = add_pos(pos, direction[0], direction[1])
        if can_go(next_pos, board, team):
            yield next_pos

class Piece():
    """ Base class for all game pieces """
    def __init__(self):
        self.icon = "X"
        self.move_gens = list()
        self.team = 0

    def valid_moves(self, pos):
        """
        Using underlying self.move_gen generate all possible moves

        move_gen is populated through the call to init_move_gens
        """
        for move_gen in self.move_gens:
            yield from move_gen(pos)

    def set_team(self):
        """ Flips the team bit """
        self.icon = self.icon.swapcase()
        # swaps between 0,1
        self.team = (self.team + 1) & 1
        return self

    def init_move_gens(self, board):
        """ All inheriting classes should implement this to populate self.move_gen """
        raise Exception(str(type(self)) + ": init_move_gens Not implemented")

class King(Piece):
    """ The King """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "K"

    def init_move_gens(self, board):
        gen = lambda pos: around_dir_gen(pos, board, self.team)
        self.move_gens.append(gen)

class Queen(Piece):
    """ The Queen """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "Q"

    def init_move_gens(self, board):
        up = lambda pos: direction_gen(pos, (0, 1), board, self.team)
        down = lambda pos: direction_gen(pos, (0, -1), board, self.team)
        left = lambda pos: direction_gen(pos, (1, 0), board, self.team)
        right = lambda pos: direction_gen(pos, (-1, 0), board, self.team)

        upleft = lambda pos: direction_gen(pos, (1, 1), board, self.team)
        upright = lambda pos: direction_gen(pos, (-1, 1), board, self.team)
        downleft = lambda pos: direction_gen(pos, (1, -1), board, self.team)
        downright = lambda pos: direction_gen(pos, (-1, -1), board, self.team)
        for gen in [up, down, left, right, upleft, upright, downleft, downright]:
            self.move_gens.append(gen)

class Pawn(Piece):
    """ The Pawn """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "P"
        self.moved = 0

    def init_move_gens(self, board):
        up = lambda pos: self.move_generator(pos, board)
        for gen in [up]:
            self.move_gens.append(gen)

    def move_generator(self, pos, board):
        """ Strangly the pawn is the move conplicated mover """
        direction = (self.team & 1) - (self.team + 1 & 1)

        attack = [(-1, direction), (1, direction)]
        row = int(pos[1])
        movement = [(0, direction)]
        if row in (2, 7):
            movement.append((0, direction * 2))

        for move in movement:
            next_pos = add_pos(pos, move[0], move[1])
            if next_pos not in board.piece_hash:
                yield next_pos

        for move in attack:
            next_pos = add_pos(pos, move[0], move[1])
            if next_pos in board.piece_hash and board.piece_hash[next_pos].team != self.team:
                yield next_pos

class Rook(Piece):
    """ The Rook """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "R"

    def init_move_gens(self, board):
        up = lambda pos: direction_gen(pos, (0, 1), board, self.team)
        down = lambda pos: direction_gen(pos, (0, -1), board, self.team)
        left = lambda pos: direction_gen(pos, (1, 0), board, self.team)
        right = lambda pos: direction_gen(pos, (-1, 0), board, self.team)
        for gen in [up, down, left, right]:
            self.move_gens.append(gen)

class Bishop(Piece):
    """ The Bishop """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "B"

    def init_move_gens(self, board):
        upleft = lambda pos: direction_gen(pos, (1, 1), board, self.team)
        upright = lambda pos: direction_gen(pos, (-1, 1), board, self.team)
        downleft = lambda pos: direction_gen(pos, (1, -1), board, self.team)
        downright = lambda pos: direction_gen(pos, (-1, -1), board, self.team)
        for gen in [upleft, upright, downleft, downright]:
            self.move_gens.append(gen)

class Knight(Piece):
    """ The Knight """
    def __init__(self):
        Piece.__init__(self)
        self.icon = "H"

    def init_move_gens(self, board):
        gen = lambda pos: knight_gen(pos, board, self.team)
        self.move_gens.append(gen)

class Board():
    """ The Knight """
    def __init__(self):
        self.rows = list(range(8, 0, -1))
        self.cols = list("ABCDEFGH")
        self.piece_hash = dict()

        # true/false for showing white or black for squares
        # because we're adding the chr and int we get the desired pattern via odd/even test
        all_keys = [col+str(row) for row in self.rows for col in self.cols]
        enumerated_keys = enumerate(all_keys)
        self.squares = dict([(k, (ord(k[0]) + int(k[1]) + 1) % 2 == 0) for i, k in enumerated_keys])

    def box(self, key):
        """ String to draw the board, with room for a piece """
        if self.squares[key]:
            # white
            return "[{}]"
        return ":{}:"

    def move(self, start, end):
        """ Move from here to there """
        self.piece_hash[end] = self.piece_hash[start]
        del self.piece_hash[start]

    def icon_at(self, key):
        """ get icon to draw at keyed location """
        piece = self.piece_hash.get(key, None)
        return piece.icon if piece else " "

    def draw(self):
        """ Draw the populated board """
        for row in self.rows:
            keys = [self.box(col+str(row)).format(self.icon_at(col+str(row))) for col in self.cols]
            print("".join(keys))


def standard_start(board):
    """ Populate a black board with pieces """
    board.piece_hash["A1"] = Rook().set_team()
    board.piece_hash["B1"] = Knight().set_team()
    board.piece_hash["C1"] = Bishop().set_team()
    board.piece_hash["D1"] = King().set_team()
    board.piece_hash["E1"] = Queen().set_team()
    board.piece_hash["F1"] = Bishop().set_team()
    board.piece_hash["G1"] = Knight().set_team()
    board.piece_hash["H1"] = Rook().set_team()

    board.piece_hash["A2"] = Pawn().set_team()
    board.piece_hash["B2"] = Pawn().set_team()
    board.piece_hash["C2"] = Pawn().set_team()
    board.piece_hash["D2"] = Pawn().set_team()
    board.piece_hash["E2"] = Pawn().set_team()
    board.piece_hash["F2"] = Pawn().set_team()
    board.piece_hash["G2"] = Pawn().set_team()
    board.piece_hash["H2"] = Pawn().set_team()

    board.piece_hash["A8"] = Rook()
    board.piece_hash["B8"] = Knight()
    board.piece_hash["C8"] = Bishop()
    board.piece_hash["D8"] = Queen()
    board.piece_hash["E8"] = King()
    board.piece_hash["F8"] = Bishop()
    board.piece_hash["G8"] = Knight()
    board.piece_hash["H8"] = Rook()

    board.piece_hash["A7"] = Pawn()
    board.piece_hash["B7"] = Pawn()
    board.piece_hash["C7"] = Pawn()
    board.piece_hash["D7"] = Pawn()
    board.piece_hash["E7"] = Pawn()
    board.piece_hash["F7"] = Pawn()
    board.piece_hash["G7"] = Pawn()
    board.piece_hash["H7"] = Pawn()

    for piece in board.piece_hash.values():
        piece.init_move_gens(board)

def try_user_movement(key, board, team):
    """ Is the User Input string valid? """
    if not key:
        print("Null Input")
        return False

    splits = key.upper().split(",")
    if len(splits) != 2:
        print("Bad format", splits)
        return False

    start = splits[0]
    end = splits[1]
    if start not in board.piece_hash:
        print("can't find", start)
        return False

    piece = board.piece_hash[start]
    if piece.team != team:
        print("Wrong team.")
        return False

    possibles = piece.valid_moves(start)
    if end not in possibles:
        print("can't move to", end)
        return False

    board.move(start, end)
    return True

def main():
    """ Program Entry Point """
    board = Board()
    standard_start(board)

    userin = ""
    team = 0
    teams = ["white", "black"]

    while userin != "exit":
        clear()
        board.draw()

        print(teams[team], "Enter Move -- example: E8,E7")
        while True:
            userin = input()
            print()
            if userin == "exit" or try_user_movement(userin, board, team):
                team = (team + 1) & 1
                break
            print("Invalid.")

if __name__ == "__main__":
    print("Chess\n")
    main()
