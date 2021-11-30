import random

if __name__ == "__main__":
    s = ''
    for i in range(3):
        s += input() + '\n'
    s = s[:-1]
    status = s[0]
    if status == "x":
        status = 1
    else:
        status = 2
    s = s[1:]
    board = [[int(i) for i in line.split()] for line in s.split('\n')]
    columns = [[board[j][i] for j in range(3)] for i in range(3)]
    diagonals = [[board[i][i] for i in range(3)], [board[i][2 - i] for i in range(3)]]
    corners = [(0, 0), (2, 2), (0, 2), (2, 0)]
    axes = [(1, 0), (2, 1), (1, 2), (0, 1)]
    nulls = 0
    for i in range(3):
        nulls += board[i].count(0)
    moves = []


    def necessary_move(status: int) -> tuple[int, int]:
        x1, y1 = -1, -1
        for i in range(3):
            if columns[i].count(status) == 2 and columns[i].count(0) == 1:
                x1, y1 = i + 1, columns[i].index(0) + 1
                return x1, y1
            if board[i].count(status) == 2 and board[i].count(0) == 1:
                x1, y1 = board[i].index(0) + 1, i + 1
                return x1, y1
        for i in range(3):
            if columns[i].count(3 - status) == 2 and columns[i].count(0) == 1:
                x1, y1 = i + 1, columns[i].index(0) + 1
                return x1, y1
            if board[i].count(3 - status) == 2 and board[i].count(0) == 1:
                x1, y1 = board[i].index(0) + 1, i + 1
                return x1, y1
        if diagonals[0].count(status) == 2 and diagonals[0].count(0) == 1:
            x1, y1 = diagonals[0].index(0) + 1, diagonals[0].index(0) + 1
            return x1, y1
        if diagonals[1].count(status) == 2 and diagonals[1].count(0) == 1:
            x1, y1 = 3 - diagonals[1].index(0), diagonals[1].index(0) + 1
            return x1, y1
        if diagonals[0].count(3 - status) == 2 and diagonals[0].count(0) == 1:
            x1, y1 = diagonals[0].index(0) + 1, diagonals[0].index(0) + 1
            return x1, y1
        if diagonals[1].count(3 - status) == 2 and diagonals[1].count(0) == 1:
            x1, y1 = 3 - diagonals[1].index(0), diagonals[1].index(0) + 1
            return x1, y1
        return x1, y1


    x, y = -1, -1
    if status == 1:
        if nulls == 9:
            x, y = 2, 2
        elif nulls == 7:
            for i in range(1, 3):
                if board[i % 2 * 2][i % 2 * 2] == 0:
                    x, y = i % 2 * 2 + 1, i % 2 * 2 + 1
                elif board[(3 - i) % 2 * 2][i % 2 * 2] == 0:
                    x, y = (3 - i) % 2 * 2 + 1, i % 2 * 2 + 1
        else:
            x, y = necessary_move(status)
            if x == -1:
                for corner in corners:
                    new_x, new_y = corner
                    if board[new_y][new_x] == 0 and board[new_y].count(2) + columns[new_x].count(2) == 1:
                        x, y = new_x + 1, new_y + 1
                        break
    if status == 2:
        if nulls == 8:
            if board[1][1] == 0:
                x, y = 2, 2
            else:
                x, y = 1, 1
        else:
            x, y = necessary_move(status)
            if x == -1:
                if nulls == 8:
                    for new_x, new_y in axes:
                        if board[new_y][new_x] == 0:
                            x, y = new_x + 1, new_y + 1

    if x == -1:
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    moves.append((j + 1, i + 1))
        x, y = random.choice(moves)
    print(x, y)

"""
x1 2 1
0 2 0
2 1 1

x2 1 1
1 1 2
2 2 1

x0 1 0
0 1 0
0 2 2

x2 0 0
0 1 0
0 2 1
"""