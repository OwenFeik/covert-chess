import random
import math

class AIPlayer():
    piece_values = {
        'pawn': 1,
        'rook': 5,
        'knight': 3,
        'bishop': 3,
        'queen': 9,
        'king': 2
    }

    def __init__(self, colour = False):
        self.colour = colour
        self.visible = {}
    
    def get_move(self, board):
        self.visible = board.visible(self.colour)

        value = self.evaluate_board(board)
        best_move_value = -1 * math.inf
        best_move = []

        for piece in [p for p in board.pieces if p.colour == self.colour]:
            for move in piece.moves(board):
                x, y = move
                target = board.board[x][y]
                move_value = value
                if target:
                    move_value += self.piece_value(target.piece_name, target.y)
                    move_value -= self.piece_value(piece.piece_name, piece.y)
                    move_value += self.piece_value(piece.piece_name, (7 - y if not self.colour else y))

                if move_value > best_move_value:
                    best_move = [(piece, move)]
                    best_move_value = move_value
                elif move_value == best_move_value:
                    best_move.append((piece, move))
                    best_move_value = move_value

        return random.choice(best_move)

    def evaluate_board(self, board):
        value = 0
        
        multiplier = lambda p: (1 if p.colour == self.colour else -1)

        for piece in board.pieces:
            if piece.pos in self.visible:
                value += self.piece_value(piece.piece_name, piece.y) * multiplier(piece)

        for piece in board.captured:
            value += self.piece_values[piece.piece_name] * multiplier(piece) * -1

        return value

    def piece_value(self, name, y):
        return self.piece_values[name] + (0.1 * y)
