"""6.009 Spring 2019 Lab 8 -- 6.009 Zoo"""

# NO IMPORTS ALLOWED!

class Constants:
    """
    A collection of game-specific constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    # width and height of keepers
    KEEPER_WIDTH = 31
    KEEPER_HEIGHT = 31

    # width and height of animals
    ANIMAL_WIDTH = 31
    ANIMAL_HEIGHT = 31

    # width and height of food
    FOOD_WIDTH = 11
    FOOD_HEIGHT = 11

    # width and height of rocks
    ROCK_WIDTH = 51
    ROCK_HEIGHT = 51

    # thickness of the path
    PATH_THICKNESS = 31

    TEXTURES = {
        'rock': '1f5ff',
        'animal': '1f418',
        'SpeedyZookeeper': '1f472',
        'ThriftyZookeeper': '1f46e',
        'OverreachingZookeeper': '1f477',
        'food': '1f34e'
    }

    KEEPER_INFO = {'SpeedyZookeeper':
                   {'price': 250,
                    'range': 50,
                    'throw_speed_mag': 20},
                   'ThriftyZookeeper':
                   {'price': 100,
                    'range': 100,
                    'throw_speed_mag': 15},
                   'OverreachingZookeeper':
                   {'price': 150,
                    'range': 150,
                    'throw_speed_mag': 5}
                   }


class NotEnoughMoneyError(Exception):
    """A custom exception to be used when insufficient funds are available
    to hire new zookeepers."""
    pass



################################################################################
################################################################################
# Static methods.

def distance(a, b):
    """Returns the Euclidian distance between the two tuple coordinates."""
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5



################################################################################
################################################################################

class Game:
    def __init__(self, game_info):
        """Initializes the game.

        `game_info` is a dictionary formatted in the following manner:
          { 'width': The width of the game grid, in an integer (i.e. number of pixels).
            'height': The height of the game grid, in an integer (i.e. number of pixels).
            'rocks': The set of tuple rock coordinates.
            'path_corners': An ordered list of coordinate tuples. The first
                            coordinate is the starting point of the path, the
                            last point is the end point (both of which lie on
                            the edges of the gameboard), and the other points
                            are corner ("turning") points on the path.
            'money': The money balance with which the player begins.
            'spawn_interval': The interval (in timesteps) for spawning animals
                              to the game.
            'animal_speed': The magnitude of the speed at which the animals move
                            along the path, in units of grid distance traversed
                            per timestep.
            'num_allowed_unfed': The number of animals allowed to finish the
                                 path unfed before the player loses.
          }
        """
        self.width = game_info["width"]
        self.height = game_info["height"]
        self.rockLocs = game_info["rocks"]
        self.path_corners = game_info["path_corners"]
        self.money = game_info["money"]
        self.spawn_interval = game_info["spawn_interval"]
        self.animal_speed = game_info["animal_speed"]
        self.num_allowed_unfed = game_info["num_allowed_unfed"]
        self.status = "ongoing"
        self.time = 0

        # initialize having empty list og all elements
        self.mobs = []
        self.rocks = []
        self.keepers = []
        self.food = []
        # empty dictionary to fill in later
        self.disp= {}
        self.numUnfed = 0
        self.pathBoxes = []

        # to remember mouse choice
        self.choice = None


        
        self.makePathHitBox()
        self.makePathDict()


        for loc in self.rockLocs:
          self.rocks+=[Rock(loc)]


    def makePathHitBox(self):
      # defines each path as a box to pass in to box collision
      thick = Constants.PATH_THICKNESS
      for i in range(len(self.path_corners)-1):
        # picks consecutive corners to use to make a box for the path between them
        pre = self.path_corners[i]
        post = self.path_corners[i+1]

        if(pre[0] == post[0]):
          #same vertical same X
          if(pre[1] < post[1]):
            self.pathBoxes.append([(pre[0]-thick//2,pre[1]-thick//2),thick,abs(post[1]-pre[1])+thick])
          else:
            self.pathBoxes.append([(post[0]-thick//2,post[1]-thick//2),thick,abs(post[1]-pre[1])+thick])
        elif(pre[1] == post[1]):
          #same horizontal same Y
          if(pre[0] < post[0]):
            self.pathBoxes.append([(pre[0]-thick//2,pre[1]-thick//2),abs(post[0]-pre[0])+thick,thick])
          else:
            self.pathBoxes.append([(post[0]-thick//2,post[1]-thick//2),abs(post[0]-pre[0])+thick,thick])
        
    def makePathDict(self):
      # makes a dictionary that maps the distance from the beginning
      # to coordinates in the plane
      d = 0
      for i in range(len(self.path_corners)-1):
        # chooses consecutive path corners to go through each of the coordinates between them
        pre = self.path_corners[i]
        post = self.path_corners[i+1]
        if(pre[0] == post[0]):
          #same vertical same X
          if(pre[1] < post[1]):
            #moving down
            x = pre[0]
            for y in range(pre[1],post[1]):
              self.disp[d] = (x,y)
              d+=1
          else:
            #moving up
            x = pre[0]
            for y in range(pre[1],post[1],-1):
              self.disp[d] = (x,y)
              d+=1
        elif(pre[1] == post[1]):
          #same horizontal same Y
          if(pre[0] < post[0]):
            #moving right
            y = pre[1]
            for x in range(pre[0],post[0]):
              self.disp[d] = (x,y)
              d+=1
          else:
            #moving left
            y = pre[1]
            for x in range(pre[0],post[0],-1):
              self.disp[d] = (x,y)
              d+=1
      # accounts for the very last coordinate and remembers the displacement of that one
      last = self.path_corners[-1]
      self.disp[d] = (last[0],last[1])
      self.maxD = d


        

    def render(self):
        serial = {"formations":[],
                  "money":self.money,
                  "status":self.status,
                  "num_allowed_remaining":self.num_allowed_unfed - self.numUnfed}
        """Renders the game in a form that can be parsed by the UI.

        Returns a dictionary of the following form:
          { 'formations': A list of dictionaries in any order, each one
                          representing a formation. Each dictionary is of the form
                            `{'loc': (x, y),
                              'texture': texture,
                              'size': (width, height)}`
                          where `(x,y)` is the center coordinate of the formation,
                          `texture` is its texture, and it has `width` and `height`
                          dimensions. The dictionary should contain the
                          formations of all animals, zookeepers, rocks, and food.
            'money': The amount of money the player has available.
            'status': The current state of the game which can be 'ongoing' or 'defeat'.
            'num_allowed_remaining': The number of animals which are still
                                     allowed to exit the board before the game
                                     status is `'defeat'`.
          }
        """
        
        # goes through each type of formation and adds tem given their attributes
        for each in self.mobs:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)
        for each in self.rocks:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)
        for each in self.keepers:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)
        for each in self.food:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)

        return serial

    def timestep(self, mouse=None):
        """Simulates the evolution of the game by one timestep.

        In this order:
            (0. Do not take any action if the player is already defeated.)
            1. Compute any changes in formation locations, and remove any
                off-board formations.
            2. Handle any food-animal collisions, and remove the fed animals
                and eaten food.
            3. Throw new food if possible.
            4. Spawn a new animal from the path's start if needed.
            5. Handle mouse input, which is the integer coordinate of a player's
               click, the string label of a particular zookeeper type, or `None`.
            6. Redeem one unit money per animal fed this timestep.
            7. Check for the losing condition to update the game status if needed.
        """
        # only do things if game isnt lost
        if self.status == "ongoing":
          # 1. Compute any changes in formation locations, and remove any
          #       off-board formations.
          # update mob movement
          remove = []
          for each in self.mobs:
              try:
                each.update()
              except KeyError:
                # if the mob is at a position not on the board remove it and decrement lives
                remove.append(each)
                self. numUnfed+=1
          # remove any that should be removes
          for each in remove:
            self.mobs.remove(each)

          # remove food off the screen
          remove = []
          for each in self.food:
            each.update()
            if not each.inRange((0,self.width),(0,self.height)):
              remove+=[each]
          for each in remove:
            if each in self.food:
              self.food.remove(each)

          # 2. Handle any food-animal collisions, and remove the fed animals
          #       and eaten food.
          # remove animals that have been hit
          removeFood = []
          removeMob = []
          moneyGain = 0
          # go through all mobs
          for mob in self.mobs:
            # go through all food
            for food in self.food:
              if self.boxCollision(((mob.pos[0]-mob.w/2,mob.pos[1]-mob.h/2),mob.w,mob.h),((food.pos[0]-food.w/2,food.pos[1]-food.h/2),food.w,food.h)):
                # if there is a box collision remove all food and the mob that collide with it
                if mob not in removeMob:
                  moneyGain+=1
                  removeMob+=[mob]
                removeFood+=[food]

          # remove these after the fact
          for each in removeFood:
            if each in self.food:
              self.food.remove(each)
          for each in removeMob:
            if each in self.mobs:
              self.mobs.remove(each)

          # 3. Throw new food if possible.
          # new food
          for keep in self.keepers:
            # for every keeper find its mob to aim at
            r = keep.range
            bestMob = None
            bestD = 0
            for mob in self.mobs:
              # remember the mob that is hungriest in the path
              dist = distance(keep.pos,mob.pos)
              if r >= dist:
                if bestD <= mob.d:
                  bestD = mob.d
                  bestMob = mob
                  
            if bestMob:
              # if there is a mob that exists find the loation to aim at
              curr = bestMob.d
              best = float("inf")
              aim = None
              for curr in range(curr+1,self.maxD+1):
                # go through each displacement
                currCord = self.disp[curr]
                time = distance(currCord,keep.pos)/keep.speed
                # find time it will take for food to reach this spot
                animalTime = abs(curr - bestMob.d)/mob.speed
                # how long the animal will take to get to that spot and the difference
                diff = abs(time - animalTime)
                # remember the best ones
                if best > diff:
                  best = diff
                  aim = currCord

              if aim:
                # make new food aimed at best spot
                self.food+=[Food(keep.pos,self.foodVel(keep.speed,keep.pos,aim))]

          if(self.time % self.spawn_interval == 0):
              # spawn new mob at start
              self.mobs.append( Mob( self.path_corners[0] ,self.disp, self.animal_speed))
          
          # 5. Handle mouse input, which is the integer coordinate of a player's
          #      click, the string label of a particular zookeeper type, or `None`.
            
          if mouse:
            if type(mouse) == str:
              # if you chose a keep er remember it for next timestep
              self.choice = mouse

            elif(self.choice):

              info = Constants.KEEPER_INFO[self.choice]
              if(info["price"] <= self.money):
                # we have enough money
                if(self.noCollisons(mouse)):
                  # the keeper can be placed at these coordinates
                  self.money -= info["price"]
                  # add a new keeper at this loc
                  self.keepers+=[Zookeeper(mouse,self.choice,info["range"],info["throw_speed_mag"])]
              else:
                raise NotEnoughMoneyError
          # 6. Redeem one unit money per animal fed this timestep.

          self.money+=moneyGain
          # 7. Check for the losing condition to update the game status if needed.
          if(self.numUnfed == self.num_allowed_unfed+1):
            self.status = "defeat"
          self.time+=1

    def foodVel(self,speed,keeper,mob):

      # gets unit vector of velocity then multiplies it by throwing speed
      deltaX = mob[0] - keeper[0]
      deltaY = mob[1] - keeper[1]

      mag = ((deltaX**2+deltaY**2)**.5)
      deltaX = deltaX*speed/mag
      deltaY = deltaY*speed/mag
      return(deltaX,deltaY)


    def noCollisons(self,mouse):

      # goes through all roks and paths and makes sure there
      # is no conflicts between them and the keepers
      x = mouse[0] - Constants.KEEPER_WIDTH//2
      y = mouse[1] - Constants.KEEPER_HEIGHT//2
      keeper = [(x,y),Constants.KEEPER_WIDTH,Constants.KEEPER_HEIGHT]
      
      for each in self.rocks:
        if self.boxCollision(keeper,[each.pos,each.w,each.h]):
          return False
      for each in self.pathBoxes:
        if self.boxCollision(keeper,each):
          return False
      return True

    def boxCollision(self,a,b):
      # defines the top left and bottom right points of a box


      la = a[0]
      ra = (a[0][0]+a[1],a[0][1]+a[2])
      lb = b[0]
      rb = (b[0][0]+b[1],b[0][1]+b[2])
      # checks if opposite left and right edges of the boxes are on one side of the other
      if la[0] >= rb[0] or ra[0] <= lb[0]:
        return False
      # checks if the opposite top and bottom edges of te boxes are on one side of the other
      if la[1] >= rb[1] or ra[1] <= lb[1]:  
        return False
      # this means that there must be a collision
      return True

################################################################################
################################################################################
# TODO: Add additional classes here.
class Zookeeper():
  def __init__(self,pos,tipe,rang,speed):
    self.w = Constants.KEEPER_WIDTH
    self.h = Constants.KEEPER_HEIGHT

    self.pos = (pos[0],pos[1])
    self.texture = Constants.TEXTURES[tipe]
    self.type = tipe
    self.size = (self.w,self.h)
    self.range = rang
    self.speed = speed


class Mob():

  def __init__(self,pos,dispDic,speed):
    self.pos = list(pos)

    # print("x",self.pos)
    self.w = Constants.ANIMAL_WIDTH
    self.h = Constants.ANIMAL_HEIGHT
    self.texture = Constants.TEXTURES["animal"]
    self.size = (self.w,self.h)
    self.d = 0
    self.dispDic = dispDic
    self.speed = speed

  def update(self):
    # updates the position given the speed 
    self.d+=self.speed
    self.pos = self.dispDic[self.d]
    


class Food():
  def __init__(self,pos,vel):
    self.pos = list(pos)
    self.vel = list(vel)
    self.w = Constants.FOOD_WIDTH
    self.h = Constants.FOOD_HEIGHT
    self.size = (self.w,self.h)
    self.texture = Constants.TEXTURES["food"]

  def update(self):
    # updates position givent he velocity
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]
  def inRange(self,x,y):
    # checks if the food is still on the screen
    if self.pos[0] >= x[0] and self.pos[0] <=x[1] and self.pos[1] >= y[0] and self.pos[1] <=y[1]:
      return True
    return False



class Rock():

  def __init__(self,pos):
    self.pos = list(pos)
    self.w = Constants.ROCK_WIDTH
    self.h = Constants.ROCK_HEIGHT
    self.texture = Constants.TEXTURES["rock"]
    self.size = (self.w,self.h)


################################################################################
################################################################################



if __name__ == '__main__':
  info = {
    "width": 640,
    "height": 480,
    "path_corners": [
        [0, 0],
        [50, 0],
        [50, 40],
        [90, 40],
        [90, 10],
        [130, 10],
        [130, 99],
        [60, 99],
        [60, 130],
        [400, 130],
        [400, 100],
        [500, 100],
        [500, 480]
    ],
    "rocks": [
        [60, 300],
        [200, 200]
    ],
    "money": 5000,
    "num_allowed_unfed": 30,
    "spawn_interval": 1,
    "animal_speed": 30
}
  # info = {"width":20,"height":40,"rocks":[],"path_corners":[[0,10],[20,10]],"money":0,"spawn_interval":1,"animal_speed":1,"num_allowed_unfed":13}
  game = Game(info)


  for i in ["ThriftyZookeeper", [20,80],"SpeedyZookeeper", [60,165],"SpeedyZookeeper", [300, 165], None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]:
    game.timestep(i)
    a = game.render()
    for each in a["formations"]:
      print(each)
    input()

