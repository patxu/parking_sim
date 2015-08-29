import argparse
import signal
import simpy
from roadmap import *
from simulation import *
from draw_city import *

logname = "foo.xml" #this will be changed everytime because output path is required

def signal_handler(signal,frame):
	fp=open(logname,"w")
	fp.write("Parking Log\n")
	totalDrivingTime=0;
	for car in carList:
		averageTime = (car.timeSpent / car.totalDestinations)
		totalAverage += averageTime
		total += car.timeSpent
		fp.write("Car: "+str(car.getCarID())+" Total Time Spent Searching: "+str(car.timeSpent)+ " Average Time Spent Searching: " + str(averageTime) + "\n")
	
	fp.write("Total Time Spent Looking for Parking by All Cars: "+str(total)+ " Average Time Spent Looking: " + str(total/len(carList)) + "\n")
	fp.close()
	sys.exit(0)	

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler) #make sure log is written too even with ctl+c
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-m','--map',help="Path to city map",required=True)
	parser.add_argument('-g','--graphics',help="Run with graphics",action="store_true")
	parser.add_argument('-o','--output',help="Path to fileoutput",required=True)
	parser.add_argument('-s','--step_length',help="Time between steps",default=.05)
	parser.add_argument('-l','--canvas_length',help="Canvas Length",default=800)
	parser.add_argument('-w','--canvas_width',help="Canvas Width",default=800)
	parser.add_argument('-z','--zoom',help="Zoom: Best results in range 20-50",default=20)
	parser.add_argument('-c','--cars',help="Number of cars",default=100)
	
	args = vars(parser.parse_args())

	logname = args["output"]
	cityFile = args["map"]

	env = simpy.Environment()

	cityMap = loadCity(cityFile)
	carList = []

	#create cars
	for i in range(args["cars"]):
		car = Car(env,i,cityMap,"random")
		car.randomlyPlaceCarOnRoads()
		car.generateDestinations(2)
		carList.append(car)
	
	#only done for graphic purposes
	if(args["graphics"]):
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				if roadSection.parkingRight.available == False:
					roadSection.parkingRight.isParkingSpot = False
				if roadSection.parkingLeft.available == False:
					roadSection.parkingLeft.isParkingSpot = False
	c = create_canvas("smart parking",CANVAS_WIDTH,CANVAS_HEIGHT,True)
	start_graphics(runGraphics,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)
	
	else:
		while True:
			numDriving = len([car for car in carList if car.parkingSpot == None])
			for i in range(numDriving):
				env.step() 
			if numDriving == 0:
				env.step()
			sleep(args["step_length"])


