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

def direction_gen(pos, dir, board, team):
    next_pos = add_pos(pos, dir[0], dir[1])
    piece_at = board.piece_hash.get(next_pos, None)
    if piece_at:
        if piece_at.team != team:
            # take enemy piece
            next_pos
    else:
        yield next_pos
        yield from direction_gen

def around_gen(pos):
    print("called")
    xs = [
        (-1,1) ,(0,1) ,(1,1),
        (-1,0)        ,(1,0),
        (-1,-1),(0,-1),(1,-1)]
    for x in xs:
        print(x)
        yield add_pos(pos, x[0], x[1])

def can_go(pos, board, team):
    if pos not in board.wb:
        print(pos)
        return False
    piece_at = board.piece_hash.get(pos, None)
    if not piece_at or piece_at.team != team:
            # take enemy piece
            return True

def around_dir_gen(pos):
    xs = [
        (-1,1) ,(0,1) ,(1,1),
        (-1,0)        ,(1,0),
        (-1,-1),(0,-1),(1,-1)]
    for x in xs:
        print(x)
        yield add_pos(pos, x[0], x[1])

def knight_gen(pos, board, team):
    xs = [
            (-1, 2)      ,(1,2),
    (-2,1)                      ,(2,1),
                
    (-2,-1)                      ,(2,-1),
            (-1,-2)      ,(1,-2)]
    for x in xs:
        print(x)
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
            yield from move_gen(pos)

    def set_team(self):
        self.icon = self.icon.swapcase()
        # swaps between 0,1
        self.team = (self.team + 1) & 1
        return self

class King(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "K"
        self.move_gens.append(around_gen)

class Queen(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "Q"

class Pawn(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "P"

class Rook(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "R"

class Bishop(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "B"


class Knight(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "H"
        self.move_gens.append(knight_gen)


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
    board.piece_hash["D1"] = Queen().set_team()
    board.piece_hash["E1"] = King().set_team()
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

class Pos:
    def __init__(self, key, board):
        self.key = key
        self.board = board


def main():
    board = Board()
    board.print()

    print()
    standard_start(board)
    board.draw()
    board.piece_hash["G1"]
    print(list(knight_gen("G1", board, board.piece_hash["G1"].team)))
    for loc in knight_gen("G1", board, board.piece_hash["G1"].team):
        board.piece_hash[loc] = Piece()
    
    print()
    board.draw()

    for loc in knight_gen("G1", board, board.piece_hash["G1"].team):
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