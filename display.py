import pygame
import loaders

class Display():
    def __init__(self, board, size = (640, 640)):
        pygame.init()
        pygame.display.set_caption('chess')

        self.board = board

        self.size = size
        self.width, self.height = size
        self.board_size = int(((min(self.size) * 0.8) // 8) * 8) # // 8 * 8 ensures a multiple of 8
        self.x_border_size = int(self.width * 0.1)
        self.y_border_size = int(self.height * 0.1) 
        self.tile_size = self.board_size // 8
        
        self.colours = loaders.get_colours()

        self.screen = pygame.display.set_mode(size)
        self.surface = pygame.Surface((self.board_size, self.board_size)).convert_alpha()
        self.board_base = pygame.Surface((self.board_size, self.board_size)).convert_alpha()
        self.draw_board(self.board_base)

        self.sprites = loaders.Spritesheet.get_pieces(int(self.tile_size * 0.8))

    def redraw(self, colour = True):
        self.surface.blit(self.board_base, (0, 0))

        if self.board.winner is not None:
            self.draw_all_tiles()
        else:
            self.draw_visible_tiles(colour)

        l = (self.width - self.board_size) // 2
        t = (self.height - self.board_size) // 2

        self.screen.blit(self.surface, (l, t))

        pygame.display.update()

    def draw_board(self, surface = None):
        if not surface:
            surface = self.surface

        # Fill board black then draw white tiles
        surface.fill(self.colours['board_black'])
        for x in range(4):
            for y in range(4):
                self.fill_tile('board_white', x * 2, y * 2, surface = surface)
                self.fill_tile('board_white', (x * 2) + 1, (y * 2) + 1, surface = surface)

    def draw_visible_tiles(self, player):
        visible = [(x, (7 - y)) for x, y in self.board.visible(player)]

        for tile in visible:
            x, y = tile
            self.fill_tile(self.colours['board_visible_overlay'], x, y, 128)

        if self.board.active_piece:
            for move in self.board.active_piece.moves(self.board):
                x, y = move
                self.fill_tile('board_possible_moves', x, (7 - y), 128)
            x, y = self.board.active_piece.draw_pos
            self.fill_tile('board_active_piece', x, y, 128)

        if self.board.feedback_tile:
            x, y = self.board.feedback_tile
            self.fill_tile('board_checked', x, 7 - y, 128)

        for piece in self.board.pieces:
            if piece.draw_pos in visible:
                x, y = piece.draw_pos
                self.surface.blit(self.sprites[piece.sprite_name], ((x * self.tile_size) + self.tile_size * 0.1, y * self.tile_size + self.tile_size * 0.1))

    def draw_all_tiles(self):
        # Grey out the board, so pieces can be seen
        grey = pygame.Surface((self.tile_size * 8, self.tile_size * 8))
        grey.set_alpha(128)
        grey.fill(self.colours['board_visible_overlay'])        
        self.surface.blit(grey, (0, 0))

        if self.board.winner is not None:
            self.fill_tile(self.colours['board_checked'], *self.board.feedback_tile)

        for piece in self.board.pieces:
            x, y = piece.draw_pos
            self.surface.blit(self.sprites[piece.sprite_name], ((x * self.tile_size) + self.tile_size * 0.1, y * self.tile_size + self.tile_size * 0.1))

    def fill_tile(self, colour, x, y, alpha = 255, surface = None):
        if type(colour) == str:
            colour = self.colours[colour]
        
        if not surface:
            surface = self.surface

        ts = self.tile_size

        # Surface.fill doesn't support alpha, but blitting does.
        if alpha != 255:
            tile = pygame.Surface((ts, ts))
            tile.set_alpha(alpha)
            tile.fill(colour)
            surface.blit(tile, (x * ts, y * ts))
        else:
            surface.fill(colour, (x * ts, y * ts, ts, ts))

    def handle_click(self, x, y):
        tile = (x - self.x_border_size) // self.tile_size, (y - self.y_border_size) // self.tile_size
        if 0 <= tile[0] < 8 and 0 <= tile[1] < 8:
            return self.board.handle_click(tile[0], (7 - tile[1]))
        return None
