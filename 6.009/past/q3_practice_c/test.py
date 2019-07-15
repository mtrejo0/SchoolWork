#!/usr/bin/env python3
import os
import quiz
import unittest
from copy import deepcopy

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

class TestProblem1(unittest.TestCase):
    def test_01(self):
        # Example from problem description
        spydict = {'SuperSpy': (7, {'spy1', 'spy2'}),
                   'spy1': (2, set()),
                   'spy2': (5, {'spy1'})}
        spynet = _make_spynet(spydict)
        expect = 140
        self.assertEqual(expect, quiz.spynet_secret(spynet))

        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: x+y)
        expect = 16
        self.assertEqual(expect, quiz.spynet_secret(spynet))

    def test_02(self):
        # Another basic case
        spydict = {'spy1': (4, set()),
                   'spy2': (3, {'spy1'}),
                   'spy3': (2, {'spy1'}),
                   'SuperSpy': (1, {'spy2', 'spy3'})}
        spynet = _make_spynet(spydict)
        expect = 96
        self.assertEqual(expect, quiz.spynet_secret(spynet))
        
        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: x+y)
        expect = 14
        self.assertEqual(expect, quiz.spynet_secret(spynet))

    def test_03(self):
        # Multiple path case
        spydict = {'spy1': (4, set()),
                   'spy2': (3, {'spy1'}),
                   'spy3': (2, {'spy1'}),
                   'SuperSpy': (1, {'spy2', 'spy3', 'spy1'})}
        spynet = _make_spynet(spydict)
        expect = 384
        self.assertEqual(expect, quiz.spynet_secret(spynet))
        
        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: x+y)
        expect = 18
        self.assertEqual(expect, quiz.spynet_secret(spynet))

    def test_04(self):
        # Another case
        spydict = {'spy1': (4, {'spy4'}),
                   'spy2': (3, {'spy1'}),
                   'spy3': (2, {'spy1'}),
                   'spy4': (8, set()),
                   'SuperSpy': (1, {'spy2', 'spy3', 'spy1'})}
        spynet = _make_spynet(spydict)
        expect = 196608
        self.assertEqual(expect, quiz.spynet_secret(spynet))
        
        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: x+y)
        expect = 42
        self.assertEqual(expect, quiz.spynet_secret(spynet))

    def test_05(self):
        # Big linear case
        num = 100
        spydict = {'spy%d' % n: (n, {'spy%d' % (n+1)}) for n in range(num-1, -1, -1)}
        spydict['spy%d' % num] = (num, set())
        spydict['SuperSpy'] = (1, {'spy1'})
        expect_sched = [['spy%d' % n, {'spy%d' %(n+1)}] for n in range(num-1,0,-1)]+[['SuperSpy', {'spy1'}]]
        expect = 1
        for n in range(1,num+1):
            expect *= n
        spynet = _make_spynet(spydict)
        self.assertEqual(expect, quiz.spynet_secret(spynet))

        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: max(x,y))
        expect = 100
        self.assertEqual(expect, quiz.spynet_secret(spynet))
        
    def test_06(self):
        # Big weave case
        num = 50
        spydict = {'spy%d' % n: (n, {'spy%d' % (n+1), 'spy%d' % (n+2)}) for n in range(num)}
        spydict['spy%d' % num] = (num, set())
        spydict['spy%d' % (num+1)] = (num, set())
        spydict['SuperSpy'] = (1, {'spy1'})
        spynet = _make_spynet(spydict, secret_op=lambda x,y: x+y)
        expect = 1983184816230
        self.assertEqual(expect, quiz.spynet_secret(spynet))
         
        # Same graph, but with a different operation
        spynet = _make_spynet(spydict, secret_op=lambda x,y: max(x,y))
        expect = 50
        self.assertEqual(expect, quiz.spynet_secret(spynet))

def _make_spynet(g, secret_op=lambda x,y: x*y):
    g = deepcopy(g)
    SECRET = 0
    REPORTS = 1
    MET = 2
    class SpyNet():
        def spies(self):
            return set(g.keys())
        def reporting_to(self, spy):
            return g[spy][REPORTS]
        def meet_and_compute(self, spy, reporting_spy_secrets=[]):
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

class TestProblem2A(unittest.TestCase):
    def test_01(self):
        # no boundary (label never changes)
        data = ((1, '+'),)
        expect = []
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_02(self):
        # no boundary (label never changes)
        data = ((1, '+'), (2, '+'), (3, '+'))
        expect = []
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_03(self):
        # starting data ordered; has boundary
        data = ((10, '-'), (11, '+'), (12, '+'))
        expect = [(10, '-')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_04(self):
        # should work for any labels
        data = ((10, 'dog'), (11, 'cat'), (12, 'cat'))
        expect = [(10, 'dog')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_05(self):
        # starting data ordered; has boundary
        data = ((11, '+'), (12, '+'), (10, '-'))
        expect = [(10, '-')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_06(self):
        data = ((4, '-'), (2, '+'))
        expect = [(2, '+')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_07(self):
        # more complicated data
        data = ((1,'+'), (2,'+'), (3,'-'), (5,'+'), (4,'+'), (6,'+'))
        expect = [(2, '+'), (3, '-')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_08(self):
        data = ((1,'+'), (3,'-'), (4,'+'), (5,'+'), (2,'+'), (6,'+'))
        expect = [(2, '+'), (3, '-')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_09(self):
        data = ((4, '-'), (2, '-'), (14, '+'), (12, '+'), (33, '+'), (15, '+'),(3, '-'), (5, '-'))
        expect = [(5, '-')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_10(self):
        data =  [(16, '+'), (25, '+'), (26, '+'), (19, '-'), (30, '-'), (11, '+'), (31, '-'), 
                 (24, '+'), (15, '+'), (20, '+'), (4, '-'), (5, '-'), (21, '-'), (10, '-'), 
                 (3, '-'), (18, '+'), (28, '+'), (38, '+'), (2, '-'), (22, '+'), (35, '+'), 
                 (34, '-'), (17, '+'), (12, '-'), (8, '+'), (27, '+'), (33, '+'), (39, '-'), 
                 (37, '+'), (13, '+'), (1, '-'), (32, '+'), (23, '-'), (0, '+'), (9, '+'), 
                 (36, '+'), (29, '-'), (7, '+'), (6, '+'), (14, '-')]
        expect = [(0, '+'), (5, '-'), (9, '+'), (10, '-'), (11, '+'), (12, '-'), (13, '+'), 
                  (14, '-'), (18, '+'), (19, '-'), (20, '+'), (21, '-'), (22, '+'), (23, '-'), 
                  (28, '+'), (31, '-'), (33, '+'), (34, '-'), (38, '+')]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)

    def test_11(self):
        num = 500; pref = 5
        data = [(n, '+' if n%pref else '-') for n in range(num, 0, -1)]
        expect = [(n, '+' if n%pref else '-') for n in range(1, num) if n%pref == pref-1 or n%pref == 0]
        result = quiz.find_boundary_pairs(data)
        self.assertEqual(expect, result)



##############
# Problem 2B #
##############

class TestProblem2B(unittest.TestCase):
    def validate_tree(self, tree):
        if tree.label: # leaf node
            self.assertIsNotNone(tree.values)
            self.assertIsNone(tree.boundary)
            self.assertIsNone(tree.left)
            self.assertIsNone(tree.right)
        else: # split node
            self.assertIsNone(tree.values)
            self.assertIsInstance(tree.boundary, (int, float))
            self.assertIsInstance(tree.left, quiz.SplitTree)
            self.assertIsInstance(tree.right, quiz.SplitTree)
            self.validate_tree(tree.left)
            self.validate_tree(tree.right)

    def validate_walk(self, tree, boundaries):
        blist = []
        tlist = [tree]
        while len(tlist)>0:
            t = tlist.pop()
            if t.boundary is not None:
                blist.append(t.boundary)
                tlist.append(t.left)
                tlist.append(t.right)
        self.assertEqual(set(boundaries), set(blist))
        self.assertEqual(len(blist), len(set(blist)), msg="duplicate boundary values in tree")

    def test_01(self):
        # Create tree with single element, no boundary
        data = ((1, '+'),)
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(tree.label, '+')
        self.assertEqual(set(tree.values), {1})

    def test_02(self):
        # Create tree with multiple elements, no boundary
        data = ((1, '+'), (3, '+'), (2, '+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(tree.label, '+')
        self.assertEqual(set(tree.values), {1, 2, 3})

    def test_03(self):
        # Create tree with single boundary
        data = ((4, '-'), (2, '+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = {'boundary': 2,
                  'label': None,
                  'left': {'boundary': None,
                           'label': '+',
                           'left': None,
                           'right': None,
                           'values': {2}},
                  'right': {'boundary': None,
                            'label': '-',
                            'left': None,
                            'right': None,
                            'values': {4}},
                  'values': None}
        self.assertEqual(expect, tree.dictify())

    def test_04(self):
        # Same as test_03, but with different labels. SplitTree
        # should not hard-wire in the specific labels.
        data = ((4, 'dog'), (2, 'cat'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = {'boundary': 2,
                  'label': None,
                  'left': {'boundary': None,
                           'label': 'cat',
                           'left': None,
                           'right': None,
                           'values': {2}},
                  'right': {'boundary': None,
                            'label': 'dog',
                            'left': None,
                            'right': None,
                            'values': {4}},
                  'values': None}
        self.assertEqual(expect, tree.dictify())

    def test_05(self):
        # tree1 example from quiz writeup: single boundary, multiple values
        self.maxDiff = None
        data = ((10, '-'), (12, '+'), (11, '+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = {'boundary': 10,
                  'label': None,
                  'left': {'boundary': None, 'label': '-', 'left': None, 'right': None, 'values': {10}},
                  'right': {'boundary': None, 'label': '+', 'left': None, 'right': None, 'values': {11,12}},
                  'values': None}
        self.assertEqual(expect, tree.dictify())

    def test_06(self):
        # More complicated tree but still with single boundary
        data = ((4, '-'), (2, '-'), (14, '+'), (12, '+'), (33, '+'), (15, '+'),(3, '-'), (5, '-'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = {'boundary': 5,
                  'label': None,
                  'left': {'boundary': None, 'label': '-', 'left': None, 'right': None, 'values': {2, 4, 3, 5}},
                  'right': {'boundary': None, 'label': '+', 'left': None, 'right': None, 'values': {14, 12, 33, 15}},
                  'values': None}
        self.assertEqual(expect, tree.dictify())

    def test_07(self):
        # Check decide method; tree with single boundary
        data = ((4, '-'), (2, '-'), (14, '+'), (12, '+'), (33, '+'), (15, '+'),(3, '-'), (5, '-'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = '-'
        for val in [1, -20, 1.5, 3, 4, 5, 3]:
            self.assertEqual(expect, tree.decide(val), msg="for val = "+str(val)+" expected "+repr(expect))
        expect = '+'
        for val in [8, 5.5, 200]:
            self.assertEqual(expect, tree.decide(val), msg="for val = "+str(val)+" expected "+repr(expect))

    def test_08(self):
        # Check boundaries iterator; single boundary
        data = ((4, '-'), (2, '-'), (14, '+'), (12, '+'), (33, '+'), (15, '+'),(3, '-'), (5, '-'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        expect = [5]
        self.assertEqual(expect, list(tree.boundaries()))
        self.validate_walk(tree, expect)

    def test_09(self):
        # Tree with more than one boundary. Result tree may not be unique!
        data = ((1,'+'), (2,'+'), (3,'-'), (5,'+'), (4,'+'), (6,'+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        for val, label in data:
            self.assertEqual(label, tree.decide(val))
        expect = [2, 3]
        self.assertEqual(expect, list(tree.boundaries()))
        self.validate_walk(tree, expect)

    def test_10(self):
        # Test __iter__ method
        data = ((1,'+'), (2,'+'), (3,'-'), (5,'+'), (4,'+'), (6,'+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(set(data), set(tree))
        self.assertEqual(len(set(data)), len(set(tree)))
        
    def test_11(self):
        # Test depth method: leaf only
        data = ((1,'+'), (2,'+'), (5,'+'), (4,'+'), (6,'+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(1, tree.depth())
        
    def test_12(self):
        # Test depth method: single boundary
        data = ((2,'+'), (1,'+'), (3,'-'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(2, tree.depth())
        
    def test_13(self):
        # Test insert method

        # Starting tree
        data = ((1,'+'), (3,'-'), (4,'+'), (5,'+'), (2,'+'), (6,'+'))
        tree = quiz.SplitTree(data)
        expect = [2, 3]
        self.assertEqual(expect, list(tree.boundaries()))
        self.assertEqual(set(data), set(tree))
        self.assertEqual(len(set(data)), len(set(tree)))

        # Now insert
        elt = (2.5,'-')
        data_post = data + (elt,)
        expect_post = expect
        tree.insert(elt)
        self.assertEqual(expect_post, list(tree.boundaries()))
        self.assertEqual(set(data_post), set(tree))
        self.assertEqual(len(set(data_post)), len(set(tree)))

        # Another insert; this time requiring restructuring
        elt = (1.5,'-')
        data_more = data_post + (elt,)
        expect_more = [1, 1.5, 2, 3]
        tree.insert(elt)
        self.assertEqual(expect_more, list(tree.boundaries()))
        self.assertEqual(set(data_more), set(tree))
        self.assertEqual(len(set(data_more)), len(set(tree)))
        self.validate_walk(tree, expect_more)

    def test_14(self):
        # Test depth method: multiple boundaries
        data = ((2,'+'), (1,'+'), (3,'-'), (5,'+'), (4,'+'), (6,'+'))
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        self.assertEqual(3, tree.depth())
        
    def test_15(self):
        # Big tree
        data =  [(16, '+'), (25, '+'), (26, '+'), (19, '-'), (30, '-'), (11, '+'), (31, '-'), 
                 (24, '+'), (15, '+'), (20, '+'), (4, '-'), (5, '-'), (21, '-'), (10, '-'), 
                 (3, '-'), (18, '+'), (28, '+'), (38, '+'), (2, '-'), (22, '+'), (35, '+'), 
                 (34, '-'), (17, '+'), (12, '-'), (8, '+'), (27, '+'), (33, '+'), (39, '-'), 
                 (37, '+'), (13, '+'), (1, '-'), (32, '+'), (23, '-'), (0, '+'), (9, '+'), 
                 (36, '+'), (29, '-'), (7, '+'), (6, '+'), (14, '-')]
        expect =  [0, 5, 9, 10, 11, 12, 13, 14, 18, 19, 20, 21, 22, 23, 28, 31, 33, 34, 38]
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        for val, label in data:
            self.assertEqual(label, tree.decide(val))
        self.assertEqual(expect, list(tree.boundaries()))
        self.assertEqual(set(data), set(tree))
        self.assertEqual(len(set(data)), len(set(tree)))
        self.validate_walk(tree, expect)
      
    def test_16(self):
        # Very big tree. Challenge case: requires a good splitting boundary heuristic,
        # as well as handling all inputs at once in the initial SplitTree creation
        # rather than one at a time.
        num = 4000; pref = 5
        data = [(n, '+' if n%pref else '-') for n in range(num, 0, -1)]
        boundaries = [n for n in range(1, num) if n%pref == pref-1 or n%pref == 0]
        tree = quiz.SplitTree(data)
        self.validate_tree(tree)
        for val, label in data:
            self.assertEqual(label, tree.decide(val))
        self.assertEqual(boundaries, list(tree.boundaries()))
        self.assertEqual(set(data), set(tree))
        self.assertEqual(len(set(data)), len(set(tree)))
        self.validate_walk(tree, boundaries)

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
