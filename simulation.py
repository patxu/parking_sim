import simpy
from roadmap import Coord,Direction,ParkingSpot,RoadSection,Road,RoadMap,loadCity

class Car(object):
	def __init__(self,env,wantsToPark,carID,cityMap,coordinates,currentStreetId):
		self.env = env
		self.action = env.process(self.run())
		self.wantsToPark = wantsToPark
		self.carID = carID
		self.parkingSpots = parkingSpots
		self.coordinates = coordinates
		self.currentStreetId
	
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

env = simpy.Environment()

#create coordinate of car
carCoord = Coord(1,1)

#car = Car(env,True,1,street,carCoord)
roadMap = loadCity("cities/city1.xml")

while env.now < 9:
	env.step()