# pgn2anki
Create Anki deck from PGN files.

# Usage
Download the PGN file of the game and type in the command line

```
python anki-pgn.py game_file.pgn
```

This will produce an Anki deck file in the same folder.

Import the file to anki (mobile or web) to learn the game. Make sure that the [FEN Visualizer plug-in](https://ankiweb.net/shared/info/807548099) is enabled.
The Cards in the deck consist of two sides:
1. Front: A position (including which turn is it)
2. Back: The following move 

# Future plans
- Option to pick side so only its turns will apear.
- Option to fetch games from the web.
- Suport sidelines.

# Libaries used in this script
- [python-chess: a chess library for Python
](https://github.com/niklasf/python-chess)
- [genanki: A Library for Generating Anki Decks](https://github.com/kerrickstaley/genanki)
