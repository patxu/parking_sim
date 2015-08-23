import simpy
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity

class Car(object):
	def __init__(self,env,wantsToPark,carID,cityMap,coordinates,currentStreetId,direction):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.cityMap = cityMap
		self.coordinates = coordinates
		self.currentStreetId = currentStreetId
		self.direction = direction
	
	def move(self,direction):
		if(self.direction == Direction.North):
			self.coordinates.increaseY(1)
		elif(self.direction == Direction.East):
			self.coordinates.increaseX(1)
		elif(self.direction == Direction.South):
			self.coordinates.decreaseY(1)
		elif(self.direction == Direction.West):
			self.coordinates.decreaseX(1)
		else:
			print("invalid direction")

	def getNextMove(self):
		return True

	def run(self):
		while self.getNextMove() is not None:
			print ('Car %d driving at time %d at coord %d, %d' % (self.carID,self.env.now,self.coordinates.x,self.coordinates.y))
			trip_duration = 1
			self.move(self.direction)
			yield self.env.timeout(trip_duration)
			

env = simpy.Environment()

#create coordinate of car
carCoord = Coord(0,0)
carCoord2 = Coord(2,0)
roadMap = loadCity("cities/city1.xml")
print roadMap.graph

car = Car(env,True,1,roadMap,carCoord,1,Direction.North)

env.run(until=15)
