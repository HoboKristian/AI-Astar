# State. Unique index + cost
class STATE:
    GOAL = (0, 1)
    START = (1, 1)
    WATER = (2, 100)
    MOUNTAIN = (3, 50)
    FOREST = (4, 10)
    GRASS = (5, 5)
    ROAD = (6, 1)
    OPEN = (7, 1)
    CLOSED = (8, 10e10)
    DRAW_CLOSED = 9
    DRAW_OPEN = 10
    DRAW_PATH = 11
    @staticmethod
    def get_state_for_char(c):
        if c == "#":
            return STATE.CLOSED
        if c == ".":
            return STATE.OPEN
        elif c == "w":
            return STATE.WATER
        elif c == "f":
            return STATE.FOREST
        elif c == "g":
            return STATE.GRASS
        elif c == "r":
            return STATE.ROAD
        elif c == "m":
            return STATE.MOUNTAIN
        elif c == "A":
            return STATE.GOAL
        elif c == "B":
            return STATE.START
    @staticmethod
    def get_color_for_state(state):
        if state == STATE.CLOSED:
            return (80,80,80)
        if state == STATE.OPEN:
            return (255,255,255)
        if state == STATE.WATER:
            return (0,0,255)
        if state == STATE.FOREST:
            return (0,255,0)
        if state == STATE.GRASS:
            return (0,150,0)
        if state == STATE.ROAD:
            return (120,120,120)
        if state == STATE.MOUNTAIN:
            return (40,40,40)
        if state == STATE.GOAL:
            return (255,0,0)
        if state == STATE.START:
            return (255,255,0)
