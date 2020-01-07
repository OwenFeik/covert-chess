import pieces

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []

    def __getitem__(self, key):
        return self.board[key]

    def __str__(self):
        return '\n'.join(' '.join([str(p) if p is not None else '_' for p in r]) for r in self.board)

    def set_up(self):
        for i in range(8):
            self.add(pieces.Pawn(i, 1, True))
            self.add(pieces.Pawn(i, 1, False))

        return self

    def place(self, piece):
        if piece.colour:
            self.board[piece.x][piece.y] = piece
        else:
            self.board[piece.x][7 - piece.y] = piece

    def add(self, piece):
        self.pieces.append(piece)
        self.place(piece)
