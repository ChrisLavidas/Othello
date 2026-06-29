from abc import ABC, abstractmethod
from Move import Move
from Board import Board
import Heuristics

class Player(ABC):
    def __init__(self, player_letter):
        self.player_letter = player_letter
    
    @abstractmethod
    def print_player(self):
        pass
    
    @abstractmethod
    def equals(self, other_player):
        pass

    @abstractmethod
    def choose_move(self, board):
        pass


class HumanPlayer(Player):
    def print_player(self):
        return "W" if self.player_letter == 1 else "B"
    
    def equals(self, other_player):
        return self.player_letter == other_player.player_letter

    def choose_move(self, board):
        moves = board.available_moves()

        if not moves:
            print("Δεν υπάρχουν διαθέσιμες κινήσεις.")
            return None

        print("Διαθέσιμες κινήσεις:")
        for i, move in enumerate(moves):
            print(f"{i}: {move}")

        while True:
            try:
                index = int(input("Δώσε το index της κίνησης: "))
        
                if index < 0 or index >= len(moves):
                    print("Άκυρο index! Δώσε έναν αριθμό από τη λίστα.")
                    continue

                return moves[index]
            
            except ValueError:
                print("Πρέπει να δώσεις αριθμό. Προσπάθησε ξανά.")


class AIPlayer(Player):
    def __init__(self, player_letter, max_depth=3):
        super().__init__(player_letter)
        self.max_depth = max_depth

    def print_player(self):
        return "W" if self.player_letter == 1 else "B"
    
    def equals(self, other_player):
        return self.player_letter == other_player.player_letter


    def evaluate_board(self, board):

        player = self.player_letter
        final_score = 0

        # Μετράμε τα άδεια κελιά για να δούμε σε ποια φάση του παιχνιδιού είμαστε
        empty_cells = sum(row.count(board.EMPTY) for row in board.Board)
        played_cells = 64 - empty_cells

        spos_score = Heuristics.Heuristics.evaluate_simple_weighted(board, player)
        pos_score = Heuristics.Heuristics.evaluate_weighted(board, player)
        mob_score = Heuristics.Heuristics.evaluate_mobility(board, player)
        frontier_score = Heuristics.Heuristics.evaluate_frontier(board, player)
        diff_score = Heuristics.Heuristics.evaluate_piece_diff(board, player)

        # Αρχή
        if played_cells <= 10:
            final_score = spos_score

        elif played_cells <= 20:
            W_POS, W_MOB, W_FRONTIER = 10, 30, -10
            final_score = (W_POS * pos_score) + (W_MOB * mob_score) + (W_FRONTIER * frontier_score)

        # Μέσον
        elif played_cells <= 62-self.max_depth:
            W_POS, W_MOB, W_FRONTIER = 25, 20, -10
            final_score = (W_POS * pos_score) + (W_MOB * mob_score) + (W_FRONTIER * frontier_score) 

        # Τέλος
        else:
            final_score = 1000 * diff_score

        return final_score


    def choose_move(self, board):
        best_move = self.minimax(board)[1]

        if best_move is None:
            return None
    
        return best_move
    

    def minimax(self, board):
        # AI είναι max-player
        if self.player_letter == board.W:
            return self.max(board, 0, float('-inf'), float('inf'))
        else:
            return self.min(board, 0, float('-inf'), float('inf'))


    def min(self, board, depth, alpha, beta):

        if depth == self.max_depth or board.is_terminal():
            return (self.evaluate_board(board), (board.last_move.row, board.last_move.col))
    
        children = board.get_children(-self.player_letter)
        if not children:
            return self.max(board, depth + 1, alpha, beta)

        best_value = float('inf')
        best_move = None

        for (row, col), child in children.items():
            child_value = self.max(child, depth + 1, alpha, beta)[0]

            if child_value < best_value:
                best_value = child_value
                best_move = (row, col)

            if best_value <= alpha:
                return (best_value, best_move)
            
            beta = min(beta, best_value)

        return (best_value, best_move)


    def max(self, board, depth, alpha, beta):

        if depth == self.max_depth or board.is_terminal():
            return (self.evaluate_board(board), (board.last_move.row, board.last_move.col))
    
        children = board.get_children(self.player_letter)
        if not children:
            return self.min(board, depth + 1, alpha, beta)

        best_value = float('-inf')
        best_move = None

        for (row, col), child in children.items():
            child_value = self.min(child, depth + 1, alpha, beta)[0]

            if child_value > best_value:
                best_value = child_value
                best_move = (row, col)

            if best_value >= beta:
                return (best_value, best_move)
            
            alpha = max(alpha, best_value)

        return (best_value, best_move)