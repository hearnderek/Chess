"""
Basic Piece Classes

Contains the rules for how pieces move, but need to be actived by x.init_move_gens
"""
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
