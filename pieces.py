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
        self.colour = colour

        self.checkable = False
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
        return b

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
        return self.remove_context(self._moves(self.get_context(board)))

    def _moves(self, board):
        # moves() sets up the board to be processed
        # by this function, and cleans this functions outputs
        pass

    def move(self):
        # Resolve any actions necessary after a
        # move of this piece, e.g. pawn replacement
        self.moved = True

class Pawn(Piece):
    def init(self):
        self.piece_name = 'pawn'

    def _moves(self, board):
        moves = []

        if board[self.x][self.y + 1] == None:
            moves.append((self.x, self.y + 1))

            if not self.moved and board[self.x][self.y + 2] == None:
                moves.append((self.x, self.y + 2))

        if 1 < self.x: 
            tile = board[self.x - 1][self.y + 1]
            if tile != None and tile.c != self.c:
                moves.append((self.x - 1, self.y + 1))
        
        if 7 > self.x:
            tile = board[self.x + 1][self.y + 1]
            if tile != None and tile.c != self.c:
                moves.append((self.x + 1, self.y + 1))

        return moves

class Rook(Piece):
    def init(self):
        self.piece_name = 'rook'

    def moves(self, board):
        b = board.board

