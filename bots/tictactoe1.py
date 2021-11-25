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
    nulls = 0
    moves = []
    for i in range(3):
        for j in range(3):
            if board[j][i] == 0:
                moves.append((i + 1, j + 1))
    x, y = random.choice(moves)
    print(x, y)