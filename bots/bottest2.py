import time
if __name__ == "__main__":
    board = [[int(i) for i in line.split()] for line in input().split('\n')]
    print(f'2 {board[0][1] + 2}')
