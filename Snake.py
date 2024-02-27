import curses
import time
import sys
from random import randint

class Field:
    def __init__(self, size):
        self.size = size
        self.icons = {
            0: ' . ',  # نماد مکان‌های خالی در بازی
            1: ' * ',  # نماد بدنهٔ مار
            2: ' # ',  # نماد سر مار
            3: ' & ',  # نماد غذا
        }
        self.snake_coords = []  # مختصات مار
        self._generate_field()  # ایجاد نقشهٔ بازی
        self.add_entity()  # اضافه کردن یک جسم جدید به بازی

    def add_entity(self):
        # اضافه کردن یک جسم جدید به بازی در مکان‌های خالی
        while(True):
            i = randint(0, self.size-1)
            j = randint(0, self.size-1)
            entity = [i, j]
            
            if entity not in self.snake_coords:
                self.field[i][j] = 3  # جسم جدید را در نقشهٔ بازی نشان می‌دهیم
                break

    def _generate_field(self):
        # ایجاد نقشهٔ بازی خالی
        self.field = [[0 for j in range(self.size)] for i in range(self.size)]

    def _clear_field(self):        
        # پاک کردن نقشهٔ بازی
        self.field = [[j if j!= 1 and j!= 2 else 0 for j in i] for i in self.field]

    def render(self, screen):
        # نمایش نقشهٔ بازی در ترمینال
        size = self.size
        self._clear_field()

        # نمایش مار در نقشه
        for i, j in self.snake_coords:
            self.field[i][j] = 1

        # نمایش سر مار
        head = self.snake_coords[-1]
        self.field[head[0]][head[1]] = 2

        for i in range(size):
            row = ''
            for j in range(size):
                row += self.icons[ self.field[i][j] ]
            screen.addstr(i, 0, row)

    def get_entity_pos(self):
        # دریافت موقعیت جسم جدید در نقشهٔ بازی
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] == 3:
                    return [i, j]
        return [-1, -1]

    def is_snake_eat_entity(self):
        # بررسی اینکه مار جسم جدید را بخورده است یا خیر
        entity = self.get_entity_pos()
        head = self.snake_coords[-1]
        return entity == head


class Snake:
    def __init__(self, name):
        self.name = name
        self.direction = curses.KEY_RIGHT  # جهت حرکت اولیهٔ مار
        self.coords = [[0, 0], [0, 1], [0, 2], [0, 3]]  # مختصات اولیهٔ مار

    def set_direction(self, ch):
        # تنظیم جهت حرکت مار بر اساس دکمه‌ای که کاربر فشرده است
        # و جلوگیری از حرکت معکوس مار
        if ch == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT:
            return
        if ch == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT:
            return
        if ch == curses.KEY_UP and self.direction == curses.KEY_DOWN:
            return
        if ch == curses.KEY_DOWN and self.direction == curses.KEY_UP:
            return 
        self.direction = ch

    def level_up(self):
        # افزایش سطح مار
        a = self.coords[0]
        b = self.coords[1]
        tail = a[:]
        if a[0] < b[0]:
            tail[0]-=1
        elif a[1] < b[1]:
            tail[1]-=1
        elif a[0] > b[0]:
            tail[0]+=1
        elif a[1] > b[1]:
            tail[1]+=1
        tail = self._check_limit(tail)
        self.coords.insert(0, tail)

    def is_alive(self):
        # بررسی اینکه مار زنده است یا نه
        head = self.coords[-1]
        snake_body = self.coords[:-1]
        return head not in snake_body

    def _check_limit(self, point):
        # بررسی اینکه مار از حدود بازی خارج نشود
        if point[0] > self.field.size-1:
            point[0] = 0
        elif point[0] < 0:
            point[0] = self.field.size-1
        elif point[1] < 0:
            point[1] = self.field.size-1
        elif point[1] > self.field.size-1:
            point[1] = 0
        return point

    def move(self):
        # حرکت مار
        head = self.coords[-1][:]
        if self.direction == curses.KEY_UP:
            head[0]-=1
        elif self.direction == curses.KEY_DOWN:
            head[0]+=1
        elif self.direction == curses.KEY_RIGHT:
            head[1]+=1
        elif self.direction == curses.KEY_LEFT:
            head[1]-=1
        head = self._check_limit(head)
        del(self.coords[0])
        self.coords.append(head)
        self.field.snake_coords = self.coords

        if not self.is_alive():
            sys.exit()

        # بررسی اینکه آیا مار جسم جدید را خورده است یا نه
        if self.field.is_snake_eat_entity():
            curses.beep()
            self.level_up()
            self.field.add_entity()

    def set_field(self, field):
        # تنظیم نقشهٔ بازی برای مار
        self.field = field

def main(screen):
    # پیکربندی صفحهٔ نمایش
    screen.timeout(0)

    # آغاز بازی
    field = Field(10)
    snake = Snake("Joe")
    snake.set_field(field)

    while(True):
        # گرفتن دکمه‌ای که کاربر فشرده است
        ch = screen.getch()
        if ch != -1:
            # تنظیم جهت حرکت مار
            snake.set_direction(ch)

        # حرکت مار
        snake.move()

        # نمایش نقشهٔ بازی
        field.render(screen)
        screen.refresh()
        
        time.sleep(.4)

if __name__=='__main__':
    # اجرای بازی
    curses.wrapper(main)
