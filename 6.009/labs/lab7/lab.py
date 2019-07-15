"""6.009 Lab 7 -- Faster Gift Delivery."""


from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!
class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        self.graph_class = graph_class
        

    def from_list(self, adj_list, labels=None):
        
        # convert adj list to adj dict and then call from _dict
        new = {}
        for i in range(len(adj_list)):
            new[i] = adj_list[i]
        return self.from_dict(new,labels)
         

    def from_dict(self, adj_dict, labels=None):

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

class FastGraph(Graph):
    """Faster implementation of `Graph`.

    Has extra optimizations for star and clique patterns.
    """
    

    def match(self,pattern,arr):
        # checks if an array matches the pattern
        if(len(set(arr)) != len(arr) ):
            return False
        for i in range(len(pattern)):
            if(pattern[i][0] != "*" and pattern[i][0] != self.labels[arr[i]]):
                return False
            for j in pattern[i][1]:
                if(arr[j] not in self.adj[arr[i]]):
                    return False
        return True

    

    def buckets(self,pattern):
        poss = []
        for nodeRep in pattern:
            poss+=[set()]
        for i in range(len(pattern)):
            nodeRep = pattern[i]
            label = nodeRep[0]
            neighbors = nodeRep[1]
            for node in self.adj:
                if(node not in poss[i] and self.degree[node]>=len(nodeRep[1])):
                    if(nodeRep[0] == "*"):
                        poss[i].add(node)
                    elif(nodeRep[0] == self.labels[node]):
                        poss[i].add(node)
        return poss


    def query(self,pattern):


        temp = self.isStar(pattern)
        if(temp[0]):
            # print("star")
            return self.starQuery(pattern,temp[1])
        elif(self.isCliquePattern(pattern)):
            # print("clique")
            return self.cliqueQuery(pattern)
        else:
            # print("query")
            poss = self.buckets(pattern)
            ans = []
            for each in poss[0]:
                tryPattern = [each]
                for i in range(len(pattern)-1):
                    tryPattern+=[None]
                self.helper(ans,pattern,tryPattern[:],poss,each,0)
            return ans
    def isStar(self,pattern):
        goal = set(range(len(pattern)))
        r = None

        for i in range(len(pattern)):
            goal.remove(i)
            if set(pattern[i][1]) == goal:
                r = i
                break
            goal.add(i)
        for i in range(len(pattern)):
            if( pattern[i][1] != [] and set(pattern[i][1]) != goal):
                return (False,None)
        return (True,r)
    
    def cliqueQuery(self,pattern):
        tot = []
        
        for each in self.cliques:
            for clique in self.cliques[each]:
                if(len(clique) == len(pattern)):
                    temp = list(clique)
                    if(temp not in tot):
                        tot+=[temp]
        
        ans = []    
        for each in tot:
            config = list(self.all_perms(each))
            for t in config:
                if(self.valid_label(pattern,t)):
                    ans+=[t]
        return ans


    def chop(self,arr,size):
        ans = []
        for i in range(len(arr)-size+1):
            ans+=[arr[i:i+size]]
        return ans
    def combinations(self,iterable, r):
        # combinations('ABCD', 2) --> AB AC AD BC BD CD
        # combinations(range(4), 3) --> 012 013 023 123
        pool = tuple(iterable)
        n = len(pool)
        if r > n:
            return
        indices = list(range(r))
        yield list(pool[i] for i in indices)
        while True:
            for i in reversed(range(r)):
                if indices[i] != i + n - r:
                    break
            else:
                return
            indices[i] += 1
            for j in range(i+1, r):
                indices[j] = indices[j-1] + 1
            yield list(pool[i] for i in indices)

    def valid_label(self,pattern,clique):
        for i in range(len(pattern)):
            try:
                if(pattern[i][0] != "*" and pattern[i][0] != self.labels[clique[i]]):
                    return False
            except KeyError:
                return False
        return True

    def all_perms(self,elements):
        if len(elements) <=1:
            yield elements
        else:
            for perm in self.all_perms(elements[1:]):
                for i in range(len(elements)):
                    yield perm[:i] + elements[0:1] + perm[i:]

    def helper(self,ans,pattern,tryPattern,poss,curr,index):

        if(None not in tryPattern and self.match(pattern,tryPattern)):
            if(tryPattern not in ans):
                ans+=[tryPattern]
            return
        rep = pattern[index]
        neighborsList = rep[1]
        for i in range(len(neighborsList)):
            each = neighborsList[i]
            for n in poss[each]:
                if(n in self.adj[curr] and n not in tryPattern):
                    temp = tryPattern[:]
                    temp[each] = n
                    self.helper(ans,pattern,temp,poss,n,each)

        # if we get to a dead end try random stuff
        if(len(neighborsList) == 0):
            for i in range(len(tryPattern)):
                if tryPattern[i] == None:
                    for n in poss[i]:
                        if(n not in tryPattern):
                            temp = tryPattern[:]
                            temp[i] = n
                            if(None not in temp and self.match(pattern,temp)):
                                if(temp not in ans):
                                    ans+=[temp]
                                return
    def isCliquePattern(self,pattern):
        total = set(range(len(pattern)))

        for i in range(len(pattern)):
            total.remove(i)
            if not (set(pattern[i][1]) == total):
                return False
            total.add(i)
        return True

    

    def starQuery(self,pattern,index):
        start = []
        for node in self.adj:
            if(self.degree[node]>=len(pattern[index][1])):
                start.append(node)
        ans = []
        poss = []
        for each in start:
            buckets = self.starBuckets(pattern,index,each)
            poss += list(self.product(buckets))

        for each in poss:
            if(self.match(pattern,each)):
                ans.append(each)
        return ans

    def starBuckets(self,pattern,index,start):
        ans = []
        for i in range(len(pattern)):
            temp = []
            if(i == index):
                temp.append(start)
            elif(pattern[i][0] == "*"):
                for node in self.adj[start]:
                    temp.append(node)
            else:
                for node in self.adj[start]:
                    if(pattern[i][0] == self.labels[node]):
                        temp.append(node)
            ans.append(temp)
        return ans

    

    def product(self,args):
        if args:
            for a in args[0]:
                for prod in self.product(args[1:]) if args[1:] else [[]]:
                    yield [a] + prod


    def __init__(self):
        self.adj = {}
        self.labels = {}
        self.degree = {}
        self.cliques = {}
    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""

        if(name not in self.adj):
            #add empty atributes for this doe and label
            self.adj[name] = set()
            self.labels[name] = label
            self.degree[name] = 0
            self.cliques[name] = [{name}]

        else:
            #we already have this node
            raise ValueError
    def remove_node(self, name):    
        """Remove the node with name `name`."""
        if(name in self.adj):
            #delete attributes of this node
            del self.adj[name]
            del self.labels[name]
            del self.degree[name]
            for each in self.adj:
                if(name in self.adj[each]):
                    self.adj[each].remove(name)

            
            for each in self.cliques:
                temp = self.cliques[each][:]
                for clique in self.cliques[each]:
                    if(name in clique):
                        temp.remove(clique)
                self.cliques[each] = temp
        else:
            # there is no node to remove
            raise LookupError
    def add_edge(self, start, end):
        if(start in self.adj and end in self.adj):
            if(end in self.adj[start]):
                raise ValueError
            self.adj[start].add(end)
            self.degree[start] +=1

            for each in self.cliques[start]:
                if(self.newClique(each,end)):
                    temp = set(each)
                    temp.add(end)
                    for node in each:
                        if(temp not in self.cliques[node]):
                            self.cliques[node].append(temp)
            for each in self.cliques[end]:
                if(self.newClique(each,start)):
                    temp = set(each)
                    temp.add(start)
                    for node in each:
                        if(temp not in self.cliques[node]):
                            self.cliques[node].append(temp)

                
        else:
            # we dont have the two nodes to make the edge
            raise LookupError
    def newClique(self,clique,end):

        for each in clique:
            if not end in self.adj[each] or not each in self.adj[end]:
                return False
        return True
    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        if(start in self.adj and end in self.adj):
            if(end not in self.adj[start]):
                # we dont have the two nodes to make the edge
                raise LookupError 
            self.adj[start].remove(end)
            self.degree[start]-=1


            for node in self.cliques:
                for n in self.cliques[node]:
                    if(end in n and start in n):
                        n.remove(end)
                        n.remove(start)


            

        else:
            # there is no edge to remove
            raise LookupError


if __name__ == '__main__':
    pass