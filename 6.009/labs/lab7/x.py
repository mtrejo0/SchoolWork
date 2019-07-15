"""6.009 Lab 7 -- Faster Gift Delivery."""

# Bellow is original Code!!!

'''
from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!

class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        #graph_factory = GraphFactory(graph_class)
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
        #print("adjacency list", adj_list)
        new_graph = self.graph_class()
        #print("new_grah", new_graph)
        for node in range(len(adj_list)):
            if labels != None and node in labels:
                new_graph.add_node(node, labels[node])
            else:
                new_graph.add_node(node,'')


        for node in range(len(adj_list)):
            for next_node in adj_list[node]:
                new_graph.add_edge(node, next_node)

        return new_graph

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
        new_graph = self.graph_class()

        for node in adj_dict:
            if labels !=None and node in labels:
                new_graph.add_node(node, labels[node])
            else:
                new_graph.add_node(node)

        for node in adj_dict:
            for next_node in adj_dict[node]:
                new_graph.add_edge(node, next_node)

        return new_graph

final_dictos = []
returned_lists = []
star_list = []
class FastGraph(Graph):
    """Faster implementation of `Graph`.

    Has extra optimizations for star and clique patterns.
    """

    def __init__(self):
        self.assigned_label = set()
        self.nodes = {}
        self.adjacent = {}
        self.degrees ={}
        self.labels = {}


    def all_possible_sols(self,pools):
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool if y not in x]
        return result

    def pot_node_list_gen_star(self, pattern, center, star_index):

        pot_node_list =[]
        for i in range(len(pattern)):
            label = pattern[i][0]
            edges = pattern[i][1]
            inner_list = []
            if i == star_index:
                inner_list.append(center)
            elif label == '*':
                for node in self.nodes[center]['adj']:
                    inner_list.append(node)
            else:
                for potential_label_1 in self.labels.keys():
                    if potential_label_1 == label:
                        for node_1 in self.labels[potential_label_1]:
                            if node_1 in self.nodes[center]['adj']:
                                inner_list.append(node_1)
            pot_node_list.append(inner_list)
        return pot_node_list

    def pot_node_list_gen_clique(self, pattern):
        pot_node_list =[]
        for i in range(len(pattern)):
            label = pattern[i][0]
            edges = pattern[i][1]
            inner_list = []
            if label == '*':
                for potential_label in self.labels.keys():
                    for node in self.labels[potential_label]:
                        inner_list.append(node)
            else:
                for potential_label_1 in self.labels.keys():
                    if potential_label_1 == label:
                        for node_1 in self.labels[potential_label_1]:
                            inner_list.append(node_1)
            pot_node_list.append(inner_list)
        return pot_node_list


    def query_star(self, pattern, star_index):
        pot_star_center = self.star_center_finder(star_index, pattern)
        ultra_pos_perms = []
        for center in pot_star_center:
            pot_node_list = self.pot_node_list_gen_star(pattern, center, star_index)
            all_pos_perms = self.all_possible_sols(pot_node_list)
            #print(" all pos perms", all_pos_perms)
            ultra_pos_perms = ultra_pos_perms + all_pos_perms
        sol_list_v1 = []
        final_ret = []
        for path in ultra_pos_perms:
            if self.valid_result(pattern, path):
                final_ret.append(path)
        return final_ret

    def query_clique(self, pattern):
        ultra_pos_perms = []
        pot_node_list = self.pot_node_list_gen_clique(pattern)
        all_pos_perms = self.all_possible_sols(pot_node_list)
        ultra_pos_perms = ultra_pos_perms + all_pos_perms
        final_ret = []
        for path in ultra_pos_perms:
            if self.valid_result(pattern, path):
                final_ret.append(path)
        return final_ret

    def valid_result(self, pattern, path):
        passed = True
        for index in range(len(pattern)):
            label = pattern[index][0]

            if len(pattern[index][1]) >0:
                for neighbor in pattern[index][1]:
                    start = path[index]
                    end = path[neighbor]
                    if end not in self.nodes[start]["adj"]:
                        passed = False
            if label != "*":
                if path[index] not in self.labels[label]:
                    passed = False
        return passed

    def valid_star_or_clique(self, pattern):
        # first boolean returned is if its a star
        # second boolean is to see if its a clique
        contained_neighbors = 0
        star_index = []

        for i in range(len(pattern)):
            if len(pattern[i][1]) > 0:
                contained_neighbors += 1
                if len(pattern[i][1]) == (len(pattern)-1):
                    star_index.append(i)
        if contained_neighbors == 1 and len(star_index) ==1:
            return (True, False, star_index[0])
        elif len(star_index) == len(pattern):
            return (False, True, None)
        else:
            return (False, False, None)

    def index_assigner(self,current_label, neighbors):
        pattern_assignments = set()
        check_label = True
        if current_label == "*":
            check_label = False

        for node in self.nodes:
            node_neighbor_len = len(self.nodes[node]["adj"])
            neighbor_len = len(neighbors)
            if node_neighbor_len >= neighbor_len:
                if check_label:
                    if self.nodes[node]["label"] == current_label:
                        pattern_assignments.add(node)
                else:
                    pattern_assignments.add(node)
            else:
                continue
        return pattern_assignments

    def pot_index_gen(self, pattern):
        #print("here we go ")
        pattern_assignments = {}
        for index in range(len(pattern)):
            label = pattern[index][0]
            neighbors = pattern[index][1]
            assign_set = self.index_assigner(label, neighbors)
            pattern_assignments[index] = assign_set
        #print("pot index gen result", pattern_assignments)
        return pattern_assignments

    def star_center_finder(self, star_index, pattern):
        potential_centers = []
        star_neighbors_len = len(pattern[star_index][1])
        for node in self.degrees:
            if self.degrees[node] >= star_neighbors_len:
                potential_centers.append(node)
        return potential_centers

    def query(self, pattern):
        global returned_lists
        global star_list
        init_list = []
        if isinstance(pattern, list):
            star_check, clique_check, star_index = self.valid_star_or_clique(pattern)
            print("star check:", star_check, "Clique check", clique_check)
            if star_check and not clique_check:
                return self.query_star(pattern, star_index)
            elif clique_check and not star_check:
                return self.query_clique(pattern)
            else:
                pot_index_gen = self.pot_index_gen(pattern)
                for value in pattern:
                    init_list.append("#")
                for index in pot_index_gen:
                    potentials = pot_index_gen[index]
                    self.query_helper(index, None, potentials, pattern, pot_index_gen, init_list)
                list_to_return = returned_lists.copy()
                returned_lists = []
                return list_to_return
        else:
            return []

    def query_helper(self, index, previous_index,potentials, pattern, pot_index_gen, current_list):
        global returned_lists
        #print("updated list:", index, current_list)
        if '#' not in current_list:
            #print("returned_lists:", returned_lists)
            if len(set(current_list)) == len(pattern) and current_list not in returned_lists:
                #print("yielding this:", current_list)
                if self.valid_result(pattern, current_list):
                    #print(current_list, self.valid_result(pattern, current_list))
                    returned_lists.append(current_list)
                #yield current_list
        elif index < len(pattern):
            if len(potentials)> 0:
                for potential in potentials:
                    pass_test = True
                    if previous_index != None :
                        last_node = current_list[previous_index]
                        if potential not in self.nodes[last_node]["adj"] or potential in current_list:
                            # check to see if it is an adjacent or we already went through it
                            pass_test = False

                    if pass_test:
                        new_list = current_list.copy()
                        if new_list[index] == "#":
                            new_list[index] = potential
                            #print("updated list:", index, new_list)
                            if len(pattern[index][1]) > 0:
                                # check to see if we have any neighbors
                                for neighbor in pattern[index][1]:
                                    next_potential_pool = pot_index_gen[neighbor]
                                    self.query_helper(neighbor, index, next_potential_pool, pattern, pot_index_gen, new_list)
                                    #yield from self.query_helper(neighbor, index, next_potential_pool, pattern, pot_index_gen, new_list)

                            else:
                                if '#' not in new_list and new_list not in returned_lists:
                                    if self.valid_result(pattern, new_list):
                                       returned_lists.append(new_list)
                                    #print("yield_short:", new_list)
                                    #yield new_list
                                elif '#' in new_list:
                                    if previous_index != None:
                                        last_neighbors = pattern[previous_index][1]
                                        neighbors_to_explore = set()
                                        for neigh in last_neighbors:
                                            if current_list[neigh] == '#':
                                                neighbors_to_explore.add(neigh)
                                        for new_neigh in neighbors_to_explore:
                                            new_pot = pot_index_gen[new_neigh]
                                            self.query_helper(new_neigh, previous_index,new_pot, pattern, pot_index_gen, new_list )
                                            #yield from self.query_helper(new_neigh, previous_index, new_pot, pattern, pot_index_gen, new_list)

                    else:
                        continue

    def add_node(self, name, label=''):

        if name not in self.nodes:
            self.nodes[name]= {"label":label, "adj":[]}

            if label not in self.labels:
                self.labels[label] = set([name])
            else:
                self.labels[label].add(name)
        else:
            raise ValueError

    def remove_node(self, name):
        if name in self.nodes:
            label_temp = self.nodes[name]["label"]
            del self.nodes[name]
            self.labels[label_temp].remove(name)
        else:
            raise LookupError

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            adjacents = self.nodes[start]["adj"]
            if end in adjacents:
                raise ValueError
            else:
                adjacents.append(end)
            if start in self.degrees:
                self.degrees[start] += 1
            else:
                self.degrees[start] = 1
        else:
            raise LookupError

    def remove_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            adjacents = self.nodes[start]["adj"]
            if end in adjacents:
                adjacents.remove(end)
            else:
                raise LookupError
            if start in self.degrees:
                self.degrees[start] -= 1
        else:
            raise LookupError


if __name__ == '__main__':
    pass
'''

from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!

class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        #graph_factory = GraphFactory(graph_class)
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
        #print("adjacency list", adj_list)
        new_graph = self.graph_class()
        #print("new_grah", new_graph)
        for node in range(len(adj_list)):
            if labels != None and node in labels:
                new_graph.add_node(node, labels[node])
            else:
                new_graph.add_node(node,'')


        for node in range(len(adj_list)):
            for next_node in adj_list[node]:
                new_graph.add_edge(node, next_node)

        return new_graph

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
        new_graph = self.graph_class()

        for node in adj_dict:
            if labels !=None and node in labels:
                new_graph.add_node(node, labels[node])
            else:
                new_graph.add_node(node)

        for node in adj_dict:
            for next_node in adj_dict[node]:
                new_graph.add_edge(node, next_node)

        return new_graph

final_dictos = []
returned_lists = []
star_list = []
class FastGraph(Graph):
    """Faster implementation of `Graph`.

    Has extra optimizations for star and clique patterns.
    """

    def __init__(self):
        self.assigned_label = set()
        self.nodes = {}
        self.adjacent = {}
        self.degrees ={}
        self.labels = {}
        self.clique_count = 0
        self.cliques = {}


    def all_possible_sols(self,pools):
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool if y not in x]
        return result

    def pot_node_list_gen_star(self, pattern, center, star_index):

        pot_node_list =[]
        for i in range(len(pattern)):
            label = pattern[i][0]
            edges = pattern[i][1]
            inner_list = []
            if i == star_index:
                inner_list.append(center)
            elif label == '*':
                for node in self.nodes[center]['adj']:
                    inner_list.append(node)
            else:
                for potential_label_1 in self.labels.keys():
                    if potential_label_1 == label:
                        for node_1 in self.labels[potential_label_1]:
                            if node_1 in self.nodes[center]['adj']:
                                inner_list.append(node_1)
            pot_node_list.append(inner_list)
        return pot_node_list

    def pot_node_list_gen_clique(self, pattern):
        pot_node_list =[]
        for i in range(len(pattern)):
            label = pattern[i][0]
            edges = pattern[i][1]
            inner_list = []
            if label == '*':
                for potential_label in self.labels.keys():
                    for node in self.labels[potential_label]:
                        inner_list.append(node)
            else:
                for potential_label_1 in self.labels.keys():
                    if potential_label_1 == label:
                        for node_1 in self.labels[potential_label_1]:
                            inner_list.append(node_1)
            pot_node_list.append(inner_list)
        return pot_node_list


    def query_star(self, pattern, star_index):
        pot_star_center = self.star_center_finder(star_index, pattern)
        ultra_pos_perms = []
        for center in pot_star_center:
            pot_node_list = self.pot_node_list_gen_star(pattern, center, star_index)
            all_pos_perms = self.all_possible_sols(pot_node_list)
            #print(" all pos perms", all_pos_perms)
            ultra_pos_perms = ultra_pos_perms + all_pos_perms
            break
        sol_list_v1 = []
        final_ret = []
        for path in ultra_pos_perms:
            if self.valid_result(pattern, path):
                final_ret.append(path)
        print(final_ret)
        return final_ret

    def query_clique(self, pattern):
        ultra_pos_perms = []
        pot_node_list = self.pot_node_list_gen_clique(pattern)
        all_pos_perms = self.all_possible_sols(pot_node_list)
        ultra_pos_perms = ultra_pos_perms + all_pos_perms
        final_ret = []
        for path in ultra_pos_perms:
            if self.valid_result(pattern, path):
                final_ret.append(path)
        return final_ret

    def valid_result(self, pattern, path):
        passed = True
        for index in range(len(pattern)):
            label = pattern[index][0]

            if len(pattern[index][1]) >0:
                for neighbor in pattern[index][1]:
                    start = path[index]
                    end = path[neighbor]
                    if end not in self.nodes[start]["adj"]:
                        passed = False
            if label != "*":
                if path[index] not in self.labels[label]:
                    passed = False
        return passed

    def valid_star_or_clique(self, pattern):
        # first boolean returned is if its a star
        # second boolean is to see if its a clique
        contained_neighbors = 0
        star_index = []

        for i in range(len(pattern)):
            if len(pattern[i][1]) > 0:
                contained_neighbors += 1
                if len(pattern[i][1]) == (len(pattern)-1):
                    star_index.append(i)
        if contained_neighbors == 1 and len(star_index) ==1:
            return (True, False, star_index[0])
        elif len(star_index) == len(pattern):
            return (False, True, None)
        else:
            return (False, False, None)

    def index_assigner(self,current_label, neighbors):
        pattern_assignments = set()
        check_label = True
        if current_label == "*":
            check_label = False

        for node in self.nodes:
            node_neighbor_len = len(self.nodes[node]["adj"])
            neighbor_len = len(neighbors)
            if node_neighbor_len >= neighbor_len:
                if check_label:
                    if self.nodes[node]["label"] == current_label:
                        pattern_assignments.add(node)
                else:
                    pattern_assignments.add(node)
            else:
                continue
        return pattern_assignments

    def pot_index_gen(self, pattern):
        #print("here we go ")
        pattern_assignments = {}
        for index in range(len(pattern)):
            label = pattern[index][0]
            neighbors = pattern[index][1]
            assign_set = self.index_assigner(label, neighbors)
            pattern_assignments[index] = assign_set
        #print("pot index gen result", pattern_assignments)
        return pattern_assignments

    def star_center_finder(self, star_index, pattern):
        potential_centers = []
        star_neighbors_len = len(pattern[star_index][1])
        for node in self.degrees:
            if self.degrees[node] >= star_neighbors_len:
                potential_centers.append(node)
        return potential_centers

    def query(self, pattern):
        global returned_lists
        global star_list
        init_list = []
        if isinstance(pattern, list):
            star_check, clique_check, star_index = self.valid_star_or_clique(pattern)
            print("star check:", star_check, "Clique check", clique_check)
            if star_check and not clique_check:
                return self.query_star(pattern, star_index)
            elif clique_check and not star_check:
                return self.query_clique(pattern)
            else:
                pot_index_gen = self.pot_index_gen(pattern)
                for value in pattern:
                    init_list.append("#")
                for index in pot_index_gen:
                    potentials = pot_index_gen[index]
                    self.query_helper(index, None, potentials, pattern, pot_index_gen, init_list)
                list_to_return = returned_lists.copy()
                returned_lists = []
                return list_to_return
        else:
            return []

    def query_helper(self, index, previous_index,potentials, pattern, pot_index_gen, current_list):
        global returned_lists
        #print("updated list:", index, current_list)
        if '#' not in current_list:
            #print("returned_lists:", returned_lists)
            if len(set(current_list)) == len(pattern) and current_list not in returned_lists:
                #print("yielding this:", current_list)
                if self.valid_result(pattern, current_list):
                    #print(current_list, self.valid_result(pattern, current_list))
                    returned_lists.append(current_list)
                #yield current_list
        elif index < len(pattern):
            if len(potentials)> 0:
                for potential in potentials:
                    pass_test = True
                    if previous_index != None :
                        last_node = current_list[previous_index]
                        if potential not in self.nodes[last_node]["adj"] or potential in current_list:
                            # check to see if it is an adjacent or we already went through it
                            pass_test = False

                    if pass_test:
                        new_list = current_list.copy()
                        if new_list[index] == "#":
                            new_list[index] = potential
                            #print("updated list:", index, new_list)
                            if len(pattern[index][1]) > 0:
                                # check to see if we have any neighbors
                                for neighbor in pattern[index][1]:
                                    next_potential_pool = pot_index_gen[neighbor]
                                    self.query_helper(neighbor, index, next_potential_pool, pattern, pot_index_gen, new_list)
                                    #yield from self.query_helper(neighbor, index, next_potential_pool, pattern, pot_index_gen, new_list)

                            else:
                                if '#' not in new_list and new_list not in returned_lists:
                                    if self.valid_result(pattern, new_list):
                                       returned_lists.append(new_list)
                                    #print("yield_short:", new_list)
                                    #yield new_list
                                elif '#' in new_list:
                                    if previous_index != None:
                                        last_neighbors = pattern[previous_index][1]
                                        neighbors_to_explore = set()
                                        for neigh in last_neighbors:
                                            if current_list[neigh] == '#':
                                                neighbors_to_explore.add(neigh)
                                        for new_neigh in neighbors_to_explore:
                                            new_pot = pot_index_gen[new_neigh]
                                            self.query_helper(new_neigh, previous_index,new_pot, pattern, pot_index_gen, new_list )
                                            #yield from self.query_helper(new_neigh, previous_index, new_pot, pattern, pot_index_gen, new_list)

                    else:
                        continue

    def add_node(self, name, label=''):

        if name not in self.nodes:
            self.nodes[name]= {"label":label, "adj":[], "Cliques":set(), "Unis": []}

            if label not in self.labels:
                self.labels[label] = set([name])
            else:
                self.labels[label].add(name)
        else:
            raise ValueError

    def remove_node(self, name):
        if name in self.nodes:
            label_temp = self.nodes[name]["label"]
            del self.nodes[name]
            self.labels[label_temp].remove(name)
        else:
            raise LookupError

    def add_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            adjacents = self.nodes[start]["adj"]

            if end in adjacents:
                raise ValueError
            else:
                adjacents.append(end)

            if start in self.degrees:
                self.degrees[start] += 1
            else:
                self.degrees[start] = 1
            if start in self.nodes[end]["adj"] and end in self.nodes[start]["adj"]:
                self.nodes[start]["Unis"].append(end)
                self.nodes[end]["Unis"].append(start)
        else:
            raise LookupError







    def remove_edge(self, start, end):
        if start in self.nodes and end in self.nodes:
            adjacents = self.nodes[start]["adj"]
            if end in adjacents:
                adjacents.remove(end)
            else:
                raise LookupError
            if start in self.degrees:
                self.degrees[start] -= 1
        else:
            raise LookupError


    def find_cliques_with_start_or_end(self, start, end):
        clique_only_start = {}
        cliques_only_end = {}
        start_cliques = self.nodes[start]["Cliques"]
        end_cliques = self.nodes[end]["Cliques"]
        for start_clique in start_cliques:
            modify = True
            for node in self.cliques[start_clique]:
                if node not in self.nodes[end]["Unis"]:
                    modify = False
            if modify:
                self.cliques[start_clique].add(end)
                self.nodes[end]["Cliques"].add(start_clique)
            # Still need to think of the inverse of this


    def update_cliques(self, start, end):

        start_cliques = self.nodes[start]["Cliques"]
        end_cliques = self.nodes[end]["Cliques"]

        # Now we check to see if our start has any cliques
        if len(start_cliques) == 0:
            # if no cliques
            start_cliques.add(self.clique_count)
            self.cliques[self.clique_count] = set([start, end])
            self.clique_count += 1

        else:
            # if some cliques exist, we need to look through them
            cliques_to_modify = set()
            for clique in start_cliques:
                # clique will be value index for our self.cliques dict
                clique_to_check = self.cliques[clique]
                if start in clique_to_check or end in clique_to_check:
                    # if we find that both start and end are in this clique,
                    # we add it to  cliques to modify
                    cliques_to_modify.add(clique)

            if len(cliques_to_modify) == 0:
                # if this is a new clique, we just add it
                start_cliques.add(self.clique_count)
                self.cliques[self.clique_count] = set([start, end])
                self.cliques += 1
            else:
                # If we find cliques where we can find both start and end, we look at the other nodes in there
                # then we record them
                other_nodes_to_check_dict = {}
                for mini_clique in cliques_to_modify:
                    other_nodes_to_check = []
                    for node in self.cliques[mini_clique]:
                        if node != start and node != end:
                            if self.unidirectional(start, end, node):
                                other_nodes_to_check.append(node)

                    if len(other_nodes_to_check) > 0:
                        other_nodes_to_check_dict[mini_clique] = other_nodes_to_check



if __name__ == '__main__':
    pass