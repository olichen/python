# Text-based minesweeper game

import random


class Board:
    def __init__(self, n, num_bombs):
        self.cells = [[0 for y in range(n)]
                         for x in range(n)]
        if num_bombs > n * n:
            raise Exception

        bomb_pos = list(range(n*n))
        random.shuffle(bomb_pos)
        for pos in bomb_pos[:num_bombs]:
            self.cells[pos%n][pos//n] = 9

        for x in range(n):
            for y in range(n):
                self.cells[y][x] = self._count_adj_bombs(x, y, n)

    def _count_adj_bombs(self, x, y, n):
        if self.cells[y][x] == 9:
            return 9

        x_s = x - 1 if x > 0 else 0
        x_e = x + 2 if x < n - 1 else n
        y_s = y - 1 if y > 0 else 0
        y_e = y + 2 if y < n - 1 else n
        count = 0
        for i in range(x_s, x_e):
            for j in range(y_s, y_e):
                if self.cells[j][i] == 9:
                    count += 1
        return count


class Game:
    def __init__(self):
        self.reset_game(20, 40)
        self.render()
        print('Type h for help')
        self.mainloop()

    def reset_game(self, n, bombs):
        self.flags = [[False for y in range(n)]
                             for x in range(n)]
        self.hidden = [[True for y in range(n)]
                             for x in range(n)]
        self.board = Board(n, bombs)

    def render(self):
        # header
        n = len(self.flags)
        line = '  '
        for i in range(n):
            line += str(int(i)%10) + ' '
        print(line)

        for y, arr in enumerate(self.hidden):
            line = f'{y%10} '
            for x, hidden in enumerate(arr):
                if self.flags[y][x]:
                    line += 'F'
                elif hidden:
                    line += '?'
                else:
                    cell = self.board.cells[y][x]
                    if cell == 9:
                        line += 'B'
                    elif cell == 0:
                        line += ' '
                    else:
                        line += str(cell)
                line += ' '
            print(line)

    def flip_cell(self, x, y):
        # Mark as flipped
        self.hidden[y][x] = False

        # Lose if cell is a bomb
        cell = self.board.cells[y][x]
        if cell == 9:
            return False
        # Return if cell is a flag or not empty
        if self.flags[y][x]:
            return True
        if cell > 0:
            return True

        # Otherwise, cell is empty:
        n = len(self.flags)
        x_s = x - 1 if x > 0 else 0
        x_e = x + 2 if x < n - 1 else n
        y_s = y - 1 if y > 0 else 0
        y_e = y + 2 if y < n - 1 else n
        for i in range(x_s, x_e):
            for j in range(y_s, y_e):
                if self.hidden[j][i]:
                    val = self.board.cells[j][i]
                    if val == 0:
                        self.flip_cell(i, j)
                    else:
                        self.hidden[j][i] = False
        return True

    def set_flag(self, x, y):
        self.flags[y][x] = not self.flags[y][x]

    def mainloop(self):
        self.get_input()
        self.render()
        self.mainloop()

    def get_input(self):
        print('Input > ', end='')
        x = input().split(' ')
        cmd = x[0]
        if cmd == 'h':
            self.print_help()
            return
        try:
            arg1, arg2 = int(x[1]), int(x[2])
            if cmd == 'd':
                self.flip_cell(arg1, arg2)
            elif cmd == 'f':
                self.set_flag(arg1, arg2)
            elif cmd == 'f':
                self.reset_game(arg1, arg2)
            else:
                print('Unable to parse command')
        except:
            print('Unable to parse command')

    def print_help(self):
        print('d <X> <Y>: Defuse cell (X,Y)')
        print('f <X> <Y>: Flag cell (X,Y)')
        print('h: Help')
        print('r <N> <B>: Restart with an NxN board and B bombs')
