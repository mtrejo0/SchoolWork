# No imports!


#############
# Problem 1 #
#############

def mix_tape(songs, desired_duration):
    

    s = []
    for i in songs:
    	s+=[(i,songs[i])]
    ans =  helper(s,desired_duration)
    return ans
def helper(songs,desired_duration):
	if(desired_duration < 1):
		return None
	if(len(songs) == 0 ):
		return None
	pick = songs[0]
	if(pick[1] == desired_duration):
		return [pick[0]]

	choose = helper(songs[1:],desired_duration-pick[1])

	if(choose):
		return [pick[0]]+choose
	else:
		return helper(songs[1:],desired_duration)


#############
# Problem 2 #
#############

def k_mins(seq, k):
    
    pass


##############
# Problem 3: #
##############

# def scenic_route(grid):
# 	dirs = [(1,0),(0,1),(-1,0),(0,-1)]
# 	adj = {}
# 	start = 0
# 	goal = 0


# 	for i in range(len(grid)):
# 		for j in range(len(grid[i])):
# 			if(grid[i][j] != "X"):
# 				if(grid[i][j] == "S"):
# 					start = (i,j)
# 				if(grid[i][j] == "G"):
# 					goal = (i,j)
# 				adjList = []
# 				for each in dirs:
# 					Inew = i+each[0]
# 					Jnew = j+each[1]
# 					if(Inew >=0 and Inew < len(grid) and Jnew >=0 and Jnew < len(grid[i])):
# 						if(grid[Inew][Jnew]!="X"):
# 							adjList+=[(Inew,Jnew)]
# 				adj[(i,j)] = adjList

# 	ans = explore(asj,[]curr)


# def explore(adj,seen,curr,paths,goal):
# 	seen +=[curr]
# 	n = adj[curr]
# 	if(curr == goal):
# 		paths=[seen]
# 		return

# 	for i in n:
# 		if(i not in seen):
# 			return explore(adj,seen,i)

# 	return paths
def scenic_route(grid):
    def in_bounds(loc):
        return 0 <= loc[0] < len(grid) and 0 <= loc[1] < len(grid[0])

    def length_from_loc(loc, seen=None):
        seen = seen or set()
        r, c = loc
        if grid[r][c] == 'G':
            return 0
        elif grid[r][c] == 'X':
            return None

        results = {length_from_loc(new_loc, seen | {loc})
                   for new_loc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1))
                   if new_loc not in seen and in_bounds(new_loc)}
        results = {i for i in results if i is not None}
        if not results:
            return None
        return 1 + max(results)

    s = None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                s = (r, c)
                break
    return length_from_loc(s)

	
	

