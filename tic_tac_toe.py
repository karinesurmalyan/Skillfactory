def X_move(array):
    i, j = map(int, input('Введите координаты для X:').split())
    while array[i][j] != '_':
        print(f'Клетка с координатами ({i}, {j}) занята')
        i, j = map(int, input('Введите координаты для X:').split())
    array[i][j] = 'X'

def O_move(array):
    i, j = map(int, input('Введите координаты для O:').split())
    while array[i][j] != '_':
        print(f'Клетка с координатами ({i}, {j}) занята')
        i, j = map(int, input('Введите координаты для O:').split())
    array[i][j] = 'O'

def check_if_win(array):
    for i in range(3):
        if array[i][0] == array[i][1] == array[i][2] and array[i][0] != '_':
            print(f'Выиграл игрок {array[i][0]}')
            return True
        elif array[0][i] == array[1][i] == array[2][i] and array[0][i] != '_':
            print(f'Выиграл игрок {array[0][i]}')
            return True
    if (array[0][0] == array[1][1] == array[2][2] or
        array[0][2] == array[1][1] == array[2][0]) and array[1][1]!='_':
        print(f'Выиграл игрок {array[1][1]}')
        return True

def print_board(array):
    for i in range(3):
        for j in range(3):
            print(array[i][j], end=' ')
        print()
board = [['_']*3 for i in range(3)]
b = 0
print('Нумерация координат начинается с 0 и заканчивается с 2. Приятной игры!')
for i in range(9):
    if i%2==0:
        X_move(board)
        print_board(board)
        if check_if_win(board):
            b = 1
            break
    else:
        O_move(board)
        print_board(board)
        if check_if_win(board):
            b = 1
            break
if b == 0:
    print('Ничья!')