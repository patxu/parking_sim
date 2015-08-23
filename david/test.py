import simpy

BLOCK_LENGTH = 10

class Coord:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def equal(self,other):
		if(self.x == other.x and self.y == other.y):
			return True
		else:
			return False
	def increaseX(self,value):
		self.x += value
	def increaseY(self,value):
		self.y += value


class Car(object):
	def __init__(self,env,wantsToPark,carID,parkingSpots,coordinates):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.parkingSpots = parkingSpots
		self.coordinates = coordinates
	
	def run(self):
		while True:
			if (self.wantsToPark == True and self.parkingSpots[self.coordinates.x][self.coordinates.y] is not None):
				if(self.parkingSpots[self.coordinates.x][self.coordinates.y].available==True):
					print('Car %d Start parking at time %d at coord %d,%d' % (self.carID,self.env.now,self.coordinates.x,self.coordinates.y))
					self.parkingSpots[self.coordinates.x][self.coordinates.y].request()
					parking_duration = 5
					yield env.timeout(parking_duration)
					self.parkingSpots[self.coordinates.x][self.coordinates.y].release()
					self.wantsToPark = False

			print ('Car %d driving at time %d at coord %d, %d' % (self.carID,self.env.now,self.coordinates.x,self.coordinates.y))
			trip_duration = 1
			self.coordinates.increaseY(1)
			yield env.timeout(1)


class ParkingSpot(object):
	def __init__(self,env,coord,available):
		self.env = env
		self.coord = coord
		self.available = available
	
	def request(self):
		self.available = True

	def release(self):
		self.available = False

	def available(self):
		return self.available

env = simpy.Environment()

#create coordinate of car
carCoord = Coord(1,1)

#create coordinate,resource of parking space
coord = Coord(1,3)
parkingSpot = ParkingSpot(env,coord,True)

#add to list of parkin spaces
street = [[None for x in range(BLOCK_LENGTH)] for x in range(BLOCK_LENGTH)] 
street[parkingSpot.coord.x][parkingSpot.coord.y] = parkingSpot

car = Car(env,True,1,street,carCoord)


while env.now < 9:
	env.step()
