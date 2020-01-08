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
        self.sprites = loaders.Spritesheet.get_pieces(int(self.tile_size * 0.8))

    def redraw(self, board, colour = True):
        self.draw_board()
        self.draw_visible_tiles(board, colour)

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

    def draw_visible_tiles(self, board, colour):
        visible = []
        for piece in board.pieces:
            if piece.colour == colour:
                visible.extend(piece.visible())
        visible = list(set(visible))
        
        ts = self.tile_size
        for tile in visible:
            x, y = tile
            # x % 2 == y % 2 for white tiles on a chess board.
            # flipped because we number from 0 not 1
            if x % 2 == y % 2:
                colour = self.colours['board_visible_black']
            else:
                colour = self.colours['board_visible_white']

            # (7 - y) because piece pos is given from BL rather than TR
            self.surface.fill(colour, (x * ts, (7 - y) * ts, ts, ts))

        for piece in board.pieces:
            if piece.pos in visible:
                x, y = piece.draw_pos
                self.surface.blit(self.sprites[piece.sprite_name], ((x * self.tile_size) + self.tile_size * 0.1, y * self.tile_size + self.tile_size * 0.1))
