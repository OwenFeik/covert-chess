import pygame
import loaders

class Display():
    def __init__(self, size = (640, 640)):
        pygame.init()
        pygame.display.set_caption('chess')

        self.size = size
        self.width, self.height = size
        self.board_size = int(((min(self.size) * 0.8) // 8) * 8) # // 8 * 8 ensures a multiple of 8
        self.tile_size = self.board_size // 8
        self.screen = pygame.display.set_mode(size)
        self.surface = pygame.Surface((self.board_size, self.board_size)).convert()
        self.colours = loaders.get_colours()

    def redraw(self, board, colour = True):
        self.draw_board()
        self.colour_visible_tiles(board, colour)

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
                self.surface.fill(self.colours['board_hidden_white'], (x * ts * 2, y * ts * 2, ts, ts))
                self.surface.fill(self.colours['board_hidden_white'], ((x + 0.5) * ts * 2, (y + 0.5) * ts * 2, ts, ts))

    def colour_visible_tiles(self, board, colour):
        tiles = []
        for piece in board.pieces:
            if piece.colour == colour:
                tiles.extend(piece.visible())
        tiles = list(set(tiles))
        
        ts = self.tile_size
        for tile in tiles:
            x, y = tile
            # x % 2 == y % 2 for white tiles on a chess board.
            if x % 2 == y % 2:
                colour = self.colours['board_visible_black']
            else:
                colour = self.colours['board_visible_white']

            # (7 - y) because piece pos is given from BL rather than TR
            self.surface.fill(colour, (x * ts, (7 - y) * ts, ts, ts))
