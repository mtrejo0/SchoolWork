# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def vals_at_depth(tree, depth):
	a = explore1(tree,{})
	if(depth in a):
		return a[depth]
	else:
		return []


def explore1(tree,dic ={},curr= 0):
	if(len(tree)==0):
		return dic
	if(curr not in dic):
		dic[curr] = [tree[0]]
	else:
		dic[curr] += [tree[0]]
	for i in range(1,len(tree)):
		explore1(tree[i],dic,curr+1)
	return dic


    


##################################################
##  Problem 2
##################################################

def weave(list1, list2):
	ans = [list1[0]]
	list1 = list1[1:]
	state = 2
	while(len(list2)>0 or len(list1)>0):
		  
		if(state == 2):
			if(len(list2)<1):
				state = 1
			elif(ans[-1]!=list2[0]):
				ans+=[list2[0]]
				state = 1
				list2 = list2[1:]
			else:
				list2 = list2[1:]
		else:
			if(len(list1)<1):
				state = 2
			elif(ans[-1]!=list1[0]):
				ans+=[list1[0]]
				state = 2
				list1 = list1[1:]
			else:
				list1 = list1[1:]
	
	return ans

##################################################
##  Problem 3
##################################################

def all_blobs(world):
	grid = world["grid"]
	
	ans = []
	for i in range(len(grid)):
		for j in range(len(grid[i])):
			if(grid[i][j]!=None):
				
				temp = [grid[i][j]]
				setAns = explore(grid,grid[i][j],(i,j),set())
				temp+=[setAns]
				ans+=[temp]
	
	return ans
    

def explore(grid,typeOf,start, seen = set()):
	n = neighbors(grid,start)
	seen.add(start)
	grid[start[0]][start[1]] = None
	for i in n:
		if(grid[i[0]][i[1]] != None and grid[i[0]][i[1]] == typeOf ):
			explore(grid,typeOf,(i[0],i[1]),seen)
	return seen

def neighbors(world,coords):
    row = coords[0]
    col = coords[1]
    all_neighbors = []
    all_neighbors.append([row + 1, col])
    all_neighbors.append([row , col + 1])
    all_neighbors.append([row -1, col])
    all_neighbors.append([row, col-1])
    return [neighbor for neighbor in all_neighbors if is_in_bounds(world,neighbor)]
def is_in_bounds(world,coords):
	if(coords[0]>=0 and coords[0] < len(world) and coords[1]>=0 and coords[1] < len(world[0])):
		return True
	else:
		return False

if __name__ == "__main__":
	pass
