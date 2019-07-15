# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def all_simple_paths(graph, start_node, end_node):
    """ Set of all simple paths from start_node to end_node in the graph """
    ans = set()
    explore(graph,start_node,end_node,None,ans)
    return ans


def explore(graph,start,end,seen = None, ans = None):
    # print(seen)
    if seen == None:
        seen = []
    if ans == None:
        ans = set()
    if start in seen:
        return
    seen +=[start]

    if start == end:
        ans.add(tuple(seen))
        return

    for node in graph[start]:
        explore(graph,node,end,seen[:],ans)



##################################################
##  Problem 2
##################################################

class Item:
    def __init__(self, owner, price):
        self.owner = owner
        self.price = price

    def __repr__(self):
        return "<" + self.__class__.__name__ + ", " + str(self.owner) + ", " + str(self.price) + ">"

    def is_a_kind_of(self, other):
        return isinstance(self, type(other))


class Vehicle(Item): pass
class Sedan(Vehicle): pass
class Truck(Vehicle): pass
class SUV(Vehicle): pass
class F150(Truck): pass
class Ram(Truck): pass


a = Vehicle(100,"a")
b = Sedan(100,"a")
c = Truck(100,"a")
d = F150(100,"a")

print(isinstance(d,type(c)))

class Market:

    def __init__(self):
        self.sellItems = []
        self.buyItems = []

    def offer_to_sell(self, item):
        """
        Behavior: the "best" current sell match is found between the given
        item, and any want-to-buy items currently in the market. By "best sell
        match", we mean:

          (1) the for-sale item must (for sure) be a kind of item the buyer is
              willing to buy.

          (2) the want-to-buy item with the highest willing-to-pay price is
              found. If more than one matching want-to-buy item with the same
              highest willing-to-pay price is found, any such match can be
              used.  That highest willing-to-pay price is the price the seller
              will get, even if it is higher than the price the seller was
              willing to sell for.

        If there is a matching want-to-buy item, ownership of the for-sale item
        should be transferred to the buyer (i.e., the owner of the for-sale
        item should be set to the buyer, and the price of the for-sale item
        should be set to the price actually paid by the buyer for the item).
        The sold item should be returned as the result of offer_to_sell, and
        taken off the market.

        If there is no matching want-to-buy item, None should be returned, and
        the want-to-sell item should be remembered for future possible matches
        later, as new want-to-buy items are submitted to the market.
        """

        bestItem ,bestPrice = None,None

        # print("buy",self.buyItems)
        # print('sell',self.sellItems)
        # print("=============")
        for other in self.buyItems:
            # print(other)
            if isinstance(item,type(other)):
                if other.price >= item.price:
                    if bestItem == None:
                        bestItem = other
                        bestPrice = other.price
                    if bestPrice > item.price:
                        bestItem = other
                        bestPrice = other.price

        if bestItem == None:
            self.sellItems += [item]
        else:
            # bestItem.owner = .owner
            # bestItem.price = item.price
            # self.buyItems.remove(bestItem)
            item.owner = bestItem.owner
            item.price = bestItem.price

            return item


    def offer_to_buy(self, item):
        """
        Behavior: the "best" current purchase match is found between the given
        item, and any items currently listed for sale in the market. By "best
        buy match", we mean:

          (1) the for-sale item must (for sure) be a kind of item the buyer is
              willing to buy.

          (2) the cheapest for-sale matching item is found. If more than one
              matching for-sale item with the same lowest sell price is found,
              any such matching for-sale item can be returned. That lowest
              for-sale price is the price the buyer will pay, even if it is
              lower than the price the buyer was willing to pay.

        If there is a matching for-sale item, ownership of that item should be
        transferred to the buyer (i.e., the owner of the for-sale item should
        be set to the buyer, and the price of the for-sale item should be set
        to the price actually paid by the buyer for the item). The sold item
        should be returned (and taken off the market), and the buyer is
        understood to no longer be seeking to buy another of the item (unless
        they again later register their desire with another offer_to_buy
        submission).

        If there is no matching for-sale item, None should be returned, and the
        offer_to_buy item should be remembered for future possible matches
        later, as new items for sale are submitted to the market.
        """
        bestItem ,bestPrice = None,None
        # print("buy",self.buyItems)
        # print('sell',self.sellItems)
        # print("=============")
        for other in self.sellItems:
            if isinstance(other,type(item)):
                if other.price <= item.price:
                    if bestItem == None:
                        bestItem = other
                        bestPrice = other.price
                    if bestPrice > item.price:
                        bestItem = other
                        bestPrice = other.price

        if bestItem == None:
            self.buyItems += [item]
        else:
            bestItem.owner = item.owner
            # bestItem.price = item.price
            self.sellItems.remove(bestItem)
            return bestItem



##################################################
##  Problem 3
##################################################

allwords = set(open('words2.txt').read().splitlines())

def word_squares(top):
    """ Return (top, right, bottom, left) words """
    # print(top)
    # print(allwords)

    first = top[0]
    last = top[-1]
    n = len(top)
    all = set()
    left = set()
    right = set()
    for word in allwords:
        if len(word) == n:
            all.add(word)
            if word[0] == first:
                left.add(word)
            if word[0] == last:
                right.add(word)
    leftComp = {}
    for w in all:
        for l in left:
            if l not in leftComp:
                leftComp[l] = set()
            if l[-1] == w[0]:
                if l not in leftComp:
                    leftComp[l] = set()
                leftComp[l].add(w)

    ans = set()
    for l in left:
        if l != top:
            for r in right:
                if r != l and r!= top :
                    for w in leftComp[l]:
                        if w != l and w != r and w != top:
                            if valid((top,r,w,l)):
                                yield (top,r,w,l)

    # for a in ans:
    #     yield a
def valid(tup):
    top = tup[0]
    right = tup[1]
    bottom = tup[2]
    left = tup[3]

    if top[-1] == right[0] and right[-1] == bottom[-1] and bottom[0] == left[-1] and left[0] == top[0]:
        return True
    return False

# print(valid(('is', 'so', 'to', 'it')))
# print(valid(('is', 'so', 'no', 'in')))






if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
