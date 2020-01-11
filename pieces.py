# Note:
# because I'm an idiot, the chess piece coordinates
# work as follows; Each piece takes it's own starting
# side as the zero of a y axis, while they share x
# values. White (True) has the actual coordinates
# while black coordinates need to be adapted by
# subtracting their y-coordinate from 7. This does
# allow each piece a notion of forward, which is
# somewhat interesting.

class Piece:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y

        # True for white, False for black
        self.colour = colour

        self.moved = False
        self.piece_name = 'piece'

        self.init()

    def init(self):
        # Set up anything necessary about the piece
        # e.g. the king is checkable, pawn double move
        pass

    def __str__(self):
        return ('White ' if self.c else 'Black ') + self.piece_name.capitalize()

    @property
    def c(self):
        return self.colour

    @property
    def sprite_name(self):
        return ('white' if self.colour else 'black') + '_' + self.piece_name

    @property
    def pos(self):
        return (self.x, self.y) if self.colour else (self.x, (7 - self.y))

    @property
    def draw_pos(self):
        # Returns the position of the piece relative
        # to the top left rather than the bottom right.

        return (self.x, (7 - self.y)) if self.colour else (self.x, self.y)

    def get_context(self, board):
        # Black pieces deal with the board from the opposite
        # perspective of white pieces.

        b = board.board
        if self.colour == False:
            b = [list(reversed(column)) for column in b]

        v = board.visible(self.c)
        if self.colour == False:
            v = [(t[0], (7 - t[1])) for t in v]

        return b, v

    def remove_context(self, tiles):
        if self.colour == False:
            # Because the board is flipped on black, fix moves
            return [(tile[0], 7 - tile[1]) for tile in tiles]
        else:
            return tiles

    def visible(self):
        # Tiles on the board that this piece can see
        # Default of all adjacent tiles (Pawn)

        tiles = []
        for x in range(3):
            for y in range(3):
                tiles.append((self.x + x - 1, self.y + y - 1))

        # Only tiles that are actually on the board
        tiles = [t for t in self.remove_context(tiles) if 0 <= t[0] < 8 and 0 <= t[1] < 8] 

        return tiles

    def moves(self, board):
        # Return a list of possible moves for this
        # piece, based on the current boardstate
        return self.remove_context(self._moves(*self.get_context(board)))

    def _moves(self, board, visible):
        # moves() sets up the board to be processed
        # by this function, and cleans this functions outputs
        pass

    def move(self, board, x, y):
        new_x, new_y = self._move(board, x, y)

        self.x = new_x
        if self.c:
            self.y = new_y
        else:
            self.y = (7 - new_y)
        self.moved = True

    def _move(self, board, x, y):
        target_piece = board.board[x][y]
        if target_piece:
            board.captured.append(target_piece)
            board.pieces.remove(target_piece)

        old_x, old_y = self.pos
        board.board[old_x][old_y] = None
        board.board[x][y] = self

        return (x, y)

    def can_move_to(self, board, x, y):
        return (x, y) in self.moves(board)

class Pawn(Piece):
    def init(self):
        self.piece_name = 'pawn'

    def _moves(self, board, visible):
        moves = []

        # A pawn can't move if it's in the final tile (should have upgraded)
        if self.y == 7:
            return moves

        # Forward
        if board[self.x][self.y + 1] == None:
            moves.append((self.x, self.y + 1))

            if not self.moved and board[self.x][self.y + 2] == None:
                moves.append((self.x, self.y + 2))

        # Forward-left
        if 1 < self.x: 
            tile = board[self.x - 1][self.y + 1]
            if tile != None and tile.c != self.c:
                moves.append((self.x - 1, self.y + 1))
        
        # Forward-right
        if 7 > self.x:
            tile = board[self.x + 1][self.y + 1]
            if tile != None and tile.c != self.c:
                moves.append((self.x + 1, self.y + 1))

        return moves

class Rook(Piece):
    def init(self):
        self.piece_name = 'rook'

    def _moves(self, board, visible):
        moves = []

        for x in range(self.x + 1, 8):
            if board[x][self.y] and (x, self.y) in visible:
                if board[x][self.y].c != self.c:
                    moves.append((x, self.y))    
                break
            else:
                moves.append((x, self.y))

        for x in range(self.x - 1, -1, -1):
            if board[x][self.y] and (x, self.y) in visible:
                if board[x][self.y].c != self.c:
                    moves.append((x, self.y))    
                break
            else:
                moves.append((x, self.y))

        for y in range(self.y + 1, 8):
            if board[self.x][y] and (self.x, y) in visible:
                if board[self.x][y].c != self.c:
                    moves.append((self.x, y))    
                break
            else:
                moves.append((self.x, y))

        for y in range(self.y - 1, -1, -1):
            if board[self.x][y] and (self.x, y) in visible:
                if board[self.x][y].c != self.c:
                    moves.append((self.x, y))    
                break
            else:
                moves.append((self.x, y))

        return moves

    def _move(self, board, x, y):
        old_x, old_y = self.pos
        
        if x != self.x:
            offset = 1 if old_x < x else -1

            for _x in range(old_x + offset, x + offset, offset):
                if board.board[_x][old_y]:
                    break
            else:
                _x = x
            _y = old_y
        elif y != self.y:
            offset = 1 if old_y < y else -1
            for _y in range(old_y + offset, y + offset, offset):
                if board.board[old_x][_y]:
                    break
            else:
                _y = y
            _x = old_x

        target_piece = board.board[_x][_y]
        if target_piece:
            board.captured.append(target_piece)
            board.pieces.remove(target_piece)
        board.board[old_x][old_y] = None
        board.board[_x][_y] = self

        return (_x, _y)

class Knight(Piece):
    def init(self):
        self.piece_name = 'knight'

    def _moves(self, board, visible):
        moves = []
        x, y = self.pos

        for i in range(1, 3):
            moves.append((x + i, y + (3 - i))) # TR moves
            moves.append((x + (3 - i), y - i))
            moves.append((x - i, y - (3 - i)))
            moves.append((x - (3 - i), y + i))

        moves = [m for m in self.remove_context(moves) if 0 <= m[0] < 8 and 0 <= m[1] < 8]
        moves = [m for m in moves if (not board[m[0]][m[1]]) or (not board[m[0]][m[1]].c == self.c)]

        return moves

class Bishop(Piece):
    def init(self):
        self.piece_name = 'bishop'

    def _moves(self, board, visible):
        moves = []
        x, y = self.x, self.y

        # TR for white, BR for black
        for i in range(1, min(7 - x, 7 - y) + 1):
            if board[x + i][y + i] and (x + i, y + i) in visible:
                if board[x + i][y + i].c != self.c:
                    moves.append((x + i, y + i))
                break
            else:
                moves.append((x + i, y + i))

        # TL for white, BL for black
        for i in range(1, min(x, 7 - y) + 1):
            if board[x - i][y + i] and (x - i, y + i) in visible:
                if board[x - i][y + i].c != self.c:
                    moves.append((x - i, y + i))
                break
            else:
                moves.append((x - i, y + i))

        # BL for white, TL for black
        for i in range(1, min(x, y) + 1):
            if board[x - i][y - i] and (x - i, y - i) in visible:
                if board[x - i][y - i].c != self.c:
                    moves.append((x - i, y - i))
                break
            else:
                moves.append((x - i, y - i))

        # BR for white, TR for black
        for i in range(1, min(7 - x, y) + 1):
            if board[x + i][y - i] and (x + i, y - i) in visible:
                if board[x + i][y - i].c != self.c:
                    moves.append((x + i, y - i))
                break
            else:
                moves.append((x + i, y - i))


        return moves

    def _move(self, board, x, y):
        old_x, old_y = self.pos

        x_dir = 1 if old_x < x else -1
        y_dir = 1 if old_y < y else -1
        
        in_range_x = lambda i: (x_dir > 0  and (0 <= i < x)) or (x_dir < 0 and (x < i < 8)) 
        in_range_y = lambda i: (y_dir > 0  and (0 <= i < y)) or (y_dir < 0 and (y < i < 8))

        _x, _y = old_x, old_y
        while in_range_x(_x) and in_range_y(_y):
            _x += x_dir
            _y += y_dir

            if board.board[_x][_y]:
                break
        else:
            _x, _y = x, y

        target_piece = board.board[_x][_y]
        if target_piece:
            board.captured.append(target_piece)
            board.pieces.remove(target_piece)
        board.board[old_x][old_y] = None
        board.board[_x][_y] = self

        return (_x, _y)

class Queen(Piece):
    def init(self):
        self.piece_name = 'queen'
        self.rook = Rook(self.x, self.y, self.colour)
        self.rook.moved = True # prevent castling
        self.bishop = Bishop(self.x, self.y, self.colour)

    def _moves(self, board, visible):
        moves = self.rook._moves(board, visible)
        moves.extend(self.bishop._moves(board, visible))

        return moves

    def _move(self, board, x, y):
        old_x, old_y = self.pos
        if old_x != x and old_y != y:
            self.bishop.move(board, x, y)
            new_x, new_y = self.bishop.pos
            board.board[new_x][new_y] = self
            self.rook.x, self.rook.y = self.bishop.x, self.bishop.y
            return new_x, new_y
        else:
            self.rook.move(board, x, y)
            new_x, new_y = self.rook.pos
            board.board[new_x][new_y] = self
            self.bishop.x, self.bishop.y = self.rook.x, self.rook.y
            return new_x, new_y

class King(Piece):
    def init(self):
        self.piece_name = 'king'

    def _moves(self, board, visible):
        moves = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (0 <= self.x + x < 8):
                    continue
                elif self.c and not (0 < self.y + y <= 8):
                    continue
                elif not (0 < 7 - (self.y + y) <= 8):
                    continue
                elif board[x + self.x][y + self.y] and board[x + self.x][y + self.y].c == self.c:
                    continue

                moves.append((self.x + x, self.y + y))

        return moves
