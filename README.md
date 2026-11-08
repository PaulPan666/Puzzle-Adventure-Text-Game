# Puzzle-Adventure Text Game

## Game Introduction & Rules
- This is a turn‑based text puzzle adventure game built with Python standard library only.
- The player starts at the central hub and can travel to four puzzle rooms.
- Players navigate between rooms by typing the room number `1`, `2`, `3`, or `4` when they are at the hub.
- The goal is to solve puzzles in each room to collect keys. Once all four keys are obtained, the player can use the `final` command to unlock the final lock and win the game.
- If the player runs `final` before collecting all four keys, access will be denied, and the game will prompt the player to gather the remaining keys.
- The program requires a terminal window of at least 80 columns × 24 rows. If the terminal is smaller, the game will pause and remind the player to resize the window.
- Players can type supported commands to explore, check inventory, get help or quit the game.

## Available Commands
| Command | Description |
| :--- | :--- |
| `look` | Check the current room description |
| `inventory` | Check collected keys |
| `help` | Show command list |
| `move room1` | Travel to Room 1 from the hub |
| `move room2` | Travel to Room 2 from the hub |
| `move room3` | Travel to Room 3 from the hub |
| `move room4` | Travel to Room 4 from the hub |
| `final` | Attempt to unlock the final puzzle (only usable after collecting all keys) |
| `quit` | Exit the game |

## Group Information
- Subclass: ENGG1330 1N
- Group members:
    1. Pan Yuze
    2. Li Xinyuan
    3. Wong Yat To
    4. Tan Jia Le

## How to Run
> Requirements: Docker must be installed and running. Use the provided `engg1330-project:2026-v03` container image.
1. Open a terminal in the project folder (the directory that contains `docker-compose.yml`).
2. Run the following commands in sequence:
    ```bash
    docker compose build
    docker compose run --rm game bash
    python main.py

## Tests and Known Limitations
### Test Cases
| Test category | Example test | Expected result |
| :--- | :--- | :--- |
| Normal gameplay | Complete all four rooms | Four keys are collected and stored in inventory |
| Invalid input | Enter an unsupported command | The game prints an error/help message and does not crash |
| Boundary case | Attempt invalid room selection | The move is rejected, and the game stays in the hub |
| Final puzzle | Run `final` before collecting all keys | Access denied, prompt to collect missing keys |
| Winning condition | Run `final` with all four keys collected | The winning message is displayed |
| Exit behaviour | Enter `quit` at any time | The game terminates cleanly |
| Docker execution | Launch game inside the specified container | The game starts and runs correctly |
| Terminal check | Launch with a small terminal | Game pauses and asks user to resize terminal |

### Known Limitations
1. There is no save system; all progress will be lost once the program closes.
2. The game only supports typed turn-based input, no real-time keyboard control.
3. There are no adjustable difficulty levels for the puzzles.

## Contributions
- Pan Yuze: Overall gameplay framework, function definition structure, screen clearing function, terminal size detection, input validation and robustness improvement, README.md writing, demonstration video outline
- Li Xinyuan: Design and implementation of puzzle rooms and the final puzzle, story and background setting, `ai_use.md` writing, demonstration video script writing
- Wong Yat To: Demo and technical video production
- Tan Jia Le: Trailer production

## Sources and Acknowledgements
- The project uses Python standard library modules only. No external third-party packages are imported.
- The storyline, puzzles, and game logic were designed and implemented by our group.
- Generative AI assistance used during development is documented in `ai_use.md`.
- All other assets and content in this submission are original work of our group.
