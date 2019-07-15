# 6.009 Spring 2019 - Quiz 3 Practice Quiz B Solutions

# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def all_simple_paths(graph, start_node, end_node):
    """Set of all simple paths from start_node to end_node in the graph"""
    return set(_gen(graph, start_node, end_node))

def _gen(graph, start, end):
    """Generator for all simple paths in the graph"""
    def node_paths(node, path_so_far = ()):
        """path_so_far up to but not including this node"""
        path = path_so_far + (node,)
        if node == end:
            yield path
            return
        if node in path_so_far: # cycle
            return
        for c in graph[node]:
            yield from node_paths(c, path)
    yield from node_paths(start, tuple())


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

class Market:
    def __init__(self):
        self.items_to_sell = [] #actual items
        self.items_to_buy = []  #notional items

    def __repr__(self):
        return "<Market sell: "+str(self.items_to_sell)+", buy: "+str(self.items_to_buy)+">"

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
        willing_to_sell_for = item.price
        best_bid_item = None
        best_bid_price = willing_to_sell_for + 1
        for x in self.items_to_buy:
            if isinstance(item, type(x)) and x.price >= willing_to_sell_for:
                if best_bid_item is None or x.price > best_bid_price:
                    best_bid_item = x
                    best_bid_price = x.price
        if best_bid_item:
            return self._transfer(item, best_bid_item, best_bid_price)
        else:
            # No matching items. Remember request to sell
            self.items_to_sell.append(item)
            return None

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
        willing_to_buy_for = item.price
        best_sell_item = None
        best_sell_price = willing_to_buy_for + 1
        for x in self.items_to_sell:
            if isinstance(x, type(item)) and x.price <= willing_to_buy_for:
                if best_sell_item is None or x.price < best_sell_price:
                    best_sell_item = x
                    best_sell_price = x.price
        if best_sell_item:
            return self._transfer(best_sell_item, item, best_sell_price)
        else:
            # No matching items. Remember request to sell
            self.items_to_buy.append(item)
            return None


    def _transfer(self, sell_item, buy_item, price_paid):
        """Sell sell_item to person seeking to buy buy_item. Remember price
        paid. Remove items from the Market.
        """
        # transfer ownership
        seller = sell_item.owner
        sell_item.owner = buy_item.owner
        sell_item.price = price_paid
        # remove items from Market
        self.items_to_sell = [x for x in self.items_to_sell if x is not sell_item]
        self.items_to_buy = [x for x in self.items_to_buy if x is not buy_item]
        return sell_item


##################################################
##  Problem 3
##################################################

allwords = set(open('words2.txt').read().splitlines())

def word_squares(top):
    """ Return (top, right, bottom, left) words """
    if top not in allwords:
        return
    n = len(top)
    nwords = {word for word in allwords if len(word) == n}
    for left in {word for word in nwords if word[0] == top[0] and word != top}:
        for right in {word for word in nwords if word[0] == top[-1] and word != top and word != left}:
            for bottom in nwords:
                if bottom[0] == left[-1] and bottom[-1] == right[-1] and bottom != top and bottom != right and bottom != left:
                    yield (top, right, bottom, left)


if __name__ == "__main__":
    pass        
