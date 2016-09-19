import pygame
import sys

from state import STATE

width = 20
height = 20

def draw_nodes(nodes, board_x, board_y):
    pygame.init()
    screen = pygame.display.set_mode((board_x*width, board_y*height))
    screen.fill((255,255,255))
    for n in nodes:
        x,y = n.x, n.y
        col = STATE.get_color_for_state(n.state)
        pygame.draw.rect(screen, col, (x*width,y*height,width,height), 0)
        center = (x*width + width/2, y*height+height/2)
        if n.draw_state == STATE.DRAW_CLOSED:
            pygame.draw.lines(screen, (0,0,0), False, [((x+1)*width, y*height), (x*width, (y+1)*height)], 2)
            pygame.draw.lines(screen, (0,0,0), False, [(x*width, y*height), ((x+1)*width, (y+1)*height)], 2)
        elif n.draw_state == STATE.DRAW_OPEN:
            pygame.draw.rect(screen, (0,0,0), (x*width+width/4,y*height+height/4,width/2,height/2), 0)
        elif n.draw_state == STATE.DRAW_PATH:
            pygame.draw.circle(screen, (0,0,0), center, 5)

    for x in range(board_x):
        for y in range(board_y):
            pygame.draw.rect(screen, (0,0,0), (x*width,y*height,width,height), 1)

    pygame.display.update()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit(); sys.exit();
