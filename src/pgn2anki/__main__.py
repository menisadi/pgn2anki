import chess
import sys
import chess.pgn
import genanki
import random
from bs4 import BeautifulSoup
import requests
import io
import numpy as np
import argparse


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("source", help="Source of PGN.", type=str)

    # Optional arguments
    parser.add_argument("-C", "--color", help="Pick a color.", type=str, default="")

    # Print version
    parser.add_argument("--version", action="version", version="%(prog)s - Version 0.2")

    # Parse arguments
    args = parser.parse_args()

    return args


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


def fetch_pgn(url):

    # # The website server expected a header to be passed:
    # So we give him this
    # Taken from https://stackoverflow.com/questions/60837734/you-dont-have-permission-to-access-this-resource-python-webscraping
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/75.0.3770.80 Safari/537.36"
    }

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    # For some reason the id of the div containing the PGN is named olga-data
    olga = soup.find(id="olga-data")
    # print(olga.attrs['pgn'])
    return olga.attrs["pgn"]


def convert(source_pgn, color_pick):
    pgn = chess.pgn.read_game(source_pgn)
    # board = pgn.board()
    name = pgn.headers["White"] + " vs " + pgn.headers["Black"]
    if "?" in name:
        name = "ankipgn"
    print(name)

    # Pick a pseudo-unique (random) model ID
    model_id = random.randrange(1 << 30, 1 << 31)

    # Define the model
    anki_model = genanki.Model(
        model_id,
        "Chess PGN",
        fields=[
            {"name": "Before"},
            {"name": "After"},
            {"name": "Move Number"},
            {"name": "Turn"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": '<div style="text-align: center; font-weight: bold;">{{Move Number}}.</div><div style="text-align: center; font-weight: bold;">{{Turn}} To Move</div>[fen]{{Before}}[/fen]',
                "afmt": '{{FrontSide}}<hr id="after">[fen]{{After}}[/fen]',
            },
        ],
    )

    # Create a new Anki deck
    deck = genanki.Deck(model_id, name)

    # Initialize the move counter
    move_counter = 0

    # Iterate through the moves
    traveler = pgn_travel(pgn)
    if color_pick != "":
        selected_moves = (step for step in traveler if step[3] == color_pick)
    else:
        selected_moves = (step for step in traveler)

    for move in selected_moves:
        board, following_board, play, turn = move
        move_counter = int(np.ceil((play + 1) / 2))

        # turn = board.turn
        # if turn == chess.WHITE:
        #     move_counter += 1
        #     turn = 'White'
        # else:
        #     turn = 'Black'

        # current_board = board.fen()

        # Make the move on the board
        # board.push(move)
        # following_board = board.fen()

        # Create a new Anki note with the board in FEN notation on the front
        note = genanki.Note(
            model=anki_model,
            fields=[board.fen(), following_board.fen(), str(move_counter), turn],
        )
        deck.add_note(note)

    # Save the deck to a file
    try:
        file_name = name.replace(" vs ", "_vs_").replace(" ", "")
        print(file_name)
        genanki.Package(deck).write_to_file(file_name + ".apkg")
    except:
        file_name = "ankipgn"
        print(file_name)
        genanki.Package(deck).write_to_file(file_name + ".apkg")


def main(args):
    # Raw print arguments
    print("You are running the script with arguments: ")
    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))

    game_source = args.source
    color_pick = args.color

    if game_source[-4:] == ".pgn":
        source_pgn = open(game_source)
    elif game_source.find("chessgames.com") >= 0:
        pgn_string = fetch_pgn(game_source)
        source_pgn = io.StringIO(pgn_string)
    else:
        print("Source doesn't seem to be neither PGN file nor chessgames game link")
        sys.exit()

    if color_pick and color_pick not in ["White", "Black"]:
        print("Color pick can be either 'White' or 'Black'")
        sys.exit()

    convert(source_pgn, color_pick)


if __name__ == "__main__":
    # Parse the arguments
    args = parseArguments()
    main(args)
