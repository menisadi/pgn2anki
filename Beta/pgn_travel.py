import sys
import chess
import chess.pgn
import numpy as np

def colors(color):
    if color:
        return "White"
    else:
        return "Black"

    
def pgn_travel(node):
    if not node.is_end():
        for child in node.variations:
            yield [node.board(), child.board(), node.ply(), colors(node.turn())]
            yield from pgn_travel(child)


def main(source_pgn):
    pgn = chess.pgn.read_game(source_pgn)
    traveler = pgn_travel(pgn)
    white_steps = (step for step in traveler if step[3]=='White')
    for step in white_steps:
        b, c, p, t = step
        print(b)
        print(f"{int(np.ceil((p+1)/2))}: {t}")

        
if __name__ == '__main__':
    source = sys.argv[1]
    source_pgn = open(source)
        
    main(source_pgn)
