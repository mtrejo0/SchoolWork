# 6.009 Spring 2019 Quiz 3

##################################################
##  Problem 1
##################################################

class Inventory:
    def __init__(self):
        self.items = {}
        self.inventory = {}
        self.tagged = {}
        self.tagNum = {}


    def add_items(self, item_name, item_tags, quantity):
        """
        Adds quantity additional items with the specified name and tags
            to the inventory. If the item has already been added to the
            inventory and the tags do not match, a ValueError will be
            raised.

        Args:
            item_name: (string) the name of the item being added
            item_tags: (set) a set of tags corresponding to the provided item
            quantity: (int) number of items to add
        """
        if item_name not in self.items:
            self.items[item_name] = item_tags
            self.inventory[item_name] = quantity
        else:
            if not self.items[item_name].issubset(item_tags):
                raise ValueError
            self.items[item_name] = self.items[item_name] | item_tags
            self.inventory[item_name] += quantity

        for tag in item_tags:
            if tag not in self.tagged:
                self.tagged[tag] = set()
            self.tagged[tag].add(item_name)
            if tag not in self.tagNum:
                self.tagNum[tag] = 0
            self.tagNum[tag]+=quantity






    def get_item_tags(self, item_name):
        """
        Gets the tags of a particular item in the inventory. If
        no item with the name item_name has been added, it will return
        an empty set.

        Args:
            item_name: (string) the name of the item

        Returns:
            (set of strings) the set of tags the specified item has
        """
        if item_name in self.items:
            return self.items[item_name]
        return set()
    def get_num_of_item(self, item_name):
        """
        Returns the total number of items added with the specified name.
        If no item with item_name has been added, it will return 0.

        Args:
            item_name: (string) name of the item

        Returns:
            (int) a summed total of all the items added with that name
        """
        if item_name in self.inventory:
            return self.inventory[item_name]
        return 0

    def get_tag_items(self, item_tag):
        """
        Returns all of the item names that have a specified tag. If
        no item with the tag item_tag has been added, it will return
        an empty set.

        Args:
            item_tag: (string) an item tag

        Returns:
            (set of strings) the set of names for all the items
                that have the inputted tag
        """
        if item_tag in self.tagged:
            return self.tagged[item_tag]
        return set()

    def get_num_with_tag(self, item_tag):
        """
        Returns the summed total of all the items that have the specified tags.
        If no item with the tag item_tag has been added, it will return 0.

        Args:
            item_tag: (string) an item tag

        Returns:
            (int) the total number of items with the specified tag
        """
        if item_tag in self.tagNum:
            return self.tagNum[item_tag]
        return 0



##################################################
##  Problem 2
##################################################

def binary_treesPREVIOUS_IMPLEMENTATION(k):
    """As a generator, return all possible binary trees of size `k`,
    in any order, with no duplicates."""

    if k == 0:
        # base case simplest BST
        yield None

    else:
        for i in range(0,k):
            # generates BSTs for i
            a = tuple(binary_trees(i))
            # generates BSTs for what is left
            b = tuple(binary_trees(k-i-1))
            # combines them to make a tuple to represent left and right
            yield a+b


def binary_trees(k):
    """As a generator, return all possible binary trees of size `k`,
    in any order, with no duplicates."""

    if k == 0:
        # base case simplest BST
        yield None
    else:
        for i in range(k):
            # generates BSTs for i
            for a in binary_trees(i):
                # generates BSTs for what is left
                for b in binary_trees(k-i-1):
                    # combines them to make a tuple to represent left and right
                    yield (a,b)

# In my previous implementation I didnt realize that binary_trees(i) gave all binary trees of size i
# I thought that it returned the whole binary tree for the left side as it should be
#
# Now i realize that all the values in binary_trees(i) are all of size i and all of the values for
# binary_trees(k-i-1) are of size k-i-1
#
# All that is needed to be done after that is match all the possible combinations of those two sets
# to make every possible BTS of size k wielding each one as they are ready
#
# an attempt i had earlier was (below) but this was too slow and defeats the purpose
# of having a a generator in the first place
#
# def binary_trees(k):
#     """As a generator, return all possible binary trees of size `k`,
#     in any order, with no duplicates."""
#
#     if k == 0:
#         # base case simplest BST
#         yield None
#     else:
#         for i in range(k):
#             a = tuple(binary_trees(i))
#             b = tuple(binary_trees(k-i-1))
#             for left in a:
#                 for right in b:
#                     yield (left,right)



##################################################
##  Problem 3
##################################################
class Race:

    def __init__(self, finish, hills):
        """Initializes a Race.

           Args:
                finish: (float) position of finish
                hills: (list of float) positions of hills
        """
        self.finish = finish
        self.hills = hills
        self.all = []


    def add_runner(self, id_num):
        """Adds a Runner with ID id_num to position 0."""
        self.all += [Runner(id_num)]

    def add_walker(self, id_num):
        """Adds a Walker with ID id_num to position 0."""
        self.all += [Walker(id_num)]

    def timestep(self):
        """Advances the race by one timestep.

        * Participants will move unless they are resting or their position is >= finish.
        * Remember to calculate speeds of the Participants using the positions at the beginning of the timestep.
        """

        for p in self.all:
            curr = p.speed
            if isinstance(p,Runner):
                if p.left == 0:
                    p.speed = 0
                    p.left = 3
                else:
                    p.speed = 5
                    p.left-=1
            if isinstance(p,Walker):
                for other in self.all:
                    if other != p:
                        if abs(other.pos-p.pos) <= 1:
                            p.speed = 3
                            print(other,p)
                            break
                        else:
                            p.speed = 2
            for h in self.hills:
                if isinstance(p,Runner):
                    if abs(h-p.pos) <= 1 and p.speed !=0:
                        p.speed -=1
                        break
                elif abs(h-p.pos) <= 1:
                    p.speed -=1
                    break

        for p in self.all:
            p.update(self.finish)



    def get_participants(self):
        """Returns a list of all Runner and Walker
            objects in the race, in any order."""
        return self.all


class Participant:

    def __init__(self,id):
        self.id = id
        self.pos = 0
        self.speed = 0

    def get_id_num(self):
        """Returns the participant ID."""
        return self.id

    def get_position(self):
        """Returns the participant position."""
        return self.pos
    def __repr__(self):
        return str([self.id,self.pos,self.speed])
    def setSpeed(self,s):
        self.speed = s




class Runner(Participant):
    def __init__(self,id):
        Participant.__init__(self,id)
        self.speed = 3
        self.left = 3
    def update(self,end):
        if end > self.pos:
            self.pos += self.speed



class Walker(Participant):
    def __init__(self,id):
        Participant.__init__(self,id)
        self.speed = 2
    def update(self,end):
        if end > self.pos:
            self.pos += self.speed

##################################################

if __name__ == "__main__":
    pass
