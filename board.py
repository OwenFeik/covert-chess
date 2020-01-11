import pieces

class Board:
    def __init__(self, player = True):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.active_piece = None
        self.captured = []
        self.player = player

        # Cache results of expensive operations
        self._visible = {True: set(), False: set()}
        self.recalc_visible = {True: True, False: True}
        self._moves = {True: set(), False: set()}
        self.recalc_moves = {True: True, False: True}

    def visible(self, colour):
        if self.recalc_visible[colour]:
            visible = []
            for piece in self.pieces:
                if piece.colour == colour:
                    visible.extend(piece.visible())
            visible = set(visible)
            self._visible[colour] = visible
            self.recalc_visible[colour] = False

        return self._visible[colour]

    def moves(self, colour):
        if self.recalc_moves[colour]:
            moves = []
            for piece in self.pieces:
                if piece.colour == colour:
                    moves.extend(piece.moves(self))
            moves = set(moves)
            self._moves[colour] = moves
            self.recalc_moves[colour] = False

        return self._moves[colour]

    def recalc(self):
        self.recalc_moves[True] = True
        self.recalc_moves[False] = True
        self.recalc_visible[True] = True
        self.recalc_visible[False] = True

    def checked(self, colour):
        for piece in self.pieces:
            if (piece.piece_name == 'king') and (piece.colour == colour):
                king = piece
                if king.pos in self.moves(not colour).intersection(self.visible(not colour)):
                    return king
                break
        return None

    def set_up(self):
        for x in range(8):
            self.add(pieces.Pawn(x, 1, True))
            self.add(pieces.Pawn(x, 1, False))

        for x in [0, 7]:
            self.add(pieces.Rook(x, 0, True))
            self.add(pieces.Rook(x, 0, False))

        for x in [1, 6]:
            self.add(pieces.Knight(x, 0, True))
            self.add(pieces.Knight(x, 0, False))

        for x in [2, 5]:
            self.add(pieces.Bishop(x, 0 ,True))
            self.add(pieces.Bishop(x, 0, False))

        self.add(pieces.Queen(3, 0, True))
        self.add(pieces.Queen(3, 0, False))

        self.add(pieces.King(4, 0, True))
        self.add(pieces.King(4, 0, False))

        return self

    def place(self, piece):
        if piece.colour:
            self.board[piece.x][piece.y] = piece
        else:
            self.board[piece.x][7 - piece.y] = piece

    def add(self, piece):
        self.pieces.append(piece)
        self.place(piece)

    def handle_click(self, x, y):
        if self.active_piece and self.active_piece.can_move_to(self, x, y):
            self.active_piece.move(self, x, y)
            self.active_piece = None
            self.recalc()
        elif self.board[x][y]:
            if self.board[x][y].colour == self.player:
                self.active_piece = self.board[x][y]
