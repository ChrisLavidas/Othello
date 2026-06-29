import copy
from Move import Move

class Board:
    W = 1
    B = -1
    EMPTY = 0


    def __init__(self):
        self.last_move = Move()
        self.last_player = self.W
        self.Board = [[self.EMPTY for _ in range(8)] for _ in range(8)]
        # αρχική θέση Othello        
        self.Board[3][3] = self.W
        self.Board[4][4] = self.W
        self.Board[3][4] = self.B
        self.Board[4][3] = self.B

        self.move_history = []

        #self.Board[0][0] = self.W
        #self.Board[1][1] = self.W
        #self.Board[1][0] = self.B
        #self.Board[2][1] = self.B


    def __copy__(self):
        new_board = Board()
        new_board.last_move = copy.copy(self.last_move)
        new_board.last_player = self.last_player
        new_board.Board = [row[:] for row in self.Board]
        new_board.move_history = self.move_history
        return new_board


    def print_board(self):
        symbols = {1: 'W', -1: 'B', 0: '.'}
        print("    0 1 2 3 4 5 6 7")
        print("  __________________")
        for i, row in enumerate(self.Board):
            print(i, "|", " ".join(symbols[cell] for cell in row))
        print()
    
    def change_last_player(self):
        self.last_player = self.B if self.last_player == self.W else self.W

    def copy_change_last_player(self):
            new_board = copy.copy(self)
            new_board.last_player = self.B if self.last_player == self.W else self.W
            return new_board

    # βοηθητική συνάρτηση, επιστρέφει λίστες με τις 8 κατευθύνσεις (οριζόντια, κάθετα, διαγώνια)
    def get_lines(self, i, j):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]               
        lines = []
        
        for di, dj in directions:
            path = []
            ni, nj = i + di, j + dj
            while 0 <= ni < len(self.Board) and 0 <= nj < len(self.Board[0]):
                path.append((ni, nj))
                ni += di
                nj += dj
            if path:
                lines.append(path)
        return lines
        

    def available_moves(self, is_sorted=False):
        # ο παίκτης που έχει σειρά
        current_player = self.B if self.last_player == self.W else self.W
        # ο τελευταίος που έπαιξε
        opponent = self.last_player

        def get_valid_moves():
            valid_moves = {}
            for i in range(8):
                for j in range(8):
                    if self.Board[i][j] != self.EMPTY:
                        continue

                    total_flips = 0

                    for path in self.get_lines(i, j):
                        if len(path) < 2:
                            continue

                        first = self.Board[path[0][0]][path[0][1]]
                        if first != opponent:
                            continue

                        count = 0
                        for (x, y) in path:
                            if self.Board[x][y] == self.EMPTY:
                                break
                            if self.Board[x][y] == opponent:
                                count += 1
                            if self.Board[x][y] == current_player:
                                total_flips += count
                                break

                    if total_flips > 0:
                        valid_moves[(i, j)] = total_flips

            return valid_moves

        if not is_sorted:
            return list(get_valid_moves().keys())
        else:

            def weights(move):
                i, j = move
                if (i == 0 or i == 7) and (j == 0 or j == 7):
                    return 5  # γωνίες
                elif i == 0 or i == 7 or j == 0 or j == 7:
                    return 3  # άκρα
                else:
                    return 1  # εσωτερικά
                
            sorted_moves = sorted(get_valid_moves().items(), key=lambda item: item[1] + weights(item[0]), reverse=True)
            return [move for move, flips in sorted_moves]
            
    def available_moves_for(self, player):
        opponent = self.W if player == self.B else self.B
        valid_moves = []
        
        for i in range(8):
            for j in range(8):
                if self.Board[i][j] != self.EMPTY:
                    continue

                for path in self.get_lines(i, j):
                    if len(path) < 2:
                        continue

                    first = self.Board[path[0][0]][path[0][1]]
                    if first != opponent:
                        continue

                    for (x, y) in path[1:]:
                        if self.Board[x][y] == self.EMPTY:
                            break
                        if self.Board[x][y] == player:
                            valid_moves.append((i, j))
                            break
                            
        return list(set(valid_moves))
    
    def make_move(self, row, col, letter):
        current_player = letter
        opponent = self.last_player
        
        self.Board[row][col] = letter
        self.last_move = Move(row, col)

        for path in self.get_lines(row, col):
            if len(path) < 2:
                continue
            
            first = self.Board[path[0][0]][path[0][1]]
            if first != opponent:
                continue

            for index, (x, y) in enumerate(path[1:], start = 1):
                if self.Board[x][y] == self.EMPTY:
                    break
                if self.Board[x][y] == current_player:
                    for (x, y) in path[:index]:
                        self.Board[x][y] = current_player
                    break

        self.move_history.append((row, col))
        self.last_player = letter

    
    def is_valid_move(self, row, col):
        if row > 7 or col > 7 or row < 0 or col < 0:
            return False  
        
        if self.Board[row][col] != self.EMPTY:
            return False
        
        if (row, col) not in self.available_moves():
            return False 
        
        return True
    
    
    def get_children(self, letter):
        children = {}

        for (i, j) in self.available_moves(is_sorted=True):
            if self.is_valid_move(i, j):
                child = copy.deepcopy(self)
                child.make_move(i, j, letter)
                children[(i, j)] = child

        return children
    

    def is_terminal(self):
        if len(self.available_moves()) == 0 and len(self.copy_change_last_player().available_moves()) == 0:
            return True
        return False


    def get_move_history(self):
        return self.move_history   

    def get_scores(self):
        whites = sum(row.count(self.W) for row in self.Board)
        blacks = sum(row.count(self.B) for row in self.Board)
        return {"W": whites, "B": blacks}
