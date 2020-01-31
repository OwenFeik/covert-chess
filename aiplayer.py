import copy
import math

class AIPlayer():
    piece_values = {
        'pawn': 1,
        'rook': 5,
        'knight': 3,
        'bishop': 3,
        'queen': 9
    }

    def __init__(self, colour = False, depth = 1):
        self.colour = colour
        self.depth = depth
        self.visible = None

    def get_move(self, board):
        self.visible = board.visible(self.colour)
        return self.minimax(board, depth = self.depth, turn = self.colour)

    def minimax(self, board, depth, turn = None):
        if turn is None:
            turn = self.colour

        values = {}

        for piece in [p for p in board.pieces if p.colour == turn]:
            for move in piece.moves(board):
                x, y = piece.pos
                move_board = copy.deepcopy(board)
                move_board.board[x][y].move(move_board, *move)
                if depth == 0:
                    values[(x, y, *move)] = self.evaluate_board(move_board) 
                else:
                    values[(x, y, *move)] = self.minimax(move_board, depth - 1, not turn)

        if turn == self.colour:
            best_val = math.inf * -1
            best_move = None
            for move in values:
                if values[move] > best_val:
                    best_val = values[move]
                    best_move = move
        
            return best_move if depth == self.depth else best_val
        else:
            worst_val = math.inf
            for move in values:
                if values[move] > worst_val:
                    worst_val = values[move]

            return worst_val

    def evaluate_board(self, board):
        value = 0
        
        multiplier = lambda p: (1 if p.colour == self.colour else -1)

        for piece in board.pieces:
            if (piece.colour == self.colour or piece.pos in self.visible) and not piece.piece_name == 'king':
                value += (self.piece_values[piece.piece_name] + (0.1 * piece.y)) * multiplier(piece)

        for piece in board.captured:
            value += self.piece_values[piece.piece_name] * multiplier(piece) * -1

        return value
