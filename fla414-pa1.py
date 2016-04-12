"""
    File name: fla414-pa1.py
    Author: Fei Luo
    NetId: fla414
    Date created: 3/31/2016
    Date last modified: 4/8/2016
    Python Version: 2.7.10
    Description:
        This file is for the 1st assignment of course EECS-348: Intro to Artificial Intelligence @ Northwestern.
        It includes 5 major functions and 1 class as follows:
          - binarySearch()
          - mean()
          - median()
          - dfs()
          - bfs()
          - class TTTBoard
"""

def binarySearch(L,v):
    """
    This function performs binary search in the list L.
    Args:
        @param1 L: The list to be searched
        @param2 v: Target value to be searched
    Returns:
        @(t,n)
        @t: boolean value corresponding to whether v is in L
        @n: the number of iterations
    """
    if not L:
        return (False, 0)
    l = len(L)
    i, left, right = 0, 0, l - 1
    while left <= right:
        mid = left + (right - left) / 2
        # target value found
        if L[mid] == v:
            return (True, i)
        elif L[mid] > v:
            right = mid - 1
        else:
            left = mid + 1
        # increase iterations by 1
        i += 1
    # the value is not in the list
    return (False, i)

def mean(L):
    """
    This function calculates the arithmetic average of the list L.
    Args:
        @param L: target list
    Returns:
        arithmetic average of the numbers in the list L.
        0 if the list is empty.
    """
    if not L:
        return 0
    # sum of the list divided by the length of it
    return sum(L) * 1.0 / len(L)

def median(L):
    """
    This function calculates the median value of the list L.
    Args:
        @param L: target list
    Returns:
        median value of the numbers in the list L.
        0 if the list is empty.
    """
    if not L:
        return 0
    l = len(L)
    # sort the list in ascending order
    L.sort()
    # returns the central item in the sorted list if the length of the list is odd number.
    # Otherwise, returns the average of two central items in the sorted list.
    return L[l / 2] if l & 1 else (L[l / 2] + L[l / 2 - 1]) * 1.0 / 2

def dfs(tree, elem):
    """
    This function performs depth first search on a tree which is represented by a list.
    Args:
        @param tree: the tree to be searched on
        @param elem: the target element
    Returns:
        true if the element is in the tree
        false if the element is not in the tree
    """
    # base case: current tree is empty
    if not tree:
        return False
    # base case: current node is the target element
    if tree[0] == elem:
        print tree[0]
        return True
    print tree[0]
    # recursively search on the subtrees
    for subtree in tree[1:]:
        if dfs(subtree, elem):
            return True
    # search is finished, target not found
    return False

def bfs(tree, elem):
    """
    This function performs breadth first search on a tree which is represented by a list.
    Args:
        @param tree: the tree to be searched on
        @param elem: the target element
    Returns:
        true if the element is in the tree
        false if the element is not in the tree
    """
    if not tree:
        return False
    queue = []
    # initialize the queue
    queue.append(tree)
    while queue:
        # pop the current subtree out of the queue
        current = queue.pop(0)
        if current:
            print current[0]
            # root node of current subtree is the target element
            if current[0] == elem:
                return True
            # add the children to the queue
            for child in current[1: len(current)]:
                if child:
                    queue.append(child)
    # queue is empty, target not found
    return False
class TTTBoard:
    def __init__(self):
        """initializes the game board with a list filled by 9 '*' characters """
        self.board = ['*'] * 9

    def __str__(self):
        """returns string representation of the current board state"""
        res = ''
        for i in range(3):
            # split the list into 3 slices
            res += ' '.join(self.board[3 * i: 3 * i + 3]) + '\n'
        return res

    def makeMove(self, player, pos):
        """places a move for player in postion pos and return true if the move is made"""
        if 0 <= pos < 9 and self.board[pos] == '*':
            #The postion is valid and empty.
            self.board[pos] = player
            return True
        return False

    def hasWon(self, player):
        """returns true if the player has won the game"""
        #map the player on the board to true and others to false
        mapper = map(lambda x: True if x == player else False, self.board)
        #three in a row or a column
        for i in range(3):
            if all(mapper[3 * i: 3 * i + 3]):
                return True
            if mapper[i] and mapper[i + 3] and mapper[i + 6]:
                return True
        #three in a diagonal
        if mapper[4] and ((mapper[0] and mapper[8]) or (mapper[2] and mapper[6])):
            return True
        return False

    def gameOver(self):
        """returns true if the game is over(one of the player has won or the board is full)"""
        if self.hasWon('X') or self.hasWon('O'):
            return True
        return self.isFull()

    def isFull(self):
        """returns true if the game board is full"""
        mapper = map(lambda x: False if x == '*' else True, self.board)
        return all(mapper)

    def clear(self):
        """resets the game"""
        self.board = ['*'] * 9
