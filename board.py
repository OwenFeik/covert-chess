import pieces

class Board:
    def __init__(self, player = True):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.active_piece = None
        self.captured = []
        self.player = player

    def __str__(self):
        return '\n'.join(' '.join([str(p) if p is not None else '_' for p in r]) for r in self.board)

    def visible(self, colour):
        visible = []
        for piece in self.pieces:
            if piece.colour == colour:
                visible.extend(piece.visible())
        visible = list(set(visible))

        return visible

    def set_up(self):
        for x in range(8):
            self.add(pieces.Pawn(x, 1, True))
            self.add(pieces.Pawn(x, 1, False))

        for x in [0, 7]:
            self.add(pieces.Rook(x, 0, False))
            self.add(pieces.Rook(x, 0, True))

        return self

    def place(self, piece):
        if piece.colour:
            self.board[piece.x][piece.y] = piece
        else:
            self.board[piece.x][7 - piece.y] = piece

    def add(self, piece):
        self.pieces.append(piece)
        self.place(piece)

    def move(self, piece, x, y):
        target_piece = self.board[x][y]
        if target_piece:
            self.captured.append(target_piece)
            self.pieces.remove(target_piece)
        old_x, old_y = piece.pos
        self.board[old_x][old_y] = None
        self.board[x][y] = piece
        piece.move(x, y)

    def handle_click(self, x, y):
        if self.active_piece and self.active_piece.can_move_to(self, x, y):
            self.active_piece.move(self, x, y)
            self.active_piece = None
        elif self.board[x][y]:
            if self.board[x][y].colour == self.player:
                self.active_piece = self.board[x][y]
