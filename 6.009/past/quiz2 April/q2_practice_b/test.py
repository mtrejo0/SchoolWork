#!/usr/bin/env python3
import os
import ast
import quiz
import types
import unittest

from copy import deepcopy

TEST_DIRECTORY = os.path.dirname(__file__)


#############
# Problem 1 #
#############

class TestProblem1(unittest.TestCase):
    graph1 = {1: {2, 4, 5},
              2: {1, 8},
              4: {2, 7},
              7: {9},
              9: set(),
              5: {9},
              8: set(),}

    def verify_path(self, graph, start, end, path, expect):
        case = "\n(case: graph = "+repr(graph)+", start = "+str(start)+", end = "+str(end)+")"
        if expect is None:
            self.assertIsNone(path, msg="got a non-None path, where one does not exist"+case)
            return
        else:
            self.assertIsNotNone(path, msg=case)
        self.assertGreater(len(path), 0, msg="expected valid path with at least some nodes"+case)
        for node in path:
            self.assertIn(node, graph, msg="node "+str(node)+" does not exist in graph"+case)
        self.assertEqual(start, path[0], msg="path does not begin with node "+str(start)+case)
        self.assertEqual(end, path[-1], msg="path does not end with node "+str(end)+case)
        for from_node, next_node in zip(path, path[1:]):
            self.assertIn(next_node, graph[from_node],
                          msg="no edge from "+str(from_node)+" to "+str(next_node)+case)
            self.assertGreater(next_node, from_node, msg="node values not in ascending order!"+case)

    def test_01(self):
        g = deepcopy(self.graph1)
        start, end = 2, 2; expect = [2]
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

    def test_02(self):
        g = self.graph1
        start, end = 1, 2; expect = [1, 2]
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

        start, end = 2, 1; expect = None
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

    def test_03(self):
        g = self.graph1
        start, end = 1, 7; expect = [1, 4, 7]
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

        start, end = 2, 7; expect = None
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

        start, end = 4, 8; expect = None
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

    def test_04(self):
        g = self.graph1
        start, end = 1, 9; expect = [1, 4, 7, 9] #or [1, 5, 9]
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

    def test_05(self):
        g = self.graph1
        start, end = 1, 8; expect = [1, 2, 8]
        result = quiz.ascending_path(deepcopy(g), start, end)
        self.verify_path(g, start, end, result, expect)

    def test_06(self):
        # long graph
        start, end = 1, 11
        elts = list(range(start, end+1, 2))
        graph = {}
        for a,b in zip(elts, elts[1:]):
            graph.setdefault(a,set()).add(b)
            graph.setdefault(b,set()).add(a)
        result = quiz.ascending_path(deepcopy(graph), start, end)
        self.verify_path(graph, start, end, result, True)

    def test_07(self):
        # big graph
        start, end = 1, 100*3+1
        elt = list(range(start, end+1, 3))
        graph = {}
        for a,b in zip(elt, elt[1:]):
            graph.setdefault(a,set()).add(b)
            graph.setdefault(b,set()).add(a)
            c = a+1
            graph.setdefault(a,set()).add(c)
            graph.setdefault(c,set()).add(a)
            d = c+1
            graph.setdefault(c,set()).add(d)
            graph.setdefault(d,set()).add(c)
        result = quiz.ascending_path(deepcopy(graph), start, end)
        self.verify_path(graph, start, end, result, True)


#############
# Problem 2 #
#############

# class TestProblem2(unittest.TestCase):
#     def _test_generator(self, inp, expected):
#         result = quiz.split_words(inp)
#         self.assertIsInstance(result, types.GeneratorType, msg="split_words should be a generator")
#         self.assertEqual(set(result), expected)

#     def _test_from_file(self, inp, n):
#         with open(os.path.join(TEST_DIRECTORY, 'test_outputs', 'words_%02d.py' % n), 'r') as f:
#             self._test_generator(inp, ast.literal_eval(f.read()))

#     def test_00(self):
#         self._test_generator('cake', {('cake', )})
#         self._test_generator('iateanicecreamcone', {('i', 'a', 'tea', 'nice', 'cream', 'cone'), ('i', 'ate', 'a', 'nice', 'cream', 'cone'), ('i', 'ate', 'an', 'ice', 'cream', 'cone')})
#         self._test_generator('mycatscaneatcarrots', {('my', 'cat', 'scan', 'eat', 'car', 'rots'), ('my', 'cat', 'scan', 'eat', 'carrots'), ('my', 'cats', 'can', 'eat', 'car', 'rots'), ('my', 'cats', 'can', 'eat', 'carrots'), ('my', 'cats', 'cane', 'at', 'car', 'rots'), ('my', 'cats', 'cane', 'at', 'carrots')})

#     def test_01(self):
#         self._test_from_file('etudeshakewithholdsmansards', 1)

#     def test_02(self):
#         self._test_from_file('redissolvebeseeminggrandeurs', 2)

#     def test_03(self):
#         self._test_from_file('ushersbreaknecktreblingnitrified', 3)
#         self._test_from_file('antennasflameoutnothingstrackless', 4)
#         self._test_from_file('abatersboardingapproveduntanglingcirrus', 5)
#         self._test_from_file('challengetissuesgrippesrivuletsodiumparties', 6)

#     def test_04(self):
#         self._test_from_file('relationsharesabridgetheisticwithinslingshots', 7)
#         self._test_from_file('opensospreytipsgiftedmenmiscallingdisarmsuprooted', 8)
#         self._test_from_file('earningsbrawnsflusmopingyourselfmillinerybicyclistsadrenal', 9)
#         self._test_from_file('unmistakenracefilterintertwinedeepdefrayexaminingherefords', 10)
#         self._test_from_file('semaphoresixpaperingquadrantalbulldozingvelocitypolesolider', 11)
#         self._test_from_file('erstwhilesophisticsocialeagerlyasparagustryingforearmstipple', 12)
#         self._test_from_file('accidentalbailoutenlargebegirtquakerswashroompromotersdroves', 13)
#         self._test_from_file('barbadosmistookannoysbotfliesincubationdetachescatnipicicles', 14)
#         self._test_from_file('hamsterraceapprovesproconsulzonkedwantshadyhearkenamplifyides', 15)
#         self._test_from_file('multilithhikersinstallingsquirelacingswaggeredintendedsyapped', 16)
#         self._test_from_file('buntbrainpansbeardeddashikihelenapageboyssolipsistpatchpippedomaha', 17)
#         self._test_from_file('rethinkaviditiesspearswrenchcapturedaversionspaddlesmisquotespajamas', 18)
#         self._test_from_file('sequinsamericanabilletfrightfultimpanistsavertedivyexactorimmolateddisappointsow', 19)
#         self._test_from_file('intervenedsendingtrimmingpreemptingpersuasionbudgemoochingextortionwhelksjoustbikes', 20)
#         self._test_from_file('federalsunheardtelephonesaliasdepositimbruingartifactspositivecurrentpluralistsullying', 21)
#         self._test_from_file('sportingpackagecheshireyearlyenfiladedstomachingpersistsailshelteringsulkyoleoresinpolio', 22)
#         self._test_from_file('activationemigratethiamineinstincttypesetquoteskindliestapproachedparchmentstenonsadherent', 23)
#         self._test_from_file('stragglypalladiumraspiestplatoonsferrousdeceitsduffersbeaconssuperhumancorvettesaugmentingtallying', 24)
#         self._test_from_file('arcslanderousreptilehotheadedsympathyeulogistichabituatedcorianderbarbarouscoercionpopulaceultimatum', 25)


#############
# Problem 3 #
#############

class TestProblem3A(unittest.TestCase):
    """Test game_status"""

    def test_01(self):
        # Game won by X with initial board
        expect = 'X'

        board = "XXX" + \
                "XOO" + \
                "OOX"
        self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

        board = "OOOXXXOOO"
        self.assertEqual(expect, quiz.game_status(board), msg="Both X and O have three in a row, so X wins")

        cases = ["---XXX---",
                 "X--X--X--",
                 "-X-XX--X-",
                 "XOOOXOOOX",
                 ]
        for board in cases:
            self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

    def test_02(self):
        # Game won by O with initial board
        expect = 'O'

        board = "XXO" + \
                "XOO" + \
                "OOX"
        self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

        cases = ["OOOX-XO-O",
                 "--O-O-O--",
                 ]
        for board in cases:
            self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

    def test_03(self):
        # Tie. No '-' and no three in a row by X or O
        expect = 'T'

        board = "OXX" + \
                "XOO" + \
                "OOX"
        self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

        cases = ["XOXXOOOXX",
                 ]
        for board in cases:
            self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

    def test_04(self):
        # No winner yet, but still have empty square
        expect = '-'

        board = "OXX" + \
                "X-O" + \
                "OOX"
        self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

        cases = ["XOXXOOOX-",
                 ]
        for board in cases:
            self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")

    def test_05(self):
        # Various other cases
        cases =  [('XXOXXOXXX', 'X'), ('XXXOXOXXO', 'X'), ('XO------X', '-'), ('XOO-OO--X', '-'),
                  ('X-XOXXX-X', 'X'), ('OOOOOOXOX', 'O'), ('XXXO-XO-X', 'X'), ('OXOOOXXOX', 'T'),
                  ('---O-XX-X', '-'), ('-O-OXO-OX', '-'), ('-----OOXX', '-'), ('-OOO-XXOX', '-'),
                  ('O-X--X-XX', 'X'), ('XOOOXXOOX', 'X'), ('OO-O-OO-X', 'O'), ('OXX-X---O', '-'),
                  ('---XOO-X-', '-'), ('XXOX-XO-X', '-'), ('XOXXOXXOX', 'X'), ('OOXOXXXXO', 'X'),
                  ('XOOOXXOXX', 'X'), ('XOXXOOOOX', 'O'), ('OOXXX-XX-', 'X'), ('-OOXOOOX-', 'O'),
                  ('OOOOOXOXX', 'O'), ('OXOOOO-XX', 'O'), ('XXOOXOXOX', 'X'), ('XXXXXOXXO', 'X'),
                  ('XOXX-XOOO', 'O'), ('OXO-X---X', '-'), ('XXOXOXXXO', 'X'), ('OOOOOXXXO', 'O'),
                  ('XXOXXXOOX', 'X'), ('X-OOOO--X', 'O'), ('XXXXOXOOO', 'X'), ('XXXXOX-X-', 'X'),
                  ('-OXXXOX-X', 'X'), ('OOXXOOXXO', 'O'), ('XOXOOOXOO', 'O'), ('OXOO-O-OX', '-'),
                  ('OOOXXOXXX', 'X'), ('XOXXOXOOO', 'O'), ('-OOXXXXX-', 'X'), ('O-X-XX-XX', 'X'),
                  ('OOXOXXXOX', 'X'), ('OXOXOOXXO', 'O'), ('O-OX-X--O', '-'), ('OOOOXXXOX', 'O'),
                  ('XXOOXOOOO', 'O'), ('-X-O--XOO', '-'), ('--XO-OXXX', 'X'), ('O-OX-OO--', '-'),
                  ('OOXXXXOOO', 'X'), ('-XXO-O-O-', '-'), ('XOOOOXXXO', 'T'), ('-OOO-XXOO', '-'),
                  ('OXXXXXOOX', 'X'), ('-OXOO---O', '-'), ('--OX-OO-O', 'O'), ('XXXOXOOXX', 'X'),
                  ('O-OXOX---', '-'), ('XOXOOXOOX', 'X'), ('XXXXOXXXO', 'X'), ('XXOXOOOXO', 'O'),
                  ('XOOXXOOOX', 'X'), ('-X--XX-XO', 'X'), ('OXOXOXXXO', 'O'), ('XOX-O----', '-'),
                  ('XXOXXXXXO', 'X'), ('-X--O-OXO', '-'), ('OOXOOXXXO', 'O'), ('XOOOXOXOX', 'X'),
                  ('XXOXOOOOO', 'O'), ('OX-X----O', '-'), ('--OOOXOXO', 'O'), ('XXOOOOOOX', 'O'),
                  ('OOOOXXXXO', 'O'), ('XOOXXOO-X', 'X'), ('OXXOOOXOX', 'O'), ('XX--XXX--', '-'),
                  ('OXXXOOOXX', 'T'), ('XXXOOOOOX', 'X'), ('OOXOOXXXX', 'X'), ('X-XOOOOXO', 'O'),
                  ('OOXOOOOO-', 'O'), ('OXXOXOXOO', 'X'), ('XOXOOOOOO', 'O'), ('-X---OXXO', '-'),
                  ('-XOXO--X-', '-'), ('-X-XOXOO-', '-'), ('XOOXOOXXX', 'X'), ('XXX-X-OOO', 'X'),
                  ('O-XO-OOO-', 'O'), ('XXO-OX-O-', '-'), ('OOXXXXXOO', 'X')]
        for board, expect in cases:
            self.assertEqual(expect, quiz.game_status(board), msg="(for board ="+repr(board)+")")


class TestProblem3B(unittest.TestCase):
    """Test forced_win"""

    def verify_win(self, board, expect):
        result = quiz.forced_win(board[:])
        if expect is None:
            self.assertIsNone(result, msg="(for board ="+repr(board)+")")
        elif expect == -1:
            self.assertEqual(result, -1, msg="(for board ="+repr(board)+")")
        else:
            self.assertIn(result, expect, msg="(for board ="+repr(board)+")")

    def test_01(self):
        # Game has already been won, lost, or tied with initial board
        board = "XXX" + \
                "XOO" + \
                "OOX"
        expect = -1
        self.verify_win(board, expect)

        cases = [("OOOOOOXXX", -1),
                 ("XOOOXOOOX", -1),
                 ("XXOXOOOOX", None),
                 ("XXOOOXXOX", None),
                 ("OOOOOOOOO", None),
                 ("XX-OOOOOX", None),
                 ("XOXOO-OOX", None),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)

    def test_02(self):
        # Single move immediate wins or non-wins
        board = "XXO" + \
                "XOO" + \
                "-OX"
        expect = {6}
        self.verify_win(board, expect)

        board = "XOX" + \
                "OX-" +  \
                "OXO"
        expect = None
        self.verify_win(board, expect)

        cases = [("XX-XOOOOX", {2}),
                 ("XX-OOXOOX", {2}),
                 ("XXOO-OOOX", {4}),
                 ("XOOOXOOO-", {8}),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)

    def test_03(self):
        # Single X move with single O response
        board = "XO-" + \
                "OXO" +  \
                "OO-"
        expect = {8}
        self.verify_win(board, expect)

        cases = [("XOXO--OO-", None),
                 ("XOOOX-X-O", None),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)

    def test_04(self):
        # Cases involving two X moves
        board = "XOX" + \
                "O--" +  \
                "OO-"
        expect = None
        self.verify_win(board, expect)

        cases = [("XOX-X-O-O", None),
                 ("OX-X--XOX", {2, 4, 5}),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)

    def test_05(self):
        # Classic early forced wins
        board = "XO-" + \
                "---" +  \
                "---"
        expect = {3, 4, 6}
        self.verify_win(board, expect)

        board = "X-O" + \
                "---" +  \
                "---"
        expect = {8, 3, 6}
        self.verify_win(board, expect)

        board = "---" + \
                "---" +  \
                "-OX"
        expect = {2, 4, 5}
        self.verify_win(board, expect)

    def test_06(self):
        # Medium cases
        cases = [("XX-------", {2, 3, 4, 5, 6, 7, 8}),
                 ("X--O-----", {1, 2, 4}),
                 ("XO--X---O", {3, 6}),
                 ("-X-X----X", {0, 2, 4, 5, 6, 7}),
                 ("-O-O----O", None),
                 ("X----O---", {2, 4, 6}),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)

    def test_07(self):
        # Long games
        cases = [("---------", None),
                 ("-----X---", {0, 1, 2, 3, 4, 6, 7, 8}),
                 ("----O----", None),
        ]
        for board, expect in cases:
            self.verify_win(board, expect)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
