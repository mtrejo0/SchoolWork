import unittest, pickle, marshal, types, json
import quiz as quiz
from quiz import Tree

##################################################
#  Problem 1
##################################################

class TestProblem1(unittest.TestCase):
    @staticmethod
    def _load_tree(f_name):
        with open("test_inputs/{}".format(f_name),"rb") as handle:
            tree = pickle.load(handle)
        return tree

    def test_01(self):
        """ Tests that a correct line tree is marked as valid"""
        valid_line = Tree("black", Tree("black", Tree("blue", Tree("blue"))))
        self.assertIs(quiz.validate(valid_line), True)

    def test_02(self):
        """ Tests that a small correct tree is marked as valid"""
        small_valid_tree = Tree("black",
                                Tree("black",
                                     Tree(
                                         "blue",
                                     )
                                     ),
                                Tree("black",
                                     Tree(
                                         "blue",
                                         Tree("blue",
                                              Tree("black")
                                              )
                                     )

                                     )
                                )
        self.assertIs(quiz.validate(small_valid_tree), True)

    def test_03(self):
        """ Tests that a small incorrect tree is marked as invalid"""
        small_invalid_tree = Tree("blue",
                                  Tree("blue",
                                       Tree(
                                           "black",
                                           Tree("black")
                                       )
                                       ),
                                  Tree("blue",
                                       Tree(
                                           "blue",
                                           Tree("blue",
                                                Tree("black")
                                                )
                                       )

                                       )
                                  )
        self.assertIs(quiz.validate(small_invalid_tree), False)

    def test_04(self):
        """ Tests that a medium-sized correct tree is marked as valid"""
        medium_valid_tree = self._load_tree("medium_valid.pickle")
        self.assertIs(quiz.validate(medium_valid_tree), True)

    def test_05(self):
        """ Tests that a medium-sized incorrect tree is marked as invalid"""
        medium_invalid_tree = self._load_tree("medium_invalid.pickle")
        self.assertIs(quiz.validate(medium_invalid_tree), False)

    def test_06(self):
        """ Tests that a medium-large-sized incorrect tree is marked as invalid"""
        medium_large_invalid_tree = self._load_tree("medium_large_invalid.pickle")
        self.assertIs(quiz.validate(medium_large_invalid_tree), False)

    def test_07(self):
        """ Tests that a larged-sized full correct tree is marked as valid"""
        large_valid_tree = self._load_tree("large_valid.pickle")
        self.assertIs(quiz.validate(large_valid_tree), True)

##################################################
#  Problem 2
##################################################

checker = types.FunctionType(marshal.loads(open('resources/checker','rb').read()), globals())

class TestProblem2(unittest.TestCase):

    def validate_possible(self, n, init_bishop_locs, target):
        result = quiz.n_bishops(n, init_bishop_locs, target)
        self.assertTrue(result is not None)
        self.assertTrue(isinstance(result, set))
        self.assertTrue(len(result) >= target)
        self.assertTrue(init_bishop_locs.issubset(result))
        self.assertTrue(
            all(((0 <= r < n) and (0 <= c < n) and isinstance(r, int) and isinstance(c, int) for r, c in result)))
        self.assertTrue(checker(n, result))

    def validate_impossible(self, n, init_bishop_locs, target):
        self.assertEqual(quiz.n_bishops(n, init_bishop_locs, target), None)

    def test_01(self):
        """n=3 initially empty board -> possible"""
        self.validate_possible(3, set(), 4)

    def test_02(self):
        """n=4 initially partially filled board -> possible"""
        self.validate_possible(4, {(3, 0), (3, 2), (0, 2)}, 6)

    def test_03(self):
        """n=4 initially partially filled board -> impossible"""
        self.validate_impossible(4, {(3, 0), (3, 2), (0, 2)}, 7)

    def test_04(self):
        """n=13 initially partially filled board -> impossible"""
        self.validate_impossible(13,
                                 {(12, 2), (11, 7), (4, 9), (8, 2), (11, 6), (5, 11), (3, 3), (8, 11), (5, 7), (11, 12),
                                  (0, 11), (4, 3), (12, 9), (12, 3), (5, 3)}, 20)

    def test_05(self):
        """n=18 initially partially filled board -> possible"""
        self.validate_possible(18, 
                                    {(17, 4), (0, 1), (9, 13), (6, 8), (17, 9), (3, 1), 
                                    (0, 13), (7, 13), (17, 12), (0, 9)}, 30)

    def test_06(self):
        """n=25 initially partially filled board -> possible"""
        self.validate_possible(25, 
                                    {(23, 4), (23, 19), (5, 10), (22, 24), (22, 15), (0, 6),
                                     (22, 4), (10, 24), (14, 15), (4, 3), (6, 15), (20, 15), (15, 5), (13, 10)}, 39)

#################################################
 # Problem 3
##################################################

class TestProblem3(unittest.TestCase):
    def _test_insert_with_file(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        points = set(zip(data['x'], data['y']))
        width = data['width']
        height = data['height']
        quadtree = quiz.QuadTree(0, 0, width, height)
        self._test_insert(quadtree, points)

    def _test_insert(self, quadtree, points):
        for point in points:
            quadtree.insert(point)

        # validate quadtree structure
        is_valid, message = self._is_valid(quadtree)
        self.assertTrue(is_valid, message) #
        if isinstance(points, list):
            points = set(points)
        # check to make sure all points were added
        self.assertEqual(sorted(points), sorted(self._get_all(quadtree)), "All points different from inserted points")
        for point in points:
            self.assertTrue(self._find_point(quadtree, point), "Cannot find point {} in quadtree".format(point))

    # Retrieves all points in this quadtree
    def _get_all(self, quadtree):
        points = []
        if quadtree.children is not None:
            for child in quadtree.children:
                points.extend(self._get_all(child))
        else:
            points = list(quadtree.points)
        return points

    # Checks if this quadtree is valid (follows the invariants listed at the top)
    def _is_valid(self, quadtree):
        # Checks if the ranges are valid
        if quadtree.x_start > quadtree.x_end or quadtree.y_start > quadtree.y_end:
            return False, "Node has invalid range"

        # If the quadtree has children, it should have four
        if quadtree.children is not None and len(quadtree.children) == 4:
            # Check that the children do not overlap
            for c1 in quadtree.children:
                for c2 in quadtree.children:
                    if c1 is not c2 and not (c1.x_start >= c2.x_end or c2.x_start >= c1.x_end \
                                or c1.y_start >= c2.y_end or c2.y_start >= c1.y_end):
                        return False, "Children ranges overlap"

            # Check that its children are also valid recursively
            for child in quadtree.children:
                if not self._is_valid(child):
                    return False, "Child node is not valid"

            # Check that it doesn't have any points
            if quadtree.points is not None:
                return False, "Non-leaf node cannot have points"

        elif quadtree.children is None:
            # Should have four or less points
            if len(quadtree.points) > 4:
                return False, "Leaf node should have 4 or less points"

            # Points should be in range
            for (x, y) in quadtree.points:
                if x < quadtree.x_start or x >= quadtree.x_end or y < quadtree.y_start or y >= quadtree.y_end:
                    return False, "Point should be in range of the node's range"
        else:
            return False, "Non-leaf node does not have 4 children"

        return True, "Success!"

    def _find_point_in_quadtree(self, q, point):
        """
        Returns True if point exists in the quadtree
        :param point: point (x, y) to find
        """
        x, y = point
        if q.children is not None:
            for c in q.children:
                # If a child's range includes the point, recurse into this child
                if x >= c.x_start and x < c.x_end and y >= c.y_start and y < c.y_end:
                    return self._find_point_in_quadtree(c, point)
        else:
            # If the quadtree doesn't have children, we can check for the point
            if point in q.points:
                return True
            else:
                return False

    def _find_point(self, quadtree, point):
        x, y = point
        if quadtree.children is not None:
            for c in quadtree.children:
                # If a child's range includes the point, recurse into this child
                if x >= c.x_start and x < c.x_end and y >= c.y_start and y < c.y_end:
                    return self._find_point_in_quadtree(c, point)
        else:
            # If the quadtree doesn't have children, we can check for the point
            if point in quadtree.points:
                return True
            else:
                return False

    def test_01(self):
        width = 5
        height = 5
        quadtree = quiz.QuadTree(0, 0, width, height)
        points = {(0, 0), (2, 4)}
        self._test_insert(quadtree, points)

    def test_02(self):
        width = 10
        height = 20
        quadtree = quiz.QuadTree(0, 0, width, height)
        points = {(7, 6), (6, 8), (8, 9), (9, 6), (5, 2)}
        self._test_insert(quadtree, points)

    def test_03(self):
        width = 5
        height = 10
        quadtree = quiz.QuadTree(0, 0, width, height)
        points = [(0, 1), (0, 1), (2, 3), (1, 8), (2, 3)]
        self._test_insert(quadtree, points)

    def test_04(self):
        self._test_insert_with_file('test_inputs/insert_quadtree_many_points_small_rectangle.json')

    def test_05(self):
        self._test_insert_with_file('test_inputs/insert_quadtree_small.json')

    def test_06(self):
        self._test_insert_with_file('test_inputs/insert_quadtree_medium.json')

    def test_07(self):
        self._test_insert_with_file('test_inputs/insert_quadtree_large.json')

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
