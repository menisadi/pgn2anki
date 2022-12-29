import chess
import sys
import chess.pgn
import genanki
import random


def main(pgn_file):
    
    # Read the PGN from file
    pgn = chess.pgn.read_game(pgn_file)
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
    source_file = open(sys.argv[1])
    main(source_file)
