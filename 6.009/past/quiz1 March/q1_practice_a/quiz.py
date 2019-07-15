# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def trailing_weighted_average(S, W):
    ans = []

    for i in range(len(S)):
    	prod = 0
    	for k in range(len(W)):
    		wk = W[k]

    		if(i-k<0):
    			sik = S[0]
    		else:
    			sik = S[i-k]
    		
    		prod += wk * sik
    	ans+=[prod]
    return ans





##################################################
##  Problem 2
##################################################

def all_consecutives(vals, n):
	vals = list(vals)
	vals.sort()
	ans = set()
	for i in range(len(vals)):
		curr = i
		while(curr < len(vals)-1 and vals[curr]+1 == vals[curr+1]):
			curr +=1
		# print(i,curr)
		if(curr - i >= n-1):
			if(curr - i > n-1):
				ans.add(tuple(vals[i:i+n]))
			else:
				ans.add(tuple(vals[i:curr+1]))
	return ans



##################################################
##  Problem 3
##################################################

def cost_to_consume(seq1, seq2):
	# print(seq1+","+seq2)
	if(len(seq1)<1 and len(seq2)<1):
		return 0
	elif(len(seq1)<1):
		return len(seq2)
	elif(len(seq2)<1):
		return len(seq1)
	else:
		if(seq1[0] == seq2[0]):
			return  min(cost_to_consume(seq1[1:], seq2)+1,cost_to_consume(seq1, seq2[1:])+1,cost_to_consume(seq1[1:], seq2[1:]))
		return min(cost_to_consume(seq1[1:], seq2)+1,cost_to_consume(seq1, seq2[1:])+1,cost_to_consume(seq1[1:], seq2[1:])+1)



if __name__ == "__main__":
	print("test1")
	print(trailing_weighted_average([1, 2], [0.8, 0.7]) == [1.5, 2.3])
	print(trailing_weighted_average([1, 5, 6, 7], [1]) == [1, 5, 6, 7])
	print(trailing_weighted_average([1, 5, 6, 7], [0.5, 0.5]) == [1.0, 3.0, 5.5, 6.5])
	print(trailing_weighted_average([1, 5, 6, 7], [0, 1]) == [1, 1, 5, 6])
	print(trailing_weighted_average([1, 5, 6, 7], [1, 0]) == [1, 5, 6, 7])
	print(trailing_weighted_average([1, 5, 6, 7], [2, 0, 0, 0, 100]) == [102, 110, 112, 114])
	print("test2")
	print(all_consecutives({0, 1, 2, 3, 4}, 1) == {(0,), (1,), (2,), (3,), (4,)})
	print(all_consecutives({0, 1, 2, 3, 4}, 2) == {(0, 1), (3, 4), (2, 3), (1, 2)})
	print(all_consecutives({0, 1, 2, 3, 4}, 5) == {(0, 1, 2, 3, 4)})
	print(all_consecutives({0, 1, 2, 3, 4}, 6) == set())
	print(all_consecutives({0, 2, 4}, 1) == {(2,), (0,), (4,)})
	print(all_consecutives({0, 2, 4}, 2) == set())
	print(all_consecutives({0, 83, 2, 3, 81, 7, 82}, 2) == {(81, 82), (2, 3), (82, 83)})
	print("test3")
	print(cost_to_consume('ab', 'b'))
	print(cost_to_consume('mast', 'mast'))
	print(cost_to_consume('mast', 'must'))
	print(cost_to_consume('misty', 'must'))
	print(cost_to_consume('color', 'colour'))
	print(cost_to_consume('car', 'boat'))
	print(cost_to_consume('frog', 'apple'))
	print(cost_to_consume('aba', 'bbb'))
	print(cost_to_consume('aba', 'bab'))
	print([1,0,1,2,1,3,5,2,2])