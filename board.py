import pieces
import aiplayer

class Board:
    def __init__(self, player = True):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.pieces = []
        self.active_piece = None
        self.feedback_tile = None # e.g. "can't move king here, checked"
        self.captured = []
        self.player = player
        self.winner = None

        self.ai = aiplayer.AIPlayer(not player)

        # Cache results of expensive operations
        self.cache = {}
        self.clear_cache()
        self.calculated = {}
        self.recalc()

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

    def clear_cache(self):
        self.cache = {
            'visible': {
                True: set(),
                False: set()
            },
            'moves': {
                True: set(),
                False: set()
            }
        }

    def recalc(self):
        self.calculated = {
            'visible': {
                True: False,
                False: False
            },
            'moves': {
                True: False,
                False: False
            }
        }

    def visible(self, colour):
        if not self.calculated['visible'][colour]:
            visible = []
            for piece in self.pieces:
                if piece.colour == colour:
                    visible.extend(piece.visible())
            visible = set(visible)
            self.cache['visible'][colour] = visible
            self.calculated['visible'][colour] = True

        return self.cache['visible'][colour]

    def moves(self, colour):
        if not self.calculated['moves'][colour]:
            moves = []
            for piece in self.pieces:
                if piece.colour == colour:
                    moves.extend(piece.moves(self))
            moves = set(moves)
            self.cache['moves'][colour] = moves
            self.calculated['moves'][colour] = True

        return self.cache['moves'][colour]

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
            moves = piece.moves(self)
            if piece.piece_name == 'pawn':
                x, y = piece.pos
                for move in [(x, y + 1), (x, y + 2), (x, y - 1), (x, y - 2)]:
                    if move in moves:
                        moves.remove(move)
            known_checked.extend(moves)

        return set(known_checked)

    def get_king(self, colour):
        for piece in self.pieces:
            if piece.piece_name == 'king' and piece.colour == colour:
                return piece

    def take_ai_move(self):
        captured_count = len(self.captured)

        piece, move = self.ai.get_move(self)
        piece.move(self, *move)

        if len(self.captured) > captured_count:
            if self.captured[-1].piece_name == 'king':
                self.winner = self.ai.colour
                self.feedback_tile = piece.draw_pos

        self.recalc()

    def handle_click(self, x, y):
        self.feedback_tile = None
        if self.active_piece and self.active_piece.can_move_to(self, x, y):
            captured_count = len(self.captured)
            success = self.active_piece.move(self, x, y)
            if success:
                self.recalc()

                if len(self.captured) > captured_count:
                    if self.captured[-1].piece_name == 'king':
                        self.winner = self.player
                        self.feedback_tile = self.active_piece.draw_pos
                        return None

                self.active_piece = None
                return True
            else:
                self.feedback_tile = (x, y)
        elif self.board[x][y]:
            if self.board[x][y].colour == self.player:
                self.active_piece = self.board[x][y]
