# No imports!

#############
# Problem 1 #
#############

def spynet_secret(spynet):
    # print(spynet.spies())
    all = spynet.spies()

    sec = {}
    order = {}
    copy = {}
    for spy in spynet.spies():
        if spy not in sec:
            sec[spy] = 0
        if spy not in order:
            order[spy] = set()

        if spy not in copy:
            copy[spy] = set()

        under = spynet.reporting_to(spy)

        order[spy] = under
        copy[spy] = set(under)

    # print(copy)


    while set() in order.values():
        rem = []
        for spy in order:
            if len(order[spy]) == 0:

                under = copy[spy]
                meeting = []
                for s in under:
                    meeting+=[sec[s]]

                # print(meeting)
                c = spynet.meet_and_compute(spy,meeting)
                sec[spy] = c
                rem+=[spy]

        for r in rem:
            del order[r]
            for spy in order:
                if r in order[spy]:
                    order[spy].remove(r)

    return sec["SuperSpy"]


def make_spynet(g, secret_op=lambda x,y: x*y):
    """Returns a SpyNet instance based on a dictionary mapping spies
       to their own secret and the set of spies that report to them.

       DO NOT MODIFY THIS DEFINITION -- it is provided here to fully
       document for you how the spynet works, and to assist in your
       own debugging.

       Note that this version mutates spynet when subsequently used,
       so a new spynet should be created when a clean starting point
       is desired.
    """
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


##############
# Problem 2A #
##############

def find_boundary_pairs(data):
    # data.sort(key = 0)
    data = list(data)
    data.sort(key = lambda x : x[0])
    # print(data)
    if len(data) == 1:
        return []
    last = data[0][1]
    ans = []
    for i in range(len(data)-1):

        if data[i][1] != data[i+1][1]:
            # sprint(data[i][1],data[i+1][1])
            ans+=[data[i]]
            last = data[i+1][1]
    return ans

##############
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
        self.values = set()
        self.data = list(elts)
        self.data.sort(key = lambda x: x[0])

        # split info
        self.boundary = None
        self.left = None
        self.right = None

        labels = set()
        for e in elts:
            self.values.add(e[0])
            labels.add(e[1])

        if len(labels) == 1:
            self.label = list(labels)[0]
            return
        self.values = None

        bounds = self.boundaries()
        self.boundary = bounds[0]

        for i in range(len(self.data)):
            if self.data[i][0] == self.boundary:
                index = i
                break



        self.left = SplitTree(self.data[:index+1])
        self.right = SplitTree(self.data[index+1:])





    def decide(self, value):
        """Return label for `value`, by traversing SplitTree. Note
           that `value` might not explicitly be present in the tree.
        """
        if self.values != None:
            return self.label
        if value <= self.boundary:
            return self.left.decide(value)
        return self.right.decide(value)


    def insert(self, elt):
        """add given elt of form (x, label) into tree"""
        self.data += [elt]
        self.__init__(self.data)

    def depth(self):
        """return depth of tree"""
        ans = 1

        if self.values != None:
            return ans

        return ans + max(self.left.depth(),self.right.depth())

    def boundaries(self):
        """yield the decision boundaries (in order, from smallest to largest)"""
        bounds = find_boundary_pairs(self.data)

        return  [x[0] for x in bounds]


    def __iter__(self):
        """yield the (value, label) pairs that exist in the tree.

        For example, list(SplitTree(((10, '-'), (12, '+'), (11, '+')))) might
        result in [(10, '-'), (12, '+'), (11, '+')] though with those pairs
        appearing (being yielded) in any order.
        """
        for v in self.data:
            yield v


    # Some utilities that may help with viewing/debugging trees
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

    def dictify(self):
        """ Do not modify this """
        return {"label": self.label,
                "values": set(self.values) if self.values else None,
                "boundary": self.boundary,
                "left": self.left.dictify() if self.left else None,
                "right": self.right.dictify() if self.right else None}


if __name__ == "__main__":
    # You are welcome to write/use your own doctests above,
    # or include your own test code here.
    import doctest
    doctest.testmod()
