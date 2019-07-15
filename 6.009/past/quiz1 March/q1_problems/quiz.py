# NO IMPORTS!

# SPRING 2019 Quiz 1 Practice Problems

##############
# Problem 01 #
##############

def is_permutation(a,b):
    dictA = {}
    dictB = {}
    for i in a:
        if(i not in dictA):
            dictA[i] = 1
        else:
            dictA[i] +=1
    for i in b:
        if(i not in dictB):
            dictB[i] = 1
        else:
            dictB[i] +=1
    for i in dictA:

        if(i in dictA and i in dictB and dictA[i] == dictB[i]):
            continue
        else:
            return False
    return True


##############
# Problem 02 #
##############

def is_unique(A):
    """ Return True iff no repeated element in list A. """
    return len(set(A)) == len(A)


##############
# Problem 03 #
##############

def median(A):
    """ Given a list of numbers, return the median. """
    A.sort()
    i = 0 
    j = len(A)-1
    while(i < j):
        i+=1
        j-=1
    # print(A[i])
    if(i == j):
        return A[i]
    else:
        return .5*(A[i]+A[j])
    


##############
# Problem 04 #
##############

def mode(A):
    """ Return the most common value in list A. """
    dictA = {}
    for i in A:
        if(i not in dictA):
            dictA[i] = 1
        else:
            dictA[i] +=1
    max = 0
    for i in dictA:
        if(max < dictA[i]):
            max = dictA[i]
    pool = []
    for i in dictA:
        if(dictA[i] == max):
            pool+=[i]
    for i in A:
        if(i in pool):
            return i
##############
# Problem 05 #
##############

def find_triple(A):
    """ If the list ilist contains three values x, y, and z such that x + y = z
        return a tuple with x and y. Otherwise return None. """
    dictA = {}
    for i in A:
        if(i not in dictA):
            dictA[i] = 1
        else:
            dictA[i] +=1
    # print(dictA)
    for i in dictA:
        for j in dictA:
            if(i == j):
                if(dictA[i] >1 and i+i in dictA):
                    return (i,i)
            elif(i+j in dictA):
                return (i,j)

    
    return None

##############
# Problem 06 #
##############

def is_quasidrome(s):
    """ Check whether s is a quasidrome. """
    for i in range(len(s)):
        if(isPal(s[:i]+s[i+1:])):
            return True
    return False


def isPal(s):
    if(len(s)<2):
        return True
    elif(s[0] != s[-1]):
        return False
    else:
        return isPal(s[1:-1])

##############
# Problem 07 #
##############

def max_subsequence(ilist, is_circular = False):
    """ Return the start and end indices as a tuple of the maximum subsequence
        in the list.  If is_circular = True, imagine the list is circular.
        That is, after the end index comes the start index. """
    max = ilist[0]
    indices = (0,0)
    if(not is_circular):
        for i in range(len(ilist)):
            
            j = i
            while(j>=0):
                if(max<sum(ilist[j:i+1])):
                    max = sum(ilist[j:i+1])
                    indices = (j,i)
                j-=1
        return indices
    return []


##############
# Problem 08 #
##############

def count_triangles(edges):
    """ Count the number of triangles in edges. """
    print(edges)
    d = {}
    for i in edges:
        if(i[0] not in d):
            d[i[0]] = [i[1]]
        else:
            d[i[0]]+=[i[1]]
        if(i[1] not in d):
            d[i[1]] = [i[0]]
        else:
            d[i[1]]+=[i[0]]
    print(d)
    total = 0
    for i in d:
        s = i
        curr = i
        for j in range(3):
            curr = d[i]
        if(curr == s):
            total+=1

    return total


##############
# Problem 09 #
##############

def matrix_product(A, B, m, n, k):
    """ Compute m-by-k product of m-by-n matrix A with n-by-k matrix B. """
    raise NotImplementedError


##############
# Problem 10 #
##############

def transpose(A, m, n):
    """ Return n-by-m transpose of m-by-n matrix A. """ 
    raise NotImplementedError


##############
# Problem 11 #
##############

def check_valid_paren(s):
    """ Return True iff each left parenthesis is closed by exactly one
        right parenthesis later in the string and each right parenthesis
        closes exactly one left parenthesis earlier in the string. """
    raise NotImplementedError


##############
# Problem 12 #
##############

def get_all_elements(root):
    """ Return a list of all numbers stored in root, in any order. """
    raise NotImplementedError


##############
# Problem 13 #
##############

def find_path(grid):
    """ Given a two dimensional m by n grid, with a 0 or a 1 in each cell,
        find a path from the top row (0) to the bottom row (n-1) consisting of
        only ones.  Return the path as a list of coordinate tuples (row, column).
        If there is no path return None. """
    raise NotImplementedError


##############
# Problem 14 #
##############

def longest_sequence(s):
    """ Find sequences of a single repeated character in string s.
        Return the length of the longest such sequence. """
    raise NotImplementedError


##############
# Problem 15 #
##############

def integer_right_triangles(p):
    """ Let p be the perimeter of a right triangle with integral, non-zero
        length sides of length a, b, and c. Return a sorted list of
        solutions with perimeter p. """
    raise NotImplementedError


##############
# Problem 16 #
##############

def encode_nested_list(seq):
    """ Encode a sequence of nested lists as a flat list. """
    raise NotImplementedError


##############
# Problem 17 #
##############

def second_largest(A):
    """ Given a list of numbers, return the second largest element in the list. 
        You may assume the list has at least two elements. """
    raise NotImplementedError


##############
# Problem 18 #
##############

def run_length_encode(S):
    """ Given a string S, return a string that is the run length encoding of S. 
        Assume only alphabetic, capital characters occur in the string (A-Z only). """
    raise NotImplementedError


##############
# Problem 19 #
##############

def histogram(A, low, high, n):
    """ Given a dataset A (a list of integers), count how many numbers fall into each bucket.
        Include only numbers in the [low, high); any integers in A that do not fall into any bucket 
        should not be counted. Return a list of counts for each bin (a list of n elements, where the 
        ith element is the count for the ith bucket from the left). You may assume that (high-low) 
        is a multiple of n. """
    raise NotImplementedError


##############
# Problem 20 #
##############

def knight_in_two_moves(A, B):
    """ Given two locations A and B on the chessboard, determine if a knight can travel from one to 
        the other in exactly two moves. Return a Boolean, True if the knight can indeed reach B from 
        A in two moves, and False otherwise. """
    raise NotImplementedError
