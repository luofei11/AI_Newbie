#!/usr/bin/env python
"""
Group members:
    -Fei Luo netid: fla414
    -Ye Xue  netid: yxe836

Group work statement: All group members were present and contributing during all work on this project.
"""
import struct, string, math, copy, time
num_of_assignments = 0
num_of_con_check = 0
class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board, domain=None):
      """the constructor for the SudokuBoard"""
      self.BoardSize = size #the size of the board
      self.CurrentGameBoard= board #the current state of the game board
      self.subsquare = int(math.sqrt(size))
      if domain != None:
          self.Domain = domain
      else:
          self.Domain = [[[] for i in range(size)] for j in range(size)]
          for i in range(size):
              for j in range(size):
                  if self.CurrentGameBoard[i][j] == 0:
                      self.Domain[i][j] = cal_domain(self, i, j)
    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board

def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j]
                            == BoardArray[row][col])
                        and (SquareRow*subsquare + i != row)
                        and (SquareCol*subsquare + j != col)):
                            return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, Degree = False,
    LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    #print "Your code will solve the initial_board here!"
    #print "Remember to return the final board (the SudokuBoard object)."
    #print "I'm simply returning initial_board for demonstration purposes."

    #global variables to record the results
    global num_of_assignments
    global num_of_con_check
    num_of_assignments = 0
    num_of_con_check = 0
    start = time.clock()
    final_board, solvable = back_track(initial_board, forward_checking, MRV, Degree, LCV)
    end = time.clock()
    #print "Time  ", end - start
    #print "Consistency checks: ", num_of_con_check
    #print "variable assignment: ", num_of_assignments
    return final_board

def back_track(board, forward_checking, MRV, Degree, LCV):
    #base case
    if is_complete(board):
        return board, True
    #Choose next variable by MRV and Degree heuristics
    next_row, next_col = choose_next_pos(board, MRV, Degree)
    #Couldn't assign a variable
    if next_row == -1:
        return board, True
    #Choose next value by LCV heuristic
    for val in legal_values(board, next_row, next_col, LCV):
        global num_of_con_check
        num_of_con_check += 1
        #Current position and val are consistent with the board
        if is_consistent(board, next_row, next_col, val):
            nb = copy.deepcopy(board)
            nb.set_value(next_row, next_col, val)

            global num_of_assignments
            num_of_assignments += 1
            #do forward checking
            if forward_checking:
                do_forward_check(nb, next_row, next_col, val)
            #recursively call back_track
            final_board, solvable = back_track(nb, forward_checking, MRV, Degree, LCV)
            if solvable:
                return final_board, True
    return board, False
def is_consistent(board, row, col, val):
    """Checks the consistency of a move"""
    #Check consistency of the same row/col
    for i in range(board.BoardSize):
        if ((board.CurrentGameBoard[row][i] == val) and i != col):
            return False
        if ((board.CurrentGameBoard[i][col] == val) and i != row):
            return False
    #Check consistency of the same subsquare
    subsquare = board.subsquare
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
        for j in range(subsquare):
            if((board.CurrentGameBoard[SquareRow*subsquare+i][SquareCol*subsquare+j]
                    == val)
                and (SquareRow*subsquare + i != row)
                and (SquareCol*subsquare + j != col)):
                    return False
    return True
def choose_next_pos(board, MRV, Degree):
    #TODO
    """Choose the next unassigned variable by MRV and Degree heuristics"""
    board_array = board.CurrentGameBoard
    size = len(board_array)
    prev, minimum_remain = 10, 10
    row, col = -1, -1
    if not MRV and not Degree:
        for row in range(size):
            for col in range(size):
                #Choose the first unassigned variable
                if board_array[row][col] == 0:
                    return row, col
    elif MRV:
        for i in range(size):
            for j in range(size):
                if board_array[i][j] == 0:
                    #Choose variable with minimum remaining values
                    if len(legal_values(board, i, j, False)) < minimum_remain:
                        row, col = i, j
                        prev = minimum_remain
                        minimum_remain = len(legal_values(board, i, j, False))
    #tied on MRV. Use Degree heuristic
    if minimum_remain == prev and Degree:
        max_degree = -1
        for i in range(size):
            for j in range(size):
                if board_array[i][j] == 0:
                    #Choose the variable with the largest degree
                    if cal_degree(board, i, j) > max_degree:
                        row, col, max_degree = i, j, cal_degree(board, i, j)
    return row, col

def legal_values(board, row, col, LCV):
    """Returns the possible values of a postion by LCV heuristic"""
    if LCV:
        order_values(board, row, col)
    return board.Domain[row][col]

def cal_domain(board, row, col):
    """Calculate the domain of the position at (row, col)"""
    board_array = board.CurrentGameBoard
    size = len(board_array)

    initial_domain = [i + 1 for i in range(size)]
    temp = copy.deepcopy(initial_domain)
    for i in range(size):
      if board_array[row][i] in temp:
        temp.remove(board_array[row][i])
      if board_array[i][col] in temp:
        temp.remove(board_array[i][col])

    subsquare = board.subsquare
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
      for j in range(subsquare):
        if board_array[SquareRow*subsquare+i][SquareCol*subsquare+j] in temp:
          temp.remove(board_array[SquareRow*subsquare+i][SquareCol*subsquare+j])
    return temp
def cal_degree(board, row, col):
  """ Calculate the degree of the specific position using the number of spaces of its neighbor."""
  BoardArray = board.CurrentGameBoard
  size = len(BoardArray)
  count = 0
  for i in range(size):
    if BoardArray[row][i] == 0 and col != i:
      count += 1
    if BoardArray[i][col] == 0 and row != i:
      count += 1

  subsquare = board.subsquare
  SquareRow = row // subsquare
  SquareCol = col // subsquare
  for i in range(subsquare):
    for j in range(subsquare):
      if ((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == 0)
          and (SquareRow*subsquare+i != row)
          and (SquareCol*subsquare+j != col)):
          count += 1
  return count
def do_forward_check(board, row, col, val):
    """Performs the forward_checking by removing the inconsistent values of neighbors caused by a move"""
    board_array = board.CurrentGameBoard
    size = len(board_array)
    domain = board.Domain
    for i in range(size):
      if val in domain[row][i]:
        domain[row][i].remove(val)
      if val in domain[i][col]:
        domain[i][col].remove(val)

    subsquare = board.subsquare
    SquareRow = row // subsquare
    SquareCol = col // subsquare
    for i in range(subsquare):
      for j in range(subsquare):
        if val in domain[SquareRow*subsquare+i][SquareCol*subsquare+j]:
          domain[SquareRow*subsquare+i][SquareCol*subsquare+j].remove(val)

def order_values(board, row, col):
    """Order the domain at a position by LCV heuristic"""
    domain = board.Domain
    if len(domain[row][col]) == 0:
        return
    temp = []
    for v in domain[row][col]:
        count = 0
        for i in range(board.BoardSize):
            if((v in domain[row][i]) and i != col):
                count += 1
            if((v in domain[i][col]) and i != row):
                count += 1

        subsquare = board.subsquare
        SquareRow = row // subsquare
        SquareCol = col // subsquare
        for i in range(subsquare):
            for j in range(subsquare):
                if((v in domain[SquareRow*subsquare+i][SquareCol*subsquare+j])
                    and (SquareRow*subsquare + i != row)
                    and (SquareCol*subsquare + j != col)):
                    count += 1
        temp.append((v, count))
    temp.sort(key = lambda x: x[1])
    values = []
    for v, c in temp:
        values.append(v)
    board.Domain[row][col] = values
