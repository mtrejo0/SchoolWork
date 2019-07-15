# 6.009 Spring 2019 Quiz 2

##################################################
##  Problem 1
##################################################

# Resubmission:

# My previous attempt at this problem was my last minute attempt 
# to get some points but it never took into account the alternating
# color of the tree it checked that the level and the leve below all
# had the same color then continued to check the same thing for 2 levels below
# This is wrong because it never gaurantees that two adjacent double rows
# should have two different colors. I tried to add a simple way to flip flop
# bweteen two state colors that worked for all but test case 6. I decided that a 
# new approach is better where you get the lineage of every possible path to a leaf
# and if the pattern is aabbaa for every path then the tree is correct, this is
# a simpler more elegant solution than the one I had because I dont have to write
# out every relationship bweteen a node and its children that it may or may not have
# I just recurse in a direction if the node has children and once i get to a leaf 
# I check that the pattern is okay




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
def correctLineage(lin):
    if(len(lin)<2):
        # default this will always be true
        return True 

    # remember first value 
    curr = lin[0]
    i = 0

    while(i<len(lin)):

        if(i == len(lin) - 1 and lin[i] == curr):
            # if we are at the end of the list and the value
            # has correct value then its a correct lineage
            return True 

        if(lin[i] == curr and lin[i+1] == curr):
            # if consecutive values have the same value then 
            # this part of the tree is valid

            # flip the value
            if(curr == "black"):
                curr = "blue"
            else:
                curr = "black"
            # skip ahead 2
            i+=2
        else:
            return False
    return True

def validate(root,lin=None):
    # sets up empty list to remember chain of nodes in tree
    if(not lin):
        lin = []
    # remembers current color
    lin+=[root.color]

    

    if(root.left):
        # recurse in the left direction if left node exists
        if(not validate(root.left,lin[:])):
            # if we ever see that its invalid return immediately
            return False

    if(root.right):
        # recurse in the left direction if left node exists
        if(not validate(root.right,lin[:])):
            # if we ever see that its invalid return immediately
            return False

    if(root.left == None and root.right == None):
        # if we get to a leaf node check that the lineage we
        # have seen matres the aaabbaa pattern
        return  correctLineage(lin)

    return True




##################################################
##  Problem 2
##################################################

# Resubmission:

# In my past implementation of n_bishops I made a 2D list
# to represent my positioning of bishops when I never had to 
# remember all that information. All I needed to store was the
# locations of the bishops with that information I can see
# if there are any conflics and if we have enough bishops to 
# answer the problem. In my previous attempt I would recreate 
# the locations of my bishops by re calculating them. After I
# realized this I cut down everything I didnt need and
# remembered lists to add and remove whenever I made a step 
# these updates happened a lot faster than updating a whole 2D
# matrix and that is why this approach is better



def n_bishops(n, bishop_locs, target):
    """
    Finds the placement of target amount of bishops such that
    no two bishops can attack each other.
    :param n: the length of a side of the board
    :param bishop_locs: the locations of the bishops already on the board
    :param target: the number of bishops to add
    """



    # creates list of empty swuares on the board
    empty = []
    for i in range(n):
        for j in range(n):
            if((i,j) not in bishop_locs):
                empty+=[(i,j)]


    return helper(bishop_locs,target,empty)

def helper(locs,target,empty):
    
    # check to see if we are done and can return
    if(final(locs,target)):
        return locs
    
    for i in empty:
        # add bishop to empty square and update lists
        locs.add(i)
        empty.remove(i)

        # if we can place a bishop there recurse in that direction
        if(valid(locs)):
            result = helper(locs,target,empty)
            if(result):
                # if we get an answer return it
                return locs
        # update lists because the bishop we added wasnt a winner
        locs.remove(i)
        empty.append(i)

def final(locs,target):
    # checks if board is valid and we have enough bishops
    if(valid(locs) and len(locs) >= target):
        return True
    return False

def valid(locs):
    # checks if no two bishops attack each other
    for i in locs:
        for j in locs:
            if(i!=j):
                if(abs(j[0]-i[0]) == abs(j[1]-i[1])):
                    return False
    return True

##################################################
##  Problem 3
##################################################

# Resubmission

# In my previous attempt for this problem I understood 
# the limitations for when you need to add into a tree or 
# its children but messed up the value ranges because I 
# didnt realize how to get the midpoint of 2 numbers
# After realizing this I realized I have to add the points from the 
# node that was broken up and the incoming point this can be done by 
# inserting to the current node because the recursive call will check
# which of the children to insert the node into and also to 
# reset the nodes so that only leaf nodes have children

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
        print(self)


        if(self.children):
            # if we tried to insert into something that isnt a 
            # leaf node we check the children witht he valid
            # ranges and insert into that child
            for each in self.children:
                if(point[0]>=each.x_start and point[0]<each.x_end and
                 point[1]>=each.y_start and point[1]<each.y_end):
                    each.insert(point)

        else:
            # if we still have space in the child add to points
            if(len(self.points)<4): self.points.add(point)

            else:
                # we have to split this node into 4 new nodes

                # line separators for x and y
                diffX = (self.x_end + self.x_start)//2
                diffY = (self.y_end + self.y_start)//2

                self.children = []

                # the 4 new children with their ranges
                self.children+=[QuadTree(self.x_start,self.y_start,diffX,diffY)]
                self.children+=[QuadTree(diffX,diffY,self.x_end,self.y_end)]

                self.children+=[QuadTree(self.x_start,diffY,diffX,self.y_end)]
                self.children+=[QuadTree(diffX,self.y_start,self.x_end,diffY)]


                # for each of the current points insert them into
                # current node so that it automatically finds the new child
                # to put that point into it
                for each in self.points:
                    self.insert(each)

                # insert the main point
                self.insert(point)

                # current node isnt a leaf anymore so it shouldnt
                # have points anymore
                self.points = None

if __name__ == '__main__':
    pass
