#!/usr/local/bin/python3
"""
Simple Snake console game for Python 3.

Use it as introduction to curses module.

Warning: curses module available only in Unix.
On Windows use UniCurses (https://pypi.python.org/pypi/UniCurses).
UniCurses is not installed by default.

"""

import curses  # https://docs.python.org/3/library/curses.html
import time
import random


def redraw():  # Redraws game field and it's content after every turn
    win.erase()
    draw_food()  # Draws food on the game field
    draw_snake()  # Draws snake
    draw_menu()
    win.refresh()


def draw_menu():
    win.addstr(0,0, "Score: " + str(len(snake) - 2) + "      Press 'q' to quit", curses.color_pair(5))


def draw_snake():
    try:
        n = 0  # There can be only one head
        for pos in snake:  # Snake is the list of [y, x], so we swap them below
            if n == 0:
                win.addstr(pos[1], pos[0], "@", curses.color_pair(ex_foodcolor))  # Draws head
            else:
                win.addstr(pos[1], pos[0], "#", curses.color_pair(ex_foodcolor))  # Draws segment of the body
            n += 1
    except Exception as drawingerror:
        print(drawingerror, str(cols), str(rows))


def draw_food():
    for pos in food:
        win.addstr(pos[1], pos[0], "+", curses.color_pair(foodcolor))


def drop_food():
    x = random.randint(1, cols - 2)
    y = random.randint(1, rows - 2)
    for pos in snake:  # Do not drop food on snake
        if pos == [x, y]:
            drop_food()

    food.append([x, y])


def move_snake():
    global snake  # List
    global grow_snake  # Boolean
    global cols, rows  # Integers

    head = snake[0]  # Head is the first element of "snake list"
    if not grow_snake:  # Remove tail if food was not eaten on this turn
        snake.pop()
    else:  # If food was eaten on this turn, we don't pop last item of list,
        grow_snake = False  # but we restore default state of grow_snake
    if direction == DIR_UP:  # Calculate the position of the head
        head = [head[0], head[1] - 1]  # We will swap x and y in draw_snake()
        if head[1] == 0:
            head[1] = rows - 2  # Snake passes through the border
    elif direction == DIR_DOWN:
        head = [head[0], head[1] + 1]
        if head[1] == rows - 1:
            head[1] = 1
    elif direction == DIR_LEFT:
        head = [head[0] - 1, head[1]]
        if head[0] == 0:
            head[0] = cols - 2
    elif direction == DIR_RIGHT:
        head = [head[0] + 1, head[1]]
        if head[0] == cols - 1:
            head[0] = 1

    snake.insert(0, head)  # Insert new head


def is_food_collision():
    for pos in food:
        if pos == snake[0]:
            food.remove(pos)
            global foodcolor
            global ex_foodcolor
            ex_foodcolor = foodcolor
            foodcolor = random.randint(1, 6)  # Pick random color of the next food
            return True
    return False


def game_over():
    global is_game_over
    is_game_over = True
    win.erase()
    win.addstr(10, 20, "Game over! Your score is " + str(len(snake)) + "  Press 'q' to quit", curses.color_pair(1))


def is_suicide():  # If snake collides with itself, game is over
    for i in range(1, len(snake)):
        if snake[i] == snake[0]:
            return True
    return False


def end_game():
    curses.nocbreak()
    win.keypad(0)
    curses.echo()
    curses.endwin()


# Initialisation starts --------------------------------------------
DIR_UP = 0  # Snake's directions, values are not important,
DIR_RIGHT = 1  # they сan be "a", "b", "c", "d" or something else
DIR_DOWN = 2
DIR_LEFT = 3

is_game_over = False
grow_snake = False

snake = [[10, 5], [9, 5]]  # Set snake size and position
direction = DIR_RIGHT
food = []
foodcolor = 2
ex_foodcolor = 3

win = curses.initscr()  # Game field in console initialised with curses module
curses.start_color()  # Enables colors
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
win.keypad(1)  # Enable arrow keys
win.nodelay(1)  # Do not wait for keypress
curses.curs_set(0)  # Hide cursor
curses.cbreak()  # Read keys instantaneously
curses.noecho()  # Do not print stuff when keys are pressed
rows, cols = win.getmaxyx()  # Get terminal window size

#  Initialisation ends ---------------------------------------------


#  Main loop starts ------------------------------------------------
drop_food()
redraw()


while True:
    if is_game_over is False:
        redraw()
    key = win.getch()  # Returns a key, if pressed
    time.sleep(0.1)  # Speed of the game

    if key != -1:  # win.getch returns -1 if no key is pressed
        if key == curses.KEY_UP:
            if direction != DIR_DOWN:  # Snake can't go up if she goes down
                direction = DIR_UP
        elif key == curses.KEY_RIGHT:
            if direction != DIR_LEFT:
                direction = DIR_RIGHT
        elif key == curses.KEY_DOWN:
            if direction != DIR_UP:
                direction = DIR_DOWN
        elif key == curses.KEY_LEFT:
            if direction != DIR_RIGHT:
                direction = DIR_LEFT
        elif chr(key) == "q":
            break

    if is_game_over is False:
        move_snake()

    if is_suicide():
        game_over()

    if is_food_collision():
        drop_food()
        grow_snake = True

end_game()
#  Main loop ends --------------------------------------------------
