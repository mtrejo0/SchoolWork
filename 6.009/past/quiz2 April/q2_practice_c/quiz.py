# NO IMPORTS ALLOWED!

##################################################
### Problem 1: efficiency
##################################################

def unique(input_list):
     output = []
     seen = set()
     for item in input_list:
         if item not in seen:
             seen.add(item)
             output = output + [item]
     return output

     # return list(set(input_list))


##################################################
### Problem 2: phone words
##################################################

allwords = set(open('words2.txt').read().splitlines())

def is_word(i):
    return i.lower() in allwords

key_letters = {
    '2': 'ABC',
    '3': 'DEF',
    '4': 'GHI',
    '5': 'JKL',
    '6': 'MNO',
    '7': 'PQRS',
    '8': 'TUV',
    '9': 'WXYZ',
}


def phone_words(digits):
    print(digits)
    parts = part(digits)
    # print(parts)
    ans = set()
    for each in parts:
        pos = []
        for i in each:
           
            if(i == "1" or i == "0"):
                add = [""]
                pos.append(add)
            else:
                add = []
                for j in key_letters[i]:
                    add.append(j)
                pos.append(add)
        tot = product(pos)
        for i in tot:
            word = "".join(i)
            if(is_word(word)):
                ans.add(word)
    return ans



def part(digits):
    ans = set()
    for i in range(len(digits)):
        for j in range(i+1,len(digits)+1):
            ans.add(digits[i:j])
    return ans
def product(pools):
        # gives product of pools of lists to give all combinations of those lists
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        return result



##################################################
### Problem 3: radix trie
##################################################

from trie import Trie, RadixTrie


def dictify(t):
    """
    For debugging purposes.  Given a trie (or radix trie), return a dictionary
    representation of that structure, including the value and children
    associated with each node.
    """
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out

def compress_trie(trie):
    rt, prefix = helper_trie(trie, '')
    return rt
    
def helper_trie(trie, prefix=''):
    """ return (radixtrie, key) """
    rt = RadixTrie()
    rt.value = trie.value

    if len(trie.children) == 0:
        return rt, prefix

    if len(trie.children) == 1 and trie.value is None:
        (c, ct), = trie.children.items()
        new_child, new_key = helper_trie(ct, prefix + c)
        if prefix == '':
            rt.children[new_key] = new_child
            return rt, prefix
        else:
            return new_child, new_key

    # can't compress
    for c, ct in trie.children.items():
        new_child, new_key = helper_trie(ct, c)
        rt.children[new_key] = new_child
    return rt, prefix






if __name__ == "__main__":
	pass
