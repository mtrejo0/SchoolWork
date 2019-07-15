# No imports!


#############
# Problem 1 #
#############

def ascending_path(graph, start, end):
    
    parent = bfs(graph,start)[1]
    # print(parent)
    if(end not in parent):
    	return None

    path = [end]
    current = end
    while(parent[current] is not current): 
        path+=[parent[current]]
        current=parent[current]
    path.reverse()
    if(isCorrect(path)):
    		return path
    return None
def isCorrect(arr):
	for i in range(len(arr)-1):
		if(arr[i]>arr[i+1]):
			return False
	return True

def bfs(Adj, startNode):
    parent = {}
    parent[startNode] = startNode
    levelSets = [[startNode]]
    while len(levelSets[len(levelSets)-1]) > 0:
        levelSets.append([])
        for item in levelSets[len(levelSets)-2]:
            for neighbor in Adj[item]: 
                if neighbor not in parent:
                    parent[neighbor] = item
                    levelSets[len(levelSets)-1].append(neighbor)
    return levelSets,parent


#############
# Problem 2 #
#############

with open('words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

def split_words(s):
    raise NotImplementedError


##############
# Problem 3: #
##############

##
## Problem 3A
##

def game_status(board):
	# print(board)
	board = mapB(board)
	# for i in board:
	# 	print(i)
	s = set()
	for i in board:
		for j in i:
			s.add(j)
	
	if(three(board,"X")):
		return "X"
	if(three(board,"O")):
		return "O"
	if("-" in s):
		return "-"
	return "T"


    
def three(board,item):
	for i in board:
		if(i == [item]*3):
			return True
	for i in range(3):
		arr = []
		for j in range(3):
			arr+=[board[j][i]]
		if(arr == [item]*3):
			return True
	arr = []
	for i in range(3):
		arr+= board[i][i]
	if(arr == [item]*3):
		return True
	arr = []
	for i in range(3):
		arr+= board[i][2-i]
	if(arr == [item]*3):
		return True
	return False



def mapB(inputArr):
	index = 0
	arr = []
	for i in range(3):
		arr.append([])
		for j in range(3):
			arr[i].append(" ")
	# print(arr)
	for i in range(3):
		# arr.append([])
		for j in range(3):
			arr[i][j] = inputArr[index]
			index += 1
			# print(index)
	return arr



##
## Problem 3B
##

def forced_win(board):
	arr = []
	for i in board:
		arr +=[i]
	return helper(board,arr)


def helper(board,arr):
	stat = game_status(board)
	if(stat == "X"):
		return -1
	if(stat == "O" or stat == "T"):
		return None
	pos = set()
	for i in range(len(board)):
		if(board[i] == "-"):
			pos.add(i)
	if(pos == set()):
		return None
	for i in pos:
		temp = board[:i]+"X"+board[i+1:]
		if(game_status(temp) == "X"):
			return i

	for i in pos:
		temp = board[:i]+"X"+board[i+1:]
		left = set(pos)
		left.remove(i)
		valid = True
		ans = None
		for j in left:
			new = temp[:j]+"O"+temp[j+1:]
			if(forced_win(new) != None):
				ans = i
			else:
				valid = False
				break
		if(valid):
			return ans
			

	





if __name__ == "__main__":
	pass
	