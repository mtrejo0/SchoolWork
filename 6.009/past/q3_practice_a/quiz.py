import sys
sys.setrecursionlimit(1000)

# NO OTHER IMPORTS!

############################################################
## Problem 1
############################################################

# Constant folding

def constant_fold(expr):
    """Simplify parts of the expression whose constant values we can predict in advance,
    according to the rules set out in the quiz document.

    >>> constant_fold(1)
    1
    >>> constant_fold('x')
    'x'
    >>> constant_fold(('+', 2, 3))
    5
    >>> constant_fold(('+', 'x', ('*', 8, 3)))
    ('+', 'x', 24)
    >>> constant_fold(('*', 'x', ('-', 8, 7)))
    'x'
    """
    tree = operation(expr)
    # print(expr)
    # print(tree)

    for i in range(10):
        if type(tree) == operation:
            a = tree.collapse()
            if a != None:
                tree = a
            # print(tree)
        else:
            return tree
    return tree.tupRep()

class operation():

    def __init__(self,expr):
        # print(expr)
        self.op = expr[0]
        if type(expr[1]) == tuple :
            self.left = operation(expr[1])
        else:
            self.left = expr[1]
        if type(expr[2]) == tuple :
            self.right = operation(expr[2])
        else:
            self.right = expr[2]

    def collapse(self):
        if self.left == 0:
            # print("left")
            if self.op == "*":
                return 0
            if self.op == "+":
                return self.right

        if self.right == 0:
            # print("right")
            if self.op == "*":
                return 0
            if self.op == "+":
                return self.left

            if self.op == "-":
                return self.left

        if self.left == 1:
            # print("a")
            if self.op == "*":
                return self.right
        if self.right == 1:
            # print("b")
            if self.op == "*":
                return self.left

        if type(self.left) == int and type(self.right) == int:
            if self.op == "+":
                ans = self.left + self.right
            elif self.op == "-":
                ans = self.left-self.right
            elif self.op == "*":
                ans = self.left*self.right
            return ans

        if type(self.left) == operation:
            left = self.left.collapse()
            if left != None:
                self.left = left
        if type(self.right) == operation:
            right = self.right.collapse()
            if right != None:
                self.right = right


    def __str__(self, level=0):
        """
        Returns a string representation of the quadtree
        :param level: current level in the quadtree (level = 0 if node is the root)
        """
        ret = "("
        ret += self.op+","

        if self.left is not None:
            ret += self.left.__str__()+","
        if self.right is not None:
            ret += self.right.__str__()+")"

        return ret

    def tupRep(self):

        op = self.op

        if type(self.left) == operation:
            a = self.left.tupRep()
        else:
            a = self.left

        if type(self.right) == operation:
            b = self.right.tupRep()
        else:
            b = self.right
        return (op,a,b)



############################################################
## Problem 2
############################################################

# Databases

def select(table,which,filters=None,order_by=None):
    """select matching rows from the table
    result is a list containing the field values specifed by select in the order
    specified by order_by (or in table order if no order_by is specified).
    No row of table headers should be included.

    table is a list of rows, each row is a list of field values
      table[0] is a row of field names (strings)
      table[1:] are rows of data (can be any type)
      table has at least one row (ie, the field names)

    which is a sequence of field names specifing which data should
      be included in each returned row.  Must contain at least one field.

    filters, if specified, is a sequence of clauses of the form (pred, field_or_const, field_or_const)
      field has the form ['field_name'], const is a number or string
      pred is one of "=","!=","<","<=",">",">="
      if specified, row matches if all predicates evaluate to True
      if not specified, all rows match

    order_by, if specified is (field_name, asc_or_desc).
      asc_or_desc is either "asc" or "desc" for ascending or decending sort order
      if not specifed, return rows in table order"""


    cols = table[0]

    indexes = []
    for w in which:
        indexes+=[cols.index(w)]
    print(cols)
    print(which,filters,order_by)

    ans = []
    if filters != None:

        for row in table[1:]:
            new = []
            for i in indexes:
                new+=[row[i]]
            valid = True
            for f in filters:
                op = f[0]
                cat = f[1]
                val = f[2]

                if op == "=":
                    if type(cat) != list:
                        if cat not in cols:
                            continue
                    for c in cat:
                        i = cols.index(c)
                        if row[i] != val:
                            valid = False
                if op == "!=":
                    if type(cat) != list:
                        if cat not in cols:
                            continue
                    for c in cat:
                        i = cols.index(c)
                        if row[i] == val:
                            valid = False
                if op == ">":
                    if type(cat) != list:
                        if cat not in cols:
                            continue
                    for c in cat:
                        i = cols.index(c)
                        if row[i] <= val:
                            valid = False
                if op == "<":
                    for c in cat:
                        i = cols.index(c)
                        if row[i] >= val:
                            valid = False
            if valid:
                ans+=[new]


        if order_by != None:
            where = which.index(order_by[0])
            if order_by[1] == "asc":
                ans.sort(key = lambda ans: ans[where])
            else:
                ans.sort(key = lambda ans: ans[where],reverse = True)
        # print(ans)
        return ans



    if filters == None and order_by == None:
        ans = []
        for row in table[1:]:
            new = []
            for i in indexes:
                new+=[row[i]]
            ans+=[new]
        return ans
    return table







############################################################
## Problem 3
############################################################

# Infinite lists

class InfiniteList:
    def __init__(self, f):
        """Create an infinite list where position i contains value f(i)."""
        self.vals = {}
        self.f = f

    def __getitem__(self, i):
        """Standard Python method for defining notation ls[i], which expands to ls.__getitem__(i)"""
        if i not in self.vals:
            return self.f(i)
        return self.vals[i]

    def __setitem__(self, i, val):
        """Standard Python method for defining notation ls[i] = val, which expands to ls.__setitem__(i, val)"""
        self.vals[i] = val

    def __iter__(self):
        """Standard Python method for producing a generator where called for, e.g. to loop over.
        Note that this iterator has infinitely many values to return, so a usual loop over it will never finish!
        It should yield values from index 0 to infinity, one by one."""
        i = 0
        while True :
            yield self.__getitem__(i)
            i+=1

    def __add__(self, other):
        """Standard Python method for defining notation a + b, which expands to a.__add__(b).
        For this quiz question, other will be another InfiniteList, and the generated InfiniteList should
        add the elements of self and other, at each position."""

        new = InfiniteList(lambda x :x)
        i = 0
        while i < 10:
            # print (self[i],otsher[i])
            new[i] = self[i]+other[i]
            i+=1
        return new

    def __mul__(self, other):
        """Standard Python method for defining notation a * b, which expands to a.__mul__(b).
        For this quiz question, other will be a number, and the generated InfiniteList should
        multiply each position of self by other."""

        if type(other) == int:

            new = InfiniteList(lambda x :x)
            i = 0
            while i < 10:
                new[i] = self[i]*other
                i+=1
            return new

        new = InfiniteList(lambda x :x)
        i = 0
        while i < 10:
            new[i] = self[i]*other[i]
            i+=1
        return new



if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
