import pygame
import loaders

class Display():
    def __init__(self, board, size = (640, 640)):
        pygame.init()
        pygame.display.set_caption('chess')

        self.board = board
        self.active_piece = None

        self.size = size
        self.width, self.height = size
        self.board_size = int(((min(self.size) * 0.8) // 8) * 8) # // 8 * 8 ensures a multiple of 8
        self.x_border_size = int(self.width * 0.1)
        self.y_border_size = int(self.height * 0.1) 
        self.tile_size = self.board_size // 8
        
        self.screen = pygame.display.set_mode(size)
        self.surface = pygame.Surface((self.board_size, self.board_size)).convert_alpha()
        self.colours = loaders.get_colours()
        self.sprites = loaders.Spritesheet.get_pieces(int(self.tile_size * 0.8))

    def redraw(self, colour = True):
        self.draw_board()
        self.draw_visible_tiles(colour)

        l = (self.width - self.board_size) // 2
        t = (self.height - self.board_size) // 2

        self.screen.blit(self.surface, (l, t))

        pygame.display.update()

    def draw_board(self):
        ts = self.tile_size

        # Fill board black then draw white tiles
        self.surface.fill(self.colours['board_hidden_black'])
        for x in range(4):
            for y in range(4):
                self.fill_tile('board_hidden_white', x * 2, y * 2)
                self.fill_tile('board_hidden_white', (x * 2) + 1, (y * 2) + 1)

    def draw_visible_tiles(self, colour):
        visible = []
        for piece in self.board.pieces:
            if piece.colour == colour:
                visible.extend([(x, (7 - y)) for x, y in piece.visible()])
        visible = list(set(visible))
        
        for tile in visible:
            x, y = tile
            # x % 2 == y % 2 for white tiles on a chess board.
            # flipped because we number from 0 not 1
            if x % 2 == y % 2:
                colour = self.colours['board_visible_black']
            else:
                colour = self.colours['board_visible_white']

            self.fill_tile(colour, x, y)

        if self.active_piece:
            for move in self.active_piece.moves(self.board):
                x, y = move
                self.fill_tile('board_possible_moves', x, (7 - y), 128)
            x, y = self.active_piece.draw_pos
            self.fill_tile('board_active_piece', x, y, 128)

        for piece in self.board.pieces:
            if piece.draw_pos in visible:
                x, y = piece.draw_pos
                self.surface.blit(self.sprites[piece.sprite_name], ((x * self.tile_size) + self.tile_size * 0.1, y * self.tile_size + self.tile_size * 0.1))

    def fill_tile(self, colour, x, y, alpha = 255):
        if type(colour) == str:
            colour = self.colours[colour]
        
        ts = self.tile_size

        # Surface.fill doesn't support alpha, but blitting does.
        if alpha != 255:
            tile = pygame.Surface((ts, ts))
            tile.set_alpha(alpha)
            tile.fill(colour)
            self.surface.blit(tile, (x * ts, y * ts))
        else:
            self.surface.fill(colour, (x * ts, y * ts, ts, ts))

    def handle_click(self, x, y):
        tile = (x - self.x_border_size) // self.tile_size, (y - self.y_border_size) // self.tile_size
        for piece in self.board.pieces:
            if piece.draw_pos == tile:
                self.active_piece = piece
