
class Heuristics:
    
    SIMPLE_WEIGHTS = [
        [3, 2, 2, 2, 2, 2, 2, 3],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 1, 1, 1, 1, 2],
        [3, 2, 2, 2, 2, 2, 2, 3],
    ]

    WEIGHTS = [
        [ 100, -20,  10,  5,  5,  10, -20,  100],
        [ -20, -25,  -5, -5, -5,  -5, -25,  -20],
        [  10,  -5,   5,  3,  3,   5,  -5,   10],
        [   5,  -5,   3,  1,  1,   3,  -5,    5],
        [   5,  -5,   3,  1,  1,   3,  -5,    5],
        [  10,  -5,   5,  3,  3,   5,  -5,   10],
        [ -20, -25,  -5, -5, -5,  -5, -25,  -20],
        [ 100, -20,  10,  5,  5,  10, -20,  100],
    ]
    
    @staticmethod
    def evaluate_simple_weighted(board, player):
        # Ο αλγόριθμος evaluate_weighted αξιολογεί το ταμπλό όχι με βάση πόσα κομμάτια έχει ο καθένας,
        # αλλά με βάση που βρίσκονται αυτά τα κομμάτια,
        # δίνοντας μεγαλύτερη βαθμολογία σε στρατηγικά σημαντικές θέσεις
        score = 0
        opponent = board.W if player == board.B else board.B

        for i in range(8):
            for j in range(8):
                piece = board.Board[i][j]
                if piece == board.EMPTY:
                    continue

                if piece == player:
                    # Παίκτης
                    score += Heuristics.SIMPLE_WEIGHTS[i][j]
                else:
                    # Αντίπαλος
                    score -= Heuristics.SIMPLE_WEIGHTS[i][j]
        # Αν το score > 0 τότε ο παίκτης θεωρείται ότι έχει πλεονέκτημα στη συγκεκριμένη θέση του ταμπλό
        # Αν το score < 0 τότε ο αντίπαλος θεωρείται ότι έχει πλεονέκτημα στη συγκεκριμένη θέση του ταμπλό
        # Αν το score = 0 τότε το παιχνίδι θεωρείται ισορροπημένο στη συγκεκριμένη θέση του ταμπλό
        return score

    @staticmethod
    def evaluate_weighted(board, player):
        # Ο αλγόριθμος evaluate_weighted αξιολογεί το ταμπλό όχι με βάση πόσα κομμάτια έχει ο καθένας,
        # αλλά με βάση που βρίσκονται αυτά τα κομμάτια,
        # δίνοντας μεγαλύτερη βαθμολογία σε στρατηγικά σημαντικές θέσεις
        score = 0
        opponent = board.W if player == board.B else board.B

        for i in range(8):
            for j in range(8):
                piece = board.Board[i][j]
                if piece == board.EMPTY:
                    continue

                if piece == player:
                    # Παίκτης
                    score += Heuristics.WEIGHTS[i][j]
                else:
                    # Αντίπαλος
                    score -= Heuristics.WEIGHTS[i][j]
        # Αν το score > 0 τότε ο παίκτης θεωρείται ότι έχει πλεονέκτημα στη συγκεκριμένη θέση του ταμπλό
        # Αν το score < 0 τότε ο αντίπαλος θεωρείται ότι έχει πλεονέκτημα στη συγκεκριμένη θέση του ταμπλό
        # Αν το score = 0 τότε το παιχνίδι θεωρείται ισορροπημένο στη συγκεκριμένη θέση του ταμπλό
        return score
    
    @staticmethod
    def evaluate_mobility(board, player):

        opponent = board.W if player == board.B else board.B
        
        player_moves = len(board.available_moves_for(player))
        opponent_moves = len(board.available_moves_for(opponent))

        return player_moves - opponent_moves

    @staticmethod
    def evaluate_piece_diff(board, player):
        opponent = board.W if player == board.B else board.B

        player_count = 0
        opponent_count = 0

        for i in range(8):
            for j in range(8):
                piece = board.Board[i][j]
                if piece == player:
                    player_count += 1
                elif piece == opponent:
                    opponent_count += 1

        return player_count - opponent_count
        
    @staticmethod
    def evaluate_frontier(board, player):
        # Ο αλγόριθμος evaluate_frontier:
        # Σκανάρει το ταμπλό.
        # Για κάθε πιόνι, ελέγχει αν δίπλα του υπάρχει κενό τετράγωνο
        # Αν ναι, τότε το πιόνι είναι frontier disk (ευάλωτο)
        # Μετράει πόσα τέτοια κομμάτια έχει ο παίκτης και πόσα έχει ο αντίπαλος
        # Επιστρέφει το αποτέλεσμα: score = opponent_frontier - own_frontier

        # Βρες τον αντίπαλο
        opponent = board.W if player == board.B else board.B

        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1),
        ]

        own_frontier = 0  # πόσα κομμάτια του παίκτη μας είναι ευάλωτα (δίπλα σε άδειο τετράγωνο)
        opponent_frontier = 0  # πόσα ευάλωτα κομμάτια έχει ο αντίπαλος

        # Σκανάρουμε όλο το 8x8 ταμπλό
        for i in range(8):
            for j in range(8):
                piece = board.Board[i][j]
                if piece == board.EMPTY:
                    continue

                # έλεγχος αν είναι frontier disk =
                # κομμάτι που συνορεύει με κενό τετράγωνο και
                # επομένως κινδυνεύει να ανατραπεί σύντομα
                is_frontier = False
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 8 and 0 <= nj < 8:
                        if board.Board[ni][nj] == board.EMPTY:
                            is_frontier = True
                            break

                if not is_frontier:
                    continue

                if piece == player:
                    own_frontier += 1
                elif piece == opponent:
                    opponent_frontier += 1

        # Όσο λιγότερα frontier για τον παίκτη, τόσο καλύτερα
        # Δηλ. βέλτιστο αποτέλεσμα είναι το σκορ να είναι θετικό, καθώς αυτό σημαίνει ότι
        # ο αντίπαλος έχει περισσότερα ευάλωτα κομμάτια από τον παίκτη
        score = opponent_frontier - own_frontier
        return score
