def bellman_ford(Adj, w, s): # Adj: adjacency list, w: weights, s: start
	# initialization
	infinity = float(’inf’) # number greater than sum of all + weights
	d = [infinity for _ in Adj] # shortest path estimates d(s, v)
	parent = [None for _ in Adj] # initialize parent pointers
	d[s], parent[s] = 0, s # initialize source
	# construct shortest paths in rounds
	V = len(Adj) # number of vertices
	for i in range(V - 1): # relax all edges in (V - 1) rounds
		for u in range(V): # loop over all edges (u, v)
			for v in Adj[u]: # relax edge from u to v
				relax(Adj, w, d, parent, u, v)
	# check for negative weight cycles accessible from s
	for u in range(V): # Loop over all edges (u, v)
		for v in Adj[u]:
			if d[v] > d[u] + w(u,v): # If edge relax-able, report cycle
				raise Exception(’Ack! There is a negative weight cycle!’)
	return d, parent
