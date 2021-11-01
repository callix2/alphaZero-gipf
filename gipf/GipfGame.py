from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .GipfLogic import Board
import numpy as np
import string

class GipfGame(Game):
    alpha = list(string.ascii_lowercase)
    
    spot_content = {
        -1: "X",
        +0: " ",
        +1: "O"
    }

    def __init__(self, n):
        self.n = n
        #self.refill()

    def refill(self):
        self.reserve = [1, None, 1] #normal: 12, mini: 5

    def getInitBoard(self):
        """ Returns the initial board (numpy board)
        """
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (int(self.n//1.8), self.n)

    def getActionSize(self):
        # return number of actions
        return round(self.n*2.34) #normal: 42, mini:30

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        if player == -1:
            board = board*player
            r_tmp = board[0][0] 
            board[0][0] = abs(board[0][2])
            board[0][2] = abs(r_tmp)
        return board

    def stringRepresentation(self, board):
        return board.tostring()

    def getSymmetries(self, board, pi):
        # mirror, rotational

        assert(len(pi) == 30) 
        
        b = Board(self.n)
        b.pieces = np.copy(board)
        
        syms = []      
        newB = board
        newPi = pi
        for i in range(1, 5):

            if i % 2:
                # flip board left<->right: 
                newB = np.fliplr(newB)
                # flip pi left<->right:
                newPi = self.fliplr_action(newPi)
            else:
                 # flip board up<->down: 
                newB = np.flipud(newB)
                # flip pi up<->down:
                newPi = self.flipud_action(newPi)

            # record the symmetry
            syms += [(newB, list(newPi))]        
              
        return syms

    def fliplr_action(self, pi):
        """
        Input: first XOR second half of Pi
        Returns: the half of pie in a reordered list that corresponds
                 to a left<--->right flip of the board
        """
        assert (len(pi) == 30)
    
        flip_indices = [0, 3, 4, 1, 2, 7, 8, 5, 6, 10, 9, 13, 14, 11, 12, 17, 
                        18, 15, 16, 20, 19, 23, 24, 21, 22, 27, 28, 25, 26, 29]    
    
        pi_new = [pi[i] for i in flip_indices]
  
        return pi_new

    def flipud_action(self, pi):
        """
        Input: first XOR second half of Pi
        Returns: the half of pie in a reordered list that corresponds
                 to a left<--->right flip of the board
        """
        assert (len(pi) == 30)
    
        flip_indices = [29, 25, 26, 27, 28, 21, 22, 23, 24, 19, 20, 16, 15, 18, 
                        17, 12, 11, 14, 13, 9, 10, 5, 6, 7, 8, 1, 2, 3, 4, 0]

        pi_new = [pi[i] for i in flip_indices]
  
        return pi_new

    def getNextState(self, board, curPlayer, action):
        """Executes the given move and returns next (board, player)
        action must be a valid move
        """
        b = Board(self.n)
        b.pieces = np.copy(board)
        # Reserve um einen reduzieren
        self.dec_reserve(b.pieces, curPlayer)
        # Move ausführen
        b.execute_move(action, curPlayer)
        # Steine schlagen und Reserve auffüllen
        add_reserve = b.remove_lines(curPlayer)
        self.inc_reserve(b.pieces, add_reserve)
        return (b.pieces, -curPlayer)

    def getValidMoves(self, board):
        """Returns a vector with all possible moves
        """
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves_binary() 
        return legalMoves

    def getValidMovesHuman(self, board):
        """Returns a vector with all possible moves
        """
        b = Board(self.n)
        b.pieces = np.copy(board)
        allMoves =  b.get_all_moves()
        valids = b.get_legal_moves_binary()
        return allMoves, valids
    
    #def hasPiecesLeft(self, player):
    #    """Returns True if the player still has pieces left in his reserve
    #    """
    #    if self.reserve(player+1) > 0:
    #        return True
    #    else:
    #        return False  
    
    def getGameEnded(self, board):
        """Returns 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        """
        """
        if self.reserve[0] == 0: # Player -1
            return 1
        elif self.reserve[2] == 0: # Player 1
            return -1
        else:
            return 0
        """
        if board[0][0] == 0: # Player -1
            return 1
        elif board[0][2] == 0: # Player 1
            return -1
        else:
            return 0

    def dec_reserve(self, board, player):
        #self.reserve[player+1] -= 1
        board[0][player+1] -= 1

    def inc_reserve(self, board, add_reserve):
        #self.reserve = np.add(self.reserve, add_reserve, where=[1,0,1])
        board[0][0] += add_reserve[0]
        board[0][2] += add_reserve[2]

    def display(self, board):
        """Displays the current board
        """
        b = Board(self.n)
        n = board.shape
        print("\nReserve Black (X): ", board[0][0])
        # label top
        print("    ", end="")
        for y in range(n[1]):
            if y < 4:
                print(GipfGame.alpha[y]+(str(y+4)), end=" ")
            else:
                print(GipfGame.alpha[y]+(str(10-y)), end=" ")
        print("")
        # board
        for x in range(n[0]):
            print("   ", end="")
            for y in range(n[1]):
                if (x,y) in b.get_startingPoints():
                    print(" "+chr(9679), end=" ")
                elif (x,y) in b.get_actBoard():
                    piece = board[x][y]    # get the piece to print
                    print("("+GipfGame.spot_content[piece]+")", end="")
                else:
                    print("   ", end="")
            print("")
        # label bottom
        print("   ", end="")
        for y in range(n[1]):
            print(GipfGame.alpha[y]+"1", end=" ")
        print("")
        print("Reserve White (O): ", board[0][2])
        print("")
