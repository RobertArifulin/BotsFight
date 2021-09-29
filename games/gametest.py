from game import Game, Status


class GameTest(Game):

    def __init__(self):
        super().__init__()
        self.board = [[0] * 5 for _ in range(5)]

    def get_board_string(self) -> str:
        res = ''
        for line in self.board:
            res += ' '.join([str(i) for i in line]) + '\n'
        return res[:-1]

    def bot_made_turn(self, turn: str) -> Status:
        MAX = 20
        for i in range(len(self.board)):
            y, number = map(int, turn.split())
            self.board[y - 1][i] = number

        if sum([self.board[i][0] for i in range(5)]) >= MAX > sum([self.board[i][1] for i in range(5)]):
            self.status = Status.bot1_won
            return self.status

        elif sum([self.board[i][1] for i in range(5)]) >= MAX:
            self.status = Status.bot2_won
            return self.status

        elif sum([self.board[i][1] for i in range(5)]) == sum([self.board[i][0] for i in range(5)]) >= MAX:
            self.status = Status.draw
            return self.status

        elif self.status == Status.bot1_next:
            self.status = Status.bot2_next
            return self.status

        else:
            self.status = Status.bot1_next
            return self.status
