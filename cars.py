import simpy

ROAD_LENGTH = 100
CARS = [3, 12, 25,27]
NUM_CARS = len(CARS)
STOPLIGHTS = [20, 32, 49, 90]
NUM_STOPLIGHTS = len(STOPLIGHTS)
CAR_SPEED = 1
LIGHT_DURATION = 10
RED = 0
GREEN = 1

env = simpy.Environment()

class Car(object):
	def __init__(self, env, id, start, stoplights):
		self.env = env
		self.id = id
		self.position = start
		self.stoplights = stoplights

	def drive(self):
		while self.position < ROAD_LENGTH:
			at_stoplight = -1
			for i in range(NUM_STOPLIGHTS):
				if self.position == self.stoplights[i].position:
					at_stoplight = i
			if at_stoplight > -1:
				yield self.env.process(stoplights[at_stoplight].wait_until_green())
			self.position += CAR_SPEED
			yield self.env.timeout(1)
		print("Car %d finished at time %d" % (self.id, self.env.now))

class Stoplight(object):
	def __init__(self, env, position, cars):
		self.env = env
		self.position = position
		self.cars = cars
		self.color = GREEN

	def switch_colors(self):
		cars_driving = True
		while cars_driving:
			yield self.env.timeout(LIGHT_DURATION)
			self.color = not self.color
			cars_driving = False
			for car in self.cars:
				if car.position < ROAD_LENGTH:
					cars_driving = True

	def wait_until_green(self):
		while self.color != GREEN:
			yield self.env.timeout(1)

cars = []
stoplights = []

for i in range(NUM_CARS):
	car = Car(env, i, CARS[i], stoplights)
	cars.append(car)
	env.process(car.drive())

for i in range(NUM_STOPLIGHTS):
	stoplight = Stoplight(env, STOPLIGHTS[i], cars)
	stoplights.append(stoplight)
	env.process(stoplight.switch_colors())

env.run()
