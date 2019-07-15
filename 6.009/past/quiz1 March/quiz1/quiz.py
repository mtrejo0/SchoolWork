import sys
sys.setrecursionlimit(10000)

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################

def get_mode(A):
    """ Finds the mode of a list of numbers. Breaks ties
        by preferring the greatest value. """
    dictA = {}
    for i in A:
        if(i not in dictA):
            dictA[i] = 1
        else:
            dictA[i] +=1
    maxi = 0
    for i in dictA:
        if(maxi < dictA[i]):
            maxi = dictA[i]
    pool = []
    for i in dictA:
        if(dictA[i] == maxi):
            pool+=[i]
    return max(pool)


##################################################
#  Problem 2
##################################################

def find_anagram_groups(words, N):
    """ Given a list of words, returns the index i into 
        words that contains the Nth word of the first 
        appearing anagram group of size N.  """
   
    dic = {}
    for i in words:
        temp = join(sorted(i))
        
        if(temp not in dic):
            dic[temp] = 1
        else:
            dic[temp] += 1
   
    pot = []
    print(dic)
    for i in dic:
        if(dic[i]>=N):
            pot+=[i]
    if(len(pot) == 0):
        return None
    ans = []
    for i in pot:
        count = 0
        for j in range(len(words)):
            temp = join(sorted(words[j]))
            
            if(temp == i):
                count +=1
            if(count == N):
                ans+=[j]
                break    
    return min(ans)



def join(arr):
    string = ""
    for i in arr:
        string+=str(i)
    return string

def isAn(a,b):
    return sorted(a) == sorted(b)



##################################################
#  Problem 3
##################################################

def find_duplicates(L):
    """ Finds all duplicated words in an arbitrarily
        nested structure of containers and strings. """
    
    dic = explore(L,{})
    ans = set()
    for i in dic:
        if(dic[i] >1):
            ans.add(i)
    
    return ans
def explore(struc,dic):
    
    t = type(struc)
    if(t == str or t == int):
        if(struc not in dic):
            dic[struc] = 1
        else:
            dic[struc]+=1
        return dic
    
    for i in struc:
       
        t = type(i)
        if(type(struc) == dict):
            
            explore(i,dic)
            explore(struc[i],dic)
        elif(t == list or t == set or t == tuple or t == dict):
            explore(i,dic)
        elif(i not in dic):
            dic[i] = 1
        else:
            dic[i]+=1
    return dic


if __name__ == "__main__":
    pass
