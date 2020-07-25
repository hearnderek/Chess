












class Piece():
    def __init__(self):
        self.icon = "X"
        self.move_gens = list()

    def valid_moves(self, pos):
        for move_gen in self.move_gens:
            yield from move_gen(pos)

class Queen(Piece):
    def __init__(self):
        self.icon = "Q"

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

class King(Piece):
    def __init__(self):
        Piece.__init__(self)
        self.icon = "K"
        self.move_gens.append(around_gen)

class Board():
    def __init__(self):
        self.rows = list(range(8,0,-1))
        self.cols = list("ABCDEFGH")
        self.piece_hash = dict()

    def icon_at(self, key):
        piece = self.piece_hash.get(key, None)
        return (piece.icon if piece else " ")
       
    def draw(self):
        for row in self.rows:
            keys = ["["+self.icon_at(col+str(row))+"]" for col in self.cols]
            print(" ".join(keys))
            

    def print(self):
        for row in self.rows:
            print(" ".join([col+str(row) for col in self.cols]))

class Pos:
    def __init__(self, key, board):
        self.key = key
        self.board = board
        

def main():
    board = Board()
    board.print()

    q = Queen()
    k = King()
    board.piece_hash["A8"] = q
    board.piece_hash["B2"] = k
    for loc in k.valid_moves("B2"):
        print(loc)
        board.piece_hash[loc] = Piece()

    board.draw()
    
    

if __name__ == "__main__":
    print("Chess\n")
    main()