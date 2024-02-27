import time
import sys
import curses  # pip install windows-curses
from random import randint

class Field:
    def __init__(self, size):
        self.size = size
        self.icons = {
            0: ' . ',
            1: ' * ',
            2: ' # ',
            3: ' & ',
        }
        self.snake_coords = [(size // 2, size // 2)]  # Starting position of the snake
        self.direction = curses.KEY_RIGHT  # Initial direction of the snake
        self._generate_field()
        self.add_entity()

    def add_entity(self):
        while True:
            i = randint(0, self.size - 1)
            j = randint(0, self.size - 1)
            entity = (i, j)
            if entity not in self.snake_coords:
                self.field[i][j] = 3
                break

    def _generate_field(self):
        self.field = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def _clear_field(self):
        self.field = [[j if j != 1 and j != 2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        size = self.size
        self._clear_field()

        for i, j in self.snake_coords:
            self.field[i][j] = 1

        head = self.snake_coords[-1]
        self.field[head[0]][head[1]] = 2

        for i in range(size):
            row = ''.join(self.icons[self.field[i][j]] for j in range(size))
            screen.addstr(i, 0, row)

    def get_entity_pos(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 3:
                    return (i, j)
        return (-1, -1)

    def is_snake_eat_entity(self):
        entity = self.get_entity_pos()
        head = self.snake_coords[-1]
        return entity == head

    def move_snake(self):
        head = self.snake_coords[-1]
        if self.direction == curses.KEY_UP:
            new_head = (head[0] - 1, head[1])
        elif self.direction == curses.KEY_DOWN:
            new_head = (head[0] + 1, head[1])
        elif self.direction == curses.KEY_LEFT:
            new_head = (head[0], head[1] - 1)
        elif self.direction == curses.KEY_RIGHT:
            new_head = (head[0], head[1] + 1)

        # Check if the new head position is valid
        if 0 <= new_head[0] < self.size and 0 <= new_head[1] < self.size and new_head not in self.snake_coords[:-1]:
            self.snake_coords.append(new_head)
            if not self.is_snake_eat_entity():
                self.snake_coords.pop(0)
            else:
                self.add_entity()
        else:
            # Snake collided with the boundary or itself, game over
            curses.endwin()
            print("Game Over!")
            sys.exit()

def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    field = Field(10)

    while True:
        field.render(w)
        w.refresh()

        key = w.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            field.direction = key

        field.move_snake()
        time.sleep(0.1)

if __name__ == '__main__':
    curses.wrapper(main)
