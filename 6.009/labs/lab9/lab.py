"""6.009 Spring 2019 Lab 9 -- 6.009 Zoo"""

from math import ceil  # ONLY import allowed in this lab

# NO CUSTOM IMPORTS ALLOWED!

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

    # some other characters
    DEMON_WIDTH = 51
    DEMON_HEIGHT = 51
    DEMON_RADIUS = 75  # Only animals this close are affected.
    DEMON_MULTIPLIER = 2  # Animal speeds multiplied by this factor
    DEMON_PRICE = 100

    VHS_WIDTH = 31
    VHS_HEIGHT = 31
    VHS_RADIUS = 75
    VHS_MULTIPLIER = .5
    VHS_PRICE = 20

    CRAZY_NAP_LENGTH = 20
    SPLASH_LENGTH = 35

    TRAINEE_THRESHOLD = 20  # How many food hits must the trainee score,
    # before becoming a speedy zookeeper?a

    TEXTURES = {
        'rock': '1f5ff',
        'animal': '1f418',
        'SpeedyZookeeper': '1f472',
        'ThriftyZookeeper': '1f46e',
        'OverreachingZookeeper': '1f477',
        'food': '1f34e',
        'Demon': '1f479',
        'VHS': '1f4fc',
        'TraineeZookeeper': '1f476',
        'CrazyZookeeper': '1f61c',
        'SleepingZookeeper': '1f634',
        'SplashZookeeper': '1f608'
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
                        'throw_speed_mag': 5},
                   'TraineeZookeeper':
                       {'price': 50,
                        'range': 100,
                        'throw_speed_mag': 5},
                   'CrazyZookeeper':
                       {'price': 100,
                        'range': 1000,
                        'throw_speed_mag': 50},
                    'SplashZookeeper':
                       {'price': 200,
                        'range': 0,
                        'throw_speed_mag': 25}
                   }

# New spec for timestep(self, mouse):
# (0. Do not take any action if the player is already defeated.)
# 1. Compute the new speed of animals based on the presence of nearby VHS cassettes or demons.
# 2. Compute any changes in formation locations and remove any off-board formations.
# 3. Handle any food-animal collisions, and remove the fed animals and the eaten food.
# 4. Upgrade trainee zookeeper if needed.
# 5. Throw new food if possible.
# 6. Spawn a new animal from the path's start if needed.
# 7. Handle mouse input, which is the integer tuple coordinate of a player's click, the string label of a particular
#   zookeeper type, or None.
# 8. Redeem one dollar per animal fed this timestep.
# 9. Check for the losing condition.

################################################################################
##  Copy and paste your code from lab8 below EXCEPT for the Constants class.  ##
##  The Constants class above contains the changes needed for the lab.        ##
################################################################################


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
        self.demons = []
        self.vhss = []


        # to remember mouse choice
        self.choice = None


        # makes areas where nothing can be placed on due to paths
        self.makePathHitBox()
        # makes a dictionary mapping the displacement from the beginning to coords on the path
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
            self.pathBoxes.append([(pre[0]-thick/2,pre[1]-thick/2),thick,abs(post[1]-pre[1])+thick])
          else:
            self.pathBoxes.append([(post[0]-thick/2,post[1]-thick/2),thick,abs(post[1]-pre[1])+thick])
        elif(pre[1] == post[1]):
          #same horizontal same Y
          if(pre[0] < post[0]):
            self.pathBoxes.append([(pre[0]-thick/2,pre[1]-thick/2),abs(post[0]-pre[0])+thick,thick])
          else:
            self.pathBoxes.append([(post[0]-thick/2,post[1]-thick/2),abs(post[0]-pre[0])+thick,thick])

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
        for each in self.demons:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)
        for each in self.vhss:
          form = {"loc":each.pos,"texture":each.texture,"size":each.size}
          serial["formations"].append(form)


        return serial

    def timestep(self, mouse=None):

        # print (f"====================={self.time}======================")
        # only do things if game isnt lost
        if self.status == "ongoing":

            # (0. Do not take any action if the player is already defeated.)
            # 1. Compute the new speed of animals based on the presence of nearby VHS cassettes or demons.
            # 2. Compute any changes in formation locations and remove any off-board formations.
            # 3. Handle any food-animal collisions, and remove the fed animals and the eaten food.
            # 4. Upgrade trainee zookeeper if needed.
            # 5. Throw new food if possible.
            # 6. Spawn a new animal from the path's start if needed.
            # 7. Handle mouse input, which is the integer tuple coordinate of a player's click, the string label of a particular
            #   zookeeper type, or None.
            # 8. Redeem one dollar per animal fed this timestep.
            # 9. Check for the losing condition.

          # looks at every mob and looks at all multipiers and sees how much the speed would change
          for mob in self.mobs:
            change = 1
            for mult in self.demons+self.vhss:
              if distance(mult.pos,mob.pos) <= mult.r:
                change*=mult.multiplier
            # sets speed of animal to what it should be at that spot
            mob.speed = ceil(change*self.animal_speed)


          remove = []
          for mob in self.mobs:
              try:
                # adds speed animal should have at that spot to the pos
                mob.update()
              except KeyError:
                # if the mob is at a position not on the board remove it and decrement lives
                remove.append(mob)
                self.numUnfed+=1
          # remove any that should be removes
          for mob in remove:
            self.mobs.remove(mob)

          # remove food off the screen
          remove = []
          for each in self.food:
            each.update()
            if not each.inRange((0,self.width),(0,self.height)):
              remove+=[each]
          for each in remove:
            if each in self.food:
              self.food.remove(each)

          # remove animals that have been hit
          removeFood = []
          removeMob = []
          moneyGain = 0
          # go through all mobs
          for mob in self.mobs:
            # go through all food
            for food in self.food:
              if self.boxCollision((mob.pos,mob.w,mob.h),(food.pos,food.w,food.h)):
                # if there is a box collision remove all food and the mob that collide with it
                if mob not in removeMob:
                  moneyGain+=1
                  removeMob+=[mob]
                removeFood+=[food]
                if isinstance(food.source,TraineeZookeeper):
                  food.source.kills+=1

          # remove these after the fact
          for each in removeFood:
            if each in self.food:
              self.food.remove(each)
          for each in removeMob:
            if each in self.mobs:
              self.mobs.remove(each)




          # upgrade the trainee if needed
          upgraded = []
          for keeper in self.keepers:
            if isinstance(keeper,TraineeZookeeper) and keeper.kills >= Constants.TRAINEE_THRESHOLD:
              upgraded+=[keeper]
          for keeper in upgraded:
            # take them out and add a new speedy no cost
            self.keepers.remove(keeper)
            self.keepers+=[Zookeeper(keeper.pos,"SpeedyZookeeper",50,20,self.time)]

          # new food
          for keep in self.keepers:
            # for every keeper find its mob to aim at
            bestMob = None
            if not isinstance(keep,SplashZookeeper):
              r = keep.range
              bestD = 0
              if not isinstance(keep,CrazyZookeeper) or keep.awake:
                for mob in self.mobs:
                  # remember the mob that is hungriest in the path
                  dist = distance(keep.pos,mob.pos)
                  # if in range and there is a hungrier animal in the path
                  if r >= dist and bestD <= mob.d:
                    bestD = mob.d
                    bestMob = mob

            elif (self.time-keep.lastSplash)%Constants.SPLASH_LENGTH == 0:
              # if there hasnt been a spash since SPLASH_LENGTH ago then splash
              for vel in keep.vels:
                self.food+=[Food(keep.pos,vel,keep,.9)]



            if bestMob:
              # if there is a mob that exists find the loation to aim at
              currPos = bestMob.d
              bestTimeDiff = float("inf")
              aim = None
              for curr in range(currPos+1,self.maxD+1):
                # go through each displacement
                currCord = self.disp[curr]
                # time for keeper to hot spit
                time2shoot = distance(currCord,keep.pos)/keep.speed
                # time it would take animal to get to that spot
                animalTime = abs(curr - bestMob.d)/bestMob.speed

                diff = abs(time2shoot - animalTime)
                if bestTimeDiff > diff:
                  # remember the best ones
                  bestTimeDiff = diff
                  aim = currCord

              if aim:

                if not isinstance(keep,CrazyZookeeper):
                  # continue normally
                  self.food+=[Food(keep.pos,self.foodVel(keep.speed,keep.pos,aim),keep)]
                elif keep.awake:
                  # only if the keeper is awake then shoot and change to sleep
                  self.food+=[Food(keep.pos,self.foodVel(keep.speed,keep.pos,aim),keep)]
                  keep.awake = False
                  keep.texture = Constants.TEXTURES["SleepingZookeeper"]
                  keep.lastActive = self.time

          # update personal timer and if there is enough time elapsed then upgrade
          for keep in self.keepers:
            if isinstance(keep,CrazyZookeeper):
                keep.update(self.time)

          if(self.time % self.spawn_interval == 0):
              # spawn new mob at start
              self.mobs.append( Mob( self.path_corners[0] ,self.disp, self.animal_speed))



          if mouse:
            if type(mouse) == str:
              # if you chose a keep er remember it for next timestep
              self.choice = mouse
            elif self.choice == "Demon":

                if(self.noCollisions(mouse,Constants.DEMON_WIDTH,Constants.DEMON_HEIGHT)):
                  if(Constants.DEMON_PRICE <= self.money):
                    # only if there is a valid placement and money is good add it
                    self.money -= Constants.DEMON_PRICE
                    self.demons+=[Demon(mouse,2)]
                    self.choice = None

                  else:
                    raise NotEnoughMoneyError

            elif self.choice == "VHS":

                if(self.noCollisions(mouse,Constants.VHS_WIDTH,Constants.VHS_HEIGHT)):
                  if(Constants.VHS_PRICE <= self.money):
                    # only if there is a valid placement and money is good add it
                    self.money -= Constants.VHS_PRICE
                    self.vhss+=[VHS(mouse,.5)]
                    self.choice = None
                  else:
                    raise NotEnoughMoneyError




            elif(self.choice):

              info = Constants.KEEPER_INFO[self.choice]
              if(info["price"] <= self.money):
                # we have enough money
                if(self.noCollisions(mouse,Constants.KEEPER_WIDTH,Constants.KEEPER_HEIGHT)):
                  # the keeper can be placed at these coordinates
                  self.money -= info["price"]
                  # add a new keeper at this loc
                  if self.choice == "TraineeZookeeper":
                    # add new trainee object
                    self.keepers+=[TraineeZookeeper(mouse,self.choice,info["range"],info["throw_speed_mag"],self.time)]
                  elif self.choice == "CrazyZookeeper":
                    # add different object with
                    self.keepers+=[CrazyZookeeper(mouse,self.choice,info["range"],info["throw_speed_mag"],self.time)]
                  elif self.choice == "SplashZookeeper":
                    # my new addition requires new object
                    self.keepers+=[SplashZookeeper(mouse,self.choice,info["range"],info["throw_speed_mag"],self.time)]
                  else:
                    self.keepers+=[Zookeeper(mouse,self.choice,info["range"],info["throw_speed_mag"],self.time)]
                  self.choice = None
              else:
                raise NotEnoughMoneyError


          self.money+=moneyGain

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


    def noCollisions(self,mouse,w,h):

      # goes through all roks and paths and makes sure there
      # is no conflicts between them and the keepers
      x = mouse[0] - w/2
      y = mouse[1] - h/2
      box = [(x,y),w,h]

      for rock in self.rocks:
        if self.boxCollision([mouse,w,h],[rock.pos,rock.w,rock.h]):

          return False
      for each in self.pathBoxes:
        if self.boxCollision2(box,each):
          return False
      for demon in self.demons:
        if self.boxCollision([mouse,w,h],[demon.pos,demon.w,demon.h]):
          return False
      for vhs in self.vhss:
        if self.boxCollision([mouse,w,h],[vhs.pos,vhs.w,vhs.h]):
          return False
      for keeper in self.keepers:
        if self.boxCollision([mouse,w,h],[keeper.pos,keeper.w,keeper.h]):
          return False
      return True


    def boxCollision2(self,a,b):
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
    def boxCollision(self,a,b):
      # defines the top left and bottom right points of a box
      la = (a[0][0]-a[1]/2,a[0][1]-a[2]/2)
      ra = (a[0][0]+a[1]/2,a[0][1]+a[2]/2)
      lb = (b[0][0]-b[1]/2,b[0][1]-b[2]/2)
      rb = (b[0][0]+b[1]/2,b[0][1]+b[2]/2)
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
  # this is an object that will shoot at every time step food
  def __init__(self,pos,tipe,rang,speed,time):
    self.w = Constants.KEEPER_WIDTH
    self.h = Constants.KEEPER_HEIGHT
    self.pos = (pos[0],pos[1])
    self.texture = Constants.TEXTURES[tipe]
    self.type = tipe
    self.size = (self.w,self.h)
    self.range = rang
    self.speed = speed


class TraineeZookeeper(Zookeeper):
  # this is an object that needs to remember the number of animals its fed
  def __init__(self,pos,tipe,rang,speed,time):
    Zookeeper.__init__(self,pos,tipe,rang,speed,time)
    self.kills = 0
class SplashZookeeper(Zookeeper):
  # this is an object that needs to remember when it was placed and where to shoot
  def __init__(self,pos,tipe,rang,speed,time):
    Zookeeper.__init__(self,pos,tipe,rang,speed,time)
    self.lastSplash = time
    self.vels = self.foodVelocities()

  def foodVelocities(self):
    # creates a ring of food that goes out in the same velocity in a circle
    vels = []
    vels+=[[self.speed,0]]
    vels+=[[0,self.speed]]
    vels+=[[-self.speed,0]]
    vels+=[[0,-self.speed]]
    cosPiO4 = 1/(2**.5)
    unit = self.speed*cosPiO4
    vels+=[[unit,unit]]
    vels+=[[-unit,unit]]
    vels+=[[-unit,-unit]]
    vels+=[[unit,-unit]]
    return vels

class CrazyZookeeper(Zookeeper):
  # object that remembers last time it was awake and wether it is or not
  def __init__(self,pos,tipe,rang,speed,time):
    Zookeeper.__init__(self,pos,tipe,rang,speed,time)
    self.awake = True
    self.lastActive = time

  def update(self,time):
    if (time - self.lastActive) >= Constants.CRAZY_NAP_LENGTH:
        self.awake = True
        self.texture = Constants.TEXTURES["CrazyZookeeper"]


class Mob():
  # object that moves on path
  def __init__(self,pos,dispDic,speed):
    self.pos = list(pos)
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
  def __init__(self,pos,vel,source,acc = 1):
    self.pos = list(pos)
    self.vel = list(vel)
    self.w = Constants.FOOD_WIDTH
    self.h = Constants.FOOD_HEIGHT
    self.size = (self.w,self.h)
    self.texture = Constants.TEXTURES["food"]
    self.source = source
    self.acc = acc

  def update(self):
    # updates position givent he velocity

    # slows down food down to their terminal velocity of 5
    if abs(self.vel[0]) > 5:
      self.vel[0]*=self.acc
    if abs(self.vel[1]) > 5:
      self.vel[1]*=self.acc
    # changes x and y pos
    self.pos[0]+=self.vel[0]
    self.pos[1]+=self.vel[1]
  def inRange(self,x,y):
    # checks if the food is still on the screen
    if self.pos[0] >= x[0] and self.pos[0] <=x[1] and self.pos[1] >= y[0] and self.pos[1] <=y[1]:
      return True
    return False

class SpeedMultipliers:
  # changes the speed of an animal its close to
  def __init__(self,pos,mult):
    self.pos = list(pos)
    self.multiplier = mult

class Demon(SpeedMultipliers):
    # speeds up the animal
    def __init__(self,pos,mult):
        SpeedMultipliers.__init__(self,pos,mult)
        self.w = Constants.DEMON_WIDTH
        self.h = Constants.DEMON_HEIGHT
        self.texture = Constants.TEXTURES["Demon"]
        self.size = (self.w,self.h)
        self.r = Constants.DEMON_RADIUS

class VHS(SpeedMultipliers):
    # slows down the animal
    def __init__(self,pos,mult):
        SpeedMultipliers.__init__(self,pos,mult)
        self.w = Constants.VHS_WIDTH
        self.h = Constants.VHS_HEIGHT
        self.texture = Constants.TEXTURES["VHS"]
        self.size = (self.w,self.h)
        self.r = Constants.VHS_RADIUS

class Rock():
  # static rock object
  def __init__(self,pos):
    self.pos = list(pos)
    self.w = Constants.ROCK_WIDTH
    self.h = Constants.ROCK_HEIGHT
    self.texture = Constants.TEXTURES["rock"]
    self.size = (self.w,self.h)

if __name__ == '__main__':
    pass
