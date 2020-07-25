import os
clear = lambda: os.system('cls')
# Tasks:
#
#   1. [X] Teams
#   2. [ ] Valid Moves
#       2.1 [ ] My team vs theirs
#   3. [ ] Possible Moves
#       3.1 [ ] Rook
#           3.1.1 [ ] Infinate Moves
#       3.2 [ ] Knight
#       3.3 [ ] Bishop
#       3.4 [ ] Queen
#       3.5 [X] King
#       3.6 [ ] Pawn
#


def add_c(c,i):
    return chr(ord(c) + i)

def add_pos(pos,col,row):
    return add_c(pos[0], col) + add_c(pos[1], row)

def direction_gen(pos, direction, board, team):
    next_pos = add_pos(pos, direction[0], direction[1])
    piece_at = board.piece_hash.get(next_pos, None)
    if can_go(next_pos, board, team):
        yield next_pos
        if next_pos not in board.piece_hash:
            yield from direction_gen(next_pos, direction, board, team)

def around_gen(pos, board, team):
    xs = [
        (-1,1) ,(0,1) ,(1,1),
        (-1,0)        ,(1,0),
        (-1,-1),(0,-1),(1,-1)]
    for x in xs:
        print(x)
        if can_go(pos, board, team):
            yield add_pos(pos, x[0], x[1])

def can_go(pos, board, team):
    if pos not in board.wb:
        return False
    piece_at = board.piece_hash.get(pos, None)
    if not piece_at or piece_at.team != team:
            # take enemy piece
            return True

def around_dir_gen(pos, board, team):
    xs = [
        (-1,1) ,(0,1) ,(1,1),
        (-1,0)        ,(1,0),
        (-1,-1),(0,-1),(1,-1)]
    for x in xs:
        if can_go(next_pos, board, team):
            yield add_pos(pos, x[0], x[1])

def knight_gen(pos, board, team):
    xs = [
            (-1, 2)      ,(1,2),
    (-2,1)                      ,(2,1),
                
    (-2,-1)                      ,(2,-1),
            (-1,-2)      ,(1,-2)]
    for x in xs:
        next_pos = add_pos(pos, x[0], x[1])
        if can_go(next_pos, board, team):
            yield next_pos 

class Piece():
    def __init__(self):
        self.icon = "X"
        self.move_gens = list()
        self.team = 0

    def valid_moves(self, pos):
        for move_gen in self.move_gens:
            mg = move_gen(pos)
            yield from move_gen(pos)

    def set_team(self):
        self.icon = self.icon.swapcase()
        # swaps between 0,1
        self.team = (self.team + 1) & 1
        return self

    def init_move_gens(self, board):
        raise Exception("init_move_gens Not implemented")

class King(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "K"

    def init_move_gens(self, board):
        gen = lambda pos: around_dir_gen(pos, board, self.team)
        self.move_gens.append(gen)

class Queen(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "Q"

    def init_move_gens(self, board):
        up = lambda pos: direction_gen(pos, (0,1), board, self.team)
        down = lambda pos: direction_gen(pos, (0,-1), board, self.team)
        left = lambda pos: direction_gen(pos, (1,0), board, self.team)
        right = lambda pos: direction_gen(pos, (-1,0), board, self.team)
        
        upleft = lambda pos: direction_gen(pos, (1,1), board, self.team)
        upright = lambda pos: direction_gen(pos, (-1,1), board, self.team)
        downleft = lambda pos: direction_gen(pos, (1,-1), board, self.team)
        downright = lambda pos: direction_gen(pos, (-1,-1), board, self.team)
        for gen in [up, down, left, right, upleft, upright, downleft, downright]:
            self.move_gens.append(gen)

class Pawn(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "P"
        self.moved = 0

    def init_move_gens(self, board):
        up = lambda pos: self.move_generator(pos, board)
        for gen in [up]:
            self.move_gens.append(gen)

    def move_generator(self, pos, board):
        direction = (self.team & 1) - (self.team+1 & 1) 
        
        attack = [(-1,direction), (1,direction)]
        row = int(pos[1])
        movement = [(0,direction)]
        if row == 7 or row == 2:
            movement.append((0,direction*2))

        for move in movement:
            next_pos = add_pos(pos, move[0], move[1])
            if next_pos not in board.piece_hash:
                yield next_pos

        for move in attack:
            next_pos = add_pos(pos, move[0], move[1])
            if next_pos in board.piece_hash and board.piece_hash[next_pos].team != self.team:
                yield next_pos

class Rook(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "R"

    def init_move_gens(self, board):
        up = lambda pos: direction_gen(pos, (0,1), board, self.team)
        down = lambda pos: direction_gen(pos, (0,-1), board, self.team)
        left = lambda pos: direction_gen(pos, (1,0), board, self.team)
        right = lambda pos: direction_gen(pos, (-1,0), board, self.team)
        for gen in [up, down, left, right]:
            self.move_gens.append(gen)

class Bishop(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "B"

    def init_move_gens(self, board):
        upleft = lambda pos: direction_gen(pos, (1,1), board, self.team)
        upright = lambda pos: direction_gen(pos, (-1,1), board, self.team)
        downleft = lambda pos: direction_gen(pos, (1,-1), board, self.team)
        downright = lambda pos: direction_gen(pos, (-1,-1), board, self.team)
        for gen in [upleft, upright, downleft, downright]:
            self.move_gens.append(gen)

class Knight(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "H"

    def init_move_gens(self, board):
        gen = lambda pos: knight_gen(pos, board, self.team)
        self.move_gens.append(gen)

class Board():
    def __init__(self):
        self.rows = list(range(8,0,-1))
        self.cols = list("ABCDEFGH")
        self.piece_hash = dict()

        # true/false for showing white or black for squares
        # because we're adding the chr and int we get the desired pattern via odd/even test
        all_keys = [col+str(row) for row in self.rows for col in self.cols]
        self.wb = dict([(k,(ord(k[0])+int(k[1])+1)%2==0) for i,k in enumerate(all_keys)])

    def box(self, key):
        if self.wb[key]:
            # white
            return "[{}]"
        else:
            # black
            return ":{}:"

    def occupied(self, loc):
        return key in self.piece_hash

    def move(self, start, end):
        self.piece_hash[end] = self.piece_hash[start]
        del self.piece_hash[start]

    def icon_at(self, key):
        piece = self.piece_hash.get(key, None)
        return (piece.icon if piece else " ")
    
    def draw(self):
        for row in self.rows:
            keys = [self.box(col+str(row)).format(self.icon_at(col+str(row))) for col in self.cols]
            print("".join(keys))
            
    def print(self):
        for row in self.rows:
            print(" ".join([col+str(row) for col in self.cols]))

def standard_start(board):
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

def is_valid(key, board, team):
    if not key:
        print("Null Input")
        return False

    s = key.upper().split(",")
    if len(s) != 2:
        print("Bad format", s)
        return False

    start = s[0]
    end = s[1]
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
            if userin == "exit" or is_valid(userin, board, team):
                team = (team + 1) & 1
                break
            else: 
                print("Invalid.")

def test():
    board = Board()
    board.print()

    print()
    standard_start(board)
    board.draw()

    knights = [(k,v) for (k,v) in board.piece_hash.items() if isinstance(v, Knight)]

    locs = set()
    for (key, knight) in knights:
        knight.init_move_gens(board)
        for loc in list(knight.valid_moves(key)):
            board.piece_hash[loc] = Piece()
            locs.add(loc)
    print()
    print("All possible moves for knights")
    board.draw()
    for loc in locs:
        del board.piece_hash[loc]

    queens = [(k,v) for (k,v) in board.piece_hash.items() if isinstance(v, Queen)]

    locs = set()
    for (key, queen) in queens:
        queen.init_move_gens(board)
        for loc in list(queen.valid_moves(key)):
            board.piece_hash[loc] = Piece()
            locs.add(loc)
    
    print()
    print("All possible moves for queens")
    board.draw()

    for loc in locs:
        del board.piece_hash[loc]




    # q = Queen()
    # k = King()
    # p = Pawn()
    # board.piece_hash["A8"] = q
    # board.piece_hash["B2"] = k
    # board.piece_hash["E2"] = p
    # board.draw()
    # print()

    # board.move("B2", list(k.valid_moves("B2"))[2])
    # print(board.piece_hash)

    # board.draw()

    
    

if __name__ == "__main__":
    print("Chess\n")
    main()
