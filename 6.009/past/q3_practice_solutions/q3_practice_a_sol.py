# 6.009 Spring 2019 - Quiz 3 Practice Quiz A Solutions

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
    """
    if type(expr) == int or type(expr) == str:
        return expr
    else:
        op, oper1, oper2 = expr

        oper1 = constant_fold(oper1)
        oper2 = constant_fold(oper2)

        if type(oper1) == int and type(oper2) == int:
            return ops[op](oper1, oper2)
        elif (op == '+' and oper1 == 0) or (op == '*' and oper1 == 1):
            return oper2
        elif (op in {'+', '-'} and oper2 == 0) or (op == '*' and oper2 == 1):
            return oper1
        elif op == '*' and (oper1 == 0 or oper2 == 0):
            return 0
        else:
            return op, oper1, oper2

ops = {'+': (lambda x, y: x + y),
       '*': (lambda x, y: x * y),
       '-': (lambda x, y: x - y)}


############################################################
## Problem 2
############################################################

# Databases

def select(table,select,filters=None,order_by=None,limit=None):
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
      if not specifed, return rows in table order
    """
    fields = {field: i for i,field in enumerate(table[0])}
    data = table[1:]

    # apply fiter to row, return True if satisfied
    def apply_filters(row):
        if filters is not None:
            for pred,f1,f2 in filters:
                # convert field reference to corresponding value from row
                if isinstance(f1,list):
                    f1 = row[fields[f1[0]]]
                if isinstance(f2,list):
                    f2 = row[fields[f2[0]]]
                # check the predicate
                if pred == '=':
                    if not (f1 == f2): return False
                elif pred == '!=':
                    if not (f1 != f2): return False
                elif pred == '<':
                    if not (f1 < f2): return False
                elif pred == '<=':
                    if not (f1 <= f2): return False
                elif pred == '>':
                    if not (f1 > f2): return False
                elif pred == '>=':
                    if not (f1 >= f2): return False
        return True

    # find all rows that satisfy constraints
    result = [row for row in data if apply_filters(row)]

    # order if requested
    if order_by is not None:
        field = fields[order_by[0]]
        result.sort(key=lambda r: r[field], reverse=(order_by[1] == 'desc'))

    # limit number of results if requested to do so
    if limit is not None and len(result) > limit:
        result = result[:limit]

    # finally produce result rows with just requested content
    return [[row[fields[field]] for field in select]
            for row in result]


############################################################
## Problem 3
############################################################

# Infinite lists

class InfiniteList:
    def __init__(self, f):
        """Create an infinite list where position i contains value f(i)."""
        self.f = f
        self.vals = {}

    def __getitem__(self, i):
        """Standard Python method for defining notation ls[i], which
        expands to ls.__getitem__(i)"""
        if i in self.vals:
            return self.vals[i]
        return self.f(i)

    def __setitem__(self, i, val):
        """Standard Python method for defining notation ls[i] = val, which
        expands to ls.__setitem__(i, val)"""
        self.vals[i] = val

    def __iter__(self):
        """Standard Python method for producing a generator where called for,
        e.g. to loop over.  Note that this iterator has infinitely
        many values to return, so a usual loop over it will never
        finish!  It should yield values from index 0 to infinity, one
        by one."""
        x = 0
        while True:
            yield self[x]
            x += 1

    def __add__(self, other):
        """Standard Python method for defining notation a + b, which expands
        to a.__add__(b).  For this quiz question, other will be
        another InfiniteList, and the generated InfiniteList should
        add the elements of self and other, at each position."""
        if isinstance(other, (float, int)):
            f = lambda x: self[x] + other
        else:
            f = lambda x: self[x] + other[x]
        return InfiniteList(f)

    def __mul__(self, other):
        """Standard Python method for defining notation a * b, which expands
        to a.__mul__(b).  For this quiz question, other will be a
        number, and the generated InfiniteList should multiply each
        position of self by other."""
        return InfiniteList(lambda x: self[x] * other)


if __name__ == "__main__":
    pass
