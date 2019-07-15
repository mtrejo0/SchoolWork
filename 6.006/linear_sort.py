def direct_access_sort(A):
	#"Sort A assuming items have distinct non-negative keys"
	u = 1 + max([x.key for x in A]) # O(n) find maximum key
	D = [None] * u # O(u) direct access array
	for x in A: # O(n) insert items
		D[x.key] = x
	i = 0
	for key in range(u): # O(u) read out items in order
		if D[key] is not None:
		A[i] = D[key]
		i += 1
def counting_sort(A):
	#"Sort A assuming items have non-negative keys"
	u = 1 + max([x.key for x in A]) # O(n) find maximum key
	D = [0] * u # O(u) direct access array
	for x in A: # O(n) count keys
		D[x.key] += 1
	for k in range(1, u): # O(u) cumulative sums
		D[k] += D[k - 1]
	for x in list(reversed(A)): # O(n) move items into place
		A[D[x.key] - 1] = x
		D[x.key] -= 1