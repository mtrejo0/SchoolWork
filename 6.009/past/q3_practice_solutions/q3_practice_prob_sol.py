# 6.009 Spring 2019 - Quiz 3 Practice Problems Solutions


##############
# Problem 01 #
##############

def count_viable(weights, capacity):
    """ Returns the number of viable sets of animals """
    # only weights <= capacity are possible
    valid_weights = [w for w in weights if w <= capacity]
    if len(valid_weights) == 0: # base case
        return 1 # only empty set
    # can decide yes/no for first animal
    return count_viable(valid_weights[1:], capacity) + count_viable(
            valid_weights[1:], capacity - valid_weights[0])


##############
# Problem 02 #
##############

def find_valid_ordering(class_graph):
    """ Returns a valid ordering of classes """
    # build dict: class => list of required pre-reqs
    prereqs = {}
    for p,clist in class_graph.items():
        # p is a prereq for all the classes on clist
        for c in clist:
            # add c to p's list of classes
            if not c in prereqs:
                prereqs[c] = []
            prereqs[c].append(p)

    taken = []  # list of taken courses

    # do what it takes to add subj to list of taken courses
    def take(subj):
        # already taken: done!
        if subj in taken:
            return
        # take all the pre-reqs
        for c in prereqs.get(subj,[]):
            take(c)
        # finally take requested course
        taken.append(subj)

    # take all the courses!
    for c in class_graph:
        take(c)

    # return taken list
    return taken


##############
# Problem 03 #
##############

def build_rep(default_db, update_db):
    """ Returns a representation of the information in default_db and update_db.
        This representation will be used to implement the other methods."""
    meetings = {}  # subj => list of (week, day, time)

    # start by processing default schedule to create complete
    # of meetings for each class
    for subj,time,day in default_db:
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        for week in range(1,16):
            mlist.append((str(week),day,time))

    # now process updates
    for action,subj,time,day,week in update_db:
        # get list of meetings for this subj
        mlist = meetings.get(subj,[])
        meetings[subj] = mlist  # in case mlist is brand new
        # process udpate
        if action == 'DELETE':
            mlist.remove((week,day,time))
        elif action == 'ADD':
            mlist.append((week,day,time))

    return meetings

# Returns a list of lists class_dates where class_dates[i] is a list of all
#  dates on which class_list[i] meets
def get_class_days(class_list, rep):
    result = [[[week,day] for week,day,time in rep.get(subj,[])]
              for subj in class_list]
    return result

# Returns a list of all classes that never meet before the specified time
def get_late_classes(time, rep):
    # return True if there's no meeting time on mlist
    # that's before xtime
    def never_meet_before(mlist,xtime):
        xtime = int(xtime)
        for week,day,time in mlist:
            if int(time) < xtime:
                return False
        return True

    return [subj
            for subj in rep
            if never_meet_before(rep[subj],time)]


##############
# Problem 04 #
##############

class TermRecords():
    """Track subjects and students through the term."""
    # initialize term from list of records of the form
    # {"student_id": student_id, "subjects": [subject, subject, ...]}
    def __init__(self,records):
        self.students = {}   # student => set of subjects
        self.subjects = {}   # subject => set of students

        for record in records:
            sid = record['student']
            slist = record['subjects']

            self.students[sid] = set(slist)
            for subj in slist:
                if subj not in self.subjects:
                    self.subjects[subj] = set()
                self.subjects[subj].add(sid)

    # return list of records that captures all the information
    # in the database.  Each record has the form
    # {"student": student, "subjects": [subject, subject, ...]}
    def dump(self):
        return [{"student": sid,
                 "subjects": slist}
                for sid,slist in self.students.items()]

    # specified student has added a subject.  Should
    # also handle the following cases:
    #  -- student didn't exist before
    #  -- subject didn't exist before
    #  -- student was already registered for subject
    def add(self,student,subject):
        # add subject to student's list
        if student not in self.students:
            self.students[student] = set()
        self.students[student].add(subject)

        # add student to subject's list
        if subject not in self.subjects:
            self.subjects[subject] = set()
        self.subjects[subject].add(student)

    # specified student has dropped a subject.  Should
    # also handle the following cases:
    #   -- student doesn't exist
    #   -- subject doesn't exist
    #   -- student wasn't registered for subject
    def drop(self,student,subject):
        if student in self.students:
            self.students[student].discard(subject)
            self.subjects[subject].discard(student)

    # return list of subjects for which student is registered
    def transcript(self,student):
        t = self.students.get(student,None)
        if isinstance(t,set): t = list(t)
        return t

    # return list of students registered for subject
    def classlist(self,subject):
        t = self.subjects.get(subject,None)
        if isinstance(t,set): t = list(t)
        return t

    # return list of students registered for more than limit subjects
    def too_many_subjects(self,limit):
        return [sid for sid,slist in self.students.items() if len(slist) > limit]

    # return list of (subject, # of registered students) for all subjects
    def enrollments(self):
        return [[s,len(slist)] for s,slist in self.subjects.items()]

    # return list of students taking *all* of the listed subjects
    def taking_all(self,subject_list):
        result = None
        for subj in subject_list:
            sset = self.subjects.get(subj,set())
            if result is None:
                result = sset
            else:
                result = result.intersection(sset)
        return [] if result is None else list(result)

    # return list of students taking at least one of the listed subjects
    def taking_some(self,subject_list):
        result = None
        for subj in subject_list:
            sset = self.subjects.get(subj,set())
            if result is None:
                result = sset
            else:
                result = result.union(sset)
        return [] if result is None else list(result)

    # return count of students who have at least n subjects in
    # common with at least one other student
    def better_together(self,n):
        # try all pairings of students to see if they have at
        # least n classes in common.
        return len({s1
                    for s1,slist1 in self.students.items()
                    for s2,slist2 in self.students.items()
                    if s1 != s2 and len(slist1 & slist2) >= n})


##############
# Problem 05 #
##############

def has_liberty(board,row,col):
    """Return ``True`` if stone at intersection (`row`, `col`) has
    at least one liberty or if there is no stone at the
    intersection, ''False'' if the stone has no liberties."""
    # keep track of visited intersections
    visited = [[False
                for c in range(len(board[0]))]
               for r in range(len(board))]

    h = len(board)
    w = len(board[0])
    color = board[row][col]

    def visit(r,c):
        if not (0 <= r < h) or not (0 <= c < w) or visited[r][c]:
            return False
        if board[r][c] == '.':
            return True
        if board[r][c] != color:
            return False
        visited[r][c] = True
        return visit(r-1,c) or visit(r+1,c) or visit(r,c-1) or visit(r,c+1)

    return visit(row,col)

def capture(board,color):
    """Return updated `board` with all the captured stones of
    specified `color` removed."""
    h = len(board)
    w = len(board[0])

    # find set of captured stones
    captured = set()
    for r in range(h):
        for c in range(w):
            if board[r][c]==color and not has_liberty(board,r,c):
                captured.add((r,c))

    # build updated board
    update = []
    for r in range(h):
        row = ['.' if (r,c) in captured else board[r][c]
               for c in range(w)]
        update.append(''.join(row))
    return update

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

# Returns a representation of the information in default_db and update_db
#  This representation will be used to implement the other methods
class Subject:
    def __init__(self, name):
        self.name = name
        self.meetings = set()

    def schedule(self, time, day, building):
        self.meetings.update([(time, day, building, str(week)) for week in range(1,16)])

    def add(self, elt):
        self.meetings.add(elt)

    def remove(self, elt):
        self.meetings.remove(elt)

    def __iter__(self):
        return ((time,day,building,week) for (time, day, building, week) in self.meetings)

    def met_before(self, thres):
        return (min([int(time) for (time, day, building, week) in self.meetings]) >= thres)

    def meets_only_in(self, buildings):
        for time,day,building,week in self.meetings:
            if building not in buildings:
                return False
        return True

    def conflict(self, other):
        for t1,d1,b1,w1 in self:
            for t2,d2,b2,w2 in other:
                if t1==t2 and d1==d2 and w1==w2:
                    return True
        return False

    def __str__(self):
        return "<subject " + self.name + " " + str(self.meetings) + ">"

    def __repr__(self):
        return str(self)

def build_schedule_rep(default_db, update_db):
    subjects = {}  # subj (type string) => list of (week, day, time, building)

    # start by processing default schedule to create complete
    # of meetings for each class
    for subj,time,day,building in default_db:
        subjects.setdefault(subj, Subject(subj)).schedule(time, day, building)

    # now process updates
    for action,subj,time,day,building,week in update_db:
        # get list of meetings for this subj
        if action == 'DELETE':
            subjects[subj].remove((time, day, building, week))
        elif action == 'ADD':
            subjects.get(subj, Subject(subj)).add((time, day, building, week))

    return subjects

# OUTPUT: A list, in no particular order, of all classes that meet
# only in the list of buildings given by `buildings`.
def get_near_classes(buildings, rep):
    return [subj for subj in rep if rep[subj].meets_only_in(buildings)]

# OUTPUT: An integer earliest time (hour, such as `9`),
# the earliest meeting given by the combined database of classes,
# occurring on any week in `building` on `day_of_week`.
# If no meetings take place on `day_of_week` in that building on any
# week, return `None`.
def earliest_meeting(building, day_of_week, rep):
    earliest = 25
    for subj_name, subj  in rep.items():
        for t,d,b,w in subj:
            if b == building and d == day_of_week:
                earliest = min(earliest, int(t))
    return None if earliest == 25 else earliest

# OUTPUT: A Boolean (`True`/`False`) indicating whether any two classes
# in class_list conflict. Two classes conflict when they meet on the same day
# of the week during the same week at the same time.
def have_conflicts(class_list, rep):
    if class_list == []:
        return False
    for i in range(len(class_list)-1):
        cname = class_list[i]
        if cname in rep:
            c = rep[cname]
            for other in class_list[i+1:]:
                if other in rep:
                    if c.conflict(rep[other]):
                        return True
    return False


##############
# Problem 08 #
##############

def k_mins(seq, k):
    i = 0
    len_seq = len(seq)
    while i < len_seq:
        elt = seq[i]
        if all(elt <= seq[j] for j in range(max(0, i-k), i)) and \
           all(elt <= seq[j] for j in range(min(len_seq, i+1), min(len_seq, i+1+k))):
            yield elt
        i += 1


##############
# Problem 09 #
##############

with open('words2.txt') as f:
    allwords = set(f.read().splitlines())

def is_word(x):
    return x in allwords

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
