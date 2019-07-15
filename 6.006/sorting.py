def insertion_sort(A):
	#Insertion sort array A
	for i in range(1, len(A)): # O(n) loop over array
		for j in range(i, 0, -1): # O(i) loop over sub-array
			if A[j - 1] <= A[j]: # O(1) check if swap needed
				break # O(1) no swap needed
			A[j - 1], A[j] = A[j], A[j - 1] # O(1) swap

def selection_sort(A):
	#Selection sort array A
	for i in range(len(A) - 1, 0, -1): # O(n) loop over array
		m = i # O(1) initial index of max
		for j in range(i, 0, -1): # O(i) search for max in A[:i]
			if A[m] < A[j]: # O(1) check for larger value
				m = j # O(1) new max found
		A[m], A[i] = A[i], A[m] # O(1) swap
def merge_sort(A, l = 0, r = 0, temp = None):
	#’’’Merge sort sub-array A[l:r] using temp as auxiliary storage’’’
	if temp is None: # O(1) initial call
		r, temp = len(A), [None] * len(A) # O(n) allocate temp
	if 1 < r - l: # O(1) size k = r - l
		c = (l + r + 1) // 2 # O(1) compute center
		merge_sort(A, l, c, temp) # T(k/2) recursively sort left
		merge_sort(A, c, r, temp) # T(k/2) recursively sort right
		# merge ranges A[l:c] and A[c:r]
		t, p1, p2 = l, l, c # O(1) initialize pointers
		while t != r: # O(k) fill temp storage
			if p2 == r or (p1 < c and A[p1] < A[p2]): # O(1) check side
				temp[t] = A[p1] # O(1) merge from left
				p1 += 1 # O(1) increment left pointer
			else:
				temp[t] = A[p2] # O(1) merge from right
				p2 += 1 # O(1) increment right pointer
			t += 1 # O(1) increment temp pointer
		A[l:r] = temp[l:r] # O(k) copy back to array
