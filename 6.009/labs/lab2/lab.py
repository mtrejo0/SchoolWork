# NO IMPORTS ALLOWED!

import json
import os
def getID(data,actor):
    if(actor in data):
        return data[actor]
    else:
        return None
def getName(data,ID):
    for i in data:
        if(data[i] == ID ):
            return i


def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    for i in data:
        if(i[0] == actor_id_1 and i[1] == actor_id_2):
            return True
        if(i[1] == actor_id_1 and i[0] == actor_id_2):
            return True
    return False

def get_actors_with_bacon_number(data, n):
    if(n == 0):
        return {4724} 
    else:
       
        levels = bfs(makeAdj(data),4724)[0]
        
        if(n > len(levels)):
            return set()
        else:
            return set(levels[n])

def makeAdj(data):
    adj = {}
    for i in data:
        if(not(i[0] in adj)):
            adj[i[0]] = [i[1]]
        elif( not( i[1] in adj[i[0]]) and not i[0] == i[1]):
            adj[i[0]] += [i[1]]
        if(not(i[1] in adj)):
            adj[i[1]] = [i[0]]
        elif( not( i[0] in adj[i[1]] ) and not i[0]  == i[1]):
            adj[i[1]] += [i[0]]
    return adj
    

def get_bacon_path(data, actor_id):
    
    
    parent = bfs(makeAdj(data),4724)[1]   
    if(actor_id not in parent):
        return None
    path = [actor_id]
    current = actor_id
    while(parent[current] is not current):
        path+=[parent[current]]
        current=parent[current]
    
    path.reverse()
    print(path)
    return path

def get_path(data, actor_id_1, actor_id_2):
    
    parent = bfs(makeAdj(data),actor_id_1)[1]
    if(actor_id_2 not in parent or actor_id_1 not in parent ):
        return None
    path = [actor_id_2]
    current = actor_id_2
    j = 0
    while(parent[current] is not current):
        
        path+=[parent[current]]
        current=parent[current]
        j+=1
    
    path.reverse()

    return path

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


if __name__ == '__main__':
    with open('resources/large.json') as f:
        large = json.load(f)
    with open('resources/names.json') as f:
        large_names = json.load(f)
    with open('resources/movies.json') as f:
        movs = json.load(f) 
     
    path = get_path(large,getID(large_names,'Sandra Bullock'),getID(large_names,'Iva Ilakovac'))
    print(path)


    movies = []
    path_pointer = 0
    while(path_pointer < len(path)-1):
        a = path[path_pointer]
        b = path[path_pointer+1]
        for i in large:
            if(i[0] == a and i[1] == b or i[1] == a and i[0] == b):
                movies+=[i[2]]
        path_pointer+=1

    


    names = []
    for i in movies:
         names+= [getName(movs,i)]
    print(names)
