"""6.009 Lab 6 -- Gift Delivery."""


from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!


class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        self.graph_class = graph_class
        

    def from_list(self, adj_list, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency list as source, where the `labels` dictionary
        maps each node name to its label.

        Parameters:
            `adj_list`: adjacency list representation of a graph
                        (as a list of lists)
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        """
        
        # convert adj list to adj dict and then call from _dict
        new = {}
        for i in range(len(adj_list)):
            new[i] = adj_list[i]
        return self.from_dict(new,labels)
         

    def from_dict(self, adj_dict, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency dictionary as source where the `labels`
        dictionary maps each node name its label.

        Parameters:
            `adj_dict`: adjacency dictionary representation of a graph
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        """

        # empty new instance of the graph class
        new = self.graph_class()
        # add each node to the new graph instance and add a label if it exists
        for each in adj_dict:
            if(labels != None and each in labels):
                new.add_node(each,labels[each])
            else:
                new.add_node(each)

        #for each node go through its adjacency and make new edges to each one of those nodes
        for each in adj_dict:
            for n in adj_dict[each]:
                new.add_edge(each,n)              
        return new
        

class SimpleGraph(Graph):
    """Simple implementation of the Graph interface."""

    
    def __init__(self):
        self.adj = {}
        self.nodes = set()
        self.labels = {}

        
    
    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""

        if(name not in self.nodes):
            #add empty atributes for this doe and label
            self.adj[name] = set()
            self.nodes.add(name)
            self.labels[name] = label
        else:
            #we already have this node
            raise ValueError

    def remove_node(self, name):
        """Remove the node with name `name`."""
        if(name in self.adj):
            #delete attributes of this node
            del self.adj[name]
            del self.labels[name]
            self.nodes.remove(name)

        else:
            # there is no node to remove
            raise LookupError

    def add_edge(self, start, end):
        """Add a edge from `start` to `end`."""


        if(start in self.adj and end in self.adj):

            if(end in self.adj[start]):
                # we already have this edge
                raise ValueError
            self.adj[start].add(end)
        else:
            # we dont have the two nodes to make the edge
            raise LookupError

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        if(start in self.adj and end in self.adj):
            if(end not in self.adj[start]):
                # we dont have the two nodes to make the edge
                raise LookupError 
            self.adj[start].remove(end)
        else:
            # there is no edge to remove
            raise LookupError    
    def query(self, pattern):
        poss = [] 
        # get the possible nodes for each part of pattern with the given labels
        for nodeRep in pattern:
            item = set()
            if(nodeRep[0] == "*"):
                for node in self.nodes:
                    if(len(self.adj[node])>=len(nodeRep[1])):
                        item.add(node)
            else:
                for each in self.nodes:
                    if(nodeRep[0] == self.labels[each]):
                        item.add(each)
            poss+=[item]
        # get all combinations of those buckets
        result = self.product(poss)
        ans = []

        #go through each combination and if they match pattern record them
        for i in result:
            if(self.match(pattern,i)):
                ans+=[i]
        
        return ans


    def product(self,pools):
        # gives product of pools of lists to give all combinations of those lists
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        return result

    def match(self,pattern,arr):
        # checks if an array matches the pattern
        if(len(pattern) != len(arr)):
            return False
        if(len(set(arr)) != len(arr) ):
            return False
        for i in range(len(pattern)):  
            for j in pattern[i][1]:
                if(arr[j] not in self.adj[arr[i]]):
                    return False
        return True

class CompactGraph(Graph):
    """Graph optimized for cases where many nodes have the same neighbors."""

    
    def __init__(self):

        self.adj = {():set()}
        self.nodes = set()
        self.labels = {}
        
    def add_node(self, name, label=''):
        if(name not in self.nodes):
            # make new empty instances of the node
            self.adj[()].add(name)
            self.nodes.add(name)
            self.labels[name] = label
        else:
            # we already have the node
            raise ValueError

    def remove_node(self, name):
        if(name in self.nodes):
            # forget the adjacency this node used to have
            for i in self.adj:
                if(name in self.adj[i]):
                    self.adj[i].remove(name)
                    # forget this list if its empty
                    if(self.adj[i] == set()):
                        del self.adj[i]
            del self.labels[name]
            self.nodes.remove(name)

        else:
            # there is no node to remove
            raise LookupError

    def add_edge(self, start, end):
        if(start in self.nodes and end in self.nodes):
            remember = 0

            # find the adjacency of start
            for i in self.adj:
                if(start in self.adj[i]):
                    remember = i
            if(end in remember):
                # this edge already exists
                raise ValueError

            self.adj[remember].remove(start)
            # delete empty adjacency lists
            if(self.adj[remember] == set()):
                del self.adj[remember]
            # add new node and remember this new list
            new = tuple(list(remember)+[end])
            if(new not in self.adj):
                self.adj[new] = set([start])
            else:
                self.adj[new].add(start)
        else:
            # we dont have the two nodes to make the edge
            raise LookupError
        
        

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""

        
        if(start in self.nodes and end in self.nodes):
            # find the adjacency of start
            for i in self.adj:
                if(start in self.adj[i]):
                    remember = i
            if(end not in remember):
                # dont have the nodes to delete the edge
                raise ValueError
            # update
            self.adj[remember].remove(start)
            new = tuple(list(remember).remove(end))
            if(new not in self.adj):
                self.adj[new] = set([start])
            else:
                self.adj[new].add(start)
        else:
            # these nodes dont exist
            raise LookupError
   
    def query(self, pattern):
        poss = []
        for nodeRep in pattern:
            # get the possible nodes for each part of pattern with the given labels
            item = set()
            if(nodeRep[0] == "*"):
                for node in self.nodes:
                    ans = 0
                    for i in self.adj:
                        if(node in self.adj[i]):
                            ans = i
                    if(len(ans)>=len(nodeRep[1])):
                        item.add(node)
            else:
                   for each in self.nodes:
                    if(nodeRep[0] == self.labels[each]):
                        item.add(each)
            poss+=[item]
        # get all combinations of those buckets
        result = self.product(poss)

        ans = []
        # check which ones match the pattern and record them
        for i in result:
            if(self.match(pattern,i)):
                ans+=[i]
        return ans

    def product(self,pools):
        # gives product of pools of lists to give all combinations of those lists
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        return result

    def match(self,pattern,arr):
        # checks if an array matches the pattern
        if(len(pattern) != len(arr)):
            return False
        if(len(set(arr)) != len(arr) ):
            return False
        for i in range(len(pattern)):  
            for j in pattern[i][1]:
                ans = 0
                for k in self.adj:
                    if(arr[i] in self.adj[k]):
                        ans = k
                if(arr[j] not in ans):
                    return False
        return True


def allocate_teams(graph, k, stations, gift_labels):
    
    """Compute the number of teams needed to deliver each gift.

    It is guaranteed that there is exactly one node for each gift type and all
    building nodes have the label "building".

    Parameters:
        `graph`: an instance of a `Graph` implementation
        `k`: minimum number of buildings that a cluster needs to contain for a
             delivery to be sent there
        `stations`: mapping between each node name and a string representing
                    the name of the closest subway/train station
        `gift_labels`: a list of gift labels

    Returns:
        a dictionary mapping each gift label to the number of teams
        that Santa needs to send for the corresponding gift to be delivered

    """
    
    ans = {}
    for each in gift_labels:
        dic = {}
        # find the patterns of nodes that are gifts to buildings relationships
        temp = graph.query([(each,[1]),("building",[])])
        #make dictionary of closest station to each gift
        for t in temp:
            if(stations[t[1]] not in dic):
                dic[stations[t[1]]] = 1
            else:
                dic[stations[t[1]]] +=1
        count = 0
        # find the number of teams required for each gift and record in the dic
        for c in dic:
            if(dic[c]>=k):
                count+=1
        ans[each] = count
    return ans


if __name__ == '__main__':
    # Put code here that you want to execute when lab.py is run from the
    # command line, e.g. small test cases.
    pass
    