'''
Author: Eric P. Nichols
Date: Feb 8, 2008.
Board class.
Board data:
  1=white, -1=black, 0=empty
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
import numpy as np


class Board():

    # list of all 6 directions on the board, as (x,y) offsets
    __directions = [(2,0),(-2,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    
    # list of all entries of the matrix, which are actually spots on the board
    actBoard = [(2,3),(3,2),(3,4),(4,1),(4,3),(4,5),(5,2),(5,4),(6,1),(6,3),(6,5),(7,2),(7,4),(8,1),(8,3),(8,5),(9,2),(9,4),(10,3)] 
    
    # list of all starting Points on the board
    startingPoints = [(0,3),(1,2),(1,4),(2,1),(2,5),(3,0),(3,6),(5,0),(5,6),(7,0),(7,6),(9,0),(9,6),(10,1),(10,5),(11,2),(11,4),(12,3)]
    
    # dictionary for the translation of the spot names into the entries of the matrix (as tuple)
    move_dict = {"a1": (9,0), "a2": (7,0), "a3": (5,0), "a4": (3,0), "b1": (10,1), "b2": (8,1), "b3": (6,1), "b4": (4,1), "b5": (2,1), "c1": (11,2),
     "c2": (9,2), "c5": (3,2), "c6": (1,2), "d1": (12,3), "d2": (10,3), "d6": (2,3), "d7": (0,3), "e1": (11,4), "e2": (9,4), "e5": (3,4),
     "e6": (1,4), "f1": (10,5), "f2": (8,5), "f3": (6,5), "f4": (4,5), "f5": (2,5), "g1": (9,6), "g2": (7,6), "g3": (5,6), "g4": (3,6)}
    
    def __init__(self, n):
        "Set up initial board configuration."
        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n # rows: mini: 13, normal: 17
        for i in range(self.n):
            self.pieces[i] = [0]*(int(self.n//(1.8))) # columns: mini: 13//1.8=7   normal: 17//1.8=9
        
        #Set up reserve in board corner
        self.pieces[0][0] = 5
        self.pieces[0][2] = 5
        
        # Set up the initial 6 pieces.
        self.pieces[4][1] = 1
        self.pieces[4][5] = 1
        self.pieces[10][3] = 1
        self.pieces[8][1] = -1
        self.pieces[8][5] = -1
        self.pieces[2][3] = -1

        """
        #Testfall Sym
        self.pieces[8][1] = 1
        self.pieces[10][3] = 1
        self.pieces[4][5] = 1
        self.pieces[2][3] = -1
        self.pieces[7][4] = -1
        self.pieces[8][5] = -1

        #Testfall A
        self.pieces[8][1] = -1
        self.pieces[7][2] = -1
        self.pieces[4][3] = -1
        self.pieces[10][3] = 1
        self.pieces[8][3] = 1
        self.pieces[4][5] = 1
        self.pieces[5][4] = 1
        
        #Testfall B
        self.pieces[7][2] = 1
        self.pieces[6][1] = 1
        self.pieces[10][3] = 1
        self.pieces[8][3] = -1
        self.pieces[4][3] = -1
        self.pieces[2][3] = -1
        
        #Testfall C
        self.pieces[4][1] = 1
        self.pieces[5][2] = -1
        self.pieces[10][3] = 1
        self.pieces[4][3] = -1
        self.pieces[2][3] = -1
        
        #Testfall D
        self.pieces[6][1] = -1
        self.pieces[7][2] = -1
        self.pieces[9][4] = 1
        self.pieces[10][3] = -1
        self.pieces[6][3] = -1
        self.pieces[4][3] = -1
        self.pieces[2][3] = 1
        """
        
    # add [][] indexer syntax to the Board
    def __getitem__(self, index): 
        return self.pieces[index]

    def __setitem__(self, index, color): 
        self.pieces[index] = color

    def get_actBoard(self):
        if self.n == 13:
            return self.actBoard
        else:
            pass # return actBoard + ext

    def get_startingPoints(self):
        if self.n == 13:
            return self.startingPoints
        else:
            pass # return actBoard + ext
    
    @staticmethod
    def translate_move(move):
        """Returns a tuple of the spot names as a tuple of the matrix
        """
        try:
            move_new = (Board.move_dict[move[0]],Board.move_dict[move[1]])
            return move_new
        except KeyError:
            'Invalid Field'

    def get_legal_moves(self):
        """Returns all the legal moves
        """
        moves = set()  # stores the legal moves.
        # discover the possible moves for every starting point
        for start in self.startingPoints:
            newmoves = self.get_moves_for_dot(start)[1],[2]
            moves.update(newmoves)
        return list(moves)

    def get_legal_moves_binary(self):
        """Returns all the legal moves
        """
        moves = []  # stores the legal moves.
        # discover the possible moves for every starting point
        for start in self.startingPoints:
            newmoves = self.get_moves_for_dot(start)[2]
            moves.extend(newmoves)
        return moves

    def get_all_moves(self):
        """Returns all the legal moves
        """
        moves = []  # stores the legal moves.
        # discover the possible moves for every starting point
        for start in self.startingPoints:
            newmoves = self.get_moves_for_dot(start)[1]
            moves.extend(newmoves)
        return moves

    def get_moves_for_dot(self, dot):
        """Returns all the legal moves that use the given dot as a base.
        """
        # search all possible directions.
        legal_moves = []
        all_moves = []
        all_moves_binary = []
        for direction in self.__directions:
            target = tuple(np.add(dot, direction))
            if target in self.actBoard:
                move = (dot, target)
                all_moves.append(move)
                if self.check_move(target, direction):
                    legal_moves.append(move)
                    all_moves_binary.extend([1])
                else:
                    all_moves_binary.extend([0])

        # return the generated move list
        return legal_moves, all_moves, all_moves_binary

    def check_move(self, target, direction):
        """Returns True if there is a free field along the given direction
        if not returns Flase because the move is not valid
        """
        s = target
        while s in self.actBoard:
            if self[s] == 0:
                    return True
            s = tuple(np.add(s, direction))
        return False

    def execute_move(self, action, curPlayer):
        """Performs the given move on the board; does not remove pieces!
        color gives the color of the piece to play (1=white,-1=black)
        """
        all_moves = self.get_all_moves()
        move = all_moves[action]
        start=move[0]
        target=move[1]
        direction = tuple(np.subtract(target, start))
        s=target
        # Runs up to a gap and places the piece there
        while s in self.actBoard:
            if self[s] == 0:
                break
            s = tuple(np.add(s, direction))
        self[start]=curPlayer
        # Runs in opposite direction and moves the pieces
        while s in self.actBoard:
            s_prev = tuple(np.subtract(s, direction))
            s_prev_color = self[s_prev]
            self[s]= s_prev_color
            s = tuple(np.subtract(s, direction))
        self[s]=0
        # Decreases reserve
        #players[color+1].dec_reserve()

    def remove_lines(self, curPlayer):
        """Checks for each field whether a row of four results. 
        If so, removes the entire line
        """
        #prüfen ob mehrere 4er, wenn ja zuerst den der spielenden Farbe, wenn immer noch mehrere zuerst den der mehr schlägt
        rows = []
        add_reserve = [0, None, 0]
        for spot in self.actBoard:
            new_row = self.discover_row_of_4(spot)
            if new_row and new_row not in rows:
                rows.append(new_row)
        
        while len(rows)>1:
            #mehrere rows
            rows_of_color = [] #alle rows der aktuellen Farbe (haben vorrang)
            index_max = None
            for row in rows:
                row_color = self[list(row)[0]]
                if row_color == curPlayer:
                    rows_of_color.append(row)
            if len(rows_of_color)>1:
                #mehrere rows der aktiven Farbe
                #prüfen welche die meisten schlägt
                c = [None]*len(rows_of_color)
                for index, row in enumerate(rows_of_color):
                    c[index] = self.get_hit_count(row)
                index_max = np.argmax(c)
                add_reserve = np.add(add_reserve, self.remove_line(rows_of_color[index_max]), where=[1,0,1])
            elif len(rows_of_color)>0:
                #nur eine row der aktiven Farbe
                add_reserve = np.add(add_reserve, self.remove_line(rows_of_color[0]), where=[1,0,1])
            else:
                #mehrer rows der anderen Farbe und keine der aktiven
                #prüfen welche die meisten schlägt
                c = [None]*len(rows)
                for index, row in enumerate(rows):
                    c[index] = self.get_hit_count(row)
                index_max = np.argmax(c)
                add_reserve = np.add(add_reserve, self.remove_line(rows[index_max]), where=[1,0,1])
            #prüfe ob rows noch aktuell
            rows = self.check_rows(rows)
        
        if len(rows)>0:
        #nur eine row (egal welche Farbe)
            add_reserve = np.add(add_reserve, self.remove_line(rows[0]), where=[1,0,1])
        return add_reserve

    def check_rows(self, rows):
        rows_new = rows.copy()
        for row in rows:
            for spot in row:
                if self[spot] == 0:
                    rows_new.remove(row)
                    break
        return rows_new

    def get_hit_count(self, row):
        count = 0
        row = list(row)
        color_of_row = self[row[0]]
        direction = tuple(np.subtract(row[0], row[1]))
        s = row[0]
        # Runs from the first of the 4 in one direction of the line
        while s in self.actBoard:
                if self[s] == 0: 
                    break
                else:
                    color = self[s]
                    if color != color_of_row:
                        count += 1
                    #self[s] = 0
                s = tuple(np.add(s, direction))
        # Runs in the opposite direction
        s = tuple(np.subtract(row[0], direction))
        while s in self.actBoard:
                if self[s] == 0: 
                    break
                else:
                    color = self[s]
                    if color != color_of_row:
                        count += 1
                    #self[s] = 0
                s = tuple(np.subtract(s, direction))
        return count


    def discover_row_of_4(self, spot):
        """Examines all directions for the given spot to see if a row of four exists
        If found returns a array of the four, otherwise returns False
        """
        color = self[spot]
        for direction in self.__directions:
            row_of_4 = [] #set() #weil unorderd
            #row_of_4.update([spot])
            row_of_4.append(spot)
            s = tuple(np.add(spot, direction))
            while s in self.actBoard:
                if self[s] == 0 or self[s] != color:
                    break
                else:
                    #row_of_4.update([s])
                    row_of_4.append(s)
                s = tuple(np.add(s, direction))
            if len(row_of_4)>2:  #GipfMini: 3; Normal: 4
                row_of_4.sort()
                return row_of_4

    def remove_line(self, row_of_4):
        """Removes the 4 pieces and the pieces that form a direct extension of these 4 
        The pieces with the color of the 4 return to his reserve
        """
        add_reserve = [0, None, 0]
        row_of_4 = list(row_of_4)
        color_of_4 = self[row_of_4[0]]
        direction = tuple(np.subtract(row_of_4[0], row_of_4[1]))
        s = row_of_4[0]
        # Runs from the first of the 4 in one direction of the line
        while s in self.actBoard:
                if self[s] == 0: 
                    break
                else:
                    color = self[s]
                    if color == color_of_4:
                        add_reserve[color+1]+=1
                        #players[color+1].inc_reserve()
                    self[s] = 0
                s = tuple(np.add(s, direction))
        # Runs in the opposite direction
        s = tuple(np.subtract(row_of_4[0], direction))
        while s in self.actBoard:
                if self[s] == 0: 
                    break
                else:
                    color = self[s]
                    if color == color_of_4:
                        add_reserve[color+1]+=1
                        #players[color+1].inc_reserve()
                    self[s] = 0
                s = tuple(np.subtract(s, direction))
        return add_reserve

