<h1 align="center">Pgn -> Anki</h1>
<div align="center" id="logo">
    <img src="./assets/pawn.jpg" width="200", height="200">
</div>

<p align="center">In the making</p>

<p align="center">
    <a href="https://github.com/menisadi/pgn2anki/pulse">
      <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/menisadi/pgn2anki">
    </a>
</p>

Create Anki deck from PGN files or from [ChessGames.com](https://www.chessgames.com/) game's page.

# Usage
To create a deck from a local PGN file type in the command line

```
python anki-pgn.py game_file.pgn
```

Or, to create a deck from a game's page on [chessgames.com](chessgames.com) type in 
```
python anki-pgn.py https://www.chessgames.com/perl/chessgame?gid=1234567
```

This will produce an Anki deck file in your local folder. 
The deck name is automatically set to the name of the players. 

Import the file to Anki (mobile or web) to learn the game. Make sure that the [FEN Visualizer plug-in](https://ankiweb.net/shared/info/807548099) is enabled.
The Cards in the deck consist of two sides:
1. Front: A position (including which turn is it)
2. Back: The following move 

# Future plans
- [x] Option to pick color, so the cards will only ask for this color's turns.
- [x] Support sidelines.
- [ ] Support Lichess and Chess.com links
- [ ] Add GUI!

# Libaries used in this script
- [python-chess: a chess library for Python](https://github.com/niklasf/python-chess)
- [genanki: A Library for Generating Anki Decks](https://github.com/kerrickstaley/genanki)
