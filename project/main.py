import os
import random
import subprocess
import sys
import time

def check_terminal_size():
    '''Verify terminal satisfies minimum 80×24 dimension requirement.'''
    required_cols = 80
    required_rows = 24
    while True:
        try:
            size = os.get_terminal_size()
            cols = size.columns
            rows = size.lines
        except OSError:
            # Cannot read terminal size in IDE/non‑terminal environment, skip validation
            return True
        if cols >= required_cols and rows >= required_rows:
            return True
        else:
            clear_screen()
            print("[ERROR] Terminal window too small!")
            print(f"Need at least {required_cols}×{required_rows}. Current: {cols}×{rows}")
            print("Please resize your terminal window, then press Enter to check again...")
            input()

def clear_screen():
    '''Clear terminal screen, cross‑platform for Windows/Linux/macOS.'''
    if os.name == 'nt':
        subprocess.run("cls", shell=True)
    else:
        subprocess.run("clear", shell=True)

def wrap_text(text, max_width=80):
    '''Wrap long text lines to fit within terminal width limit.'''
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_width:
            if current_line == "":
                current_line = word
            else:
                current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)

def slow_print(text, delay=0.05):
    '''Print text character‑by‑character for typewriter effect.'''
    wrapped = wrap_text(text, max_width=80)
    for char in wrapped:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def award_key(game_state, room_id):
    '''Grant key reward after solving a room puzzle.'''
    room = game_state["rooms"][room_id]
    if room["solved"]:
        return False
    room["solved"] = True
    game_state["win"] += 1
    key = room["key_name"]
    game_state["inventory"].append(key)
    slow_print(f"\n✨ Correct! Obtained [KEY: {key}]")
    return True

def init_game_state(player_name):
    '''Initialize the game state dictionary storing player data and puzzle progress.'''
    # "win": count of completed rooms / collected keys
    # "location": current player location key e.g. "hub", "room1"
    # "inventory": list of acquired key items
    # "rooms": nested dict holding each room's metadata and puzzle progress
    game_state = {
        "player_name": player_name,
        "win": 0,
        "location": "hub",
        "inventory": [],
        "rooms": {
            "hub": {
                "name": "The Central Nexus",
                "description": "You stand in a glowing nexus. Four portals surround you: 'room1', 'room2', 'room3', 'room4'.",
                "exits": ["room1", "room2", "room3", "room4"]
            },
            "room1": {
                "name": "Room 1: The Word Challenge",
                "description": "A dim stone chamber with faded crimson writing on the wall. A word‑decoding puzzle awaits you here.",
                "solved": False,
                "key_name": "1. Learn fundamental Python concepts",
                "exits": ["hub"]
            },
            "room2": {
                "name": "Room 2: The Simple Maze",
                "description": "A narrow chamber covered by an active 3×3 laser grid. Navigate the grid to reach the exit portal.",
                "solved": False,
                "key_name": "2. Practice coding consistently",
                "exits": ["hub"]
            },
            "room3": {
                "name": "Room 3: The Card Duel",
                "description": "A dark void‑like arena. A mysterious guardian will challenge you to a 5‑round card battle.",
                "solved": False,
                "key_name": "3. Build real PYTHON projects",
                "exits": ["hub"]
            },
            "room4": {
                "name": "Room 4: The Master Vault",
                "description": "A secure high‑security vault chamber. A locked digital safe requires solving a numeric riddle for the passcode.",
                "solved": False,
                "key_name": "4. Be brave and confident in your further PYTHON journey",
                "exits": ["hub"]
            }
        }
    }
    return game_state

def room1_puzzle(game_state):
    """
    Word‑guessing puzzle, then riddle answer submission.
    Player guess letters to reveal riddle words, then answer "tuple" riddle.
    :param game_state: global game state dictionary
    :return bool: True = puzzle solved and key obtained; False = puzzle failed
    """
    name = game_state["player_name"]
    target_words = ["structure", "values", "immutable"]
    all_letters_to_guess = set("".join(target_words))
    guessed_letters = {"s", "v", "i"}
    attempts_left = 10
    room1_success = False
    slow_print("\n--- 🕵️ ROOM 1: THE WORD CHALLENGE ---")
    slow_print("You step into Room 1 and look around. On the crumbling wall, a phrase is written in crimson ink:")
    slow_print("'I'm a data xxx that can hold multiple xxx, but I'm xxx. What am I?'")
    slow_print("Unfortunately, three crucial words have faded into obscurity. To reveal the complete riddle, you must first clear a challenge.")
    slow_print("Squinting through the dim light, you manage to decipher the three missing words. They are:")
    slow_print("s _ _ _ _ _ _ _ _ , v _ _ _ _ s , i _ _ _ _ _ _ _ _")
    slow_print("📜 Rules: You have 10 attempts. Correct guesses cost nothing, wrong guesses cost 1 attempt, and repeated guesses cost 2 attempts.")
    slow_print("You only have ten chances. Each time, you may guess a single letter if the word contains it, it will automatically reveal itself.")
    slow_print(f"{name}, ready when you are!")
    input("\nPress Enter to start puzzle...")
    while attempts_left > 0:
        clear_screen()
        display_words = []
        for word in target_words:
            word_display = ""
            for i in range(len(word)):
                if i == 0:
                    word_display += word[0] + " "
                elif word[i] in guessed_letters:
                    word_display += word[i] + " "
                else:
                    word_display += "_ "
            display_words.append(word_display.strip())
        print(f"\n[Current Clue]: {' , '.join(display_words)}")
        print(f"[Remaining Attempts]: {attempts_left}")
        if all(letter in guessed_letters for letter in all_letters_to_guess):
            room1_success = True
            break
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("❌ Invalid input! Enter a single letter.")
            time.sleep(1.2)
            continue
        if guess in guessed_letters:
            attempts_left -= 2
            print(f"❌ Already guessed '{guess}'! Lost 2 chances.")
            time.sleep(1.2)
        else:
            guessed_letters.add(guess)
            if guess in all_letters_to_guess:
                print(f"✅ Great! '{guess}' is in the message.")
                time.sleep(1.2)
            else:
                attempts_left -= 1
                print(f"❌ '{guess}' is NOT in the message.")
                time.sleep(1.2)
    if not room1_success:
        print("❌ Failed this attempt! Type 'play' to retry.")
        time.sleep(1.2)
        return False
    print("The faded words are now fully revealed: 'I'm a data structure that can hold multiple values, but I'm immutable. What am I?'")
    while True:
        answer = input("Now, enter your answer to the riddle: ").strip().lower()
        if not answer:
            print("❌ Your answer cannot be empty! Please type your guess.")
            continue
        if answer == "tuple" or answer == "t":
            award_key(game_state, "room1")
            time.sleep(1.2)
            return True
        else:
            print("❌ Wrong answer! Try again.")
            time.sleep(1.2)

def room2_puzzle(game_state):
    """
    3×3 grid maze puzzle controlled by w/a/s/d movement commands.
    Player must collect key [K] before reaching exit, avoid obstacle [X].
    Limited maze attempts are consumed for moves and collisions.
    :param game_state: global game state dictionary
    :return bool: True = maze completed, False = attempts exhausted
    """
    x, y = 0, 0
    goal_x, goal_y = 2, 2
    key_x, key_y = 1, 0
    obstacle_x, obstacle_y = 1, 2
    has_key = False
    maze_attempts = 5
    room2_success = False
    slow_print("\n--- 🕵️ ROOM 2: THE SIMPLE MAZE ---")
    slow_print("Navigate from [P] to the exit [🚪] in a 3x3 grid using w (up), s (down), a (left), d (right).")
    slow_print("⚠️ Warning: Exit is locked! Find key [K] before you can escape. Avoid obstacle [X].")
    slow_print("❌ The exit is locked! Find the key at position (1, 0) before returning here.")
    input("\nPress Enter to start maze...")
    while maze_attempts > 0:
        clear_screen()
        print(f"\n[Attempts Left]: {maze_attempts} | Key collected: {'YES' if has_key else 'NO'}")
        for r in range(3):
            line = ""
            for c in range(3):
                if c == x and r == y:
                    line += "[P] "
                elif c == obstacle_x and r == obstacle_y:
                    line += "[X] "
                elif c == key_x and r == key_y and not has_key:
                    line += "[K] "
                elif c == goal_x and r == goal_y:
                    line += "[🚪] "
                else:
                    line += "[ ] "
            print(line)

        if x == goal_x and y == goal_y:
            if has_key:
                print("\n✨ Success! You used your key and escaped the laser grid!")
                room2_success = True
                break
            else:
                print("❌ The exit is locked! Find the key at position (1, 0) before returning here.")

        move_dir = input("Move (w/a/s/d): ").strip().lower()
        if len(move_dir) != 1:
            print("❌ Please enter ONLY one single character: w / a / s / d")
            continue
        valid_move = True
        new_x, new_y = x, y

        if move_dir == 'w':
            new_y = y - 1
        elif move_dir == 's':
            new_y = y + 1
        elif move_dir == 'a':
            new_x = x - 1
        elif move_dir == 'd':
            new_x = x + 1
        else:
            print("please type w, s,a or d")
            continue

        if new_x < 0 or new_x > 2 or new_y < 0 or new_y > 2:
            valid_move = False
        elif new_x == obstacle_x and new_y == obstacle_y:
            valid_move = False

        if valid_move:
            x, y = new_x, new_y
            maze_attempts -= 1
            if x == key_x and y == key_y and not has_key:
                print("\n🔑 You picked up the maze key! Now you can open the exit.")
                has_key = True
                time.sleep(1.2)
        else:
            print("❌ Hit wall or obstacle! Lost 2 attempts.")
            maze_attempts -= 2
            time.sleep(1.2)

        if x == goal_x and y == goal_y and has_key:
            print("\n✨ Success! You used your key and escaped the laser grid!")
            room2_success = True
            time.sleep(1.2)
            break

    if room2_success:
        award_key(game_state, "room2")
        time.sleep(1.2)
        return True
    else:
        print("\n💀 Game Over! The maze sealed shut... Type 'play' to retry.")
        time.sleep(1.2)
        return False

def room3_puzzle(game_state):
    """
    5‑round card duel puzzle against AI guardian.
    Player uses odd‑number cards; AI uses even‑number cards.
    Need at least 2 round wins to pass this challenge.
    :param game_state: global game state dictionary
    :return bool: True = duel success; False = insufficient round wins
    """
    player_cards = [1, 3, 5, 7, 9]
    ai_cards = [2, 4, 6, 8, 10]
    player_wins = 0
    rounds_played = 0
    slow_print("\n--- 🕵️ ROOM 3: THE CARD DUEL ---")
    slow_print("The instant you choose Room 3, a sudden sensation of weightlessness takes hold.")
    slow_print("You plummet into an abyss of absolute darkness. Emerging from the shadows, a mysterious figure sits directly across from you. ")
    slow_print("Held tightly in your hands are 5 icy cards. The stranger erupts into a chilling laugh: 'No foolish human could ever hope to break my game!'")
    slow_print("You hold the odd cards: [1, 3, 5, 7, 9]. The guardian holds even cards: [2, 4, 6, 8, 10].")
    slow_print("Rule: 5 rounds of card battles. You must win at least 2 rounds to unlock the exit!")
    slow_print("🔔 New Rule: Both sides pick card FIRST, then reveal simultaneously! You cannot see guardian's choice before playing.")
    input("\nPress Enter to start duel...")
    while rounds_played < 5:
        clear_screen()
        print(f"\n[Round {rounds_played + 1}]")
        print(f"your cards: {player_cards}")
        try:
            choice = int(input("Choose a card to play: "))
        except ValueError:
            print("❌ Invalid input! Please enter a valid number from your hand.")
            time.sleep(2)
            continue
        if choice not in player_cards:
            print("❌ You don't have that card, or you already played it! Try again, no turn penalty.")
            time.sleep(2)
            continue

        ai_choice = random.choice(ai_cards)
        ai_cards.remove(ai_choice)
        player_cards.remove(choice)
        print(f"Guardian played: {ai_choice} | You played: {choice}")
        if choice > ai_choice:
            player_wins += 1
            print("✨ You win this round!")
            time.sleep(2)
        else:
            print("❌ Guardian wins this round!")
            time.sleep(2)
        rounds_played += 1

    print(f"\n[Final Results]: You won {player_wins} out of 5 rounds.")
    time.sleep(1.2)
    if player_wins >= 2:
        slow_print("\n✨ Amazing! Your strategy prevailed and escaped the room!")
        award_key(game_state, "room3")
        return True
    else:
        slow_print("\n💀 Defeat! You didn't win enough rounds, and the cards vanish into dust...")
        return False

def room4_puzzle(game_state):
    """
    Vault numeric passcode puzzle with maximum 3 guessing attempts.
    Player solves logic riddle to deduce 4‑digit correct code.
    :param game_state: global game state dictionary
    :return bool: True = vault unlocked success; False = attempts used up
    """
    vault_attempts = 3
    correct_code = "2648"
    room4_success = False

    slow_print("\n--- 🕵️ ROOM 4: THE MASTER VAULT ---")
    slow_print("As you step into this chamber, a heavy steel door slides shut behind you with a loud clank.")
    slow_print("In the center of the room stands a massive digital vault. The screen flashes a final test:")
    slow_print("'I am a 4‑digit code. The first digit is 2, the last digit is 8, the sum of all four digits is 20, all digits are even. The second digit is exactly two greater than the third digit.'")
    slow_print("You have 3 attempts to enter the correct 4‑digit code to escape!")
    input("\nPress Enter to begin vault challenge...")

    while vault_attempts > 0:
        clear_screen()
        slow_print("\n📜 Riddle: first=2, last=8, sum=20, all even, second = third +2")
        print(f"\n[Vault Attempts Left]: {vault_attempts}")
        guess_code = input("Enter the 4‑digit code: ").strip()
        if len(guess_code) !=4 or not guess_code.isdigit():
            print("❌ Please enter exactly 4 numeric digits! No attempt consumed.")
            continue
        if guess_code == correct_code:
            print("\n✨ Click! The massive vault door swings open with a triumphant chime!")
            time.sleep(1.2)
            room4_success = True
            break
        else:
            vault_attempts -= 1
            print("❌ Incorrect code! A red warning light flashes.")
            time.sleep(1.2)
    if room4_success:
        award_key(game_state, "room4")
        time.sleep(1.2)
        return True
    else:
        slow_print("\n💀 Lockout! The security system permanently seals the vault, trapping you inside... type 'play' to retry")
        time.sleep(1.2)
        return False

def play_game():
    '''Main game flow: terminal check → intro story → get player name → main command‑loop game.'''
    check_terminal_size()
    clear_screen()
    intro = [
        "MOONBASE PYTHON \n (Press Enter to continue ...)",
        "It is 11:30 PM. Panic sets in as your Python DDL looms just thirty minutes away...",
        "Suddenly, a bolt of lightning flashes across the sky. Your vision blurs...",
        "You wake up in a mysterious realm. Floating in the air before you are glowing words:",
        "'Welcome to my world. To finish your PYTHON task before the deadline, you need to survive in my world! Mahahaha...",
        "'Use text commands (like 'look', 'move [room]', 'play', 'inventory') to survive!"
    ]
    for line in intro:
        print(line)
        input()

    slow_print("\nBrave explorer, what shall I call you? ")
    name = ""
    while name == "":
        temp_name = input("> ").strip()
        if len(temp_name) > 20:
            print("❌ Name is too long! Maximum 20 characters.")
            continue
        name = temp_name
    slow_print(f"Welcome, {name}, type your commands to explore!")
    time.sleep(1.2)
    game_state = init_game_state(name)

    game_running = True
    final_deferred = False
    # final_deferred = True: player exits final puzzle, return to normal exploration
    # Use command "final" to set it False and reopen final lock
    need_clear = True
    # need_clear controls whether screen will be cleared at start of each main‑loop iteration
    while game_running:
        check_terminal_size()
        if need_clear:
            clear_screen()
            need_clear = False
        current_loc = game_state["location"]
        room_info = game_state["rooms"][current_loc]
        division_line = "=" * 40
        print(f"\n{division_line}")
        slow_print(f"📍 Location: {room_info['name']} | Keys: {game_state['win']}/4")
        print(division_line)

        if game_state["win"] == 4 and not final_deferred:
            print("\nCONGRATULATIONS! You have gathered all 4 keys across the realm!")
            slow_print("Now you get the four keys to mastering Python!")
            slow_print("\n📜 Final lock clue: The final passcode is built from the NUMBER prefix on each key.\nREMEMBER: The sequence is everything!")
            # Generate final passcode using number prefix of keys, follow inventory collect order
            correct_final_sequence = 1234
            final_done = False
            while not final_done:
                final_attempts = 2
                while final_attempts > 0:
                    final_result = input("\nEnter final 4‑digit sequence (or type 'q' to return to exploration): ").strip()
                    if final_result == "":
                        print("❌ Please enter a sequence or q.")
                        continue
                    if final_result.lower() == "q":
                        slow_print("You step back from the final lock, returning to exploration.")
                        final_deferred = True
                        final_done = True
                        break
                    if final_result == correct_final_sequence:
                        print("\n✨ 🎊 YOU WIN! YOU ARE BORN TO CODE IN PYTHON!!! 🚀🔥")
                        final_done = True
                        game_running = False
                        break
                    else:
                        final_attempts -= 1
                        print(f"❌ Incorrect sequence! Remaining chances: {final_attempts}")
                if final_done:
                    break
                slow_print("\n⚠️ You have used up both attempts for this round.")
                while True:
                    choice = input("Type 'r' to retry final puzzle, 'q' to go back to game> ").strip().lower()
                    if choice == "r" or choice == "q":
                        break
                    print("❌ Invalid input! Please only enter r or q.")
                if choice == "r":
                    slow_print("Resetting final puzzle attempts...")
                    continue
                else:
                    slow_print("You decide to leave the final vault for now. You can come back any time using command 'final'.")
                    final_deferred = True
                    final_done = True
            continue

        command = input("Enter command (e.g., 'look', 'move [room]', 'play', 'inventory', 'help', 'quit', 'final'): ").strip().lower()
        parts = command.split()
        if not parts:
            continue
        action = parts[0]
        target = parts[1] if len(parts) > 1 else ""

        if action == "help":
            slow_print("\n📖 Available Commands:")
            slow_print(" look — print room description and exits")
            slow_print(" move [roomid] / go [roomid] — travel e.g. move room1")
            slow_print(" play / interact — start puzzle in current room")
            slow_print(" inventory / inv — show your collected keys")
            slow_print(" final — open final lock puzzle (only after collecting all four keys)")
            slow_print(" help — show this help list")
            slow_print(" quit — exit game immediately")
            continue
        elif action == "quit":
            slow_print("\n👋 Exiting game, thanks for playing!")
            game_running = False
            continue
        elif action == "final":
            if game_state["win"] == 4:
                final_deferred = False
            else:
                slow_print("❌ You haven't collected all four keys yet!")
            continue

        if action == "look":
            slow_print(f"Description: {room_info['description']}")
            slow_print(f"Available exits/connections: {room_info['exits']}")
            if current_loc == "hub":
                slow_print("Hint: Type 'move room1', 'move room2', 'move room3', or 'move room4' to enter a chamber.")
            elif not room_info["solved"]:
                slow_print("Hint: Type 'play' to challenge the puzzle in this room!")
                time.sleep(1)
            else:
                slow_print("Hint: You already solved this room. Type 'move hub' to return.")
                time.sleep(1)
        elif action == "inventory" or action == "inv":
            slow_print(f"Your Inventory keys: {game_state['inventory'] if game_state['inventory'] else 'Empty'}")
        elif action == "move" or action == "go":
            if target in room_info["exits"]:
                game_state["location"] = target
                slow_print(f"-> You moved to {game_state['rooms'][target]['name']}.")
                time.sleep(1.2)
                need_clear = True
            else:
                slow_print(f"❌ You cannot go to '{target}' from here! Check available exits using 'look'.")
        elif action == "play" or action == "interact":
            if current_loc == "hub":
                slow_print("There is no puzzle in the hub. Move to a room first (e.g., 'move room1').")
                continue
            if room_info["solved"]:
                slow_print("You have already conquered this room!")
                continue
            clear_screen()
            if current_loc == "room1":
                room1_puzzle(game_state)
            elif current_loc == "room2":
                room2_puzzle(game_state)
            elif current_loc == "room3":
                room3_puzzle(game_state)
            elif current_loc == "room4":
                room4_puzzle(game_state)
            need_clear = True
        else:
            slow_print("❌ Unknown command! Try 'look', 'move [room]', 'play', 'inventory', 'help', 'quit', 'final'.")

def main():
    '''Outer wrapper loop for game restart logic after finishing one play‑through.'''
    while True:
        play_game()
        while True:
            choice = input("\nDo you want to try again? (y/n): ").strip().lower()
            if choice in ("y", "yes"):
                break
            elif choice in ('n','no'):
                print("Thanks for your time, see you!")
                exit()
            else:
                print('Invalid choice, please enter y or n')
            
if __name__ == "__main__":
    main()