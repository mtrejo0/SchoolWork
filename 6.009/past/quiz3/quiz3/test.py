import unittest
import os
import string
import quiz3 as quiz

class TestProblem1(unittest.TestCase):
    def setUp(self):
        self.objects = {
            'Book': ('Book', {'Reading', 'Paper', 'Fun'}),
            'Pencils': ('Pencils', {'Writing', 'Paper', 'Supplies'}),
            'Tomato Soup': ('Tomato Soup', {'Food', 'Soup', 'Warm'}),
            'Pillow': ('Pillow', {'Linens', 'Head'}),
            'Comforter': ('Comforter', {'Linens', 'Heavy'}),
            'Sheets': ('Sheets', {'Linens', 'Light'}),
            # has same labels as tomato soup
            'Cold Tomato Soup': ('Tomato Soup', {'Food', 'Soup', 'Cold'}),
            'Potato Soup': ('Potato Soup', {'Food', 'Soup', 'Warm'}),
            'Chocolate Milk': ('Chocolate Milk', {'Food', 'Milk', 'Chocolate',
                                                  'Cold'}),
            'Vanilla Ice Cream': ('Vanilla Ice Cream', {'Food', 'Dessert',
                                                        'Vanilla', 'Cold'}),
            'Ice Pack': ('Ice Pack', {'Health', 'Cold'}),
            'Junk': ('Junk', set()),
        }
        self.temperatures = ['Warm', 'Cold', 'Medium', 'Frozen', 'Hot']

    def generateItems(self, tag_list, num_per_tag):
        items = []
        names = [''] * num_per_tag
        chars = string.ascii_lowercase[:26]
        for i in range(len(tag_list)):
            tags = tag_list[i % len(tag_list)]
            for j in range(num_per_tag):
                names[j] += chars[j]
                items.append((names[j], tags))
        return items

    def generateTags(self, num_per_temp):
        return [
            {temp, number}
            for temp in self.temperatures
            for number in [str(i) for i in range(num_per_temp)]
        ]

    def test_01(self):
        inventory = quiz.Inventory()
        inventory.add_items(*self.objects['Book'], 1)
        inventory.add_items(*self.objects['Pencils'], 1)
        inventory.add_items(*self.objects['Pencils'], 1)
        self.assertEqual(inventory.get_num_of_item('Book'), 1)
        self.assertEqual(inventory.get_num_of_item('Pencils'), 2)
        self.assertEqual(inventory.get_item_tags('Book'), {'Reading', 'Paper',
                                                           'Fun'})
        self.assertEqual(inventory.get_tag_items('Reading'), {'Book'})
        self.assertEqual(inventory.get_tag_items('Paper'), {'Book', 'Pencils'})
        self.assertEqual(inventory.get_tag_items('Writing'), {'Pencils'})
        self.assertEqual(inventory.get_tag_items('Reading'), {'Book'})
        self.assertEqual(inventory.get_tag_items('Supplies'), {'Pencils'})

    def test_02(self):
        inventory = quiz.Inventory()
        inventory.add_items(*self.objects['Book'], 1)
        inventory.add_items(*self.objects['Book'], 1)
        inventory.add_items(*self.objects['Book'], 1)
        inventory.add_items(*self.objects['Pencils'], 5)
        inventory.add_items(*self.objects['Pencils'], 5)
        self.assertEqual(inventory.get_num_of_item('Book'), 3)
        self.assertEqual(inventory.get_num_of_item('Pencils'), 10)
        self.assertEqual(inventory.get_num_of_item('Pen'), 0)
        self.assertEqual(inventory.get_item_tags('Pencils'),
                         {'Writing', 'Paper', 'Supplies'})
        self.assertEqual(inventory.get_item_tags('Pen'), set())
        self.assertEqual(inventory.get_num_with_tag('Writing'), 10)
        self.assertEqual(inventory.get_num_with_tag('Reading'), 3)
        self.assertEqual(inventory.get_num_with_tag('Paper'), 13)
        self.assertEqual(inventory.get_num_with_tag('Swimming'), 0)

    def test_03(self):
        inventory = quiz.Inventory()
        inventory.add_items(*self.objects['Pillow'], 5)
        inventory.add_items(*self.objects['Comforter'], 6)
        inventory.add_items(*self.objects['Sheets'], 7)
        self.assertEqual(inventory.get_tag_items('Light'), {'Sheets'})
        self.assertEqual(inventory.get_tag_items('Heavy'), {'Comforter'})
        self.assertEqual(inventory.get_tag_items('Head'), {'Pillow'})
        self.assertEqual(inventory.get_tag_items('Linens'),
                         {'Pillow', 'Comforter', 'Sheets'})
        self.assertEqual(inventory.get_tag_items('Feet'), set())
        self.assertEqual(inventory.get_num_with_tag('Head'), 5)
        self.assertEqual(inventory.get_num_with_tag('Heavy'), 6)
        self.assertEqual(inventory.get_num_with_tag('Light'), 7)
        self.assertEqual(inventory.get_num_with_tag('Linens'), 18)
        inventory.add_items(*self.objects['Pillow'], 5)
        inventory.add_items(*self.objects['Comforter'], 6)
        inventory.add_items(*self.objects['Sheets'], 7)
        self.assertEqual(inventory.get_num_with_tag('Head'), 10)
        self.assertEqual(inventory.get_num_with_tag('Heavy'), 12)
        self.assertEqual(inventory.get_num_with_tag('Light'), 14)
        self.assertEqual(inventory.get_num_with_tag('Linens'), 36)

    def test_04(self):
        inventory = quiz.Inventory()
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        self.assertEqual(inventory.get_num_of_item('Tomato Soup'), 3)
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        self.assertEqual(inventory.get_num_of_item('Tomato Soup'), 4)
        inventory.add_items(*self.objects['Chocolate Milk'], 1)
        self.assertEqual(inventory.get_num_of_item('Chocolate Milk'), 1)
        self.assertEqual(inventory.get_num_of_item('Tomato Soup'), 4)
        inventory.add_items(*self.objects['Chocolate Milk'], 1)
        inventory.add_items(*self.objects['Vanilla Ice Cream'], 100)
        self.assertEqual(inventory.get_num_of_item('Chocolate Milk'), 2)
        self.assertEqual(inventory.get_num_of_item('Vanilla Ice Cream'), 100)
        self.assertEqual(inventory.get_tag_items('Cold'),
                         {'Chocolate Milk', 'Vanilla Ice Cream'})
        inventory.add_items(*self.objects['Ice Pack'], 1)
        self.assertEqual(inventory.get_tag_items('Cold'),
                         {'Chocolate Milk', 'Vanilla Ice Cream', 'Ice Pack'})
        self.assertEqual(inventory.get_tag_items('Vanilla'),
                         {'Vanilla Ice Cream'})
        self.assertEqual(inventory.get_tag_items('Food'),
                         {'Chocolate Milk', 'Tomato Soup',
                          'Vanilla Ice Cream'})
        self.assertEqual(inventory.get_num_with_tag('Cold'), 103)
        self.assertEqual(inventory.get_num_with_tag('Food'), 106)

    def test_05(self):
        inventory = quiz.Inventory()
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        inventory.add_items(*self.objects['Tomato Soup'], 1)
        inventory.add_items(*self.objects['Potato Soup'], 1)
        inventory.add_items(*self.objects['Potato Soup'], 1)
        inventory.add_items(*self.objects['Potato Soup'], 1)
        self.assertEqual(inventory.get_num_of_item('Name Not There'), 0)
        self.assertEqual(inventory.get_num_of_item('Potato Soup'), 3)
        self.assertEqual(inventory.get_num_of_item('Tomato Soup'), 2)
        inventory.add_items(*self.objects['Junk'], 1)
        self.assertEqual(inventory.get_num_of_item('Junk'), 1)
        self.assertEqual(inventory.get_item_tags('Junk'), set())
        with self.assertRaises(ValueError):
            inventory.add_items(*self.objects['Cold Tomato Soup'], 1)
        self.assertEqual(inventory.get_tag_items('Food'),
                         {'Tomato Soup', 'Potato Soup'})
        self.assertEqual(inventory.get_tag_items('Soup'),
                         {'Tomato Soup', 'Potato Soup'})
        self.assertEqual(inventory.get_tag_items('Warm'),
                         {'Tomato Soup', 'Potato Soup'})
        self.assertEqual(inventory.get_num_with_tag('Drink'), 0)
        self.assertEqual(inventory.get_num_with_tag('Warm'), 5)

    def test_06(self):
        inventory = quiz.Inventory()
        tag_list = self.generateTags(10)
        items = self.generateItems(tag_list, 20)
        for i in range(25):
            for item, tags in items:
                inventory.add_items(item, tags, 1)
            for _ in range(10000):
                self.assertEqual(inventory.get_num_with_tag('Cold'), (i+1)*200)
                self.assertEqual(inventory.get_num_with_tag('Warm'), (i+1)*200)
                self.assertEqual(inventory.get_num_with_tag('Frozen'), (i+1)*200)
                self.assertEqual(inventory.get_num_with_tag('1'), (i+1)*100)
                self.assertEqual(inventory.get_num_with_tag('2'), (i+1)*100)
                self.assertEqual(inventory.get_num_with_tag('4'), (i+1)*100)

    def test_07(self):
        inventory = quiz.Inventory()
        tag_list = self.generateTags(100)
        items = self.generateItems(tag_list, 20)
        for item, tags in items:
            inventory.add_items(item, tags, 1)
        for _ in range(10000):
            expected_1 = inventory.get_tag_items('Cold')
            self.assertEqual(len(expected_1), 2000)
            expected_2 = inventory.get_tag_items('Frozen')
            self.assertEqual(len(expected_2), 2000)
            expected_3 = inventory.get_tag_items('1')
            self.assertEqual(len(expected_3), 100)
            self.assertIn('ii', expected_3)
            expected_4 = inventory.get_tag_items('4')
            self.assertEqual(len(expected_4), 100)
            self.assertIn('ttttt', expected_4)

    def test_08(self):
        inventory = quiz.Inventory()
        tag_list = self.generateTags(100)
        items = self.generateItems(tag_list, 20)
        for item, tags in items:
            inventory.add_items(item, tags, 1)
        for _ in range(50000):
            expected_1 = inventory.get_tag_items('Cold')
            self.assertEqual(len(expected_1), 2000)
            expected_2 = inventory.get_tag_items('4')
            self.assertEqual(len(expected_2), 100)
            self.assertEqual(inventory.get_num_with_tag('Cold'), 2000)
            self.assertEqual(inventory.get_num_with_tag('1'), 100)
            self.assertEqual(inventory.get_num_with_tag('2'), 100)


class TestProblem2(unittest.TestCase):
    def _validate_trees(self, k, n=None, limit=None):
        def get_size(tree):
            if tree is None:
                return 0
            elif isinstance(tree, tuple) and len(tree) == 2:
                return 1 + get_size(tree[0]) + get_size(tree[1])
            return None

        def check_tree(tree, seen):
            size = get_size(tree)
            if size is None:
                self.fail('%s is not a binary tree' % (tree,))
            if size != k:
                self.fail('%s is not of size %d' % (tree, k))
            if tree in seen:
                self.fail('repeated tree: %s' % (tree,))
            seen.add(tree)

        # Check size and uniqueness.
        trees = set()
        if limit is None:
            for tree in quiz.binary_trees(k):
                check_tree(tree, trees)
        else:
            gen = iter(quiz.binary_trees(k))
            for i in range(limit):
                try:
                    tree = next(gen)
                except StopIteration:
                    self.fail('only %d trees returned, expected more' % (i,))
                check_tree(tree, trees)

        # Check count.
        if n is not None and len(trees) != n:
            self.fail('expected %d trees, got %d' % (n, len(trees)))

    def test_01(self):
        self._validate_trees(0, n=1)

    def test_02(self):
        self._validate_trees(1, n=1)

    def test_03(self):
        self._validate_trees(2, n=2)

    def test_04(self):
        self._validate_trees(3, n=5)

    def test_05(self):
        self._validate_trees(12, n=208012)

    def test_06(self):
        self._validate_trees(13, limit=10000)

    def test_07(self):
        self._validate_trees(100, limit=10000)

    def test_08(self):
        self._validate_trees(900, limit=10000)


class TestProblem3(unittest.TestCase):
    def check_lists(self, race, case_num):
        """Run the race.

        Checks that the get_participants() results match the list in
        expected_lists before the first timestep and after all subsequent
        timesteps.
        """
        def check_list(expected, result):
            """Check that a single list matches the expected value."""

            self.assertEqual(len(expected), len(result), msg="Not the right "
                             "number of Participants: expected %d, got %d"
                             % (len(expected), len(result)))

            # Convert get_participants() result to list of dictionaries
            result = map(lambda p: {"class": type(p),
                                    "position": p.get_position(),
                                    "id_num": p.get_id_num()},
                         result)

            # Sort by unique id_num, since any order is ok
            expected = sorted(expected, key=lambda ptcp: ptcp["id_num"])
            result = sorted(result, key=lambda ptcp: ptcp["id_num"])

            msg = ("\nWe expected:\n" + "\n".join(map(str, expected)) +
                   "\n\nBut got:\n" + "\n".join(map(str, result)))
            for exp, res in zip(expected, result):
                self.assertEqual(exp["id_num"], res["id_num"], msg=msg)
                self.assertEqual(exp["class"], res["class"], msg=msg)
                self.assertAlmostEqual(exp["position"], res["position"],
                                       places=3, msg=msg)

        # List of the expected get_participants results before the first
        # timestep, after the first timestep, after the second timestep, etc.
        with open(os.path.join('cases', case_num + '.txt'), 'r') as f:
            expected_lists = eval(f.read())

        # Check before the first timestep
        result = race.get_participants()
        check_list(expected_lists[0], result)

        # Check the rest of the timesteps
        for expected in expected_lists[1:]:
            race.timestep()
            result = race.get_participants()
            print(result,expected)
            check_list(expected, result)

    def test_01(self):
        # Single runner.
        race = quiz.Race(17, [])
        race.add_runner(5383)
        self.check_lists(race, '1')

    def test_02(self):
        # Single runner passing finish line.
        race = quiz.Race(4, [])
        race.add_runner(3489)
        self.check_lists(race, '2')

    def test_03(self):
        # Single runner resting once.
        race = quiz.Race(45.5, [])
        race.add_runner(9015)
        self.check_lists(race, '3')

    def test_04(self):
        # Single walker.
        race = quiz.Race(13, [])
        race.add_walker(6021)
        self.check_lists(race, '4')

    def test_05(self):
        # Runner and walker.
        race = quiz.Race(30.25, [])
        race.add_runner(8924)
        race.add_walker(1042)
        self.check_lists(race, '5')

    def test_06(self):
        # Runners and walkers, added late. Resting. Passing finish line.
        race = quiz.Race(26.1, [])
        race.add_runner(5661)
        race.add_walker(9080)
        self.check_lists(race, '6a')

        # Add new participants to the beginning of the race.
        race.add_runner(3312)
        race.add_walker(8234)
        self.check_lists(race, '6b')

    def test_07(self):
        # Runner and walker. Resting. One hill.
        race = quiz.Race(400, [6])
        race.add_runner(5764)
        race.add_walker(2341)
        self.check_lists(race, '7')

    def test_08(self):
        # Runners and walkers, added late. Resting. Hill.
        race = quiz.Race(67.9, [11])
        race.add_walker(3321)
        race.add_walker(1999)
        self.check_lists(race, '8a')

        race.add_runner(6162)
        race.add_runner(7293)
        self.check_lists(race, '8b')

    def test_09(self):
        # Walkers and runners, added late. Resting. Hills. Passing finish line.
        race = quiz.Race(45, [1, 4, 5, 11.5, 12, 24, 37, 42, 41, 43])
        race.add_runner(1573)
        race.add_walker(9441)
        self.check_lists(race, '9a')

        race.add_walker(2364)
        race.add_runner(5723)
        self.check_lists(race, '9b')


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
