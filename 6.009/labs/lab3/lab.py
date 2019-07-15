"""6.009 Lab 3 -- HyperMines"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


class HyperMinesGame:
    def __init__(self, dimensions, bombs):
        self.dimensions = dimensions
        self.mask = self.make_board(dimensions,False)
        self.board = self.make_board(dimensions,0)
        self.state = 'ongoing' 
        self.allofem = self.all_coords()

        for bomb in bombs:

            if(self.is_in_bounds(bomb)):
                self.set_coords(bomb,'.',self.board)

        for bomb in bombs:
            for neighbor in self.neighbors(bomb):
                
                if(self.is_in_bounds(neighbor) and self.get_coords(neighbor,self.board) != "."):
                    place = self.get_coords(neighbor,self.board)
                   
                    self.set_coords(neighbor,place+1, self.board)

    def get_coords(self,coords,board):
        if(len(coords)>0):
            return self.get_coords( coords[1:]  , board[coords[0]] )
        else:
            return board
            
        
    def set_coords(self, coords, value, board):
        if(len(coords) > 1): 
            self.set_coords(coords[1:], value, board[coords[0]]) 
        else: 
            board[coords[0]] = value

    def make_board(self, dimensions, elem):
        if(len(dimensions)>1):
            return [self.make_board(dimensions[1:],elem) for i in range(dimensions[0])]
        else:
            return [elem for i in range(dimensions[0])]

       


    def is_in_bounds(self, coords):
        return self.in_helper(coords,self.dimensions)
    def in_helper(self,coords,dimensions):
        if(not len(coords) == len(dimensions)):
            return False
        elif(len(coords)>0):
            if(coords[0] in range(dimensions[0])):
                return self.in_helper(coords[1:],dimensions[1:])
            else:
                return False
        else:
            return True
    def neighbors(self, coords):
        temp = []
        for dz in (-1,0,1):
            i = [coords[0]+dz]
            temp+=[i]
        return self.neighbor_helper(coords[1:],temp)
    def neighbor_helper(self,coords,all_neighbors):
        if(len(coords)>0):
            temp = []
            for i in all_neighbors:
                for dz in (-1,0,1):
                    cop = i[:]
                    cop.append(coords[0]+dz)
                    temp+=[cop]
            return self.neighbor_helper(coords[1:],temp)
        else:
            return [neighbor for neighbor in all_neighbors if self.is_in_bounds(neighbor)]






            
    def is_victory(self):
        points = self.allofem
        
        for point in points:
                if self.get_coords(point,self.board) == '.' and self.get_coords(point,self.mask): # A bomb square has been revealed
                    return False
                if self.get_coords(point,self.board) != '.' and not self.get_coords(point,self.mask): # A non-bomb square is not yet revealed
                    return False
        self.state = "victory"
        return True
    def all_coords(self):
        temp = []
        for i in range(self.dimensions[0]):
            temp+=[[i]]
        
        return self.all_helper(temp,self.dimensions[1:])
    def all_helper(self,points,dimensions):

        if(len(dimensions)>0):
            temp = []
            for i in points:
                for j in range(dimensions[0]):
                    cop = i[:]
                    cop.append(j)
                    temp+=[cop]
            return self.all_helper(temp,dimensions[1:])
        else:
            return points




    def dig(self, coords):

        if(self.get_coords(coords,self.mask)):
            return 0    


        if(not self.state == 'ongoing'):
            return 0

        self.set_coords(coords,True,self.mask)

        if(self.get_coords(coords,self.board) == '.'):
            self.state = 'defeat'
            return 1

        neighbors = self.neighbors(coords)

        if(not self.get_coords(coords,self.board) == 0):
            self.is_victory()
            return 1

        count = 1
        for n in neighbors:
            count += self.dig(n)
        self.is_victory()
        return count

        
        
        


    def render(self, xray=False):
        

        cop = self.make_board(self.dimensions,"_")
        points = self.allofem

        for point in points:
            valB = self.get_coords(point,self.board)
            valM = self.get_coords(point,self.mask)

            
            if(not valB == 0 and (valM or xray)):
                self.set_coords(point,str(valB),cop)
            elif(xray or valM):
                self.set_coords(point," ",cop)

        return cop

    # ***Methods below this point are for testing and debugging purposes only. Do not modify anything here!***

    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))

    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game

if __name__ == '__main__':
    a = HyperMinesGame([4,4],[[1,1],[0,1],[1,0]])
    print(a.board)
    b = a.board
    for i in b:
        print(i)
    
