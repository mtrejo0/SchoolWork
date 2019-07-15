#!/usr/bin/env python3
import os
import ast
import quiz
import types
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

class TestProblem1(unittest.TestCase):
    def _test_from_file(self, n):
        with open(os.path.join(TEST_DIRECTORY, 'test_outputs', 'songs_%02d.py' % n), 'r') as f:
            (songs, target, valid) = ast.literal_eval(f.read())
        result = quiz.mix_tape(dict(songs), target)
        if valid:
            self.assertNotEqual(result, None)
            self._test_valid(songs, target, result)
        else:
            self.assertEqual(result, None)

    def _test_valid(self, songs, target, result):
        self.assertEqual(len(result), len(set(result)))
        self.assertTrue(all(s in songs for s in result))
        self.assertEqual(sum(songs[i] for i in result), target)

    def test_00_examples(self):
        songs = {'A': 5, 'B': 10, 'C': 6, 'D': 2}
        self._test_valid(songs, 11, quiz.mix_tape(songs, 11))
        self.assertEqual(quiz.mix_tape(songs, 1000), None)
        self._test_valid(songs, 21, quiz.mix_tape(songs, 21))

    def test_01(self):
        for i in range(1, 6):
            self._test_from_file(i)

    def test_02(self):
        for i in range(6, 11):
            self._test_from_file(i)

    def test_03(self):
        for i in range(11, 16):
            self._test_from_file(i)

    def test_04(self):
        for i in range(16, 21):
            self._test_from_file(i)

    def test_05(self):
        for i in range(21, 26):
            self._test_from_file(i)


#############
# Problem 2 #
#############

class TestProblem2(unittest.TestCase):
    def verify_all(self, seq, k, expected):
        result_gen = quiz.k_mins(seq[:], k)
        self.assertIsInstance(result_gen, types.GeneratorType, msg="k_mins should return a generator!")
        msg = "for sequence of length "+str(len(seq))+" starting with "+str(seq[:5])[1:-1]+"... with k = "+str(k)
        self.assertEqual(expected, list(result_gen), msg=msg)

    def verify_nth(self, seq, k, n, expected):
        result_gen = quiz.k_mins(seq, k)
        self.assertIsInstance(result_gen, types.GeneratorType, msg="k_mins should return a generator!")
        msg = "for sequence of length "+str(len(seq))+" starting with "+str(seq[:5])[1:-1]+"... with k = "+str(k)
        count = 0
        for result_elt in result_gen:
            if count == n:
                self.assertEqual(result_elt, expected, msg=msg)
                return
            count += 1
        raise IndexError("Can't get elt "+str(n)+"; only "+str(count)+" elts in result generator!")

    def test_00_examples(self):
        # Examples; check all values correctly yielded
        cases = [([1, 4, 5, 3, 4, 2], 1, [1, 3, 2]),
                 ([1, 4, 5, 3, 4, 2], 2, [1, 2]),
                 ([7, 6, 3, 4, 5], 2, [3]),
                 ([5, 4, 3, 4, 5], 0, [5, 4, 3, 4, 5]),
                 ([8, 9], 5, [8]),
                 ([], 2, []),
                 ([7, 4, 5, 6, 1, 5, 6, 4, 7, 8], 2, [4, 1, 4]),
                 ]
        for seq, k, expected in cases:
            self.verify_all(seq, k, expected)

    def test_01(self):
        # Other cases; check all values correctly yielded
        cases = [
            ((65, 47, 56, 187, 89, 45, 24, 148, 72, 86, 110, 79, 28, 40, 74, 199, 13, 19, 96, 128), 0,
             [65, 47, 56, 187, 89, 45, 24, 148, 72, 86, 110, 79, 28, 40, 74, 199, 13, 19, 96, 128]) ,
            ((127, 160, 155, 167, 76, 26, 68, 79, 160, 161, 91, 156, 51, 51, 166, 54, 172, 194, 143, 70), 1,
             [127, 155, 26, 91, 51, 51, 54, 70]) ,
            ((165, 84, 161, 157, 22, 3, 113, 77, 88, 132, 121, 148, 86, 191, 139, 190, 70, 46, 102, 70), 2, [84, 3, 86, 46]) ,
            ((71, 109, 60, 10, 123, 189, 125, 44, 10, 109, 106, 113, 146, 76, 92, 199, 113, 12, 42, 184), 3, [10, 10, 76, 12]) ,
            ((47, 145, 139, 190, 100, 93, 96, 83, 133, 158, 51, 143, 70, 80, 34, 106, 92, 191, 19, 139), 4, [47, 19]) ,
            ((194, 166, 159, 156, 157, 156, 133, 58, 78, 155, 114, 103, 61, 43, 39, 87, 9, 11, 194, 36), 5, [58, 9]) ,
            ((10, 54, 99, 182, 125, 21, 147, 47, 68, 78, 137, 198, 19, 6, 29, 89, 175, 154, 46, 163), 6, [10, 6]) ,
            ((21, 76, 101, 38, 53, 177, 117, 114, 163, 83, 147, 192, 107, 160, 19, 37, 91, 145, 29, 66), 7, [21, 19]) ,
            ((75, 143, 198, 110, 113, 24, 142, 131, 47, 39, 145, 57, 30, 44, 139, 71, 113, 37, 164, 60), 8, [24]) ,
            ((140, 18, 112, 195, 39, 130, 98, 20, 19, 32, 49, 85, 85, 195, 26, 157, 61, 154, 47, 84), 9, [18]) ,
            ((192, 170, 71, 10, 190, 98, 188, 44, 175, 44, 192, 151, 167, 163, 196, 193, 54, 126, 73, 104), 10, [10]) ,
            ((113, 191, 104, 73, 14, 107, 166, 115, 64, 78, 136, 35, 101, 42, 194, 96, 12, 111, 109, 134), 11, [14, 12]) ,
            ((144, 106, 81, 179, 18, 33, 97, 101, 74, 193, 164, 68, 54, 117, 172, 61, 191, 141, 122, 176), 12, [18]) ,
            ((199, 98, 9, 60, 54, 92, 39, 25, 192, 161, 148, 10, 138, 49, 182, 176, 178, 164, 133, 29), 13, [9]) ,
            ((25, 57, 110, 51, 44, 149, 148, 147, 106, 165, 104, 108, 154, 21, 133, 100, 87, 39, 200, 74), 14, [21]) ,
            ]
        for seq, k, expected in cases:
            self.verify_all(seq, k, expected)

    def test_02(self):
        # small sequence; yield nth
        seq = (4,)*5 + (1,1) + (5,)*4
        k = 6; n = 1; expected = 1
        self.verify_nth(seq, k, n, expected)

        # Other cases; check nth value correctly yielded
        cases = [((55, 55, 35, 35, 35, 65, 82, 82, 82, 16, 16, 25, 14, 14, 17, 86, 86, 97, 97), 0, 4, 35) ,
                 ((87, 87, 6, 65, 65, 65, 16, 16, 16, 54, 54, 54, 67, 67, 76, 76, 76, 61, 61, 65, 65, 65, 22), 1, 3, 16) ,
                 ((93, 93, 15, 15, 15, 61, 61, 42, 42, 48, 48, 55, 55, 73, 81, 32, 32, 32, 79, 79, 79), 2, 1, 15) ,
                 ((62, 31, 31, 31, 91, 73, 66, 66, 66, 0, 0, 0, 76, 76, 13, 13, 43, 100), 3, 3, 0) ,
                 ((69, 69, 70, 15, 15, 15, 19, 19, 64, 64, 26, 26, 26, 87, 87, 87, 49, 49, 4, 4, 4, 29), 4, 2, 15) ,
                 ((19, 19, 19, 14, 14, 84, 84, 84, 53, 61, 61, 27, 7, 12, 64, 52, 52), 5, 2, 7) ,
                 ((54, 54, 54, 61, 3, 3, 3, 76, 76, 76, 56, 56, 68, 82, 76, 76, 76, 6, 6, 38), 6, 1, 3) ,
                 ((35, 35, 22, 93, 93, 93, 65, 36, 36, 94, 94, 78, 78, 6, 6, 40, 40, 39, 39), 7, 2, 6) ,
                 ((83, 83, 99, 99, 99, 46, 16, 16, 90, 90, 90, 2, 2, 2, 28, 28, 28, 51, 17, 63, 63, 63), 8, 2, 2) ,
                 ((83, 64, 15, 15, 15, 17, 82, 82, 82, 45, 45, 36, 36, 2, 2, 85, 85, 49), 9, 3, 2) ,
                 ((29, 79, 79, 68, 13, 13, 95, 62, 76, 35, 42, 42, 90), 10, 1, 13) ,
                 ((47, 47, 47, 71, 89, 89, 89, 89, 89, 89, 4, 4, 4, 54, 33, 33, 79, 79, 79, 77, 77, 10, 10, 10), 11, 1, 4) ,
                 ((55, 55, 55, 91, 87, 2, 2, 2, 89, 89, 89, 48, 76, 63, 63, 70, 70, 70, 18, 18), 12, 1, 2) ,
                 ((18, 18, 31, 31, 9, 58, 97, 97, 47, 55, 55, 0, 0, 64, 94, 94), 13, 1, 0) ,
                 ((57, 57, 18, 18, 18, 27, 27, 80, 80, 86, 86, 86, 78, 78, 78, 36, 9, 9, 9, 18, 18, 57), 14, 2, 9) ,
                 ]
        for seq, k, n, expect in cases:
            self.verify_nth(seq, k, n, expect)

    def test_03(self):
        # big sequence, big k
        #
        size = 5000
        seq = [x%20 for x in range(size)]
        k = size//2
        expect = [0]*(size//20)
        self.verify_all(seq, k, expect)

    def test_04(self):
        # Bigger case
        #
        size = 2500
        seq = list(range(35, size))+list(range(size, 0, -1))
        expect = [35, 0]
        cases = [(0, seq),
                 (1, [35, 1]),
                 (2, [35, 1]),
                 (20, [35, 1]),
                 (size//2, [35, 1]),
                 (size, [35, 1]),
                 (size*2, [1]),
                ]
        for k, expected in cases:
            self.verify_all(seq, k, expected)

    def test_05(self):
        # Very big sequence, big k, yield nth
        size = 200000
        seq = (8,)*(size)
        k = size//2; n = 5; expected = 8
        self.verify_nth(seq, k, n, expected)

        # Very big sequence, small k, yield nth
        seq = (12, 10, 10, 11, 10, 17,) + seq; k = 2; n = 1; expected = 10
        self.verify_nth(seq, k, n, expected)


#############
# Problem 3 #
#############

class TestProblem3(unittest.TestCase):
    def test_00_example(self):
        inp = [[' ', 'S', ' '],
               ['G', 'X', ' '],
               [' ', ' ', ' '],
               [' ', ' ', 'X']]
        expected = 8
        self.assertEqual(quiz.scenic_route(inp), expected)

    def test_01(self):
        inp = [[' ', ' ', ' ', 'X'],
               ['X', ' ', 'X', ' '],
               [' ', ' ', 'G', ' '],
               [' ', 'X', ' ', 'X'],
               [' ', 'X', ' ', 'S'],
               ['X', 'X', 'X', ' ']]
        expected = 3
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' '],
               [' ', 'X', ' ', ' ', ' ', 'X', ' ', 'X', ' '],
               [' ', ' ', ' ', ' ', 'X', 'G', ' ', ' ', 'X'],
               [' ', ' ', ' ', 'X', ' ', ' ', 'S', ' ', 'X']]
        expected = 4
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', 'X', ' '],
               [' ', 'X', ' ', 'X'],
               ['G', ' ', ' ', 'S'],
               [' ', ' ', ' ', 'X']]
        expected = 5
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', 'S', ' '],
               [' ', ' ', ' ', 'G'],
               ['X', ' ', 'X', 'X'],
               ['X', 'X', 'X', 'X'],
               [' ', ' ', ' ', 'X'],
               ['X', 'X', 'X', ' '],
               [' ', ' ', ' ', ' '],
               [' ', ' ', 'X', ' '],
               ['X', ' ', 'X', ' '],
               [' ', 'X', ' ', ' ']]
        expected = 6
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'G', ' ', 'X', ' '],
               ['S', ' ', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', ' '],
               [' ', 'X', ' ', ' ', ' '],
               ['X', ' ', ' ', ' ', 'X']]
        expected = 6
        self.assertEqual(quiz.scenic_route(inp), expected)

    def test_02(self):
        inp = [[' ', ' ', 'X', 'X'],
               ['X', 'X', ' ', ' '],
               [' ', ' ', ' ', 'X'],
               ['X', 'X', 'X', ' '],
               [' ', ' ', ' ', ' '],
               [' ', 'X', ' ', ' '],
               ['X', ' ', ' ', ' '],
               ['X', 'G', ' ', ' '],
               [' ', 'X', ' ', ' '],
               [' ', 'X', 'X', ' '],
               ['X', 'X', ' ', 'X'],
               [' ', 'X', 'X', ' '],
               [' ', ' ', ' ', ' '],
               [' ', ' ', ' ', ' '],
               ['X', 'X', ' ', 'X'],
               ['X', ' ', 'X', 'S'],
               ['X', ' ', ' ', 'X']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', ' ', 'X'],
               [' ', 'X', ' ', 'S', ' '],
               [' ', 'X', 'X', ' ', 'X'],
               ['X', ' ', 'X', ' ', ' '],
               ['X', ' ', ' ', ' ', ' '],
               ['X', ' ', 'X', ' ', 'X'],
               [' ', ' ', ' ', ' ', 'X'],
               [' ', 'X', ' ', ' ', ' '],
               ['X', 'X', ' ', ' ', 'X'],
               [' ', ' ', 'X', ' ', 'X'],
               [' ', ' ', ' ', 'X', 'X'],
               [' ', 'G', 'X', 'X', ' '],
               ['X', 'X', 'X', 'X', ' ']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', ' ', 'X', ' ', 'X', 'X', ' '],
               [' ', 'X', ' ', ' ', ' ', 'X', 'X', ' ', ' '],
               [' ', 'X', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
               [' ', ' ', ' ', 'X', 'X', ' ', 'X', ' ', ' '],
               ['X', ' ', ' ', ' ', 'X', ' ', 'X', ' ', 'X'],
               ['S', 'X', ' ', 'X', ' ', ' ', 'X', ' ', 'X'],
               ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['X', ' ', ' ', 'X', 'X', ' ', 'X', ' ', ' '],
               [' ', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' '],
               ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
               ['G', 'X', ' ', ' ', ' ', 'X', ' ', ' ', 'X']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', 'X', ' ', ' ', ' ', ' ', 'X', 'G'],
               [' ', ' ', ' ', 'X', 'X', ' ', ' ', 'X', 'X'],
               ['X', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' '],
               ['X', ' ', ' ', 'X', ' ', ' ', 'S', ' ', ' '],
               [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'X', 'X', ' ', 'X', ' ', ' ', ' ', ' ']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', ' ', 'X'],
               ['X', ' ', 'X', 'X', 'X'],
               [' ', ' ', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', 'X'],
               ['S', 'G', ' ', ' ', 'X'],
               ['X', ' ', 'X', 'X', ' '],
               ['X', 'X', ' ', 'X', ' '],
               [' ', ' ', 'X', ' ', ' '],
               [' ', 'X', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', ' ']]
        expected = 11
        self.assertEqual(quiz.scenic_route(inp), expected)

    def test_03(self):
        inp = [['X', ' ', 'S', 'X', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', ' ', 'X', 'X'],
               [' ', ' ', ' ', 'X', 'X', ' ', ' '],
               ['G', 'X', ' ', 'X', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', ' ', 'X', ' ']]
        expected = 12
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [['X', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' '],
               [' ', 'X', ' ', ' ', ' ', 'X', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', 'X', ' ', 'X', ' ', ' '],
               [' ', ' ', ' ', 'X', 'X', ' ', ' ', 'X', ' '],
               [' ', ' ', 'X', 'X', 'X', 'X', ' ', ' ', 'X'],
               ['X', 'X', ' ', 'X', 'X', ' ', 'X', ' ', 'X'],
               ['X', ' ', 'G', 'X', 'X', ' ', ' ', ' ', ' '],
               [' ', ' ', 'S', 'X', ' ', 'X', 'X', ' ', 'X'],
               ['X', ' ', ' ', ' ', ' ', ' ', 'X', 'X', ' '],
               [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', ' ']]
        expected = 13
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'X', ' ', ' '],
               ['S', 'X', ' ', 'G'],
               ['X', 'X', ' ', ' '],
               ['X', ' ', ' ', ' ']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [['X', ' ', ' ', 'X', 'X', 'X'],
               ['G', ' ', 'X', ' ', ' ', ' '],
               [' ', 'X', ' ', 'X', ' ', ' '],
               ['X', ' ', 'X', 'X', ' ', ' '],
               [' ', ' ', 'X', 'S', ' ', ' '],
               [' ', ' ', ' ', ' ', ' ', 'X'],
               ['X', ' ', 'X', ' ', ' ', ' ']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', 'S'],
               ['X', 'X', ' ', ' '],
               [' ', 'X', ' ', ' '],
               [' ', ' ', ' ', ' '],
               [' ', 'X', 'X', ' '],
               ['G', 'X', ' ', ' '],
               [' ', ' ', ' ', 'X'],
               [' ', 'X', ' ', ' ']]
        expected = 14
        self.assertEqual(quiz.scenic_route(inp), expected)

    def test_04(self):
        inp = [[' ', ' ', ' ', ' '],
               ['G', ' ', 'X', 'X'],
               [' ', 'X', ' ', ' '],
               [' ', 'X', ' ', ' '],
               [' ', ' ', 'X', ' '],
               ['X', ' ', ' ', ' '],
               [' ', ' ', ' ', ' '],
               [' ', ' ', 'S', ' '],
               [' ', ' ', 'X', ' ']]
        expected = 16
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'X', 'X', ' ', ' ', 'X', ' ', ' ', 'X', ' '],
               [' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', ' ', 'X'],
               ['G', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
               ['X', 'X', 'S', ' ', ' ', ' ', 'X', 'X', ' ', ' '],
               ['X', ' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', 'X'],
               ['X', ' ', 'X', 'X', ' ', 'X', ' ', ' ', 'X', ' '],
               [' ', ' ', ' ', ' ', ' ', 'X', 'X', ' ', ' ', ' '],
               [' ', 'X', ' ', ' ', 'X', ' ', 'X', 'X', ' ', ' '],
               [' ', ' ', 'X', ' ', 'X', ' ', 'X', 'X', ' ', ' '],
               [' ', ' ', 'X', ' ', 'X', ' ', ' ', 'X', ' ', ' '],
               [' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', 'X', 'X'],
               ['X', 'X', 'X', ' ', ' ', 'X', ' ', ' ', ' ', 'X']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', 'X', 'X', 'X', ' ', ' '],
               [' ', 'X', ' ', 'S', ' ', 'X', ' '],
               ['X', 'X', 'X', ' ', ' ', ' ', ' '],
               [' ', 'X', ' ', ' ', 'X', ' ', 'X'],
               [' ', ' ', 'X', ' ', 'G', ' ', 'X'],
               ['X', ' ', 'X', ' ', ' ', ' ', ' '],
               ['X', 'X', ' ', 'X', ' ', ' ', ' '],
               [' ', ' ', 'X', 'X', 'X', ' ', ' ']]
        expected = 16
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [['X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', ' '],
               [' ', 'X', 'X', ' ', ' ', 'X', ' ', ' ', ' '],
               [' ', 'G', ' ', ' ', ' ', 'X', 'X', ' ', ' '],
               [' ', ' ', ' ', 'X', ' ', 'X', 'X', 'X', ' '],
               [' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ', ' '],
               ['X', ' ', 'X', 'X', ' ', ' ', ' ', 'X', ' '],
               ['X', ' ', 'X', ' ', 'X', 'X', ' ', 'X', 'X'],
               [' ', 'X', 'X', 'S', ' ', 'X', 'X', ' ', ' '],
               [' ', ' ', 'X', ' ', 'X', ' ', ' ', 'X', 'X'],
               ['X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X'],
               [' ', 'X', ' ', ' ', ' ', 'X', 'X', ' ', 'X'],
               [' ', 'X', 'X', ' ', ' ', ' ', 'X', 'X', ' '],
               [' ', ' ', 'X', ' ', ' ', 'X', ' ', 'X', ' ']]
        expected = None
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', 'G', ' '],
               [' ', ' ', ' ', ' ', ' '],
               ['S', ' ', 'X', ' ', ' '],
               [' ', ' ', 'X', ' ', ' ']]
        expected = 17
        self.assertEqual(quiz.scenic_route(inp), expected)

    def test_05(self):
        inp = [[' ', ' ', ' ', 'S', 'X', ' '],
               ['X', ' ', 'X', ' ', 'X', ' '],
               ['X', ' ', ' ', ' ', ' ', ' '],
               ['X', ' ', 'X', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', 'X', 'G'],
               [' ', ' ', ' ', ' ', 'X', 'X'],
               [' ', 'X', ' ', 'X', ' ', ' '],
               ['X', 'X', 'X', ' ', ' ', 'X']]
        expected = 18
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [['X', 'X', ' ', ' '],
               ['X', ' ', ' ', 'X'],
               ['X', 'X', 'X', ' '],
               ['X', ' ', ' ', ' '],
               [' ', 'X', 'X', ' '],
               [' ', 'S', 'X', ' '],
               [' ', ' ', ' ', ' '],
               [' ', 'X', 'X', ' '],
               [' ', ' ', ' ', ' '],
               [' ', ' ', 'X', ' '],
               ['X', ' ', 'X', 'X'],
               [' ', ' ', 'X', ' '],
               [' ', ' ', 'X', ' '],
               ['X', ' ', ' ', 'X'],
               ['X', ' ', ' ', 'G'],
               ['X', 'X', ' ', 'X'],
               [' ', 'X', ' ', ' ']]
        expected = 21
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'X', ' ', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', ' ', 'X'],
               ['X', ' ', ' ', ' ', ' ', 'X'],
               [' ', 'X', 'S', ' ', 'X', ' '],
               [' ', ' ', ' ', ' ', 'X', ' '],
               [' ', ' ', ' ', ' ', 'G', ' '],
               ['X', ' ', ' ', 'X', 'X', ' '],
               [' ', ' ', 'X', ' ', 'X', ' ']]
        expected = 22
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
               [' ', 'G', 'X', 'S', ' ', ' ', ' '],
               [' ', ' ', ' ', 'X', ' ', 'X', ' '],
               [' ', ' ', 'X', 'X', ' ', ' ', 'X'],
               [' ', ' ', ' ', ' ', ' ', ' ', 'X'],
               [' ', 'X', ' ', 'X', 'X', ' ', 'X']]
        expected = 24
        self.assertEqual(quiz.scenic_route(inp), expected)

        inp = [[' ', 'X', ' ', ' ', ' '],
               [' ', 'S', ' ', 'X', 'X'],
               [' ', ' ', ' ', ' ', ' '],
               [' ', ' ', ' ', ' ', ' '],
               ['X', ' ', 'X', ' ', ' '],
               [' ', 'G', ' ', ' ', ' '],
               [' ', ' ', 'X', ' ', ' '],
               [' ', 'X', ' ', ' ', 'X'],
               [' ', ' ', ' ', ' ', ' ']]
        expected = 26
        self.assertEqual(quiz.scenic_route(inp), expected)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
