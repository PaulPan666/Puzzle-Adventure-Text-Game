# Puzzle-Adventure Text Game

## Game Introduction & Rules
- This is a turn‑based text puzzle adventure game built with pure Python standard libraries.
- The player starts at the central hub and can travel to four puzzle rooms.
- The goal is to solve puzzles in each room to collect keys. Once all four keys are obtained, the player can use the `final` command to unlock the final lock and win the game.
- The program requires a terminal window of at least 80 columns × 24 rows. If the terminal is smaller, the game will pause and remind the player to resize the window.
- Players can type supported commands to explore, check inventory, get help or quit the game.

## Available Commands
| Command | Description |
| :--- | :--- |
| `look` | Check the current room description |
| `inventory` | Check collected keys |
| `help` | Show command list |
| `final` | Attempt to unlock the final puzzle (only after collecting all keys) |
| `quit` | Exit the game |

## Group Information
- Subclass: ENGG1330 1N
- Group members:
    1. Pan Yuze
    2. Li Xinyuan
    3. Wong Yat To
    4. Tan Jia Le

## How to Run
- Docker container version: `engg1330-project:2026-v03`
- Run the command below in the project folder:
    1. `docker compose run --rm game bash`
    2. `python main.py`

## Tests and Known Limitations
- Tests: We have tested the full game flow, including normal gameplay, invalid input, boundary cases, and the program inside the Docker container. The terminal size check and clear-screen function have also been verified.
- Known Limitations:
    1. There is no save system; all progress will be lost once the program closes.
    2. The game only supports typed turn-based input, no real-time keyboard control.
    3. There are no adjustable difficulty levels for the puzzles.

## Contributions
- Pan Yuze: Overall gameplay framework, function definition structure, screen clearing function, terminal size detection, robustness improvement, README.md writing, demonstration video script.
- Li Xinyuan: Room gameplay design, final puzzle implementation, story and background setting, AI_use.md writing, demonstration video script.
- Wong Yat To: Demo/technical video.
- Tan Jia Le: Trailer.

## Sources
This project uses only standard Python libraries. No external third-party packages are imported.
All storylines, puzzles and game logic are original work created by our group.
