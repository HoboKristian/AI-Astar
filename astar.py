import heapq
import math
import draw
from state import STATE

lines = []
goal = 0

board_name = "board-1-1.txt"
board_x = 0
board_y = 0

class Node:
    def __init__(self, x, y, s):
        self.x = x
        self.y = y
        self.state = s
        self.g = 0
        self.parent = 0
        self.draw_state = 0

    def __cmp__(self, other):
        return cmp(f(self, goal), f(other, goal))

    def set_kids(self, c):
        self.children = c

    def set_g(self, g):
        self.g = g

    def set_best_parent(self, parent):
        self.parent = parent


with open('boards/' + board_name) as f:
    for l in f:
        lines.append(l)

# Parses the textfile and creates the board
def main():
    global goal, board_x, board_y
    board = []
    board_x = len(lines[0])
    board_y = len(lines)

    for y in range(len(lines)):
        line = lines[y].strip()
        board.append([0]*len(line))
        for x in range(len(line)):
            c = line[x]
            state = STATE.get_state_for_char(c)
            node = Node(x, y, state)
            if state == STATE.START:
                start = node
            if state == STATE.GOAL:
                goal = node
            board[y][x] = node

    nodes = create_nodes(board)
    best_first_search(nodes, start)

# Flattens the two-dimensional board into a tree of the nodes
def create_nodes(board):
    nodes = []
    for y in range(len(board)):
        for x in range(len(board[0])):
            node = board[y][x]
            nodes.append(node)

    for n in nodes:
        children = []
        for c in child_nodes(n, board):
            c_x, c_y = c
            child = board[c_y][c_x]
            children.append(child)
        n.set_kids(children)

    return nodes

# h(x) which defines the estimated cost from a node to the goal
# currently uses the eucliden distance: sqrt(x_diff^2+y_diff^2)
def hier(node, goal):
    x1,y1 = float(goal.x), float(goal.y)
    x2,y2 = float(node.x), float(node.y)
    cost = math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)
    return cost

# Creates an array containing tuples of all the children (x, y)
# The tuples are trimmed to fit within the boundaries of the map
# Currently only uses adjacents nodes (which it should)
def child_nodes(node, board):
    children = []
    x = node.x
    y = node.y
    for child_x in range(max(x-1, 0), min(x+2, len(board[0]))):
        if not child_x == x:
             children.append((child_x, y))

    for child_y in range(max(y-1, 0), min(y+2, len(board))):
        if not child_y == y:
             children.append((x, child_y))

    return children

# Only cost needed is the cost of the node you are walking to
def arc_cost(child, parent):
    cost = child.state[1]
    return cost

# Cost function
def f(n, goal):
    return n.g + hier(n, goal)

def attach_and_eval(child, parent):
    child.set_best_parent(parent)
    child.set_g(parent.g + arc_cost(child, parent))

def propagate_path_improvements(parent):
    for c in parent.children:
        cost = parent.g + arc_cost(c, parent)
        if cost < c.g:
            c.set_best_parent(parent)
            c.set_g(cost)
            propagate_path_improvements(c)

# Creates the path by going back from the goal and then changes the original
# to include the path
def print_parent_path(node):
    path = []

    while node.parent:
        path.append((node.x, node.y))
        node.draw_state = STATE.DRAW_PATH
        node = node.parent

    i = 0
    for p in path:
        x,y = p
        line = list(lines[y])
        line[x] = str("-")
        lines[y] = "".join(line)
        i += 1

    for l in lines:
        print(l.strip())

def best_first_search(nodes, start):
    OPEN = []
    heapq.heappush(OPEN, start)
    CLOSED = []

    while 1:
        x = heapq.heappop(OPEN)
        if x.x == goal.x and x.y == goal.y:
            for closed_node in CLOSED:
                closed_node.draw_state = STATE.DRAW_CLOSED
            for open_node in OPEN:
                open_node.draw_state = STATE.DRAW_OPEN
            print_parent_path(x)
            draw.draw_nodes(nodes, board_x, board_y)
            break
        CLOSED.append(x)
        SUCC = x.children
        for s in SUCC:
            if s not in OPEN and s not in CLOSED:
                attach_and_eval(s, x)
                heapq.heappush(OPEN, s)
            elif x.g + arc_cost(s, x) < s.g:
                attach_and_eval(s, x)
                propagate_path_improvements(s)

main()
