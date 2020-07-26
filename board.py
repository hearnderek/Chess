
import pieces

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