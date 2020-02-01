import time
import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import display
import board
import loaders

ai_move_delay = loaders.get_config('ai_move_delay')

player = True
b = board.Board(player).set_up()

d = display.Display(b)
d.redraw(player)

move_delay = False
timer = 0

game_running = True
redraw = False
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if not move_delay:
                x, y = event.pos
                result = d.handle_click(x, y)
                if result:
                    move_delay = True
                    timer = time.time_ns() / (10 ** 6)
                redraw = True

    if move_delay:
        if time.time_ns() / (10 ** 6) - timer > ai_move_delay:
            b.take_ai_move()
            move_delay = False
            redraw = True

    if redraw:
        d.redraw(b.player)
        redraw = False

pygame.quit()


#TODO
# upgrading pawns
# castling
# visible feedback post move
# display captured pieces
# ai takes moves
