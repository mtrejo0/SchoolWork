# NO IMPORTS!

####################
## Problem 01 
####################


def solve_latin_square(grid):
    if(correct(grid)):
        return grid
    vals = set(range(1,len(grid)+1))
    poss = {}
    for i in range(len(grid)):
        for j in range(len(grid)):
            if(grid[i][j] == -1):
                row = getRow(i,grid)
                col = getCol(j,grid)
                row = vals.difference(row)
                col = vals.difference(col)
                poss[(i,j)] = [row,col]
    # print(poss)
    # for i in grid:
    #     print(i)
    # input()
    if(correct(grid)):
        return grid
    for i in poss:
        for j in poss[i]:
            val = j.pop()
            cop = grid[:]
            cop[i[0]][i[1]] = val
            a = solve_latin_square(cop)
            if(a):
                return a
    if(correct(grid)):
        return grid
    return False




def getRow(r, grid):
    ans = set()
    for i in range(len(grid)):
        if grid[r][i] != -1:
            ans.add(grid[r][i])
    return ans
def getCol(c, grid):
    ans = set()
    for i in range(len(grid)):
        if grid[i][c] != -1:
            ans.add(grid[i][c])
    return ans



def correct(grid):
    # print(grid)
    for i in grid:
        if(set(i) == set(range(1,len(grid)+1))):
            continue
        else:
            return False
    for i in range(len(grid)):
        part = []
        for j in range(len(grid)):
            part+=[grid[j][i]]
        if(set(part) == set(range(1,len(grid)+1))):
            continue
        else:
            return False
    return True
grid = [
            [-1 , 1, -1],
            [-1, -1,  2],
            [-1, -1, -1]
        ]
print(solve_latin_square(grid))



####################
## Problem 02 
####################

def is_proper(root):
    # if(root["left"] == -1 and root["right"] == -1):
    #     return True
    ans = explore(root)[0]
    return ans


def explore(root):
    # print(root)
    r = 0
    l = 0
    if(root["left"] == -1 and root["right"] == -1):
        if(root["color"] == "black"):
            return (True,1)
        else:
            return (True,0)

    r = explore(root["left"])
    l = explore(root["right"])

    return (r == l,r[1]+l[1])



####################################################
## Problem 03. Prairie Dog Housing Lottery
####################################################

def lottery(prairie_dogs, capacities):
    raise NotImplementedError


####################################################
## Problem 04. Advanced Forestry
####################################################

def one_node_tree(data):
    return {"data": data, "left": None, "right": None, "prev": None, "next": None}

def print_tree(tree):
    def tweak_indent(indent):
        if indent == "":
            return "|_"
        else:
            return "  " + indent

    def print_tree_indented(prefix, tree, indent):
        if tree == None:
            return

        print(indent + prefix + " " + str(tree["data"]))
        if tree["prev"]:
            print(indent + "Prev: " + str(tree["prev"]["data"]))
        if tree["next"]:
            print(indent + "Next: " + str(tree["next"]["data"]))

        print_tree_indented("Left:", tree["left"], tweak_indent(indent))
        print_tree_indented("Right:", tree["right"], tweak_indent(indent))

    print_tree_indented("Root:", tree, "")

def insert(tree, data):
    raise NotImplementedError


####################
## Problem 05 
####################

def solve_magicsquare_recursive(grid, magic_sum, choices):
    raise NotImplementedError


####################
## Problem 06 
####################

def alternating_colors(graph, start):
    raise NotImplementedError


####################
## Problem 07 
####################

def check_BST(btree, start):
    raise NotImplementedError


####################
## Problem 08 
####################

def pipe_cutting(requests,stock_length):
    raise NotImplementedError


####################
## Problem 09
####################

def cherrypick(A, n, required_sum):
    raise NotImplementedError


####################
## Problem 10
####################

def eval_ast(ast):
    raise NotImplementedError

####################
## Problem 11
####################

def true_for_all(tree):
    raise NotImplementedError

####################
## Problem 12
####################

def assign_cities(L, N):
    raise NotImplementedError

####################
## Problem 13
####################

def flood_fill(image, location_clicked, new_color):
    raise NotImplementedError


if __name__ == "__main__":
    pass
