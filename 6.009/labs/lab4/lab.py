"""6.009 Lab 4 -- Tent Packing"""

# NO IMPORTS ALLOWED!


# Example bag_list entries:
#      vertical 3x1 bag: { (0,0), (1,0), (2,0) }
#      horizontal 1x3 bag: { (0,0), (0,1), (0,2) }
#      square bag: { (0,0), (0,1), (1,0), (1,1) }
#      L-shaped bag: { (0,0), (1,0), (1,1) }
#      C-shaped bag: { (0,0), (0,1), (1,0), (2,0), (2,1) }
#      reverse-C-shaped bag: { (0,0), (0,1), (1,1), (2,0), (2,1) }


def pack(tent_size, missing_squares, bag_list, max_vacancy):

    total = set()
    for i in range(tent_size[0]):
        for j in range(tent_size[1]):
            total.add((i,j))

    best = explore(tent_size,missing_squares,bag_list,total,set(),max_vacancy)

    if(best == None):
        return None
    ans = best
    ret = []
    for i in ans:
        config = {"anchor":i[0],"shape":i[1]}
        ret+=[config]

    return ret  



def explore(tent_size,missing_squares,bag_list,total,currentBags,max_vacancy):
    
    
    if(max_vacancy<0):
        return None
    empty = firstEmpty(tent_size, missing_squares)


    for k in range(len(bag_list)):


        bag = bag_list[k]

        config = (empty,k)

        bagPositions = bagCoords(config,bag)

        if(not conflict(tent_size,missing_squares,bagPositions,config,total)):

            temp = set(missing_squares)|bagPositions


            curr = set(currentBags)
            curr.add(config)


            score = val(total,temp) 

            if(score <= max_vacancy):
                return curr
            
            pos = explore(tent_size,temp,bag_list,total,curr,max_vacancy)
            if(pos != None):
                return pos
            

    temp = set(missing_squares)
    temp.add(empty)
    pos = explore(tent_size,temp,bag_list,total,currentBags,max_vacancy-1)
    if(pos != None):
        return pos
    


def firstEmpty(tent_size, missing_squares):
    for i in range(tent_size[0]):
        for j in range(tent_size[1]):
            if((i,j) not in missing_squares):
                return (i,j)

def emptySpaces(total,missing_squares):
    return total.difference(missing_squares)


def val(total,missing_squares):
    return len(total) - len(missing_squares)


def bagCoords(config,bag):
    bagPositions = set()
    anchor = config[0]
    shape = config[1]
    for pos in bag:
        delPos = (anchor[0]+pos[0],anchor[1]+pos[1])
        bagPositions.add(delPos)
    return bagPositions


def conflict(tent_size, missing_squares,bagPositions,config, total):
    for i in bagPositions:
        if(i in missing_squares or i not in total):
            return True
    return False


bag_list = [
    {(0, 0), (1, 0), (2, 0)},  # vertical 3x1 bag
    {(0, 0), (0, 1), (0, 2)},  # horizontal 1x3 bag
    {(0, 0), (0, 1), (1, 0), (1, 1)},  # square bag
    {(0, 0), (1, 0), (1, 1)},  # L-shaped bag
    {(0, 0), (0, 1), (1, 0), (2, 0), (2, 1)},  # C-shaped bag
    {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)},  # reverse C-shaped bag
]


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    tent_size = (4,4)
    a = pack(tent_size, set([]), bag_list,0)


    # for i in a:
    #     print(i)

    for i in range(4):
        print("===================================================================================================================")
