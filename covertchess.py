import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import display
import board

b = board.Board().set_up()
d = display.Display()
d.redraw(b, False)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
