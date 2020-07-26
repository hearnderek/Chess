"""
Hello Doc String
"""
from board import Board
from standard_game import standard_start, try_user_movement
import os

clear = lambda: os.system('cls')

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
