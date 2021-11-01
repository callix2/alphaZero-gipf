import Arena
from MCTS import MCTS
from gipf.GipfGame import GipfGame
from gipf.GipfPlayers import *
from gipf.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_gipf = True  # Play in 6x6 instead of the normal 8x8.

p1_human = False
p2_human = True
p2_random = False
#human_vs_human = True

if mini_gipf:
    g = GipfGame(13)
else:
    g = GipfGame(17)


# nnet players
if p1_human:
    player1 = HumanGipfPlayer(g).play
else:
    n1 = NNet(g)
    if mini_gipf:
        n1.load_checkpoint('temp','best.pth.tar')
    else:
        n1.load_checkpoint('./pretrained_models/othello/pytorch/','8x8_100checkpoints_best.pth.tar')
    args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))
    player1 = n1p

if p2_human:
     player2 = HumanGipfPlayer(g).play  
elif p2_random:
    player2 = RandomGipfPlayer(g).play
else:
    n2 = NNet(g)
    n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    mcts2 = MCTS(g, n2, args2)
    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))
    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(player1, player2, g, display=GipfGame.display)

print(arena.playGames(2, verbose=True))
