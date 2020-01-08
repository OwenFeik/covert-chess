import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import display
import board
from pieces import Pawn

b = board.Board().set_up()
d = display.Display(b)
d.redraw(True)

game_running = True
redraw = False
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            d.handle_click(x, y)
            redraw = True
    d.redraw(True)
    redraw = False

pygame.quit()
