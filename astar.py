import numpy as np
import math

lines = []

class STATE:
    GOAL = 0
    START = 1
    WATER = 2
    MOUNTAIN = 3
    FOREST = 4
    GRASS = 5
    ROAD = 6

class Node:
    def __init__(self, x, y, s):
        self.x = x
        self.y = y
        self.state = s
        self.g = 0
        self.parent = 0

    def set_kids(self, c):
        self.children = c

    def set_g(self, g):
        self.g = g

    def set_best_parent(self, parent):
        self.parent = parent

with open('boards/board-2-2.txt') as f:
    for l in f:
        lines.append(l)

def f(n, goal):
    return n.g + hier(n, goal)

def main():
    board = []

    for y in range(len(lines)):
        line = lines[y].strip()
        board.append([0]*len(line))
        for x in range(len(line)):
            c = line[x]
            if c == "w":
                node = Node(x, y, STATE.WATER)
            elif c == "f":
                node = Node(x, y, STATE.FOREST)
            elif c == "g":
                node = Node(x, y, STATE.GRASS)
            elif c == "r":
                node = Node(x, y, STATE.ROAD)
            elif c == "m":
                node = Node(x, y, STATE.MOUNTAIN)
            elif c == "A":
                node = Node(x, y, STATE.GOAL)
                goal = node
            elif c == "B":
                node = Node(x, y, STATE.START)
                start = node
            else:
                continue
            board[y][x] = node

    nodes = create_nodes(board)
    best_first_search(nodes, start, goal)

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

def hier(node, goal):
    x1,y1 = float(goal.x), float(goal.y)
    x2,y2 = float(node.x), float(node.y)
    cost = math.sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)
    return cost

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

def print_node_costs(nodes, goal):
    for n in nodes:
        print(f(n, goal), n.x, n.y)

def lowest_node_cost(open_arr, goal):
    lowest_cost = 10e100
    best = 0
    for n in open_arr:
        cost = f(n, goal)
        if cost < lowest_cost:
            best = n
            lowest_cost = cost
    return best

def arc_cost(child, parent):
    print(child.state)
    if child.state == STATE.WATER:
        return 100
    elif child.state == STATE.MOUNTAIN:
        return 50
    elif child.state == STATE.FOREST:
        return 10
    elif child.state == STATE.GRASS:
        return 5
    elif child.state == STATE.ROAD:
        return 1
    elif child.state == STATE.GOAL:
        return 1
    elif child.state == STATE.START:
        return 1
    else:
        print("wops")

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

def print_parent_path(node):
    path = []

    while node.parent:
        path.append((node.x, node.y))
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

def best_first_search(nodes, start, goal):
    OPEN = [start]
    CLOSED = []

    while 1:
        x = lowest_node_cost(OPEN, goal)
        print(x.x,x.y)
        if x == goal:
            print("yay")
            print_parent_path(x)
            break
        OPEN.remove(x)
        CLOSED.append(x)
        SUCC = x.children
        for s in SUCC:
            if s not in OPEN and s not in CLOSED:
                attach_and_eval(s, x)
                OPEN.append(s)
            elif x.g + arc_cost(s, x) < s.g:
                attach_and_eval(s, x)
                propagate_path_improvements(s)

#    print_node_costs(nodes,goal)

main()