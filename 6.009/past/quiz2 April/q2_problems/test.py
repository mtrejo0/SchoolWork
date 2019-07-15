#!/usr/bin/env python3
import os,os.path,json
import quiz
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

####################
## Problem 01 
####################

class TestProblem01(unittest.TestCase):
    def verify(self,grid,result,expected):
        if expected is False:
            self.assertIs(result,False,msg="Expected False value")
            return

        self.assertIsNot(result,False,msg="Expected solution, got False")

        # Check that output is proper size
        length = len(grid)
        self.assertIsInstance(result,list,msg="Returned value not a list")
        self.assertEqual(len(result),length,msg="Returned list has incorrect length")
        for row in result:
            self.assertIsInstance(row,list,msg="Returned value is not a list of lists")
            self.assertEqual(len(row),length,msg="Returned row has incorrect length")

        # Check that the given grid elements are the same
        for r in range(length):
            for c in range(length):
                if grid[r][c] != -1:
                    self.assertEqual(result[r][c],grid[r][c],msg="You changed the given grid values")

        # Check that rows/columns contain numbers 1, 2, ...n
        all_values = set(range(1,length + 1))
        for row in result:
            self.assertEqual(set(row),all_values,"row does not contain 1, 2, ..., n")
        for c in range(length):
            column = [result[r][c] for r in range(length)]
            self.assertEqual(set(column),all_values,"column does not contain 1, 2, ..., n")

    def test_latin_1(self):
        grid = [
            [-1]
        ]
        result = quiz.solve_latin_square(grid)
        self.verify(grid,result,True)

    def test_latin_2(self):
        grid = [
            [-1 , 1, -1],
            [-1, -1,  2],
            [-1, -1, -1]
        ]
        result = quiz.solve_latin_square(grid)
        self.verify(grid,result,True)

    def test_latin_3(self):
        grid = [
            [-1,  3, -1, -1, -1],
            [-1, -1,  1, -1, -1],
            [ 1, -1, -1,  4, -1],
            [ 2, -1, -1, -1, -1],
            [-1, -1,  4, -1,  5]
        ]
        result = quiz.solve_latin_square(grid)
        self.verify(grid,result,True)

    def test_latin_4(self):
        grid = [
            [-1, -1,  6, -1, -1, -1],
            [ 2, -1, -1, -1,  6, -1],
            [-1,  4, -1,  5, -1, -1],
            [-1, -1, -1, -1, -1,  1],
            [ 5, -1, -1, -1,  3, -1],
            [-1, -1, -1,  2, -1, -1]
        ]
        result = quiz.solve_latin_square(grid)
        self.verify(grid,result,True)

    def test_latin_5(self):
        grid = [
            [ 2, -1, -1,  6, -1, -1],
            [-1, -1,  2, -1, -1, -1],
            [-1,  2, -1, -1,  3, -1],
            [-1, -1, -1, -1, -1, -1],
            [ 4, -1, -1, -1, -1, -1],
            [-1, -1, -1,  4,  1,  5]
        ]
        result = quiz.solve_latin_square(grid)
        self.verify(grid,result,False)

# ####################
# ## Problem 02 
# ####################

class TestProblem02(unittest.TestCase):
    def test_is_proper_1(self):
        root = {
            "color":  "black",
            "left":   -1,
            "right":  -1
        }
        result = quiz.is_proper(root)
        self.assertIs(result,True,"Tree is proper, expected True value")

    def test_is_proper_2(self):
        root = {
            "color":  "black",
            "left":   {
                "color":    "red",
                "left":     -1,
                "right":    -1
            },
            "right":  {
                "color":    "black",
                "left":     -1,
                "right":    -1
            }
        }
        result = quiz.is_proper(root)
        self.assertIs(result,False,"Tree is not proper, expected False value")
        
    def test_is_proper_3(self):
        root = {
            "color":  "red",
            "left": {
                "color":  "red",
                "left": {
                    "color":  "red",
                    "left": {
                        "color":  "red",
                        "left":   -1,
                        "right":  -1
                    },
                    "right": {
                        "color":  "red",
                        "left":   -1,
                        "right":  -1
                    }
                },
                "right": {
                    "color":  "red",
                    "left":   -1,
                    "right":  -1
                }
            },
            "right": {
                "color":  "red",
                "left":   -1,
                "right":  -1
            }

        }
        result = quiz.is_proper(root)
        self.assertIs(result,True,"Tree is proper, expected True value")

    def test_is_proper_4(self):
        root = {
            "color":  "red",
            "left": {
                "color":  "black",
                "left": {
                    "color":  "red",
                    "left": {
                        "color":  "red",
                        "left":  {
                            "color":  "red",
                            "left":   -1,
                            "right":  -1
                        },
                        "right": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        }
                    },
                    "right":  -1
                },
                "right": {
                    "color":  "red",
                    "left": {
                        "color":  "black",
                        "left":   -1,
                        "right":  -1
                    },
                    "right": {
                        "color":  "black",
                        "left":   -1,
                        "right":  -1
                    }
                }
            },
            "right": {
                "color":  "black",
                "left": {
                    "color":  "black",
                    "left":   -1,
                    "right":  -1
                },
                "right": {
                    "color":  "black",
                    "left":   -1,
                    "right":  -1
                }
            }
        }
        result = quiz.is_proper(root)
        self.assertIs(result,False,"Tree is not proper, expected False value")

    def test_is_proper_5(self):
        root = {
            "color":  "black",
            "left": {
                "color":  "red",
                "left": {
                    "color":  "black",
                    "left": {
                        "color":  "black",
                        "left":   -1,
                        "right":  -1
                    },
                    "right": {
                        "color":  "red",
                        "left": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        },
                        "right": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        }
                    }
                },
                "right": {
                    "color":  "red",
                    "left": {
                        "color":  "black",
                        "left": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        },
                        "right": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        }
                    },
                    "right": {
                        "color":  "black",
                        "left": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        },
                        "right": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        }
                    }
                }
            },
            "right": {
                "color":  "black",
                "left": {
                    "color":  "black",
                    "left": {
                        "color":  "red",
                        "left":   -1,
                        "right":  -1
                    },
                    "right": {
                        "color":  "red",
                        "left":   -1,
                        "right":  -1
                    }
                },
                "right": {
                    "color":  "red",
                    "left": {
                        "color":  "red",
                        "left": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        },
                        "right": {
                            "color":  "black",
                            "left":   -1,
                            "right":  -1
                        }
                    },
                    "right": {
                        "color":  "black",
                        "left":   -1,
                        "right":  -1
                    }
                }
            }
        }
        result = quiz.is_proper(root)
        self.assertIs(result,True,"Tree is proper, expected True value")

    def test_is_proper_6(self):
        root = {
            "color":  "black",
            "left": {
                "color":  "black",
                "left": -1,
                "right": -1
            },
            "right": -1
        }
        result = quiz.is_proper(root)
        self.assertIs(result,True,"Tree is proper, expected True value")

# ####################################################
# ## Problem 03. Prairie Dog Housing Lottery
# ####################################################

# class TestProblem03(unittest.TestCase):
#     def test_lottery_1(self):
#         prairie_dogs = [[2], [1], [0]]
#         capacities = [1,1,1]
#         result = quiz.lottery(prairie_dogs,capacities)
#         self.assertIn(result,[[2, 1, 0]])

#     def test_lottery_2(self):
#         prairie_dogs = [[0, 1], [1, 0], [0, 1]]
#         capacities = [1,1]
#         result = quiz.lottery(prairie_dogs,capacities)
#         self.assertIsNone(result,"No solution, expected None")

#     def test_lottery_3(self):
#         prairie_dogs = [[0, 1], [2, 3], [4, 5], [0], [2], [4]]
#         capacities = [1,1,1,1,1,1]
#         result = quiz.lottery(prairie_dogs,capacities)
#         self.assertIn(result,[[1, 3, 5, 0, 2, 4]])

#     def test_lottery_4(self):
#         with open(os.path.join(TEST_DIRECTORY,'test_data','lottery_4.json'),'r') as f:
#             expected = json.load(f)

#         prairie_dogs = [[19, 18], [24, 7], [20, 25], [21, 1], [20, 24], [15, 14], [27, 13], [28, 15], [13, 20], [26, 11], [29, 17], [3, 20], [20, 28], [20, 27], [7, 20], [1, 0], [20, 29], [11, 20], [9, 8], [17, 20], [13, 12], [23, 5], [20, 22], [1, 20], [15, 20], [20, 26], [20, 21], [19, 20], [20, 30], [5, 4], [5, 20], [7, 6], [20, 23], [30, 19], [9, 20], [25, 9], [17, 16], [3, 2], [11, 10], [22, 3]]
#         capacities = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#         result = quiz.lottery(prairie_dogs,capacities)
#         self.assertIn(result,expected)

#     def test_lottery_5(self):
#         prairie_dogs = [[7], [2], [6, 0], [1, 0], [15, 0], [2, 0], [13], [13, 0], [8, 0], [5], [4], [3], [17, 0], [16], [11], [6], [7, 0], [10], [12, 0], [17], [11, 0], [20], [14, 0], [1], [20, 0], [18, 0], [19, 0], [15], [18], [4, 0], [10, 0], [19], [9], [5, 0], [9, 0], [14], [16, 0], [8], [12], [3, 0]]
#         capacities = [20, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#         result = quiz.lottery(prairie_dogs,capacities)
#         self.assertIn(result,[[7, 2, 0, 0, 0, 0, 13, 0, 0, 5, 4, 3, 0, 16, 11, 6, 0, 10, 0, 17, 0, 20, 0, 1, 0, 0, 0, 15, 18, 0, 0, 19, 9, 0, 0, 14, 0, 8, 12, 0]])

# ####################################################
# ## Problem 04. Advanced Forestry
# ####################################################

# class TestProblem04(unittest.TestCase):
#     # We can't JSON encode "trees" with fancy DAG structure, as for the last problem
#     # on this quiz.  Instead, we work with arrays of nodes, with pointers replaced by
#     # numeric indices.  This function translates back to proper trees.
#     def make_tree(self,tarray):
#         if len(tarray) == 0:
#             return None

#         outarray = [{"data": v["data"], "left": None, "right": None, "prev": None, "next": None}
#                     for v in tarray]
#         for i in range(len(tarray)):
#             def fixupField(field):
#                 index = tarray[i][field]
#                 if index != None:
#                     outarray[i][field] = outarray[index]

#             fixupField("left")
#             fixupField("right")
#             fixupField("prev")
#             fixupField("next")

#         return outarray[0]

#     # Next, a function to reverse that last transformation.
#     def unmake_tree(self,tree):
#         tarray = [] # We build up the flattened version here.
#         index_by_id = {} # Maps node ID to index within tarray.

#         # First pass: create just the tree structure within the array
#         def make_skeleton(tree):
#             if tree:
#                 index = len(tarray)
#                 index_by_id[id(tree)] = index
#                 node = {"data": tree["data"], "prev": tree["prev"], "next": tree["next"]}
#                 tarray.append(node)
#                 node["left"] = make_skeleton(tree["left"])
#                 node["right"] = make_skeleton(tree["right"])
#                 return index

#         make_skeleton(tree)

#         # Second pass: fix up the prev and next pointers.
#         for node in tarray:
#             def fixupField(field):
#                 if node[field] != None:
#                     node[field] = index_by_id[id(node[field])]
#             fixupField("prev")
#             fixupField("next")

#         return tarray

#     def verify_insert(self,result,fname):
#         with open(os.path.join(TEST_DIRECTORY,'test_data',fname+'.json'),'r') as f:
#             expected = json.load(f)
#         result = self.unmake_tree(result)
#         self.assertEqual(result,expected)

#     def test_insert_1(self):
#         tree = self.make_tree([
#             {"data": 3, "left": None, "right": None, "prev": None, "next": None}
#         ])
#         data = 15
#         quiz.insert(tree, data)
#         self.verify_insert(tree,'insert_1')

#     def test_insert_2(self):
#         tree = self.make_tree([
#             {"data": 6, "left": 1, "right": 3, "prev": 2, "next": 3},
#             {"data": 2, "left": None, "right": 2, "prev": None, "next": 2},
#             {"data": 4, "left": None, "right": None, "prev": 1, "next": 0},
#             {"data": 8, "left": None, "right": None, "prev": 0, "next": None}
#         ])
#         data = 3
#         quiz.insert(tree, data)
#         self.verify_insert(tree,'insert_2')

#     def test_insert_3(self):
#         tree = self.make_tree([
#             {"data": 6, "left": 1, "right": 3, "prev": 2, "next": 3},
#             {"data": 2, "left": None, "right": 2, "prev": None, "next": 2},
#             {"data": 4, "left": None, "right": None, "prev": 1, "next": 0},
#             {"data": 8, "left": None, "right": None, "prev": 0, "next": None}
#         ])
#         data = 7
#         quiz.insert(tree, data)
#         self.verify_insert(tree,'insert_3')

#     def test_insert_4(self):
#         tree = self.make_tree([
#             {"data": 0, "left": None, "right": 1, "prev": None, "next": 1},
#             {"data": 1, "left": None, "right": 2, "prev": 0, "next": 2},
#             {"data": 3, "left": None, "right": 3, "prev": 1, "next": 3},
#             {"data": 4, "left": None, "right": None, "prev": 2, "next": None}
#         ])
#         data = 2
#         quiz.insert(tree, data)
#         self.verify_insert(tree,'insert_4')

#     def test_insert_5(self):
#         tree = self.make_tree([
#             {"data": 1, "left": None, "right": 1, "prev": None, "next": 1},
#             {"data": 2, "left": None, "right": 2, "prev": 0, "next": 2},
#             {"data": 4, "left": None, "right": 3, "prev": 1, "next": 3},
#             {"data": 5, "left": None, "right": None, "prev": 2, "next": None}
#         ])
#         data = 0
#         quiz.insert(tree, data)
#         self.verify_insert(tree,'insert_5')

# ####################
# ## Problem 05 
# ####################

# class TestProblem05(unittest.TestCase):
#     def verify(self,grid,magic_sum,choices,result):
#         # Check that output is proper size
#         length = len(grid)
#         self.assertIsInstance(result,list,msg="Returned value not a list")
#         self.assertEqual(len(result),length,msg="Returned list has incorrect length")
#         for row in result:
#             self.assertIsInstance(row,list,msg="Returned value is not a list of lists")
#             self.assertEqual(len(row),length,msg="Returned row has incorrect length")

#         # Check that the given grid elements are the same
#         for r in range(length):
#             for c in range(length):
#                 if grid[r][c] != -1:
#                     self.assertEqual(result[r][c],grid[r][c],msg="You changed the given grid values")

#         # Check that only valid choices were placed in empty squares
#         missingSquares = []
#         for r in range(length):
#             for c in range(length):
#                 if grid[r][c] == -1:
#                     missingSquares.append((r, c))
#         for (r,c) in missingSquares:
#             self.assertIn(result[r][c],choices,msg="Square has invalid values")

#         # Check that rows/columns/diagonals sum to magic_sum
#         for row in result:
#             self.assertEqual(sum(row),magic_sum,msg="Row does not add up to the magic_sum")
#         for c in range(length):
#             s = sum(result[r][c] for r in range(length))
#             self.assertEqual(s,magic_sum,msg="Column does not add up to the magic_sum")
#         s = sum(result[i][i] for i in range(length))
#         self.assertEqual(s,magic_sum,msg="Main diagonal does not add up to the magic_sum")
#         s = sum(result[i][length-i-1] for i in range(length))
#         self.assertEqual(s,magic_sum,msg="Off diagonal does not add up to the magic_sum")

#     def test_magic_1(self):
#         grid = [
#             [-1]
#         ]
#         magic_sum = 8
#         choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] 
#         result = quiz.solve_magicsquare_recursive(grid, magic_sum, choices)
#         self.verify(grid,magic_sum,choices,result)

#     def test_magic_2(self):
#         grid = [
#             [-1, -1],
#             [-1, -1]
#         ]
#         magic_sum = 10
#         choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18] 
#         result = quiz.solve_magicsquare_recursive(grid, magic_sum, choices)
#         self.verify(grid,magic_sum,choices,result)

#     def test_magic_3(self):
#         grid = [
#             [-1, 54, -1],
#             [-1, -1, -1],
#             [-1, -1, 48]
#         ]
#         magic_sum = 90
#         choices = [4, 6, 12, 16, 18, 20, 24, 28, 30, 33, 36, 42]
#         result = quiz.solve_magicsquare_recursive(grid, magic_sum, choices)
#         self.verify(grid,magic_sum,choices,result)

#     def test_magic_4(self):
#         grid = [
#             [-1, 8, -1, 1],
#             [2, -1, -1, 14],
#             [-1, 10, -1, -1],
#             [-1, -1, 9, -1]
#         ]
#         magic_sum = 34
#         choices = [1, 3, 4, 5, 6, 8, 9, 11, 13, 14, 15, 17, 18]
#         result = quiz.solve_magicsquare_recursive(grid, magic_sum, choices)
#         self.verify(grid,magic_sum,choices,result)

#     def test_magic_5(self):
#         grid = [
#             [15, 16, -1, 3, -1],
#             [-1, -1, 20, -1, 2],
#             [-1, -1, -1, -1, 25],
#             [24, -1, 6, 12, 18],
#             [17, -1, 4, 10, -1]
#         ]
#         magic_sum = 65
#         choices = [1, 2, 3, 5, 7, 8, 9, 11, 13, 14, 16, 17, 19, 21, 22, 23, 25, 27]
#         result = quiz.solve_magicsquare_recursive(grid, magic_sum, choices)
#         self.verify(grid,magic_sum,choices,result)

# ####################
# ## Problem 06 
# ####################

# class TestProblem06(unittest.TestCase):
#     def verify(self, graph, start, result, expected):
#         if expected is False:
#             self.assertEqual(result,{},msg="Expected {} got %s" % str(result))
#         else:
#             self.assertIsInstance(result,dict,msg="Expected result of type dict")

#             # Need to check that a valid coloring was returned in result
#             for vertex in result.keys():
#                 self.assertIn(result[vertex],('Red','Blue'),msg="Illegal color: %s" % result[vertex])

#             for vertex in graph.keys():
#                 self.assertIn(vertex,result,msg="Result doesn't include vertex %s" % vertex)
#                 for dest in graph[vertex]:
#                     # neighbors must have different colors
#                     self.assertNotEqual(result[vertex],result[dest],
#                                         msg="Neighboring vertices must have different colors: %s, %s" % (vertex,dest))

#     def test_colors_1(self):
#         graph = {
#             "A": ["B"],
#             "B": ["A", "C"],
#             "C": ["B", "D"],
#             "D": ["C", "E", "F"],
#             "E": ["D"],
#             "F": ["D", "G", "H", "I"],
#             "G": ["F"],
#             "H": ["F"],
#             "I": ["F"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, True)

#     def test_colors_2(self):
#         graph = {
#             "A": ["B"],
#             "B": ["A", "C"],
#             "C": ["B", "D"],
#             "D": ["C", "E", "F"],
#             "E": ["D"],
#             "F": ["D", "G", "H", "I"],
#             "G": ["F", "H"],
#             "H": ["F", "G"],
#             "I": ["F"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, False)

#     def test_colors_3(self):
#         graph = {
#             "A": ["B", "D"],
#             "B": ["C", "A"],
#             "C": ["D", "B"],
#             "D": ["A", "C", "E", "G"],
#             "E": ["D", "F"],
#             "F": ["E", "G"],
#             "G": ["D", "F", "H", "J"],
#             "H": ["G", "I"],
#             "I": ["H", "J"],
#             "J": ["G", "I"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, True)

#     def test_colors_4(self):
#         graph = {
#             "A": ["B", "D"],
#             "B": ["C", "A"],
#             "C": ["D", "B"],
#             "D": ["A", "C", "E", "G"],
#             "E": ["D", "F"],
#             "F": ["E", "G"],
#             "G": ["D", "F", "H", "J"],
#             "H": ["G", "I", "J"],
#             "I": ["H", "J"],
#             "J": ["G", "H", "I"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, False)

#     def test_colors_5(self):
#         graph = {
#             "A": ["B", "F"],
#             "B": ["C", "A"],
#             "C": ["D", "B", "G", "I"],
#             "D": ["C", "E"],
#             "E": ["D", "F"],
#             "F": ["A", "E"],
#             "G": ["C", "H"],
#             "H": ["G", "I"],
#             "I": ["C", "H"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, True)

#     def test_colors_6(self):
#         graph = {
#             "A": ["B", "D", "F"],
#             "B": ["C", "A", "H"],
#             "C": ["D", "B", "F", "G", "I"],
#             "D": ["A", "C", "E", "H"],
#             "E": ["D", "F"],
#             "F": ["A", "C", "E"],
#             "G": ["C", "H"],
#             "H": ["B", "D", "G", "I"],
#             "I": ["C", "H"]
#         }
#         start = "A"
#         result = quiz.alternating_colors(graph, start)
#         self.verify(graph, start, result, True)
        
# ####################
# ## Problem 07 
# ####################

# class TestProblem07(unittest.TestCase):
#     def test_check_BST_1(self):
#         btree = {
#             "root": [22, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertTrue(result,"Tree was a BST, expected True")

#     def test_check_BST_2(self):
#         btree = {
#             "root": [22, "A", "B"],
#             "A": [20, "", "C"],
#             "B": [25, "", ""],
#             "C": [23, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertFalse(result,"Tree wasn't a BST, expected False")

#     def test_check_BST_3(self):
#         btree = {
#             "root": [22, "A", "B"],
#             "A": [14, "C", "D"],
#             "B": [33, "E", "F"],
#             "C": [2, "", ""],
#             "D": [17, "", ""],
#             "E": [27, "", ""],
#             "F": [45, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertTrue(result,"Tree was a BST, expected True")

#     def test_check_BST_4(self):
#         btree = {
#             "root": [22, "A", "B"],
#             "A": [14, "C", "D"],
#             "B": [33, "E", "F"],
#             "C": [2, "", ""],
#             "D": [17, "", ""],
#             "E": [27, "", ""],
#             "F": [45, "G", ""],
#             "G": [32, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertFalse(result,"Tree wasn't a BST, expected False")

#     def test_check_BST_5(self):
#         btree = {
#             "root": [22, "A", ""],
#             "A": [14, "B", ""],
#             "B": [12, "C", "F"],
#             "C": [11, "D", ""],
#             "D": [10, "E", ""],
#             "E": [9, "", ""],
#             "F": [13, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertTrue(result,"Tree was a BST, expected True")

#     def test_check_BST_6(self):
#         btree = {
#             "root": [22, "A", ""],
#             "A": [14, "B", ""],
#             "B": [12, "C", "F"],
#             "C": [11, "D", ""],
#             "D": [10, "E", ""],
#             "E": [9, "", ""],
#             "F": [13, "", "G"],
#             "G": [15, "", ""]
#         }
#         start = "root"
#         result = quiz.check_BST(btree, start)
#         self.assertIn(result,(True,False),"Result should be True or False")
#         self.assertFalse(result,"Tree wasn't a BST, expected False")

# ####################
# ## Problem 08 
# ####################

# class TestProblem08(unittest.TestCase):
#     def test_pipecutting_01(self):
#         requests = []
#         stock_length = 8
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,0,"Expected 0 pipes, got %d" % result)

#     def test_pipecutting_02(self):
#         requests = [7]
#         stock_length = 7
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,1,"Expected 1 pipe, got %d" % result)

#     def test_pipecutting_03(self):
#         requests = [7,6,4]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,2,"Expected 2 pipes, got %d" % result)

#     def test_pipecutting_04(self):
#         requests = [4,3,4,1,7,8]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,3,"Expected 3 pipes, got %d" % result)

#     def test_pipecutting_05(self):
#         requests = [5,6,7,8,1,2,3,4,5,9]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,5,"Expected 5 pipes, got %d" % result)

#     def test_pipecutting_06(self):
#         requests = [6,7,8,2,3,4]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,3,"Expected 3 pipes, got %d" % result)

#     def test_pipecutting_07(self):
#         requests = [1,2,3,4]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,1,"Expected 1 pipe, got %d" % result)

#     def test_pipecutting_08(self):
#         requests = [10,9,8,7,6,5]
#         stock_length = 10
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,6,"Expected 6 pipes, got %d" % result)

#     def test_pipecutting_09(self):
#         requests = [1.3, 1.2, 0.15, 0.2, 0.5, 0.6]
#         stock_length = 2
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,2,"Expected 2 pipes, got %d" % result)

#     def test_pipecutting_10(self):
#         requests = [1, 1, 1.05]
#         stock_length = 3
#         result = quiz.pipe_cutting(requests, stock_length)
#         self.assertIsInstance(result,int,"Expected a result of type int, got %s" % result)
#         self.assertEqual(result,2,"Expected 2 pipes, got %d" % result)

# ####################
# ## Problem 09
# ####################

# class TestProblem09(unittest.TestCase):
#     def test_cherrypick_01(self):
#         A = [1,2,3,4,5]
#         n = 0
#         required_sum = 0
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,True,"Expected True")

#     def test_cherrypick_02(self):
#         A = [1,2,3,4,5]
#         n = 3
#         required_sum = 0
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,False,"Expected False")

#     def test_cherrypick_03(self):
#         A = [1,2,3,-7,4,5]
#         n = 3
#         required_sum = 0
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,True,"Expected True")

#     def test_cherrypick_04(self):
#         A = [7,5,19,7,4,16,1,18,18,5]
#         n = 10
#         required_sum = 100
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,True,"Expected True")

#     def test_cherrypick_05(self):
#         A = [7,5,19,7,-100,4,16,1,18,18,5]
#         n = 10
#         required_sum = 0
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,False,"Expected False")

#     def test_cherrypick_06(self):
#         A = [27, 31, 77, 35, 87, 27, 61, 30, 16, 70, 6, 58, 78, 6, 72, 7, 89, 34, 1, 98, 55, 42, 85, 78, 6, 86, 54, 3, 41, 77, 49, 79, 93, 45, 16, 41, 80, 20, 47, 1, 4, 28, 48, 32, 89, 89, 39, 9, 47, 53, 50, 100, 77, 34, 77, 57, 1, 96, 20, 76, 15, 28, 26, 50, 36, 76, 77, 73, 24, 40, 1, 83, 24, 22, 92, 68, 49, 8, 5, 69, 43, 55, 29, 56, 60, 46, 69, 31, 62, 30, 50, 53, 59, 53, 43, 15, 57, 38, 54, 63]
#         n = 10
#         required_sum = 423
#         result = quiz.cherrypick(A, n, required_sum)
#         self.assertEqual(result,True,"Expected True")

# ####################
# ## Problem 10
# ####################

# class TestProblem10(unittest.TestCase):
#     def test_eval_ast_01(self):
#         ast = {"node": 99}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,99)

#     def test_eval_ast_02(self):
#         ast = { "node": "+",
#              "left": { "node": -10 },
#              "right": { "node": 13 } }
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,3)

#     def test_eval_ast_03(self):
#         ast = { "node": "*",
#              "left": { "node": -1 },
#              "right": { "node": 8 } }
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,-8)

#     def test_eval_ast_04(self):
#         ast = { "node": "*",
#              "left": { "node": 2 },
#              "right": { "node": "+",
#                         "left": { "node": 3 },
#                         "right": { "node": 4 }}}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,14)

#     def test_eval_ast_05(self):
#         ast = {  "node": "+",
#               "left": { "node": "*",
#                         "left": { "node": 7 },
#                         "right": {  "node": "*",
#                                     "left": { "node": 5 },
#                                     "right": {  "node": 2 }}},
#              "right": { "node": "+",
#                         "left": { "node": 11 },
#                         "right": {  "node": -5 }}}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,76)

#     def test_eval_ast_06(self):
#         ast = { "node": "+",
#              "left": { "node": "+",
#                        "left": { "node": "+",
#                                  "left": { "node": "+",
#                                            "left": { "node": 1 },
#                                            "right": { "node": 2 }},
#                                  "right": { "node": 3 }},
#                        "right": { "node": 4 }},
#              "right": { "node": 5 }}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,15)

#     def test_eval_ast_07(self):
#         ast = { "node": "*",
#              "left": { "node": 2 },
#              "right": { "node": "*",
#                         "left": { "node": 2 },
#                         "right": { "node": "*",
#                                    "left": { "node": 2 },
#                                    "right": { "node": "*",
#                                               "left": { "node": 2 },
#                                               "right": { "node": 2 } }}}}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,32)

#     def test_eval_ast_08(self):
#         ast = {  "node": "+",
#               "left": { "node": "*",
#                         "left": { "node": 7 },
#                         "right": {  "node": "*",
#                                     "left": { "node": 5 },
#                                     "right": {  "node": "*",
#                                                 "left": { "node": -2 },
#                                                 "right": {  "node": "*",
#                                                             "left": { "node": 4 },
#                                                            "right": { "node": 3 } }}}},
#              "right": { "node": "+",
#                         "left": { "node": "+",
#                                   "left": { "node": 11 },
#                                   "right": {  "node": "*",
#                                               "left": { "node": 2 },
#                                               "right": { "node": -5 } }},
#                         "right": {  "node": "+",
#                                     "left": { "node": 10 },
#                                     "right": { "node": -7 } }}}
#         result = quiz.eval_ast(ast)
#         self.assertEqual(result,-836)




# ####################
# ## Problem 11
# ####################

# class TestProblem11(unittest.TestCase):
#     def test_true_for_all_01(self):
#         simple_cases = [(('<', 1, 2), True),
#                         (('<', 1, 1), False),
#                         (('<', 2, 1), False),
#                         (('>', 1, 2), False),
#                         (('>', 2, 2), False),
#                         (('>', 3, 2), True)]
#         for i in range(len(simple_cases)):
#             with self.subTest(test=i):
#                 tree, expect = simple_cases[i]
#                 self.assertIs(quiz.true_for_all(tree), expect)

#     def test_true_for_all_02(self):
#         tree = ('>', ('>', 10, 5), 6)
#         expect = False
#         self.assertIs(quiz.true_for_all(tree), expect)
#         tree = ('<', 6, ('>', 10, 7))
#         expect = True
#         self.assertIs(quiz.true_for_all(tree), expect)

#     def test_true_for_all_03(self):
#         tree = ('<', ('>', 4, 3), ('>', ('>', 7, 5), 2))
#         expect = False
#         self.assertIs(quiz.true_for_all(tree), expect)
#         tree = ('<', ('>', 4, 3), ('>', ('>', 7, 6), 5))
#         expect = True
#         self.assertIs(quiz.true_for_all(tree), expect)

#     def test_true_for_all_04(self):
#         tree = ('<', ('>', 4, 1), ('<', ('<', 2, 4), 5))
#         expect = False
#         self.assertIs(quiz.true_for_all(tree), expect)

#     def test_true_for_all_05(self):
#         tree = ('<', ('>', 4, 1), ('<', 5, ('<', 7, 6)))
#         expect = False
#         self.assertIs(quiz.true_for_all(tree), expect)

#     def test_true_for_all_06(self):
#         tree = make_tree('<', list(range(100)))
#         expect = True
#         self.assertIs(quiz.true_for_all(tree), expect)
#         self.assertIs(quiz.true_for_all(('<', tree, 0)), False)

#         tree = make_tree('>', list(range(500,-1,-1)))
#         expect = True
#         self.assertIs(quiz.true_for_all(tree), expect)
#         self.assertIs(quiz.true_for_all(('>', tree, 0)), False)


# def make_tree(ineq, nums):
#     n = len(nums)
#     if n == 2:
#         return (ineq, nums[0], nums[1])
#     elif n%3 == 0:
#         return (ineq, nums[0], make_tree(ineq, nums[1:]))
#     elif n%5 == 0:
#         return (ineq, make_tree(ineq, nums[:-1]), nums[-1])
#     else:
#         return (ineq, make_tree(ineq, nums[:n//2]), make_tree(ineq, nums[n//2:]))


# ####################
# ## Problem 12
# ####################

# class TestProblem12(unittest.TestCase):
#     def test_cities_01(self):
#         simple_cases = [([{3}, {1}, {2}], 3, [3, 1, 2]),
#                         ([{1,2,3}, {1,2,3}, {1,2,3}], 3, [1, 2, 3]),
#                         ([{1,2,3}, {1,2}, {1}], 3, [3, 2 ,1]),
#                         ([{1,2}, {1,2}, {1,2}], 3, None),
#                         ([set(), {1,2,3}, {2,3}], 3, None)]
#         for i in range(len(simple_cases)):
#             with self.subTest(test=i):
#                 L, N, expect = simple_cases[i]
#                 self.check_assign_cities(L, N, expect)

#     def test_cities_02(self):
#         L = [{10, 6, 7}, {8, 9, 4}, {8, 9, 5}, {1, 9}, {1, 2, 7},
#              {8, 10, 6}, {2, 4, 6}, {10, 4}, {3}, {8, 2}]
#         N = 10
#         expect = not None
#         self.check_assign_cities(L, N, expect)

#     def test_cities_03(self):
#         L = [{3, 4, 5}, {8, 10, 6}, {10, 5, 6}, {10, 3, 5}, {2, 7},
#              {1, 10, 4}, {3, 4, 6}, {8, 4, 7}, {1, 10, 7}, {10, 7}]
#         N = 10
#         expect = None # no pigeon is able to fly to city 9
#         self.check_assign_cities(L, N, expect)
            
#     def test_cities_04(self):
#         L = [{9, 18, 11}, {2, 19, 12}, {16, 20, 15}, {18, 12, 14}, {13, 6, 7},
#              {1, 10, 19}, {9, 5}, {11, 12}, {11, 3, 20}, {9, 2}, {19, 5, 6},
#              {10, 12, 13}, {18, 10, 5}, {16, 8, 4}, {2, 10, 6}, {17, 10, 3},
#              {10, 11, 13}, {4, 14}, {16, 18}, {11, 4}]
#         N = 20
#         expect = None
#         self.check_assign_cities(L, N, expect)

#     def test_cities_05(self):
#         L = [{16, 20, 14}, {19, 20, 13}, {8, 1}, {17, 10, 6}, {11, 9, 19},
#              {16, 9, 3}, {10, 13, 14}, {2, 13, 6}, {8, 10, 5}, {2, 11},
#              {16, 5, 14}, {16, 3, 20}, {12, 5, 14}, {2, 20, 15}, {2, 13, 15},
#              {16, 4, 5}, {1, 2, 20}, {11, 20, 5}, {18, 4, 12}, {16, 13, 7}]
#         N = 20
#         expect = not None
#         self.check_assign_cities(L, N, expect)

#     def skip_test_cities_06(self):
#         # Slow if optimization not present.
#         # Even then, may take a very long time depending on how recursion is ordered.
#         L = [{33, 3, 17, 49, 25, 27}, {32, 38, 20, 23, 26, 31}, {33, 9, 14, 49, 19},
#              {35, 7, 40, 39, 46, 17}, {5, 7, 10, 44, 47, 20}, {36, 7, 22, 23, 28, 31},
#              {36, 40, 41, 14, 21, 31}, {1, 34, 4, 36, 17, 29}, {6, 41, 43, 46, 47, 26},
#              {32, 1, 40, 47, 16, 22}, {37, 5, 13, 46, 15, 21}, {35, 6, 10, 16, 29},
#              {32, 33, 36, 7, 20, 21}, {35, 36, 8, 46, 19, 22}, {36, 38, 39, 14, 19, 29},
#              {37, 6, 39, 16, 21, 25}, {3, 40, 12, 13, 19}, {5, 6, 43, 44, 17, 31},
#              {3, 6, 9, 10, 45, 49}, {34, 35, 44, 46, 18, 26}, {34, 38, 44, 14, 16, 27},
#              {32, 38, 42, 43, 18, 29}, {6, 40, 8, 45, 21, 23}, {32, 38, 41, 13, 16, 22},
#              {2, 8, 46, 47, 15, 18}, {4, 7, 11, 22, 24, 28}, {3, 37, 41, 10, 45, 15},
#              {2, 35, 5, 39, 8, 44}, {37, 39, 8, 41, 13, 26}, {2, 3, 6, 39, 8, 24},
#              {8, 12, 13, 46, 14, 31}, {2, 35, 4, 44, 47, 28}, {5, 7, 40, 15, 17},
#              {4, 42, 12, 20, 23, 28}, {33, 3, 7, 39, 45, 30}, {13, 47, 17, 23, 26, 31},
#              {37, 11, 44, 45, 14, 50}, {34, 4, 11, 44, 22}, {39, 8, 43, 12, 17, 29},
#              {1, 33, 37, 44, 27, 31}, {42, 43, 17, 20, 23, 25}, {1, 36, 10, 45, 48, 30},
#              {35, 3, 6, 48, 18, 22}, {40, 9, 16, 49, 23, 31}, {38, 40, 41, 44, 19, 23},
#              {9, 46, 48, 20, 25, 27}, {1, 6, 39, 42, 13, 45}, {41, 11, 15, 16, 22, 29},
#              {3, 37, 44, 46, 25, 27}, {37, 43, 45, 50, 26, 27}]
#         N = 50
#         expect = not None
#         self.check_assign_cities(L, N, expect)
        
#     def skip_test_cities_07(self):
#         # worst-case search test: requires optimization to finish in reasonable time.
#         # Even then, may take a very long time depending on how recursion is ordered.
#         L = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
#              {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, {1, 2, 3, 4, 5, 6, 7, 8, 9},
#              {1, 2, 3, 4, 5, 6, 7, 8}, {1, 2, 3, 4, 5, 6, 7}, {1, 2, 3, 4, 5, 6},
#              {1, 2, 3, 4, 5}, {1, 2, 3, 4}, {1, 2, 3}, {1, 2}, {1}]
#         N = 20
#         expect = not None
#         self.check_assign_cities(L, N, expect)

#     def skip_test_cities_08(self):
#         # worst-case search test: requires optimization to finish in reasonable time.
#         # Even then, may take a very long time depending on how recursion is ordered.
#         L = [{3, 17, 49, 25, 27}, {32, 33, 20, 26, 31}, {33, 38, 9, 14, 23}, {7, 40, 9, 49, 19},
#              {35, 39, 10, 46, 17}, {5, 7, 44, 47, 20}, {36, 7, 22, 23, 31}, {40, 41, 14, 21, 28},
#              {34, 36, 17, 29, 31}, {1, 4, 36, 6, 47}, {1, 41, 43, 46, 26}, {32, 40, 47, 16, 22},
#              {37, 5, 13, 46, 21}, {35, 10, 15, 16, 29}, {32, 33, 21, 6}, {36, 7, 46, 19, 20},
#              {35, 36, 8, 14, 22}, {36, 38, 39, 19, 29}, {37, 6, 39, 21, 25}, {16, 19, 12, 13},
#              {3, 40, 43, 17, 31}, {5, 6, 9, 44, 49}, {35, 3, 6, 10, 45}, {34, 44, 46, 18, 26},
#              {34, 38, 44, 14, 16}, {32, 38, 18, 27, 29}, {6, 42, 43, 45, 23}, {32, 38, 40, 8, 21},
#              {2, 41, 13, 16, 22}, {8, 46, 15, 47, 18}, {4, 11, 22, 24, 28}, {3, 7, 10, 45, 15},
#              {35, 37, 39, 41, 44}, {2, 5, 8, 41, 13}, {37, 6, 39, 8, 26}, {2, 3, 39, 8, 24},
#              {8, 12, 13, 46, 31}, {2, 4, 44, 14, 47}, {35, 7, 40, 17, 28}, {42, 20, 5, 15},
#              {33, 4, 12, 23, 28}, {3, 7, 39, 45, 30}, {13, 47, 17, 23, 26}, {37, 11, 44, 45, 31},
#              {4, 11, 44, 14, 50}, {34, 8, 11, 17, 22}, {1, 39, 43, 12, 29}, {33, 37, 44, 27, 31},
#              {42, 43, 20, 23, 25}, {1, 36, 10, 45, 17}]
#         N = 50
#         expect = None
#         self.check_assign_cities(L, N, expect)
        
#     def legal_assignment(self, L, result):
#         # defend against ill-formed results
#         self.assertIsInstance(result, list)
#         assigned = set()
#         for i, city in enumerate(result):
#             # defend against ill-formed results
#             self.assertIsInstance(city, int)
#             # person must be willing to do city
#             self.assertIn(city, L[i])
#             # city has already been assigned to another
#             self.assertNotIn(city, assigned)
#             assigned.add(city)
#         # check if all citys were assigned
#         self.assertEqual(len(set(assigned)), len(L))

#     def check_assign_cities(self, L, N, expect):
#         LL =[{e for e in p} for p in L]
#         result = quiz.assign_cities(LL, N)
#         if expect:
#             self.legal_assignment(L, result)
#         else:
#             self.assertIsNone(result)

# ####################
# ## Problem 13
# ####################

# class TestProblem13(unittest.TestCase):
#     def test_flood_fill_01(self):
#         img =    {'height': 1, 'width': 3, 'pixels': [ 0,  0, 255]}
#         expect = {'height': 1, 'width': 3, 'pixels': [12, 12, 255]}
#         result = quiz.flood_fill(img, (0, 1), 12)
#         self.assertDictEqual(expect, result)

#     def test_flood_fill_02(self):
#         pix = [ 0,  0, 255, 0]
#         img =    {'height': 4, 'width': 1, 'pixels': pix[:]}
#         expect = {'height': 4, 'width': 1, 'pixels': [12, 12, 255, 0]}
#         result = quiz.flood_fill(img, (1, 0), 12)
#         self.assertDictEqual(expect, result)

#         img_check = {'height': 4, 'width': 1, 'pixels': pix[:]}
#         self.assertDictEqual(img, img_check, msg="original image has been changed (should not be)")

#     def test_flood_fill_03(self):
#         img = {'height': 3, 'width': 3, 'pixels': [0, 255, 0, 255, 255, 255, 0, 255, 0]}
#         expect = {'height': 3, 'pixels': [0, 12, 0, 12, 12, 12, 0, 12, 0], 'width': 3}
#         result = quiz.flood_fill(img, (0, 1), 12)
#         self.assertDictEqual(expect, result)

#     def test_flood_fill_04(self):
#         img = {'height': 3, 'width': 3, 'pixels': [0, 0, 1, 0, 1, 0, 1, 0, 0]}
#         expect = {'height': 3, 'width': 3, 'pixels': [0, 0, 12, 0, 1, 0, 1, 0, 0]}
#         result = quiz.flood_fill(img, (0, 2), 12)
#         self.assertDictEqual(expect, result)

#     def test_flood_fill_05(self):
#         img = {'height': 3, 'width': 4, 'pixels': [0, 0, 1, 0,
#                                                    1, 0, 1, 0,
#                                                    1, 0, 0, 1]}
#         expect = {'height': 3, 'width': 4, 'pixels': [0, 0, 12, 0,
#                                                       1, 0, 12, 0,
#                                                       1, 0,  0, 1]}
#         result = quiz.flood_fill(img, (0, 2), 12)
#         self.assertDictEqual(expect, result)

#     def test_flood_fill_06(self):
#         img = {'height': 3, 'width': 4, 'pixels': [0, 0, 1, 0,
#                                                    1, 0, 1, 0,
#                                                    1, 0, 0, 1]}
#         expect = {'height': 3, 'width': 4, 'pixels': [12, 12,  1, 0,
#                                                        1, 12,  1, 0,
#                                                        1, 12, 12, 1]}
#         result = quiz.flood_fill(img, (0, 0), 12)
#         self.assertDictEqual(expect, result)
        
#     def test_flood_fill_07(self):
#         self.maxDiff = None
#         img1 = {'height': 4, 'width': 8, 'pixels': [0, 255, 255, 0, 0, 0, 255, 0,
#                                                     0, 0, 255, 0, 0, 0, 255, 0,
#                                                     0, 0, 255, 255, 255, 0, 255, 0,
#                                                     0, 0, 0, 0, 0, 0, 0, 255]}
#         expect1 = {'height': 4, 'width': 8, 'pixels': [0, 155, 155, 0, 0, 0, 255, 0,
#                                                        0, 0, 155, 0, 0, 0, 255, 0,
#                                                        0, 0, 155, 155, 155, 0, 255, 0,
#                                                        0, 0, 0, 0, 0, 0, 0, 255]}
#         result1 = quiz.flood_fill(img1, (1, 2), 155)
#         self.assertDictEqual(expect1, result1)

#         img2 = {'height': 4, 'width': 8, 'pixels': [0, 255, 255, 0, 0, 0, 255, 0,
#                                                     0, 0, 255, 0, 0, 0, 255, 0,
#                                                     0, 0, 255, 255, 255, 0, 255, 0,
#                                                     0, 0, 0, 0, 0, 0, 0, 255]}
#         expect2 = {'height': 4, 'width': 8, 'pixels': [155, 255, 255, 155, 155, 155, 255, 0,
#                                                        155, 155, 255, 155, 155, 155, 255, 0,
#                                                        155, 155, 255, 255, 255, 155, 255, 0,
#                                                        155, 155, 155, 155, 155, 155, 155, 255]}
#         result2 = quiz.flood_fill(img2, (0, 0), 155)
#         self.assertDictEqual(expect2, result2)

# ##################################################
# ##  test setup
# ##################################################

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
