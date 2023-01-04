import sys
import chess
import chess.pgn

def colors(color):
    if color:
        return "White"
    else:
        return "Black"

    
def node_travel(node):
    if not node.is_end():
        for child in node.variations:
            yield [node.board(), child.board(), child.ply(), colors(child.turn())]
            yield from node_travel(child)


def main(source_pgn):
    pgn = chess.pgn.read_game(source_pgn)
    traveler = node_travel(pgn)
    for step in traveler:
        b, c, p, t = step
        print(f"{p} : {t}")
    
if __name__ == '__main__':
    source = sys.argv[1]
    source_pgn = open(source)
        
    main(source_pgn)




