import pieces

class Board:
    def __init__(self, player = True):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.active_piece = None
        self.feedback_tile = None # e.g. "can't move king here, checked"
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
        king = self.get_king(colour) 
        if king and (king.pos in self.checked_tiles(colour)):
            return king
        return None

    def checked_tiles(self, colour):
        return self.moves(not colour).intersection(self.visible(not colour))

    def checkmate(self, colour):
        king = self.get_king(colour)
        old_x, old_y = king.pos
        for m in king.moves(self):
            x, y = m
            target = self.board[x][y]
            self.board[x][y] = king
            self.board[old_x][old_y] = None

            self.recalc()
            result = (x, y) in self.checked_tiles(colour)

            self.board[old_x][old_y] = king
            self.board[x][y] = target

            if not result:
                return False
        return True

    def legal_king_move(self, king, x, y):
        old_x, old_y = king.pos
        target = self.board[x][y]
        self.board[x][y] = king
        self.board[old_x][old_y] = None

        result = (x, y) in self.known_checked_tiles(king.colour)

        self.board[old_x][old_y] = king
        self.board[x][y] = target

        return result

    def known_checked_tiles(self, colour):
        visible = self.visible(colour)
        visible_enemies = [p for p in self.pieces if (p.pos in visible) and (p.colour != colour)] 
        known_checked = [] 
        for piece in visible_enemies:
            known_checked.extend(piece.moves(self))

        return set(known_checked)

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

    def get_king(self, colour):
        for piece in self.pieces:
            if piece.piece_name == 'king' and piece.colour == colour:
                return piece

    def handle_click(self, x, y):
        self.feedback_tile = None
        if self.active_piece and self.active_piece.can_move_to(self, x, y):
            success = self.active_piece.move(self, x, y)
            if success:
                self.active_piece = None
                self.recalc()
            else:
                self.feedback_tile = (x, y)
        elif self.board[x][y]:
            if self.board[x][y].colour == self.player:
                self.active_piece = self.board[x][y]
