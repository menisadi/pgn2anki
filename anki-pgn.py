import chess
import sys
import chess.pgn
import genanki
import random
from bs4 import BeautifulSoup
import requests
import io


def fetch_pgn(url):
    
    print(url)
    # The website server expected a header to be passed:
    # So we give him this
    # Taken from https://stackoverflow.com/questions/60837734/you-dont-have-permission-to-access-this-resource-python-webscraping
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '\
            'AppleWebKit/537.36 (KHTML, like Gecko) '\
            'Chrome/75.0.3770.80 Safari/537.36'}

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    # For some reason the id of the div containing the PGN is named olga-data
    olga = soup.find(id = "olga-data")
    print(olga.attrs['pgn'])
    return olga.attrs['pgn']

def main(source_pgn):

    pgn = chess.pgn.read_game(source_pgn)
    board = pgn.board()
    name = pgn.headers["White"] + " vs " + pgn.headers["Black"]
    print(name)

    # Pick a pseudo-unique (random) model ID
    model_id = random.randrange(1 << 30, 1 << 31)

    # Define the model
    anki_model = genanki.Model(
        model_id,
        'Chess PGN',
        fields=[
            {'name': 'Before'},
            {'name': 'After'},
            {'name': 'Move Number'},
            {'name': 'Turn'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div style="text-align: center; font-weight: bold;">{{Move Number}}.</div><div style="text-align: center; font-weight: bold;">{{Turn}} To Move</div>[fen]{{Before}}[/fen]',
                'afmt': '{{FrontSide}}<hr id="after">[fen]{{After}}[/fen]',
            },
        ]
    )
    
    # Create a new Anki deck
    deck = genanki.Deck(model_id, name)

    # Initialize the move counter
    move_counter = 0

    # Iterate through the moves
    for move in pgn.mainline_moves():
        
        turn = board.turn
        if turn == chess.WHITE:
            move_counter += 1
            turn = 'White'
        else:
            turn = 'Black'

        current_board = board.fen()
        
        # Make the move on the board
        board.push(move)        
        following_board = board.fen()

        # Create a new Anki note with the board in FEN notation on the front
        note = genanki.Note(
            model=anki_model,
            fields=
            [current_board, 
            following_board, 
            str(move_counter),
            turn
            ]
        )
        deck.add_note(note)

    # Save the deck to a file
    file_name = name.replace(" vs ", "_vs_").replace(" ", "")
    print(file_name)
    genanki.Package(deck).write_to_file(file_name+'.apkg')
        

if __name__ == "__main__":
    game_source = sys.argv[1]

    if game_source[-4:] == ".pgn":
        source_pgn = open(game_source)        
    elif game_source.find("chessgames.com") >= 0:
        pgn_string = fetch_pgn(game_source)
        source_pgn = io.StringIO(pgn_string)
    else: 
        print("Source doesn't seem to be neither PGN file nor chessgames game link")
        sys.exit()

    main(source_pgn)
