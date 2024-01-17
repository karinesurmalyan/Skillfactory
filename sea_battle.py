import random
from time import sleep

MARK = '■'
MISS = 'T'
HIT = 'X'
AROUND = '-'

class UserException(Exception):
    pass

class IndexException(Exception):
    pass
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x, self.y == self.y

class Ship:
    def __init__(self, length, dot, direction):
        self.length = length
        self.dot = Dot(*dot)
        self.direction = direction
        self.intact_dots = None

    def dots(self):
        dots_list = [] #список всех точек корабля
        for i in range(self.length):
            if self.direction:
                x = self.dot.x
                y = self.dot.y + i
            else:
                x = self.dot.x + i
                y = self.dot.y
            dots_list.append(Dot(x, y))
        return dots_list

    def check_intact_dots(self, lost_dots):
        self.intact_dots = self.length - lost_dots + self.length
        return self.intact_dots

    def get_direction(self):
        if self.length[0][0] != self.length[1][0]:
            return 1
        else:
            return 0

class Board:
    def __init__(self):
        self.field = self.create_board()
        self.enemy_field = self.create_board()
        self.ships_sizes = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]
        self.hid = bool(0)
        self.ship_indexes = []
        self.shots_indexes = [[]]
        self.ship_counter = 0

    def get_my_board(self):
        for i in range(len(self.field)):
            print(self.field[i], end='')
            print()

    def get_enemy_board(self):
        for i in range(len(self.enemy_field)):
            print(*self.enemy_field[i], end='')
            print()

    def get_board(self):
        return self.field

    @staticmethod
    def create_board():
        field = []
        for _ in range(7):
            k = [i for i in range(7)]
            field.append(k)
        for row in range(1, 7):
            for column in range(7):
                if column == 0:
                    field[row][column] = row
                else:
                    field[row][column] = 'O'
        field[0][0] = ' '
        return field

    def add_ship(self, row, column, direction, length):
        try:
            @staticmethod
            def check_if_used(ships_sizes, length):
                flag = False
                for i in ships_sizes:
                    if len(i) == length:
                        flag = True
                        ships_sizes.remove(i)
                        break
                if not flag:
                    raise UserException('Кораблей данного типа больше нет')
                return ships_sizes

            @staticmethod
            def available_ship_indexes(field, row, column, direction, length):
                if field[row][column] == MARK:
                    raise UserException
                if direction != 0 and direction != 1:
                    raise UserException
                if length > 3 or length <= 0:
                    raise UserException
                if (0 < row < len(field)) and (0 < column < len(field)):
                    if (column > 4 and direction == 0 and length == 3) or (column == 6 and direction == 0 and length > 1):
                        raise IndexException
                    if (row > 4 and direction == 1 and length == 3) or (row == 6 and direction == 1 and length > 1):
                        raise IndexException
                else:
                    raise IndexException('Неверные координаты')
                ship = Ship(length, (row, column), direction).dots()
                if direction:
                    for i in ship:
                        dot = Dot(*i)
                        if field[dot.x - 1][dot.y] == MARK or field[dot.x - 1][dot.y - 1] == MARK:
                            raise IndexException
                        try:
                            if field[dot.x - 1][dot.y + 1] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if field[dot.x][dot.y - 1] == MARK:
                                raise IndexException
                            if field[dot.x][dot.y + 1] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if field [dot.x + 1][dot.y] == MARK:
                                raise IndexException
                            if field[dot.x + 1][dot.y - 1] == MARK:
                                raise IndexException
                            if field[dot.x + 1][dot.y + 1] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
                else:
                    for i in ship:
                        dot = Dot(*i)
                        if field[dot.x][dot.y - 1] == MARK or field[dot.x - 1][dot.y - 1] == MARK:
                            raise IndexException
                        try:
                            if field[dot.x + 1][dot.y - 1] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if field[dot.x - 1][dot.y] == MARK:
                                raise IndexException
                            if field[dot.x+ 1][dot.y] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
                        try:
                            if field[dot.x][dot.y + 1] == MARK:
                                raise IndexException
                            if field[dot.x - 1][dot.y + 1] == MARK:
                                raise IndexException
                            if field[dot.x + 1][dot.y + 1] == MARK:
                                raise IndexException
                        except IndexError:
                            pass
            available_ship_indexes(self.field, row, column, direction, length)
            ships_sizes = check_if_used(self.ships_sizes, length)
        except (IndexException, UserException) as err:
            pass
        else:
            self.ship_indexes.append(Ship(length, (row, column), direction).dots())
            self.ships_sizes = ships_sizes.copy()
            for i in self.ship_indexes[self.ship_counter]:
                dot = Dot(*i)
                self.field[dot.x][dot.y] = MARK
            self.field = self.contour(direction, self.field, self.ship_counter, self.ship_indexes)
            self.ship_counter += 1

        @staticmethod
        def contour(direction, field, counter, indexes):
            CONTOUR = MARK + MISS + HIT + '-123456'
            if direction:
                for i in indexes[counter]:
                    dot = Dot(*i)
                    try:
                        if str(field[dot.x - 1][dot.y]) not in CONTOUR:
                            field[dot.x - 1][dot.y] = AROUND
                            if str(field[dot.x - 1][dot.y - 1]) not in CONTOUR:
                                field[dot.x - 1][dot.y - 1] = AROUND
                        if str(field[dot.x - 1][dot.y + 1]) not in CONTOUR:
                            field[dot.x - 1][dot.y + 1] = AROUND
                    except IndexError:
                        pass
                    if str(field[dot.x][dot.y - 1]) not in CONTOUR:
                        field[dot.x][dot.y - 1] = AROUND
                    try:
                        if str(field[dot.x][dot.y + 1]) not in CONTOUR:
                            field[dot.x][dot.y + 1] = AROUND
                    except IndexError:
                        pass
                    try:
                        if str(field[dot.x + 1][dot.y]) not in CONTOUR:
                            field[dot.x + 1][dot.y] = AROUND
                            if str(field[dot.x + 1][dot.y - 1]) not in CONTOUR:
                                field[dot.x + 1][dot.y - 1] = AROUND
                        if str(field[dot.x + 1][dot.y + 1]) not in CONTOUR:
                            field[dot.x + 1][dot.y + 1] = AROUND
                    except IndexError:
                        pass
            else:
                for i in indexes[counter]:
                    dot = Dot(*i)
                    try:
                        if str(field[dot.x][dot.y - 1]) not in CONTOUR:
                            field[dot.x][dot.y - 1] = AROUND
                            if str(field[dot.x - 1][dot.y - 1]) not in CONTOUR:
                                field[dot.x - 1][dot.y - 1] = AROUND
                        if str(field[dot.x + 1][dot.y - 1]) not in CONTOUR:
                            field[dot.x + 1][dot.y - 1] = AROUND
                    except IndexError:
                        pass
                    if str(field[dot.x - 1][dot.y]) not in CONTOUR:
                        field[dot.x - 1][dot.y] = AROUND
                    try:
                        if str(field[dot.x + 1][dot.y]) not in CONTOUR:
                            field[dot.x + 1][dot.y] = AROUND
                    except IndexError:
                        pass
                    try:
                        if str(field[dot.x][dot.y + 1]) not in CONTOUR:
                            field[dot.x][dot.y + 1] = AROUND
                            if str(field[dot.x - 1][dot.y + 1]) not in CONTOUR:
                                field[dot.x - 1][dot.y + 1] = AROUND
                        if str(field[dot.x + 1][dot.y + 1]) not in CONTOUR:
                            field[dot.x + 1][dot.y + 1] = AROUND
                    except IndexError:
                        pass
            return field

        def shot(self, x, y):
            dot = Dot(x, y)
            if (0 < x < len(self.field)) and (0 < y < len(self.field)):
                if HIT in self.field[dot.x][dot.y] or MISS in self.field[dot.x][dot.y]:
                    raise UserException('Вы уже стреляли в данную точку')
            else:
                raise IndexException('Введенные координаты вне поля')
            if MARK in self.field[dot.x][dot.y]:
                self.field[dot.x][dot.y] = HIT
                self.enemy_field[dot.x][dot.y] = HIT
                self.shots_indexes[0].append((dot.x, dot.y))
                for i in range(len(self.ship_indexes)):
                    if (dot.x, dot.y) in self.ship_indexes[i]:
                        lost1 = len(self.ship_indexes[i]) - self.ship_indexes[i].count(HIT)
                        self.ship_indexes[i].append(HIT)
                        intact_dots = self.is_destroyed(lost1, self.ship_indexes[i])
                        return True, intact_dots
            else:
                self.field[dot.x][dot.y] = MISS
                self.enemy_field[dot.x][dot.y] = MISS
                return False, False

        def is_destroyed(self, lost1, lost2):
            intact_dots = Ship(lost1, lost2[0]).check_intact_dots(len(lost2))
            if intact_dots == 0:
                if lost1 != 1:
                    direction = Ship(lost2, lost2[0]).get_direction()
                else:
                    direction = 1
                self.enemy_field = self.contour(direction, self.enemy_field, 0, self.shots_indexes)
                self.shots_indexes = [[]]
                self.ship_counter -= 1
            return intact_dots

class Player:
    def __init__(self):
        self.moves = Board()

    def ask(self):
        pass

    def move(self):
        return self.moves.shot(*self.ask())

class User(Player):
    def ask(self):
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        return x, y

class AI(Player):
    def ask(self):
        try:
            x, y = map(int, input('Введите координаты точки выстрела').split())
        except ValueError as e:
            print('Нужно ввести 2 аргумента')
        return x, y

class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.turn = random.randint(1, 6)
        self.flag = False

    def start(self):
        self.clear_user_board()
        self.clear_ai_board()
        self.greeting()
        print(f'Хотите рандомное расставление кораблей? \n Y -Да \n N - Нет\n')
        answer = input().lower()
        if answer == 'y':
            self.flag = True
            self.random_board()
            print('Ваша доска \n')
            self.ai.moves.get_enemy_board()
            print()
            self.user.moves.get_user_board()
            print()
        else:
            self.random_board()
            self.own_board()
        self.loop()

    def loop(self):
        if self.turn:
            print('Ваш ход\n')
            self.ai.moves.get_enemy_board()
            print()
            self.user.moves.get_user_board()
            if self.ai.moves.intact_dots > 0:
                print()
                self.user.moves.get_user_board()
            while True:
                try:
                    is_hit, intact_dots = self.ai.move()
                    if is_hit:
                        if intact_dots == 0:
                            print('Корабль врага уничтожен!\n')
                        else:
                            print('Корабль врага подбит!\n')
                        sleep(2)
                        self.ai.moves.get_enemy_board()
                        print()
                        self.user.moves.get_user_board()
                        if self.ai.moves.hid > 0:
                            print()
                            self.ai.moves.get_users_board()
                        if self.ai.moves.ship_counter == 0:
                            break
                        continue
                    print('Промах\n')
                    self.turn = 0
                    break
                except Exception as e:
                    print(e)
        if self.ai.moves.ship_counter == 0:
            print('\nВсе корабли уничтожены! Желаете снова сыграть?\n Y - Да\n N - Нет\n')
            ask = input().lower()
            if ask == 'y':
                self.start()
            else:
                raise SystemExit('Спасибо за игру!')
        print('Ход противника\n')
        while True:
            try:
                is_hit, intact_dots = self.user.move()
                if is_hit:
                    sleep(2)
                    if intact_dots == 0:
                        print('Ваш корабль уничтожен!\n')
                    else:
                        print('Ваш корабль подбит!\n')
                        sleep(4)
                    self.user.moves.get_user_board()
                    print()
                    if self.user.moves.ship_counter == 0:
                        print()
                        self.ai.moves.get_users_board()
                    if self.ai.moves.ship_counter == 0:
                        break
                    continue
                sleep(2)
                print('Промах\n')
                sleep(1)
                self.turn = 1
                break
            except UserException:
                pass
        if self.user.moves.ship_counter == 0:
            print('\nПобедил компьютер! Желаете снова сыграть?\n Y - Да\n N - Нет\n')
            ask = input().lower()
            if ask == 'y':
                self.start()
            else:
                raise SystemExit('Спасибо за игру!')
        self.loop()
    def user_board(self):
        print(f'Список доступных кораблей: {self.user.moves.ships_sizes}')
        print('Введите параметры корабля в виде: <Номер строки> <Номер столбца> <Направление, где 0 - горизонтально, 1 - вертикально> <Длина>')
        while True:
            if len(self.user.moves.ships_sizes) <= 2:
                print('Если хотите поменять размещение кораблей введите латинскую С')
                ask = input().lower()
                if ask == 'c':
                    self.clear_user_board()
                try:
                    s = [int(i) for i in input().split()]
                    row, column, direction, length = s
                    self.user.moves.add_ship(row, column, direction, length)
                except (ValueError, IndexError) as e:
                    print(f'Данные введены неверно.\nВведите параметры корабля в виде: <Номер строки> <Номер столбца> <Направление, где 0 - горизонтально, 1 - вертикально> <Длина>')
                else:
                    self.ai.moves.get_enemy_board()
                    print()
                    self.user.moves.get_user_board()
                    if len(self.user.moves.ships_sizes) == 0:
                        break

    def random_board(self):
        counter = 0
        if self.flag:
            while counter < 100:
                length = len(self.user.moves.ships_sizes[0])
                row = random.randint(1, 6)
                column = random.randint(1, 6)
                direction = random.randint(0, 1)
                self.user.moves.add_ship(row, column, direction, length)
                if len(self.user.moves.ships_sizes) == 0:
                    self.flag = False
                    self.random_board()
                    break
                counter += 1
            if len(self.user.moves.ships_sizes) != 0:
                self.clear_user_board()
                self.random_board()
        else:
            counter = 0
            while counter < 100:
                length = len(self.ai.moves.ships_sizes[0])
                row = random.randint(1, 6)
                column = random.randint(1, 6)
                direction = random.randint(0, 1)
                self.ai.moves.add_ship(row, column, direction, length)
                if len(self.ai.moves.ships_sizes) == 0:
                    break
                counter += 1
            if len(self.ai.moves.ships_sizes) != 0:
                self.clear_ai_board()
                self.random_board()

    def clear_user_board(self):
        self.user.moves.field = self.user.moves.create_board()
        self.user.moves.enemy_field = self.user.moves.create_board()
        self.user.moves.ships_sizes = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]
        self.user.moves.ship_indexes = []
        self.user.moves.ship_counter = 0

    def clear_ai_board(self):
        self.ai.moves.field = self.ai.moves.create_board()
        self.ai.moves.enemy_field = self.ai.moves.create_board()
        self.ai.moves.ships_sizes = [('■', '■', '■'), ('■', '■'), ('■', '■'), ('■'), ('■'), ('■'), ('■')]
        self.ai.moves.ship_indexes = []
        self.ai.moves.ship_counter = 0

    def greeting(self):
        print('Вы играете в иорской бой.\nУ Вас будет выбор распределения кораблей самостоятельно или случайным образом')
        print('Вверхнее поле - поле врага, где будут отмечаться Ваши выстрелы. Нижнее поле - Ваша доска.')
        print('Игрок, делающий 1 ход, определяется случайным образом.')
        print('Хотите вывести доску врага на экран? Y - Да, N - Нет')
        ask = input().lower()
        if ask == 'y':
            self.ai.moves.hid = bool(1)
        else:
            self.ai.moves.hid = bool(0)

Game().start()