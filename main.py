import logging
import coloredlogs
import sys
import math
from Coach import Coach
from gipf.GipfGame import GipfGame as Game
from gipf.pytorch.NNet import NNetWrapper as nn
from utils import *

sys.setrecursionlimit(10**3)

log = logging.getLogger(__name__)

coloredlogs.install(level='DEBUG')  # Change this to DEBUG to see more info. else INFO

args = dotdict({
    'numIters': 5, #1000
    'numEps': 50,         #100   # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 20,     #25     # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,  #40    # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': math.sqrt(2), #1

    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('C:\\Users\\calli\\Documents\\VSCode\\my_alpha-zero-general-master\\temp','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})


def main():

    print(sys.getrecursionlimit())


    log.info('Loading %s...', Game.__name__)
    g = Game(13)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)

    if args.load_model:
        log.info('Loading checkpoint "%s\%s"...' % args.load_folder_file)
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)

    if args.load_model:
        log.info("Loading 'trainExamples' from file...")
        c.loadTrainExamples()

    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
