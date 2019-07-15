# 6.009 Spring 2019 - Quiz 3 Practice Quiz C Solutions

from copy import deepcopy

# NO OTHER IMPORTS!

#############
# Problem 1 #
#############

def spynet_secret(spynet):
    secrets = {}
    def walk(spy):
        if spy in secrets:
            return secrets[spy]
        report_secrets = [walk(report) for report in spynet.reporting_to(spy)]
        spy_secret = spynet.meet_and_compute(spy, report_secrets)
        secrets[spy] = spy_secret
        return spy_secret
    return walk('SuperSpy')

def make_spynet(g, secret_op=lambda x,y: x*y):
    """Returns a SpyNet instance based on a dictionary mapping spies
       to their own secret and the set of spies that report to them.

       DO NOT MODIFY THIS DEFINITION -- it is provided here to document
       the methods that may be called on the instance.
    """
    g = deepcopy(g)
    SECRET = 0
    REPORTS = 1
    MET = 2

    class SpyNet():
        def spies(self):
            """Return set of spies in the spy network"""
            return set(g.keys())

        def reporting_to(self, spy):
            """Return set of spies that report to `spy`"""
            return g[spy][REPORTS]

        def meet_and_compute(self, spy, reporting_spy_secrets=[]):
            """Convene a meeting called by `spy` with all of `spy`'s reports, and
               calculate the combined secret using `op` successively
               on each of the reporting_spy_secrets as computed by
               their own previous meeting. If `spy` has already
               previously convened a meeting, this call with result in
               a spy network failure (test.py case will not succeed).
               Similarly, if a report has not yet computed a combined
               secret before this meeting, this call will result in a
               spy network failure. If `meet_and_compute` succeeds,
               the combined secret value will be returned.

               Note that a spy with no spies that report to them must
               still call a meeting with just themself, in order to
               pass along (return) their own secret.

            """
            self.spynet_check()
            if len(g[spy]) > MET:
                self.spynet_fail()
                raise ValueError("Spy "+repr(spy)+" already convened a meeting - can't call another one!")
            for report in self.reporting_to(spy):
                if not len(g[report]) > MET:
                    self.spynet_fail()
                    raise ValueError("Spy "+repr(report)+" reporting to "+repr(spy)+" has not yet convened their own meeting!")
            result = g[spy][SECRET]
            for s in reporting_spy_secrets:
                result = secret_op(result, s)
            g[spy] += (True,)
            return result

        def spynet_check(self):
            status = g['SuperSpy'][MET-1:]
            if len(status) > 1:
                raise ValueError("This spy network has already failed.")

        def spynet_fail(self):
            g['SuperSpy'] += ('Fail',)

    return SpyNet()


############*#
# Problem 2A #
##############

def find_boundary_pairs(data):
    elts = sorted(data)
    return [elts[ix-1] for ix in boundary_indices(elts)]

def boundary_indices(data):
    """ yield indices whenever label changes """
    elts = sorted(data)
    if len(elts) == 0:
        return
    prev_label = elts[0][1]
    for ix, elt in enumerate(elts):
        if elt[1] != prev_label:
            prev_label = elt[1]
            yield ix

############*#
# Problem 2B #
##############

class SplitTree():
    def __init__(self, elts):
        """Create SplitTree given sequence of elements; each elt
           in elts is of form (x, label) where x is a number, and
           label is a string label. An invariant is that labels 
           will only have one of two different values; however, 
           those two different values are not pre-defined (they
           may be different for any given SplitTree as based on
           the data provided to the SplitTree).
        """
        # leaf info
        self.label = None
        self.values = None

        # split info
        self.boundary = None
        self.left = None
        self.right = None

        # put elts into tree
        self.split(elts)

    def split(self, elts):
        """Recursively create leaf and/or split nodes. Various
           ways can be tried to decide on the split boundary.
        """
        if len(elts) == 0:
            return
        s_elts = sorted(elts)
        ##splits = list(boundary_indices(s_elts))
        splits = find_boundary_pairs(s_elts)
        if splits == []: # homogenous -- save leaf info
            self.label = s_elts[0][1]
            self.values = [val for val, _ in s_elts]
            self.boundary = None
            self.left = None
            self.right = None
        else:  # found split; remember split and create branches
            #split_index = splits[0] # just use first split in greedy case
            split_elt = splits[len(splits)//2] # pick middle split
            split_index = s_elts.index(split_elt)
            self.label = None
            self.values = None
            self.boundary = s_elts[split_index][0]
            self.left =  SplitTree(s_elts[:split_index+1])
            self.right = SplitTree(s_elts[split_index+1:])

    def optimal_split(self, elts):
        """optimal split: try all splits; choose one with least depth.
           This gets ways too slow when there are very many splits"""
        if len(elts) == 0:
            return
        s_elts = sorted(elts)
        #splits = list(boundary_indices(s_elts))
        splits = find_boundary_pairs(s_elts)
        if splits == []: # homogenous -- save leaf info
            self.label = s_elts[0][1]
            self.values = [val for val, _ in s_elts]
            self.boundary = None
            self.left = None
            self.right = None
        else:  # found splits. Try each and pick best
            best_depth = None
            for split_elt in splits:
                split_index = s_elts.index(split_elt)
                left =  SplitTree(s_elts[:split_index+1])
                right = SplitTree(s_elts[split_index+1:])
                depth = max(left.depth(), right.depth())
                if best_depth is None or depth < best_depth:
                    best_depth = depth
                    self.boundary = s_elts[split_index][0]
                    self.left = left
                    self.right = right
                    self.label = None
                    self.values = None

    def decide(self, value):
        """Return label for `value`, by traversing SplitTree. Note
           that `value` might not explicitly be present in the tree.
        """
        if self.label:
            return self.label
        return self.left.decide(value) if value <= self.boundary else self.right.decide(value)

    def validate(self):
        if self.label:
            assert self.values is not None
            assert self.boundary is None
            assert self.left is None
            assert self.right is None
        else:
            assert self.values is None
            assert self.boundary is not None
            assert self.left is not None
            assert self.right is not None

    def insert(self, elt):
        """add given elt of form (x, label) into tree"""
        self.validate()

        if self.label and self.label == elt[1]:
            # Tree is homogenous (leaf) and matches element label; just add element to leaf
            self.values.append(elt[0])
            self.values.sort()
            return

        if self.label and self.label != elt[1]:
            # Tree is homogenous (leaf) but does not match this element's label. Need
            # to create a new split here.
            elts = [(val, self.label) for val in self.values]
            elts.append(elt)
            self.split(elts)
            return

        # Otherwise we're at a split point; continue along the appropriate branch
        if elt[0] <= self.boundary:
            self.left.insert(elt)
            self.left.validate()
        else:
            self.right.insert(elt)
            self.right.validate()

    def depth(self):
        """return depth of tree"""
        if self.label:
            return 1
        return max(1+self.left.depth(), 1+self.right.depth())

    def boundaries(self):
        """yield the decision boundaries (in order, from smallest to largest)"""
        self.validate()
        if self.label:
            return
        yield from self.left.boundaries()
        yield self.boundary
        yield from self.right.boundaries()

    def __iter__(self):
        """yield the (value, label) pairs that exist in the tree.

        For example, list(SplitTree(((10, '-'), (12, '+'), (11, '+')))) might
        result in [(10, '-'), (12, '+'), (11, '+')] though with those pairs
        appearing (being yielded) in any order.
        """
        if self.values:
            yield from ((val, self.label) for val in self.values)
            return
        if self.left:
            yield from self.left
        if self.right:
            yield from self.right

    def dictify(self):
        """ Do not modify this """
        return {"label": self.label,
                "values": set(self.values) if self.values else None,
                "boundary": self.boundary,
                "left": self.left.dictify() if self.left else None,
                "right": self.right.dictify() if self.right else None}

    def __repr__(self):
        return repr(self.dictify())
        
    def __str__(self, level=0):
        """ utility: a string version to (textually) visualize the SplitTree"""
        sp = "    "
        res = ""
        if self.label:
            res += level*sp + self.label + "\n"
            res += level*sp + "values: " + str(self.values) + "\n"
        else:
            res += level*sp + " <= " + str(self.boundary) + "\n"
            if self.left:
                res += level*sp + "left:\n" + self.left.__str__(level = level+1)
            if self.right:
                res += level*sp + "right:\n" + self.right.__str__(level = level+1)
        return res
    
    
if __name__ == '__main__':
    pass
