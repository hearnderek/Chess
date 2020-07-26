from pieces import Rook, Bishop, Knight, King, Queen, Pawn
from board import Board

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
