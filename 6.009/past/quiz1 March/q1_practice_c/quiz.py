# NO IMPORTS!

#############
# Problem 1 #
#############

def runs(vals):
	if(len(vals)<1):
		return vals
	ans = []
	i = 0
	while(i < len(vals)):
		j = i
		while(j<len(vals)-1 and vals[j]==vals[j+1]-1):
			j+=1
		
		add = vals[i:j+1]
		if(len(add) == 1):
			ans+=add
		else:
			ans+=[add]

		i = j+1
	return ans

#############
# Problem 2 #
#############

def is_cousin(parent_db, A, B):
    """ If A and B share at least one grandparent but do not share a parent,
        return one of the shared grandparents, else return None. """
    db = {}
    for pair in parent_db:
    	if(pair[1] not in db):
    		db[pair[1]] = [pair[0]]
    	else:
    		db[pair[1]] += [pair[0]]
    parentsA = db[A]
    parentsB = db[B]
    par = set(parentsA+parentsB)
    if(not len(par) == len(parentsA)+len(parentsB)):
    	return None
    grandA = []
    for i in parentsA:
    	grandA += db[i]
    grandB = []
    for i in parentsB:
    	grandB += db[i]
    for i in grandA:
    	if(i in grandB):
    		return i

    return None

#############
# Problem 3 #
#############

def all_phrases(grammar, root):
    """ Using production rules from grammar expand root into
        all legal phrases. """
    print(grammar)
    print(root)
    input()
    pass




    
    
