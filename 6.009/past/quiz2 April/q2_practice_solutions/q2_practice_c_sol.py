# NO IMPORTS!

#############
# Problem 1 #
#############

def unique(input_list):
    output = []
    seen = set()
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output.append(item)
    return output

def unique_original_slow(input_list):
     output = []
     seen = []
     for item in input_list:
         if item not in set(seen):
             seen = seen + [item]
             output = output + [item]
     return output


#############
# Problem 2 #
#############

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
    def get_words(word_so_far, digits):
        if is_word(word_so_far):
            yield word_so_far

        if len(digits) == 0:
            return

        nxt, rest = digits[0], digits[1:]
        yield from get_words('', rest)  # end of this word; try after
        if nxt == '0' or nxt == '1':
            return
        for d in key_letters[nxt]:
            # extending word so far...
            yield from get_words(word_so_far + d, rest)

    return set(get_words("", digits))


#############
# Problem 3 #
#############

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

def dictify(t):
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


if __name__ == "__main__":
    pass
