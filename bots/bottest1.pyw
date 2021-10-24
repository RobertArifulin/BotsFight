if __name__ == "__main__":
    board = [[int(i) for i in line.split()] for line in input().split('\n')]
    print(f'1 {board[0][0] + 1}')
