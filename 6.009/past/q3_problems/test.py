#!/usr/bin/env python3
import os,os.path,json
import unittest
import types
import ast
import quiz

TEST_DIRECTORY = os.path.dirname(__file__)

#############
# Problem 1 #
#############

class TestProblem01(unittest.TestCase):
    def test_01(self):
        weights = [6, 7, 8, 9, 10]
        capacity = 5
        result = quiz.count_viable(weights,capacity)
        self.assertEqual(result,1)

    def test_02(self):
        weights = [3, 4, 4.5, 6, 7, 8, 9, 10]
        capacity = 5
        result = quiz.count_viable(weights,capacity)
        self.assertEqual(result,4)

    def test_03(self):
        weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        capacity = 55.5
        result = quiz.count_viable(weights,capacity)
        self.assertEqual(result,1024)

    def test_04(self):
        weights = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
        capacity = 28
        result = quiz.count_viable(weights,capacity)
        self.assertEqual(result,3302)

    def test_05(self):
        weights = [4, 1, 2, 3, 4, 1, 1, 3, 5, 7, 15, 18, 21, 16, 9, 5, 3, 5, 6, 10, 3]
        capacity = 50
        result = quiz.count_viable(weights,capacity)
        self.assertEqual(result,344844)

#############
# Problem 2 #
#############

class TestProblem02(unittest.TestCase):
    # check that result ordering obeys all the constraints
    def validate(self,class_graph,result):
        result = map(str,result)
        self.assertEqual(sorted(result), sorted(class_graph.keys()),
                         msg = str(result) + 'is not a valid ordering of all classes')

        # build dictionary of prerequisites
        prereq_dict = {}
        for node in class_graph:
            prereq_dict[node] = []
        for node in class_graph:
            for successor in class_graph[node]:
                prereq_dict[successor] += [node]

        valid_next = set([c for c in prereq_dict if len(prereq_dict[c]) == 0])
        for c in result:
            self.assertIn(c, valid_next, msg = str(result) + 'is not a valid ordering of all classes')
            valid_next.remove(c)
            for succ in class_graph[c]:
                valid_next.add(succ)

    def test_01(self):
        class_graph = {
            "6.009": []
        }
        result = quiz.find_valid_ordering(class_graph)
        self.validate(class_graph,result)

    def test_02(self):
        class_graph = {
            "6.01": ["6.006"],
            "6.046": [],
            "6.006": ["6.046"]
        }
        result = quiz.find_valid_ordering(class_graph)
        self.validate(class_graph,result)

    def test_03(self):
        class_graph = {
            "6.006": [],
            "6.008": [],
            "18.01": ["6.042"],
            "6.01": ["6.006", "6.008"],
            "6.042": ["6.006"]
        }
        result = quiz.find_valid_ordering(class_graph)
        self.validate(class_graph,result)

    def test_04(self):
        class_graph = {
            "18.062": [],
            "18.05": [],
            "18.03": [],
            "18.01": ["18.062", "18.02", "18.05"],
            "18.06": [],
            "18.600": [],
            "18.02": ["18.03", "18.06", "18.600"]
        }
        result = quiz.find_valid_ordering(class_graph)
        self.validate(class_graph,result)

    def test_05(self):
        class_graph = {
            "6.033": ["6.828"],
            "8.01": ["8.02"],
            "6.864": [],
            "6.006": ["6.046"],
            "6.012": [],
            "18.02": ["18.03", "18.06"],
            "18.03": ["6.002", "6.004", "6.02"],
            "18.06": ["6.02"],
            "5.111": [],
            "6.042": ["6.005", "6.006"],
            "8.02": ["6.002", "6.004", "6.01"],
            "6.002": ["6.012"],
            "6.004": ["6.033"],
            "7.012": [],
            "6.046": ["6.864"],
            "6.01": ["6.002", "6.004", "6.005", "6.006", "6.02"],
            "6.02": ["6.033"],
            "6.005": ["6.828"],
            "18.01": ["18.02", "6.042"],
            "6.828": []
        }
        result = quiz.find_valid_ordering(class_graph)
        self.validate(class_graph,result)

#############
# Problem 3 #
#############

class TestProblem03(unittest.TestCase):
    def run_test(self,test):
        with open(os.path.join(TEST_DIRECTORY,'test_data','p3','default_db.txt')) as f:
            default_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
        with open(os.path.join(TEST_DIRECTORY,'test_data','p3','update_db.txt')) as f:
            update_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
        with open(os.path.join(TEST_DIRECTORY,'test_data','p3',test+'.in')) as f:
            input_data = json.load(f)
        with open(os.path.join(TEST_DIRECTORY,'test_data','p3',test+'.out')) as f:
            expected = json.load(f)

        input_data["inputs"]["rep"] = quiz.build_rep(default_db, update_db)
        fn_name = input_data["function"]
        f = getattr(quiz, fn_name)
        result = f(**input_data["inputs"])

        if fn_name == "get_late_classes":
            self.assertEqual(sorted(result),sorted(expected))
        elif fn_name == "get_class_days":
            # result should be list of lists
            if not isinstance(result,list) or not all(isinstance(e,list) for e in result):
                raise AssertionError('result should be a list of lists')
            # and have the same length as expected result
            self.assertEqual(len(expected), len(result), msg='result is not of correct length')
            result2 = [sorted(item) for item in result]
            expected2 = [sorted(item) for item in expected]
            self.assertEqual(sorted(result2), sorted(expected2), msg="result doesn't match expected value")

    def test_01(self):
        self.run_test('11')

    def test_02(self):
        self.run_test('12')

    def test_03(self):
        self.run_test('13')

    def test_04(self):
        self.run_test('14')

    def test_05(self):
        self.run_test('15')

    def test_06(self):
        self.run_test('16')

#############
# Problem 4 #
#############

class TestProblem04(unittest.TestCase):
    def run_test(self,test):
        # read in initial records and create instance
        with open(os.path.join(TEST_DIRECTORY,'test_data','p4','records.json'),'r') as f:
            term = quiz.TermRecords(json.load(f))

        # read in test data and expected results
        with open(os.path.join(TEST_DIRECTORY,'test_data','p4',test+'.in'),'r') as f:
            input_data = json.load(f)
        with open(os.path.join(TEST_DIRECTORY,'test_data','p4',test+'.out'),'r') as f:
            expected = json.load(f)

        # invoke specified method, capture result
        #print('\n%s' % input_data['test'])
        mname = input_data["method"]
        f = getattr(term, mname)
        args = []
        if "method_args" in input_data:
            args = input_data["method_args"]
        result = f(*args)

        # check some transcripts and classlists?
        if "check_transcripts_and_classlists" in input_data:
            result = {"transcripts": [], "classlists": []}
            checks = input_data["check_transcripts_and_classlists"]
            result["classlists"] = [term.classlist(s)
                                    for s in checks.get("classlists",[])]

            # check transcripts
            rlist = [term.transcript(s)
                     for s in checks.get("transcripts",[])]
            glist = expected.get('transcripts',[])
            if len(rlist) != len(glist):
                raise AssertionError("result has wrong number of transcripts!")
            # make sure transcripts are the same
            for r,g in zip(rlist,glist):
                if g is None:
                    if r is not None:
                        raise AssertionError("expected None for transcript")
                elif not isinstance(r,list):
                    raise AssertionError("expected list for transcript")
                else:
                    r.sort()   # put transcripts in canonical order
                    g.sort()
                    self.assertEqual(r,g,msg='transcript incorrect')
                    if r != g:
                        raise AssertionError('Expected transcript: %s\nReceived transcript: %s\nTranscript incorrect' % (g,r))

            # check classlists
            rlist = [term.classlist(s)
                     for s in checks.get("classlists",[])]
            glist = expected.get('classlists',[])
            if len(rlist) != len(glist):
                raise AssertionError("result has wrong number of classlists!")
            # make sure transcripts are the same
            for r,g in zip(rlist,glist):
                if g is None:
                    if r is not None:
                        raise AssertionError("expected None for classlist")
                elif not isinstance(r,list):
                    raise AssertionError("expected list for classlist")
                else:
                    r.sort()   # put transcripts in canonical order
                    g.sort()
                    if r != g:
                        raise AssertionError('Expected classlist: %s\nReceived classlist: %s\nclasslist incorrect' % (g,r))

        elif "method" in input_data:
            if isinstance(expected,list):
                # if we're expecting a list, make sure result is a list
                if not isinstance(result,list):
                    raise AssertionError(input_data["method"]+" must return a list, not "+str(result))
                else:
                    # sort both lists, then compare
                    result.sort()
                    expected.sort()

            if result != expected:
                raise AssertionError('Expected:\n%s\nReceived:\n%s\nresult incorrect' % (str(expected),str(result)))

    def test_01(self): self.run_test('1')
    def test_02(self): self.run_test('2')
    def test_03(self): self.run_test('3')
    def test_04(self): self.run_test('4')
    def test_05(self): self.run_test('5')
    def test_06(self): self.run_test('6')
    def test_07(self): self.run_test('7')
    def test_08(self): self.run_test('8')
    def test_09(self): self.run_test('9')
    def test_10(self): self.run_test('10')
    def test_11(self): self.run_test('11')
    def test_12(self): self.run_test('12')
    def test_13(self): self.run_test('13')
    def test_14(self): self.run_test('14')
    def test_15(self): self.run_test('15')
    def test_16(self): self.run_test('16')
    def test_17(self): self.run_test('17')
    def test_18(self): self.run_test('18')
    def test_19(self): self.run_test('19')
    def test_20(self): self.run_test('20')
    def test_21(self): self.run_test('21')
    def test_22(self): self.run_test('22')

#############
# Problem 5 #
#############

class TestProblem05(unittest.TestCase):
    def test_01(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        row,col = 0,0
        result = quiz.has_liberty(board,row,col)
        self.assertTrue(result)

    def test_02(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        row,col = 4,2
        result = quiz.has_liberty(board,row,col)
        self.assertFalse(result)

    def test_03(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        row,col = 3,3
        result = quiz.has_liberty(board,row,col)
        self.assertTrue(result)

    def test_04(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        row,col = 2,1
        result = quiz.has_liberty(board,row,col)
        self.assertFalse(result)

    def test_05(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        row,col = 4,1
        result = quiz.has_liberty(board,row,col)
        self.assertTrue(result)

    def test_06(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        color = "w"
        result = quiz.capture(board,color)
        expected = [".bwwb",
                    "bbwwb",
                    "b.b.w",
                    "bb.bw",
                    ".b..b"]
        self.assertEqual(result,expected)

    def test_07(self):
        board = [
            ".bwwb",
            "bbwwb",
            "bwb.w",
            "bbwbw",
            "wbwwb"
        ]
        color = "b"
        result = quiz.capture(board,color)
        expected = [".bww.",
                    "bbww.",
                    "bwb.w",
                    "bbwbw",
                    "wbww."]
        self.assertEqual(result,expected)

#############
# Problem 6 #
#############

class TestProblem06(unittest.TestCase):
    def test_01(self):
        # Base case
        k = 1; L = 1; n = 1
        expect = 1
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_02(self):
        # Single Label
        k = 1; L = 13; n = 5
        expect = 1287
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_03(self):
        # Example 1 from problem descripton
        k = 2; L = 3; n = 4
        expect = 5
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_04(self):
        # Example 2 from problem descripton
        k = 3; L = 5; n = 2
        expect = 205
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_05(self):
        # Medium Test 1
        k = 3; L = 3; n = 3
        expect = 28
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_06(self):
        # Medium Test 2
        k = 4; L = 3; n = 4
        expect = 33
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_07(self):
        # No Valid Hands
        k = 5; L = 2; n = 5
        expect = False
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)

    def test_08(self):
        # Large Case
        k = 6; L = 4; n = 3
        expect = 1094
        result = quiz.count_straights(k, L, n)
        self.assertEqual(expect, result)


#############
# Problem 7 #
#############

class TestProblem07(unittest.TestCase):
    def setUp(self):
        with open("test_data/p7/default_db.txt") as f:
            self.default_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
        with open("test_data/p7/update_db.txt") as f:
            self.update_db = [line.split() for line in f.read().split("\n") if len(line) > 0]
        self.rep = quiz.build_schedule_rep(self.default_db, self.update_db)

    def test_01(self):
        # Part A
        buildings = []
        expect = []
        result = quiz.get_near_classes(buildings, self.rep)
        self.assertEqual(expect, result)

    def test_02(self):
        # Part A
        buildings = ["Walker", "Stata", "W20", "Koch", "Kresge", "W66", "W36", "E17", "E51"]
        expect = sorted(["6.337", "6.003", "6.002", "6.005", "6.004", "6.007", "6.006", "6.008", "6.338", "6.163", "6.111", "6.009", "6.012", "6.013", "6.854", "6.011", "6.852", "6.851", "6.858", "6.555", "6.207", "6.334", "6.840", "6.867", "6.141", "6.142", "6.864", "6.025", "6.024", "6.023", "6.022", "6.021", "6.541", "6.621", "6.131", "6.875", "6.034", "6.035", "6.036", "6.376", "6.344", "6.345", "6.341", "6.260", "6.263", "6.262", "6.265", "6.267", "6.438", "6.434", "6.435", "6.436", "6.437", "6.431", "6.01", "6.02", "6.03", "6.801", "6.803", "6.042", "6.602", "6.045", "6.047", "6.046", "6.041", "6.608", "6.524", "6.525", "6.522", "6.521", "6.441", "6.440", "6.442", "6.243", "6.241", "6.813", "6.115", "6.816", "6.814", "6.452", "6.453", "6.450", "6.866", "6.828", "6.251", "6.252", "6.253", "6.580", "6.255", "6.589", "6.UAR", "6.UAP", "6.UAT", "6.503", "6.630", "6.857", "6.302", "6.301", "6.170", "6.172"])
        result = sorted(quiz.get_near_classes(buildings, self.rep))
        self.assertEqual(expect, result)

    def test_03(self):
        # Part A
        buildings = ["Walker", "Stata", "Koch", "W66", "E51"]
        expect = sorted(["6.004", "6.111", "6.025", "6.376", "6.437", "6.02", "6.440", "6.813", "6.589"])
        result = sorted(quiz.get_near_classes(buildings, self.rep))
        self.assertEqual(expect, result)

    def test_04(self):
        # Part B
        building = "Stata"
        day_of_week = "Tuesday"
        expect = 9
        result = quiz.earliest_meeting(building, day_of_week, self.rep)
        self.assertEqual(expect, result)

    def test_05(self):
        # Part B
        building = "W36"
        day_of_week = "Friday"
        expect = 12
        result = quiz.earliest_meeting(building, day_of_week, self.rep)
        self.assertEqual(expect, result)

    def test_06(self):
        # Part B
        building = "Walker"
        day_of_week = "Saturday"
        expect = None
        result = quiz.earliest_meeting(building, day_of_week, self.rep)
        self.assertEqual(expect, result)

    def test_07(self):
        # Part B
        building = "W66"
        day_of_week = "Tuesday"
        expect = 10
        result = quiz.earliest_meeting(building, day_of_week, self.rep)
        self.assertEqual(expect, result)

    def test_08(self):
        # Part B
        building = "W20"
        day_of_week = "Monday"
        expect = 9
        result = quiz.earliest_meeting(building, day_of_week, self.rep)
        self.assertEqual(expect, result)

    def test_09(self):
        # Part C
        class_list = ["6.854"]
        expect = False
        result = quiz.have_conflicts(class_list, self.rep)
        self.assertEqual(expect, result)

    def test_10(self):
        # Part C
        class_list = ["6.003", "6.03"]
        expect = True
        result = quiz.have_conflicts(class_list, self.rep)
        self.assertEqual(expect, result)

    def test_11(self):
        # Part C
        class_list = ["6.004", "6.005", "6.006", "6.334"]
        expect = True
        result = quiz.have_conflicts(class_list, self.rep)
        self.assertEqual(expect, result)

    def test_12(self):
        # Part C
        class_list = ["6.801", "6.828", "3.091", "6.111", "18.03", "6.001", "6.004", "6.003", "6.002", "6.01"]
        expect = False
        result = quiz.have_conflicts(class_list, self.rep)
        self.assertEqual(expect, result)


#############
# Problem 8 #
#############

class TestProblem08(unittest.TestCase):
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
# Problem 9 #
#############

class TestProblem09(unittest.TestCase):
    def _test_generator(self, inp, expected):
        result = quiz.split_words(inp)
        self.assertIsInstance(result, types.GeneratorType, msg="split_words should be a generator")
        self.assertEqual(set(result), expected)

    def _test_from_file(self, inp, n):
        with open(os.path.join(TEST_DIRECTORY, 'test_outputs', 'words_%02d.py' % n), 'r') as f:
            self._test_generator(inp, ast.literal_eval(f.read()))

    def test_00(self):
        self._test_generator('cake', {('cake', )})
        self._test_generator('iateanicecreamcone', {('i', 'a', 'tea', 'nice', 'cream', 'cone'), ('i', 'ate', 'a', 'nice', 'cream', 'cone'), ('i', 'ate', 'an', 'ice', 'cream', 'cone')})
        self._test_generator('mycatscaneatcarrots', {('my', 'cat', 'scan', 'eat', 'car', 'rots'), ('my', 'cat', 'scan', 'eat', 'carrots'), ('my', 'cats', 'can', 'eat', 'car', 'rots'), ('my', 'cats', 'can', 'eat', 'carrots'), ('my', 'cats', 'cane', 'at', 'car', 'rots'), ('my', 'cats', 'cane', 'at', 'carrots')})

    def test_01(self):
        self._test_from_file('etudeshakewithholdsmansards', 1)

    def test_02(self):
        self._test_from_file('redissolvebeseeminggrandeurs', 2)

    def test_03(self):
        self._test_from_file('ushersbreaknecktreblingnitrified', 3)
        self._test_from_file('antennasflameoutnothingstrackless', 4)
        self._test_from_file('abatersboardingapproveduntanglingcirrus', 5)
        self._test_from_file('challengetissuesgrippesrivuletsodiumparties', 6)

    def test_04(self):
        self._test_from_file('relationsharesabridgetheisticwithinslingshots', 7)
        self._test_from_file('opensospreytipsgiftedmenmiscallingdisarmsuprooted', 8)
        self._test_from_file('earningsbrawnsflusmopingyourselfmillinerybicyclistsadrenal', 9)
        self._test_from_file('unmistakenracefilterintertwinedeepdefrayexaminingherefords', 10)
        self._test_from_file('semaphoresixpaperingquadrantalbulldozingvelocitypolesolider', 11)
        self._test_from_file('erstwhilesophisticsocialeagerlyasparagustryingforearmstipple', 12)
        self._test_from_file('accidentalbailoutenlargebegirtquakerswashroompromotersdroves', 13)
        self._test_from_file('barbadosmistookannoysbotfliesincubationdetachescatnipicicles', 14)
        self._test_from_file('hamsterraceapprovesproconsulzonkedwantshadyhearkenamplifyides', 15)
        self._test_from_file('multilithhikersinstallingsquirelacingswaggeredintendedsyapped', 16)
        self._test_from_file('buntbrainpansbeardeddashikihelenapageboyssolipsistpatchpippedomaha', 17)
        self._test_from_file('rethinkaviditiesspearswrenchcapturedaversionspaddlesmisquotespajamas', 18)
        self._test_from_file('sequinsamericanabilletfrightfultimpanistsavertedivyexactorimmolateddisappointsow', 19)
        self._test_from_file('intervenedsendingtrimmingpreemptingpersuasionbudgemoochingextortionwhelksjoustbikes', 20)
        self._test_from_file('federalsunheardtelephonesaliasdepositimbruingartifactspositivecurrentpluralistsullying', 21)
        self._test_from_file('sportingpackagecheshireyearlyenfiladedstomachingpersistsailshelteringsulkyoleoresinpolio', 22)
        self._test_from_file('activationemigratethiamineinstincttypesetquoteskindliestapproachedparchmentstenonsadherent', 23)
        self._test_from_file('stragglypalladiumraspiestplatoonsferrousdeceitsduffersbeaconssuperhumancorvettesaugmentingtallying', 24)
        self._test_from_file('arcslanderousreptilehotheadedsympathyeulogistichabituatedcorianderbarbarouscoercionpopulaceultimatum', 25)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
