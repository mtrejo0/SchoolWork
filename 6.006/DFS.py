	def dfs(Adj, s, parent = None, order = []): # Adj: adjacency list, s: start
	if parent is None: # O(1) initialize parent list
		parent = [None for v in Adj] # O(V) (use hash if unlabeled)
		parent[s] = s # O(1) root
	for v in Adj[s]: # O(Adj[s]) loop over neighbors
	if parent[v] is None: # O(1) parent not yet assigned
		parent[v] = s # O(1) assign parent
		dfs(A, v, parent, order) # Recursive call
	order.append(s) # O(1) amortized
	return parent, order