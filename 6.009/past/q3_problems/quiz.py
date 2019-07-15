# NO IMPORTS!

##############
# Problem 01 #
##############

def count_viable(weights, capacity):

    ans = helper(weights,capacity)
    return ans+1
def helper(weights, capacity,curr = []):
    # print(weights,capacity,curr)
    if capacity <= 0:
        return 0
    if len(weights) == 0:
        return 0
    ans = 0
    if weights[0] <= capacity:
        temp = weights[0]
        ans+=1
        ans+=helper(weights[1:],capacity-temp,curr+[temp])
    ans+= helper(weights[1:],capacity,curr)

    return ans


##############
# Problem 02 #
##############

def find_valid_ordering(class_graph):
    """ Returns a valid ordering of classes """
    # print(class_graph)
    ans = []
    for each in class_graph:
        ans+=[each]
    return ans

##############
# Problem 03 #
##############

def build_rep(default_db, update_db):
    """ Returns a representation of the information in default_db and update_db.
        This representation will be used to implement the other methods."""
    # Default Representation
    rep = [default_db, update_db] # CHANGE ME!
    total = set()

    for i in range(1,16):
        for j in default_db:
            # print(j+[str(i)])
            total.add(tuple(j+[str(i)]))
    # print(total )
    for i in update_db:
        # print(i)
        if i[0] == "ADD":
            total.add(tuple(i[1:]))
        else:
            total.remove(tuple(i[1:]))
    # print(total)
    return total
# print(build_rep([
#       ["6.009", "15", "Monday"],
#       ["6.009", "14", "Friday"],
#       ["6.01", "10", "Tuesday"],
#     ], [
#       ["ADD", "6.009", "12", "Thursday", "15"],
#       ["DELETE", "6.009", "15", "Monday", "15"]
#     ]))


def get_class_days(class_list, rep):
    """ Returns a list of lists class_dates where class_dates[i] is a list of all
        dates on which class_list[i] meets """
    # for a in rep:
    #     print(a)
    dic = {}
    for c in class_list:
        dic[c] = []
    for r in rep:
        for c in dic:
            if c in r:
                # print(r[0],r[1:])
                dic[c].append([r[3],r[2]])

    ans = []
    for c in dic:
        ans += [dic[c]]
    return ans




def get_late_classes(time, rep):
    """ Returns a list of all classes that never meet before the specified time """
    ans = []
    notCorr = []

    # for a in rep:
    #     print(a)
    # print(time)
    for r in rep:
        if int(r[1])>=int(time):
            if r[0] not in ans and r[0] not in notCorr:
                ans+=[r[0]]
        else:
            if r[0] in ans:
                ans.remove(r[0])
            if r[0] not in notCorr:
                notCorr+=[r[0]]
    return ans




    raise NotImplementedError


##############
# Problem 04 #
##############

class TermRecords():
    """Track subjects and students through the term."""

    def __init__(self,records):
        """Initialize term from list of records.

        Each record has the following form:
            {"student": student, "subjects": [subject, subject, ...]}
        """
        self.students = set()
        self.dic = {}
        self.reg = {}
        for each in records:
            stud = each["student"]
            classes = each["subjects"]
            self.dic[stud] = classes

            for c in classes:
                if c not in self.reg:
                    self.reg[c] = set([stud])
                else:
                    self.reg[c] .add(stud)





    def transcript(self,student_id):
        """Return list of subjects for which student is registered."""
        if student_id in self.dic:
            return self.dic[student_id]

    def classlist(self,subject):
        """Return list of students registered for `subject`."""
        if subject in self.reg:
            return list(self.reg[subject])

    def add(self,s,sub):
        """Specified student has added a `subject`.

        Should also handle the following cases:
        -- student didn't exist before
        -- subject didn't exist before
        -- student was already registered for subject
        """

        if s not in self.dic:
            self.dic[s] = []
        if sub not in self.reg:
            self.reg[sub] = set()
        if sub in self.dic[s]:
            return
        self.dic[s]+=[sub]
        self.reg[sub].add(s)


    def drop(self,s,sub):
        """Specified student has dropped a subject.

        Should also handle the following cases:
        -- student doesn't exist
        -- subject doesn't exist
        -- student wasn't registered for subject
        """
        if s not in self.dic:
            return
        if sub not in self.reg:
            return
        if not sub in self.dic[s]:
            return
        self.dic[s].remove(sub)
        self.reg[sub].remove(s)

    def too_many_subjects(self,limit):
        """Return list of students registered for more than `limit` subjects."""
        ans = []
        for s in self.dic:
            if len(self.dic[s])>limit :
                ans+=[s]
        return ans

    def enrollments(self):
        """Return list of [subject, # of registered students] for all subjects."""
        ans = []

        for each in self.reg:
            ans+=[[each,len(self.reg[each])]]
        return ans

    def taking_all(self,subject_list):
        """Return list of students taking *all* of the listed subjects."""

        ans = []
        for stud in self.dic:
            correct = True
            curr = self.dic[stud]
            for each in subject_list:
                if each not in curr:
                    correct = False
            if  correct:
                ans+=[stud]
        return ans

    def taking_some(self,subject_list):
        """Return list of students taking *at least one* of the listed subjects."""
        ans = []
        for stud in self.dic:
            correct = False
            curr = self.dic[stud]
            for each in subject_list:
                if each  in curr:
                    correct = True
                    break
            if  correct:
                ans+=[stud]
        return ans

    def better_together(self,N):
        """Return count of students who have at least n subjects in
        common with at least one other student."""
        count = 0
        for stud in self.dic:
            c1 = set(self.dic[stud])
            bool = False
            for other in self.dic:
                if stud != other:
                    c2 = set(self.dic[other])
                    un = c1 & c2
                    if len(un) >= N:
                        bool = True
                        break
            if bool:
                count+=1
        return count


##############
# Problem 05 #
##############

def has_liberty(board,row,col,explored = None,color = None):
    """Return ``True`` if stone at intersection (`row`, `col`) has
    at least one liberty or if there is no stone at the
    intersection, ''False'' if the stone has no liberties."""
    if explored == None:
        explored = []
    explored+=[(row,col)]
    if color == None:
        color = board[row][col]

    if board[row][col] == ".":
        return True
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    for d in dirs:
        i = row+d[0]
        j = col+d[1]
        if inRange(board,i,j) and (i,j) not in explored and (board[i][j] == color or board[i][j] == "."):
            if has_liberty(board,i,j,explored,color):
                return True
    return False

def capture(b,c):
    """Return updated `board` with all the captured stones of
    specified `color` removed."""
    # print(c)
    # for each in b:
    #     print(each)

    remove = []
    for i in range(len(b)):
        for j in range(len(b[i])):
            if b[i][j] == c:
                if not has_liberty(b,i,j):
                    remove+=[(i,j)]
    for coord in remove:
        i = coord[0]
        j = coord[1]
        b[i] = b[i][:j]+"."+b[i][j+1:]
    return b



def inRange(b,i,j):
    if i >= 0 and i < len(b) and j < len(b) and j >= 0 :
        return True
    return False

# handy test board
board= [
  '.bwwb',
  'bbwwb',
  'bwb.w',
  'bbwbw',
  'wbwwb'
]


##############
# Problem 06 #
##############

def count_straights(k, L, n):
    """
    Count the possible hands in k-Label Poker where
      k = # labels
      L = # levels, 1...L inclusive
      n = number cards in a hand

    """
    def helper(n):
        if n == 0:
            return []
        if n == 1:
            return [[c] for c in possible_cards(k, L)]
        else:
            hands = []
            sofar = helper(n-1)
            for h in sofar:
                last_val = h[-1][-1]
                for c in possible_cards(k, L):
                    if in_order(last_val, c) and c not in h:
                        hands.append(h+[c])
            return hands

    straights = helper(n)
    length = len(straights)
    return length

def in_order(prev, card):
    for i in card:
        if i < prev:
            return False
        prev = i
    return True

def possible_cards(k, L):
    if k == 1:
        for label in range(1, L+1):
            yield tuple([label])
    else:
        for p in possible_cards(k - 1, L):
            last = p[-1]
            for label in range(1, L+1):
                if label >= last:
                    yield p + tuple([label])


##############
# Problem 07 #
##############

def build_schedule_rep(default_db, update_db):

    total = set()

    for c in default_db:
        name = c[0]
        time = c[1]
        day = c[2]
        loc = c[3]
        for num in range(16):
            new = tuple([name,time,day,loc,str(num)])
            total.add(new)

    for up in update_db:
        name = up[1]

        if up[0] == "ADD":
            total.add(tuple(up[1:]))
        elif tuple(up[1:]) in total:
            total.remove(tuple(up[1:]))

    return total


def get_near_classes(buildings, rep):
    """
    OUTPUT: A list, in no particular order, of all classes that meet
    only in the list of buildings given by `buildings`.
    """
    where = {}
    for r in rep:
        name = r[0]
        if name not in where:
            where[name] = set()
        where[name].add(r[3])
    ans = []
    for name in where:
        locs = where[name]
        if locs.issubset(set(buildings)):
            ans+=[name]
    return ans

def earliest_meeting(building, day_of_week, rep):
    """
    OUTPUT: An integer earliest time (hour, such as 9),
    the earliest meeting given by the combined database of classes,
    occurring on any week in `building` on `day_of_week`.
    If no meetings take place on `day_of_week` in that building on any
     week, return `None`.
    """

    map = {}

    for i in range(9,21):
        map[i] = i
        if i>12:
            map[i-12] = i




    ans = None
    for meet in rep:
        day = meet[2]
        b = meet[3]
        time = map[int(meet[1])]
        if building == b and day == day_of_week:
            if ans == None:
                ans = time
            ans = min(ans,time)

    return ans

def have_conflicts(class_list, rep):
    """
    OUTPUT: A Boolean (True/False) indicating whether any two classes
    in class_list conflict. Two classes conflict when they meet on the same day
    of the week during the same week at the same time.
    """
    all = set()
    meets = []

    for r in rep:
        name = r[0]
        time = r[1]
        day = r[2]
        week = r[4]
        if name in class_list:
            # print(r)
            all.add((time,day,week))
            meets+=[(time,day,week)]

    return len(all)!=len(meets)



##############
# Problem 08 #
##############

def k_mins(seq, k):
    i = 0
    len_seq = len(seq)
    while i < len_seq:
        elt = seq[i]
        if all(elt <= seq[j] for j in range(max(0, i-k), i)) and  all(elt <= seq[j] for j in range(min(len_seq, i+1), min(len_seq, i+1+k))):
            yield elt
        i += 1

##############
# Problem 09 #
##############

with open('words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

def correct(arr):
    return all(is_word(x) for x in arr)

def split_words(x):
    if len(x) == 0:
        yield ()
        return
    for ix in range(len(x)+1):
        first = x[:ix]
        rest = x[ix:]
        if is_word(first):
            for result in split_words(rest):
                yield (first, ) + result


if __name__ == '__main__':
    pass
