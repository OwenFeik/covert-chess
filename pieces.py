# Note:
# because I'm an idiot, the chess piece coordinates
# work as follows. Each piece takes it's own starting
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

        self.init()

    def __str__(self):
        return 'G'

    @property
    def c(self):
        return self.colour

    def visible(self):
        # Tiles on the board that this piece can see
        # Default of all adjacent tiles (Pawn)

        tiles = []
        for x in range(3):
            for y in range(3):
                tiles.append((self.x + x - 1, self.y + y - 1))

        if self.c == False:
            tiles = [(t[0], (7 - t[1])) for t in tiles]
        tiles = [t for t in tiles if 0 <= t[0] < 8 and 0 <= t[1] < 8] # Only tiles that are actually on the board

        return tiles

    def init(self):
        # Set up anything necessary about the piece
        # e.g. the king is checkable, pawn double move
        pass

    def moves(self, board):
        # Return a list of possible moves for this
        # piece, based on the current boardstate
        pass

    def move(self):
        # Resolve any actions necessary after a
        # move of this piece, e.g. pawn replacement
        pass

class Pawn(Piece):
    def init(self):
        self.moved = False

    def __str__(self):
        return 'P' + ('W' if self.c else 'B')

    def moves(self, board):
        board = board.board

        # To do moves for black, simply flip the board
        if self.c == False:
            board = list(reversed(board))
        
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

        if self.c == False:
            # Because the board is flipped on black, fix moves
            return [(m[0], 7 - m[1]) for m in moves]
        else:
            return moves

    def move(self):
        self.moved = True
