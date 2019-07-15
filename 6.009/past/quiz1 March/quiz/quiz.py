def mode(A):
    """ Return the most common value in list A. """
    count_d, first_seen_index = {}, {}
    for i, elem in enumerate(A): # O(len(A))
        first_seen_index.setdefault(elem,i)
        count_d.setdefault(elem,0)
        count_d[elem] += 1
    freq_d = {}
    for val, count in count_d.items(): # O(len(count_d)) => O(len(A))
        freq_d.setdefault(count, set()).add(val)
    most_commons = {first_seen_index[val]:val for val in freq_d[max(freq_d)]} # O(len(A))
    return most_commons[min(most_commons)]
def anagrams():
    pass

def duplicates(L):
    dic = explore(L,{})
    print(dic)
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
        if(t == list or t == set or t == dict):
            
            explore(i,dic)
        elif(i not in dic):
            
            dic[i] = 1
        else:
            
            dic[i]+=1
    return dic

def deck(word):
    arr = []
    for i in range(len(word)-2):
        a = join(sorted(word[i:i+3]))
        arr+=[a]

    print(sorted(arr))
def join(arr):
    string = ""
    for i in arr:
        string+=str(i)
    return string
deck("koperrepokpokeropkre")