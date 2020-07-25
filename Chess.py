def add_c(c,i):
    return chr(ord(c) + i)

def add_pos(pos,col,row):
    return add_c(pos[0], col) + add_c(pos[1], row)

def around_gen(pos):
    print("called")
    xs = [
        (-1,1) ,(0,1) ,(1,1),
        (-1,0)        ,(1,0),
        (-1,-1),(0,-1),(1,-1)]
    for x in xs:
        print(x)
        yield add_pos(pos, x[0], x[1])

class Piece():
    def __init__(self):
        self.icon = "X"
        self.move_gens = list()

    def valid_moves(self, pos):
        for move_gen in self.move_gens:
            yield from move_gen(pos)

    def set_team(self):
        self.icon = self.icon.swapcase()
        return self

class King(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "K"
        self.move_gens.append(around_gen)

class Queen(Piece):
    def __init__(self):
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




class Board():
    def __init__(self):
        self.rows = list(range(8,0,-1))
        self.cols = list("ABCDEFGH")
        self.piece_hash = dict()
        all_keys = [col+str(row) for row in self.rows for col in self.cols]
        self.wb = dict([(k,(ord(k[0])+int(k[1])+1)%2==0) for i,k in enumerate(all_keys)])

    def box(self, key):
        if self.wb[key]:
            return "[{}]"
        else:
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

    standard_start(board)
    board.draw()

    print(board.box("A8"))

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