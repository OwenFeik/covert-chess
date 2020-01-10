import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import display
import board
from pieces import Pawn

player = False

b = board.Board(player).set_up()
b.add(Pawn(3, 5, True))
d = display.Display(b)
d.redraw(player)

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
    if redraw:
        d.redraw(player)
        redraw = False

pygame.quit()
