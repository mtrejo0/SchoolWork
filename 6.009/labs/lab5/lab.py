# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        self.children = {}
        self.value = None
        self.type = None

        

    def set(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if(self.type == None):
            self.type = type(key)
        if type(key) != self.type:
            raise TypeError
        if(len(key) < 1):
            self.value = value
        else:
            if(key[:1] not in self.children):
                self.children[key[:1]] = Trie()
            self.children[key[:1]].set(key[1:],value)


    def get(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if type(key) != self.type :
            raise TypeError
        if(len(key) == 0):
            if(self.value == None):
                return KeyError
            return self.value
        elif(key[:1] not in self.children):
            raise KeyError
        return self.children[key[:1]].get(key[1:])

    def autoGet(self,key):
        #returns the instance of the current Trie
        if type(key) != self.type :
            raise TypeError
        if(len(key) == 0):
            return self
        elif(key[:1] not in self.children):
            raise KeyError
        return self.children[key[:1]].autoGet(key[1:])
    
    


    def delete(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        if type(key) != self.type :
            raise TypeError
        if(len(key) == 0):
            if(self.value == None):
                return KeyError
            self.value = None
        else:
            if(key[:1] not in self.children):
                raise KeyError
            return self.children[key[:1]].delete(key[1:])

    def contains(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        
        if type(key) != self.type :
            raise True
        if(len(key) == 0):
            if(self.value == None):
                return False
            if(self.value != None):
                return True
        else:
            if(key[:1] not in self.children):
                return False
            return self.children[key[:1]].contains(key[1:])

    def items(self,total = None,pastKey = None):

        """
        Returns a list of (key, value) pairs for all keys/values in this trie and
        its children.
        """
        
        if(total == None): 
            total = []
        if(pastKey == None):
            pastKey = self.type("")
        if(self.value != None):
            total+=[(pastKey,self.value)]
        for each in self.children:
            childItems = self.children[each].items(total,pastKey+each)
        return total

        


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    dic = {}

    sentences = tokenize_sentences(text)
    for each in sentences:
        words = each.split(" ")
        for word in words:
            if(word not in dic):
                dic[word] = 1
            else:
                dic[word] +=1
    trie = Trie()
    for each in dic:
        trie.set(each,dic[each])
    return trie


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    dic = {}
    sentences = tokenize_sentences(text)
    for each in sentences:
        temp = tuple(each.split(" "))
        if(temp not in dic):
            dic[temp] = 1
        else:
            dic[temp] +=1
    trie = Trie()
    for each in dic:
        trie.set(each,dic[each])
    return trie


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    
    try:
        t = trie.autoGet(prefix)
        possible = t.items()
    except KeyError:
        return []
    if(max_count == None): 
        return [prefix+i[0] for i in possible]
    if(max_count == 0):
        return []
    possible = sorted(possible,  key=lambda x: x[1])
    if(len(possible) < max_count):
        return [prefix+i[0] for i in possible]

    return [prefix+i[0] for i in possible[-max_count:]]
    
    
def edits(t,string):
    alph = "abcdefghijklmnopqrstuvwxyz"
    pos = set()
    for each in alph:
        for i in range(len(string)):
            pos.add(string[:i]+each+string[i+1:])
            pos.add(string[:i]+each+string[i:])
            pos.add(string[:i]+string[i+1:])
        pos.add(string[:]+each)
        pos.add(string[:-1]+each)
        pos.add(string[:-1])

    for i in range(len(string)-1):
        temp = string[:i]+string[i+1]+string[i]+string[i+2:]
        pos.add(temp)

    ans = []
    for i in pos:
        if(t.contains(i)):
            ans+=[(i,t.get(i))]
    return ans



def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """

    auto = autocomplete(trie,prefix,max_count)
    ans = []
    pos = edits(trie,prefix)
    final = set(auto)
    edited = sorted(pos,  key=lambda x: x[1])
    
    if(max_count != None):
        if(len(auto)<max_count):        
            for i in edited[len(auto)-max_count:]:
                final.add(i[0])
        return list(final)
    else:
        for i in edited:
            final.add(i[0])
        return list(final)


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """

    words = trie.items()
    ans = set()
    for word in words:
        if(match(word[0],pattern)):
            ans.add(word)

    return list(ans)



def match(word,pattern):

    if(word == pattern):
        return True
    if len(pattern) == 0 and len(word) == 0:
        return True
    if len(pattern) == 0 and len(word) != 0:
        return False
    if len(pattern) != 0 and len(word) == 0:
        return False

    if pattern[0] == "*":
        for i in range(len(word)):
            if(match(word[i:],pattern[1:])):
                return True
        if(match("",pattern[1:])):
            return True
        return False

    if pattern[-1] == "*":
        for i in range(len(word)):
            if(match(word[:len(word)-i],pattern[:-1])):
                return True
        if(match("",pattern[:-1])):
            return True
        return False

    if pattern[0] == "?" :
        return match(word[1:],pattern[1:])
    if pattern[0] == word[0]:
        return match(word[1:],pattern[1:])

    if pattern[-1] == "?":
        return match(word[:-1],pattern[:-1])
    if pattern[-1] == word[-1]:
        return match(word[:-1],pattern[:-1])



# you can include test cases of your own in the block below.
if __name__ == '__main__':
    with open("resources/corpora/Pride and Prejudice.txt", encoding="utf-8") as f:
        text = f.read()
    # print(text)
    a = make_phrase_trie(text)

    
    a = a.items()
    a = sorted(a,  key=lambda x: x[1])
    b = []
    a = a[-4:]
    for i in a:
        b += [i[0]]

    a = []
    for i in b:
        a+=[" ".join(i)]
    print(b)

    a = make_word_trie(text)
    
    a = autocomplete(a,"gre",6)
    print(a)

    a = make_word_trie(text)
    
    a = autocorrect(a,"tear",9)
    print(a)

    a = make_word_trie(text)

    a = word_filter(a,"r?c*t")
    b = []
    for i in a:
        b+=[i[0]]
    print(b)


