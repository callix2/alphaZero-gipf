import numpy as np
from .GipfLogic import Board

class GipfPlayer():
    def __init__(self, game):
        self.game = game
        #self.refill()

    #reserve = 5 #normal: 12, mini: 5
    """
    def get_reserve(self):
        return self.reserve

    def dec_reserve(self):
        self.reserve -= 1

    def inc_reserve(self):
        self.reserve += 1

    def refill(self):
        self.reserve = 1 #normal: 12, mini: 5
    """
class RandomGipfPlayer(GipfPlayer):
    def __init__(self, game):
        super().__init__(game)

    def play(self, board):
        valids = self.game.getValidMovesHuman(board)
        a = np.random.randint(0, (len(valids)-1))
        print(valids[a])
        return valids[a]


class HumanGipfPlayer(GipfPlayer):
    def __init__(self, game):
        super().__init__(game)

    def play(self, board):
        allMoves, valids = self.game.getValidMovesHuman(board)
        while True:
            input_move = input()
            input_tuple = tuple(input_move.split(" "))
            if len(input_tuple) == 2:
                try:
                    input_num = Board.translate_move(input_tuple)
                    action = allMoves.index(input_num)
                    if valids[action] == 1:
                        break
                except ValueError:
                    'Invalid Field'
            print('Invalid move')
        return action


class GreedyOthelloPlayer():

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        candidates = []
        for a in range(self.game.getActionSize()):
            if valids[a]==0:
                continue
            nextBoard, _ = self.game.getNextState(board, 1, a)
            score = self.game.getScore(nextBoard, 1)
            candidates += [(-score, a)]
        candidates.sort()
        return candidates[0][1]
