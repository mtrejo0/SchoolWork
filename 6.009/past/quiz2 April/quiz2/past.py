# 6.009 Spring 2019 Quiz 2

##################################################
##  Problem 1
##################################################

class Tree(object):
    """
    Tree object where each tree node has a color and can have left/right
    children, which are also trees

    DO NOT edit this class.
    """
    def __init__(self, color, left = None, right = None):
        self.color = color
        self.left = left
        self.right = right

def validate(root, color = None):
    """
    Determines whether the given tree is a valid black-blue tree
    :param root: the root of the tree
    """

    if(color == None):
        color = root.color
    opp = 0
    if(color == "blue"):
        opp = "black"
    else:
        opp = "blue"
    # print(color,opp)
    # print("curr",root.color)
    # print(root.color,color,opp)
    if(root.left == None and root.right == None):
        return True

    if(root.left):
        # print("left",root.left.color)
        if(root.left.color == color):
            pass
        else:
            return False
    if(root.right):
        # print("right",root.right.color)
        if(root.right.color == color):
            pass
        else:
            return False
    if(root.right):
        if(root.right.right):
            if(validate(root.right.right,opp)):
                pass
            else:
                return False
        if(root.right.left):
            if(validate(root.right.left,opp)):
                pass
            else:
                return False
    if(root.left):
        if(root.left.right):
            if(validate(root.left.right,opp)):
                pass
            else:
                return False
        if(root.left.left):
            if(validate(root.left.left,opp)):
                pass
            else:
                return False

    return True


##################################################
##  Problem 2
##################################################

def n_bishops(n, bishop_locs, target):
    """
    Finds the placement of target amount of bishops such that
    no two bishops can attack each other.
    :param n: the length of a side of the board
    :param bishop_locs: the locations of the bishops already on the board
    :param target: the number of bishops to add
    """
    board = []
    for i in range(n):
        arr = []
        for j in range(n):
            arr+=[0]
        board +=[arr]
    for i in bishop_locs:
        r,c = i
        board[r][c] = 1
    ans = helper(board,target)
    if(ans == None):
        return None
    for i in range(n):
        for j in range(n):
            if(ans[i][j] == 1 and (i,j) not in bishop_locs):
                bishop_locs.add((i,j))
    return bishop_locs

def helper(board,target):
    
    if(final(board,target)):
        return board

    pos = empty(board)
    for i in pos:
        board[i[0]][i[1]] = 1
        if(correct(board)):
            if(final(board,target)):
                return board
            result = helper(board,target)
            if(result):
                return board
        board[i[0]][i[1]] = 0
    if(final(board,target)):
        return board

def count(board):
    count = 0
    for i in board:
        for j in i:
            if(j == 1):
                count+=1
    return count

def empty(board):
    spaces = []
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != 1:
                spaces+=[(i,j)]
    return spaces

def final(board,target):
    locations = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                locations.add((i,j))
    for i in locations:
        for j in locations:
            if(i!=j):
                if(abs(j[0]-i[0]) == abs(j[1]-i[1])):
                    return False
    
    if(count(board) >= target):
        return True
    return False

def correct(board):
    locations = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                locations.add((i,j))
    for i in locations:
        for j in locations:
            if(i!=j):
                if(abs(j[0]-i[0]) == abs(j[1]-i[1])):
                    return False
    return True


##################################################
##  Problem 3
##################################################

class QuadTree():
    """
    Contains points that range between x values [x_start, x_end) 
    and y values [y_start, y_end).

    If the QuadTree is a leaf node, self.children should be None and 
    self.points should contain a set of at most four points.
    If the QuadTree is an internal (non-leaf) node, self.points should be None and 
    self.children should contain a list of four QuadTree nodes.

    The QuadTree should not have children with ranges that overlap.
    """
    def __init__(self, x_start, y_start, x_end, y_end):
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        self.points = set()
        self.children = None

    def __str__(self, level=0):
        """
        Returns a string representation of the quadtree
        :param level: current level in the quadtree (level = 0 if node is the root)
        """
        ret = "\t"*level+"start:("+str(self.x_start)+", "+str(self.y_start)+\
                "), end:("+str(self.x_end)+", "+str(self.y_end)+")\n"
        if self.children is not None:
            for child in self.children:
                ret += child.__str__(level+1)
        else:  
            if len(self.points) == 0:
                ret += "\t"*(level+1)+"<No points>\n"
            for (x, y) in self.points:
                ret += "\t"*(level+1)+"("+str(x)+", "+str(y)+")\n"
        return ret

    def insert(self, point):
        """
        Insert a point into this quadtree by modifying the tree 
        directly, without returning anything.
        :param point: a tuple of 2 integers (x, y)
        """
        if(len(self.points)<4):
            if(point[0]>=self.x_start and point[0]<=self.x_end and point[1]>=self.y_start and point[0]<=self.y_end):
                self.points.add(point)
        elif(self.children == None):
            self.children = []
            self.children+=[QuadTree(x_start,y_start,x_end//2,y_end//2)]
            self.children+=[QuadTree(x_end//2,y_end//2,x_end,y_end)]
            self.children+=[QuadTree(x_end//2,y_start,x_end,y_end//2)]
            self.children+=[QuadTree(x_start,y_end//2,x_end//2,y_end)]



if __name__ == '__main__':
    pass
