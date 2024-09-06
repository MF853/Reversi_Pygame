# Reversi Game

## Overview

**Reversi** game, also known as **Othello**, implemented using **Pygame**! Reversi is a strategy board game for two players. The aim is to have the majority of your color pieces on the board at the end of the game.

This project showcases a fully functioning game of Reversi with an interactive graphical interface. You can play against another player locally, flipping the opponent's pieces by surrounding them with your own.

## Features

- **Two-player mode**: Play with a friend on the same computer.
- **Pygame GUI**: A clean graphical interface built using Pygame.
- **Move validation**: The game enforces all rules, ensuring valid moves.
- **Score tracking**: See the current score at all times.
- **End-game detection**: The game recognizes when no valid moves are available and declares the winner.

## How to Play

1. **Run the Game**: Execute the Python script to start the game.
   
   ```bash
   python reversi.py
   ```

2. **Game Rules**:
   - Players take turns placing their pieces on the board.
   - A player must place their piece in such a way that they "sandwich" one or more of their opponent's pieces between two of their own. This flips the opponent's pieces to the player's color.
   - If a player cannot make a valid move, they must pass their turn.
   - The game ends when neither player can make a valid move. The player with the most pieces on the board at the end wins.

## Installation

### Requirements

- **Python 3.x**: Make sure you have Python installed. You can download it [here](https://www.python.org/).
- **Pygame**: Install the Pygame library using pip:

  ```bash
  pip install pygame
  ```

### Running the Game

After installing the necessary dependencies, clone this repository or download the source code, then run the main file:

```bash
python reversi.py
```
