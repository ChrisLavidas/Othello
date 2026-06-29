from Board import Board
from Player import HumanPlayer, AIPlayer

def main():
    game = Board()

    # ----- Επιλογή χρώματος -----
    human_letter = input("Διάλεξε χρώμα W ή B: ").upper()
    while human_letter not in ['W', 'B']:
        human_letter = input("Άκυρο χρώμα! Διάλεξε W ή B: ").upper()

    while True:
        try:
            max_depth = int(input("Διάλεξε το βάθος του ΑΙplayer: "))
            break
        except:
            print("Άκυρη τιμή! Πρέπει να δώσεις έναν ακέραιο")

    print(f"Εσύ παίζεις με τα {human_letter}.")
    ai_letter = 'B' if human_letter == 'W' else 'W'
    print(f"Ο υπολογιστής παίζει με τα {ai_letter}.")

    human = HumanPlayer(Board.W if human_letter == 'W' else Board.B)
    ai    = AIPlayer(Board.W if ai_letter == 'W' else Board.B, max_depth)

    # ----- Ο ΜΑΥΡΟΣ ΠΑΙΖΕΙ ΠΑΝΤΑ ΠΡΩΤΟΣ -----
    current_player = human if human_letter == 'B' else ai

    # ----- ΚΥΡΙΩΣ ΒΡΟΧΟΣ ΠΑΙΧΝΙΔΙΟΥ -----
    while True:

        print("\n-----------------------------------")
        print("🔄 Σειρά του", current_player.print_player())

        if game.is_terminal():
            break

        game.print_board()

        moves = game.available_moves()
        if not moves:
            print("⚠️ Δεν υπάρχουν διαθέσιμες κινήσεις. Πάσο.")
            game.change_last_player()
            current_player = ai if current_player is human else human
            continue

        move = current_player.choose_move(game)
        row, col = move if move is not None else (None, None)
        if move is None or game.is_valid_move(row, col) == False:
            game.change_last_player()
            current_player = ai if current_player is human else human
            continue

        print(f"▶ Κίνηση στο ({row}, {col})")

        game.make_move(row, col, current_player.player_letter)

        current_player = ai if current_player is human else human

    # ----- ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ -----
    print("\n🏁 Τελική κατάσταση:")
    game.print_board()

    whites = sum(r.count(game.W) for r in game.Board)
    blacks = sum(r.count(game.B) for r in game.Board)

    print(f"Λευκά (W): {whites}")
    print(f"Μαύρα (B): {blacks}")

    if whites > blacks:
        print("🎉 Νίκη για τα λευκά!")
    elif blacks > whites:
        print("🎉 Νίκη για τα μαύρα!")
    else:
        print("🤝 Ισοπαλία!")

    print(game.get_move_history())

main()
