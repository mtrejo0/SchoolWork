# NO IMPORTS!

#############
# Problem 1 #
#############

def mix_tape(songs, duration):
    if duration == 0:
        return []
    if duration < 0:
        return None
    for song, dur in songs.items():
        rec_result = mix_tape({k:v for k,v in songs.items() if k != song}, duration-dur)
        if rec_result is not None:
            return [song] + rec_result
    return None


#############
# Problem 2 #
#############

def k_mins(seq, k):
    raise NotImplementedError # reserved for Quiz 3 practice


#############
# Problem 3 #
#############

def scenic_route(grid):
    def in_bounds(loc):
        return 0 <= loc[0] < len(grid) and 0 <= loc[1] < len(grid[0])

    def length_from_loc(loc, seen=None):
        seen = seen or set()
        r, c = loc
        if grid[r][c] == 'G':
            return 0
        elif grid[r][c] == 'X':
            return None

        results = {length_from_loc(new_loc, seen | {loc})
                   for new_loc in ((r+1, c), (r-1, c), (r, c+1), (r, c-1))
                   if new_loc not in seen and in_bounds(new_loc)}
        results = {i for i in results if i is not None}
        if not results:
            return None
        return 1 + max(results)

    s = None
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'S':
                s = (r, c)
                break
    return length_from_loc(s)


if __name__ == "__main__":
    pass
