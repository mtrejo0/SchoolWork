# NO IMPORTS!

##############
# Problem 01 #
##############

def solve_latin_square(grid):
    n = len(grid)

    # return True if there are blanks, or if each number appears exactly once
    def vals_okay(vlist):
        return vlist.count(-1) > 0 or len(set(vlist)) == n

    # return True if square is still solvable
    def check_square():
        # check for legal vals in all rows
        for row in grid:
            if not vals_okay(row):
                return False
        # check for legal vals in all columns
        for c in range(n):
            if not vals_okay([grid[r][c] for r in range(n)]):
                return False
        return True

    # search for empty square
    for r in range(n):
        for c in range(n):
            if grid[r][c] == -1:
                # compute possible choices by eliminating values
                # already appearing in same row or col
                choices = set(range(1,n+1))
                for v in grid[r]:
                    choices.discard(v)
                for v in [grid[rr][c] for rr in range(n)]:
                    choices.discard(v)

                # now try each choice
                for choice in choices:
                    grid[r][c] = choice
                    if check_square():
                        # if square with trial value is still solvable,
                        # recursively look for solution
                        result = solve_latin_square(grid)
                        # if result isn't False, we're done
                        if result != False:
                            return result

                # no valid choice produces a solution, so fail at this level
                grid[r][c] = -1
                return False

    # no empty squares, we have a solution
    return grid


##############
# Problem 02 #
##############

def is_proper(root):
    # return number of black nodes on all paths if proper, else False
    def black_count(root):
        # reached bottom of the tree descent
        if root == -1:
            return 0

        # count number of black nodes in left child
        lchild = root["left"]
        lcount = black_count(lchild)
        if lcount is False:
            return False

        # count number of black nodes in right child
        rchild = root["right"]
        rcount = black_count(rchild)
        if rcount is False:
            return False

        # we'll add 1 to the count if the current node is black
        root_contribution = 1 if root["color"] == "black" else 0

        if lchild == -1:
            # no left child, so count depends only on right child
            return root_contribution + rcount
        elif rchild == -1:
            # no right child, so count depends only on left child
            return root_contribution + lcount
        elif lcount != rcount:
            # if count from both children doesn't match, we're not proper
            return False
        else:
            # otherwise return count including the current root node
            assert lcount == rcount
            return root_contribution + lcount

    return black_count(root) is not False


##############
# Problem 03 #
##############

def lottery(prairie_dogs, capacities):
    if prairie_dogs == []:
        # Easy case: there is no one to assign!
        return []
    else:
        # Let's consider every choice for the first prairie dog.
        for burrow in prairie_dogs[0]:
            # We only consider burrows that have space left.
            if capacities[burrow] != 0:
                # Assume optimistically that we can put this one here.
                # We'd better reduce the capacity accordingly.
                capacities[burrow] -= 1

                # Let's see if we can now place the others.
                others = lottery(prairie_dogs[1:], capacities)

                if others == None:
                    # No luck.  We'd better return this burrow spot to circulation.
                    capacities[burrow] += 1
                else:
                    # Oh, good!  We found a solution for the rest, and it's easily
                    # amended to cover the first prairie dog, too.
                    return [burrow] + others

        # None of the burrows work.  It was worth a try.
        return None

# Exercise for the reader: make the above code even faster by adding an
# optimization that notices prairie dogs where only one remaining burrow has
# capacity above zero.

# You might have been tempted to write a brute-force enumeration function like
# this one, but we included a few test cases that would be too slow that way.
def slow_lottery(prairie_dogs, capacities):
    # Return all possible assignments, ignoring capacities.
    def all_combos(prairie_dogs):
        if prairie_dogs == []:
            return [[]]
        else:
            return [[burrow] + others
                    for burrow in prairie_dogs[0]
                    for others in all_combos(prairie_dogs[1:])]

    # Does an assignment obey the capacities?
    def obeys_capacities(assignment):
        caps = list(capacities)
        for burrow in assignment:
            caps[burrow] -= 1
        return all(cap >= 0 for cap in caps)

    everything = all_combos(prairie_dogs)
    obeying_capacities = [assignment
                          for assignment in everything
                          if obeys_capacities(assignment)]
    if obeying_capacities == []:
        return None
    else:
        return obeying_capacities[0]

from random import shuffle

# These functions generate inputs that should be hard to solve quickly by
# brute force.

def first_choice_is_wrong(n):
    ls1 = [[i+1, 0] for i in range(n)] + [[i+1] for i in range(n)]
    ls2 = [n] + [1 for i in range(n)]
    shuffle(ls1)
    return ls1, ls2

def first_choice_is_doomed(n):
    ls1 = [[2*i+1, 2*i] for i in range(n)] \
          + [[2*i+1, 2*n] for i in range(n)] \
          + [[2*n, 2*n+1+i] for i in range(n)] \
          + [[2*n+1+i, 2*i+1] for i in range(n)]
    ls2 = [1 for i in range(2*n)] + [n] + [1 for i in range(n)]
    shuffle(ls1)
    return ls1, ls2

# This function we used only to generate the cases.
def all_solutions(prairie_dogs, capacities):
    if prairie_dogs == []:
        return [[]]
    else:
        sols = []

        for burrow in prairie_dogs[0]:
            if capacities[burrow] != 0:
                capacities[burrow] -= 1
                sols.extend([[burrow] + rest
                             for rest in all_solutions(prairie_dogs[1:], capacities)])
                capacities[burrow] += 1

        return sols


##############
# Problem 04 #
##############

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

# Given a tree of the kind explained in the readme, modify it to add the new data value.
def insert(tree, data):
    # A familiar kind of loop descending the tree:
    while tree:
        if data < tree["data"]:
            # The position we want is to the left of here.
            if tree["left"]:
                # There's a subtree to the left?  OK, switch to descending that one.
                tree = tree["left"]
            else:
                # No subtree to the left?  Then this new node goes there.
                prev = tree["prev"]
                new_node = {"data": data, "left": None, "right": None,
                            "prev": prev, "next": tree}
                tree["left"] = new_node
                tree["prev"] = new_node
                if prev:
                    prev["next"] = new_node
                return
        else:
            # The position we want is to the right of here.
            if tree["right"]:
                # There's a subtree to the right?  OK, switch to descending that one.
                tree = tree["right"]
            else:
                # No subtree to the right?  Then this new node goes there.
                next = tree["next"]
                new_node = {"data": data, "left": None, "right": None,
                            "prev": tree, "next": next}
                tree["right"] = new_node
                tree["next"] = new_node
                if next:
                    next["prev"] = new_node
                return

    assert False


##############
# Problem 05 #
##############

def solve_magicsquare_recursive(grid, magic_sum, choices):
    # return True if square is still solvable
    def check_square():
        # check rows
        for row in grid:
            # if there are no blanks and sum doesn't match, fail
            if row.count(-1)==0 and sum(row)!=magic_sum:
                return False

        # check cols
        for c in range(len(grid[0])):
            # build list of column values
            col = [grid[r][c] for r in range(len(grid))]
            # if there are no blanks and sum doesn't match, fail
            if col.count(-1)==0 and sum(col)!=magic_sum:
                return False

        # check main diag by building list of values
        diag = [grid[r][r] for r in range(len(grid))]
        # if there are no blanks and sum doesn't match, fail
        if diag.count(-1)==0 and sum(diag)!=magic_sum:
            return False

        # check other diag
        diag = [grid[r][len(grid) - 1 - r] for r in range(len(grid))]
        # if there are no blanks and sum doesn't match, fail
        if diag.count(-1)==0 and sum(diag)!=magic_sum:
            return False

        # all checks passed
        return True

    # search for first empty square
    for r,row in enumerate(grid):
        for c,col in enumerate(row):
            if col == -1:
                # try all the choices for this empty square
                for choice in choices:
                    grid[r][c] = choice
                    # check if square is still solvable after inserting guess
                    if check_square():
                        # recusively solve updated puzzle
                        result = solve_magicsquare_recursive(grid,magic_sum,choices)
                        # if answer isn't False, we have a solution
                        if result != False:
                            return result
                # no choice worked, so restore grid and indicate failure
                grid[r][c] = -1
                return False

    # no empty squares, return filled in grid
    return grid


##############
# Problem 06 #
##############

def alternating_colors(graph, start):
    coloring = {}

    # color or check a node, propagate to neighbors
    # return True if coloring okay, False otherwise
    def color_node(node, color):
        # if node has been colored, check for consistency
        if node in coloring:
            return coloring[node] == color
        # color the node
        coloring[node] = color
        # color/check neighbors
        other_color = 'Blue' if color == 'Red' else 'Red'
        for neighbor in graph[node]:
            if not color_node(neighbor,other_color):
                return False
        return True

    return coloring if color_node(start,'Red') else {}


##############
# Problem 07 #
##############

def check_BST(btree, start):
    # check that BST values fall in range (minv,maxv).
    # one or both bounds may be None
    def check(vertex, minv, maxv):
        value,left,right = vertex
        # check vertex value against the specified bounds
        if minv and value <= minv: return False
        if maxv and value >= maxv: return False
        # verify left child obeys updated constraints
        if left != '' and not check(btree[left],minv,value):
            return False
        # verify right child obeys updated constraints
        if right != '' and not check(btree[right],value,maxv):
            return False
        return True

    return check(btree[start],None,None)


##############
# Problem 08 #
##############

def pipe_cutting(requests,stock_length):
    # lower-bound pruning needed when many short requests
    # need at least ceil(sum(requests)//stock_length) pipes
    # lower_bound = (sum(requests) + (stock_length-1)) // stock_length

    # satisfy remaining requests, perhaps using
    # left-over pipe lengths listed in pipes.
    # returns number of pipes required
    def pc_helper(requests,pipes):
        # no more requests?  We're done!
        if len(requests) == 0: return len(pipes)

        # have at least one more request to fill
        request,rest = requests[0],requests[1:]
        smallest = None

        # try using each left-over piece
        for i,p in enumerate(pipes):
            if request <= p:
                # we can cut from this pipe
                pipes[i] -= request
                # satisfy remaining requests
                result = pc_helper(rest,pipes)
                # did we find a better solution?
                if smallest is None or result < smallest:
                    smallest = result
                    # stop here if we've already achieved lower bound
                    # if smallest == lower_bound: return smallest
                # restore cut for next experiment
                pipes[i] += request

        # finally try buying a new pipe
        result = pc_helper(rest,pipes + [stock_length - request])
        if smallest is None or result < smallest:
            smallest = result

        return smallest

    return pc_helper(requests,[])


##############
# Problem 09 #
##############

def cherrypick(A, n, required_sum):

    def cherrypick_helper(needed_sum, choose_count, available_elements):
        if (needed_sum == 0 and choose_count == 0): return True
        if (needed_sum < 0 or choose_count == 0): return False
        for element_to_add in available_elements:
            available_elements_new = available_elements[:]
            available_elements_new.remove(element_to_add)
            solution = cherrypick_helper(needed_sum - element_to_add, choose_count-1, available_elements_new)
            if solution: return True
        return False

    return cherrypick_helper(required_sum, n, A)


##############
# Problem 10 #
##############

def eval_ast(ast):

    def ea_helper(node):
        node_value = node["node"]
        
        if node_value == "*" or node_value == "+":
            evalLeft = ea_helper(node["left"])
            evalRight = ea_helper(node["right"])
            if node_value == "*":
                return evalLeft * evalRight
            elif node_value == "+":
                return evalLeft + evalRight
            else:
                print("Code should not reach here")
        else:
            # Base case
            return node_value

    return ea_helper(ast)


##############
# Problem 11 #
##############

def true_for_all(tree):
    def tfa_helper(tree): # returns a tuple -- as (Boolean, all_values_in_tree)
        
        # Base case
        if type(tree) == int:
            return (True, [tree])
        
        else:
            comparison = tree[0]
            tree_left = tree[1]
            tree_right = tree[2]
            (left_success, left_values) = tfa_helper(tree_left)
            (right_success, right_values) = tfa_helper(tree_right)
            
            if not left_success or not right_success:
                return (False, left_values + right_values)
            # Now check the current comparison
            
            if comparison == ">":
                bigger_side = left_values
                smaller_side = right_values
            else:
                bigger_side = right_values
                smaller_side = left_values
            
            if (min(bigger_side) > max(smaller_side)):
                return (True, left_values + right_values)
            else:
                return (False, left_values + right_values)

    return tfa_helper(tree)[0]


##############
# Problem 12 #
##############

def assign_cities(L, N):

    def ac_helper(current_assignment, unassigned_options, assigned_cities):
        
        # base case
        if (len(unassigned_options) == 0):
            return current_assignment

        city_option_assigments = unassigned_options[0]
        for city_option in city_option_assigments:
            if city_option not in assigned_cities:
                new_current_assignment = current_assignment[:]
                new_assigned_cities = assigned_cities.copy()
                new_current_assignment.append(city_option)
                new_assigned_cities.add(city_option)
                assignment = ac_helper(new_current_assignment, unassigned_options[1:], new_assigned_cities)
                if assignment is not None:
                    return assignment
        
        return None # No solution

    # in this solution we don't need to know how many total cities because the len(L) == N
    return ac_helper([], L, set())


##############
# Problem 13 #
##############

def flood_fill(image, location_clicked, new_color):
    height = image["height"]
    width = image["width"]

    # Copy pixels because we don't want to change the original image
    pixels = image["pixels"].copy()
    start_color = pixels[location_clicked[0] * width + location_clicked[1]]
    processed = set()
    queue = [location_clicked]

    # Possible flood_fill directions
    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    # BFS Search
    while(len(queue) > 0):
        (row, col) = queue.pop(0)
        
        # Out of bounds value
        if row < 0 or row >= height or col < 0 or col >= width: continue
        
        # We have already checked out this grid so no need to BFS it again
        if (row,col) in processed: continue

        index = row * width + col
        processed.add((row,col))
        
        # only change the cell color and iterate if the adjacent cell has the same color
        # as the one we are trying to change
        if pixels[index] == start_color:
            pixels[index] = new_color
            for (xmod, ymod) in directions:
                queue.append((row + xmod, col + ymod))

    return {'height': height, 'width': width, 'pixels': pixels}


if __name__ == "__main__":
    pass
