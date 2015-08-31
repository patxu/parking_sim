import argparse
import signal
import simpy
from roadmap import *
from simulation import *
from cs1lib import *
import time
import sys
import matplotlib.colors as colors

logname = "cities/test.log" #this will be changed everytime because output path is required
env = simpy.Environment()
carList = []
cityMap = RoadMap()
CANVAS_HEIGHT = 100
CANVAS_WIDTH = 100
ROAD_SECTION_WIDTH=20
ROAD_SECTION_HEIGHT=20
STEP_LENGTH = 0.05

# Color enum
def enum(**enums):
  """Declares enums for various colors.
  """
  return type('Enum',(),enums)

Color = enum(Red="#F44336", Pink="#E91E63", Yellow="#FFEB3B", Orange="#FF9800", DarkGreen="#388E3C", Green="#4CAF50", LightGreen="#8BC34A", Lime="#DCE775", Blue="#2196F3", Grey="#9E9E9E", White="#FFFFFF")
Theme= enum(Background=Color.Green, Closed_Spot=Color.DarkGreen, Open_Spot=Color.Yellow, Occupied_Spot=Color.Red, Car_Done=Color.Blue, Car_Parking=Color.Orange)

def signal_handler(signal,frame):
	fp=open(logname,"w")
	fp.write("Parking Log\n")
	total=0
	totalAverage = 0
	totalDistanceAverage = 0
	for car in carList:
		averageTime = (car.timeSpent / car.totalDestinations)
		averageDistance = (car.distanceFrom / car.totalDestinations)
		
		totalAverage += averageTime
		totalDistanceAverage += averageDistance
		
		total += car.timeSpent
		fp.write("Car: "+str(car.getCarID())+" Total Time Spent Searching: "+str(car.timeSpent)+ " Average Time Spent Searching: " + str(averageTime) + "For an average distance from destination of: " + str(averageDistance) + "\n")
	
	fp.write("Total Time Spent Looking for Parking by All Cars: "+str(total)+ " Average Time Spent Looking: " + str(totalAverage/len(carList)) + " Average Distance from destination: " + str(totalDistanceAverage/len(carList))+"\n")
	fp.close()
	sys.exit(0)	

def runGraphics():	
	color = colors.hex2color(Color.White)
	set_clear_color(color[0],color[1],color[2])
	clear()

	#Grass
	disable_stroke()
	color = colors.hex2color(Theme.Background)
	set_fill_color(color[0],color[1],color[2])
	draw_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)

	while not window_closed():
		numDriving = len([car for car in carList if car.parkingSpot == None])
		for i in range(numDriving):
			env.step() 
		if numDriving == 0:
			env.step()
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				drawRoadSection(roadSection)
		for car in carList:
			drawCar(car)
		request_redraw()
		sleep(STEP_LENGTH)

		if is_key_pressed("p"):
			while 1:
				if is_key_pressed("r"):
					break;
				sleep(0.1)

		update_progress(float(len([car for car in carList if len(car.destinations) == 0]))/float(len(carList)))
		if float(len([car for car in carList if len(car.destinations) == 0]))/float(len(carList)) > .97:
			sys.stdout.write("\n")
			print("Finished Simulation!")
			break

	fp=open(logname,"w")
	fp.write("Parking Log\n")
	total=0
	totalAverage = 0
	totalDistanceAverage = 0
	for car in carList:
		averageTime = (car.timeSpent / car.totalDestinations)
		averageDistance = (car.distanceFrom / car.totalDestinations)
		
		totalAverage += averageTime
		totalDistanceAverage += averageDistance
		
		total += car.timeSpent
		fp.write("Car: "+str(car.getCarID())+" Total Time Spent Searching: "+str(car.timeSpent)+ " Average Time Spent Searching: " + str(averageTime) + "For an average distance from destination of: " + str(averageDistance) + "\n")
	
	fp.write("Total Time Spent Looking for Parking by All Cars: "+str(total)+ " Average Time Spent Looking: " + str(totalAverage/len(carList)) + " Average Distance from destination: " + str(totalDistanceAverage/len(carList))+"\n")
	fp.close()
	sys.exit(0)

def drawRoadSection(roadSection):
	myCoordinates=roadSection.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	y_coor = y_coor*ROAD_SECTION_HEIGHT
	x_coor = x_coor*ROAD_SECTION_WIDTH

	if (roadSection.intersection==True):
		enable_stroke()
		set_stroke_width(2)
		color = colors.hex2color(Color.White)
		set_stroke_color(color[0],color[1],color[2])
		color = colors.hex2color(Color.Grey)
		set_fill_color(color[0],color[1],color[2])
		draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_WIDTH)
		disable_stroke()
	else:
		if (roadSection.direction==Direction.North):

			disable_stroke()
			color = colors.hex2color(Color.Grey)
			set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_HEIGHT)

			#dividing line
			enable_stroke()
			set_stroke_width(2)
			if(roadSection.crossable == True):
				color = colors.hex2color(Color.White)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			#left parking spot
			# enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingLeft.isParkingSpot == True):
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Theme.Closed_Spot)
				set_stroke_color(color[0],color[1],color[2])
			if (roadSection.parkingLeft.available==True):
				color = colors.hex2color(Theme.Open_Spot)
				set_fill_color(color[0],color[1],color[2])
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					color = colors.hex2color(Theme.Closed_Spot)
					set_fill_color(color[0],color[1],color[2])
				else:
					color = colors.hex2color(Theme.Occupied_Spot)
					set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			# enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Theme.Closed_Spot)
				set_stroke_color(color[0],color[1],color[2])
			if (roadSection.parkingRight.available==True):
				color = colors.hex2color(Theme.Open_Spot)
				set_fill_color(color[0],color[1],color[2])
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					color = colors.hex2color(Theme.Closed_Spot)
					set_fill_color(color[0],color[1],color[2])
				else:
					color = colors.hex2color(Theme.Occupied_Spot)
					set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor+((3*(ROAD_SECTION_WIDTH))/4),y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()


		if (roadSection.direction==Direction.East):

			disable_stroke()
			color = colors.hex2color(Color.Grey)
			set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH)
			enable_stroke()
			set_stroke_width(2)
			if(roadSection.crossable == True):
				color = colors.hex2color(Color.White)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			
			# enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingLeft.isParkingSpot == True):
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Theme.Closed_Spot)
				set_stroke_color(color[0],color[1],color[2])
			if (roadSection.parkingLeft.available==True):
				color = colors.hex2color(Theme.Open_Spot)
				set_fill_color(color[0],color[1],color[2])
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					color = colors.hex2color(Theme.Closed_Spot)
					set_fill_color(color[0],color[1],color[2])
				else:
					color = colors.hex2color(Theme.Occupied_Spot)
					set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
			# enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				color = colors.hex2color(Color.Yellow)
				set_stroke_color(color[0],color[1],color[2])
			else:
				color = colors.hex2color(Theme.Closed_Spot)
				set_fill_color(color[0],color[1],color[2])
			if (roadSection.parkingRight.available==True):
				color = colors.hex2color(Theme.Open_Spot)
				set_fill_color(color[0],color[1],color[2])
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					color = colors.hex2color(Theme.Closed_Spot)
					set_fill_color(color[0],color[1],color[2])
				else:
					color = colors.hex2color(Theme.Occupied_Spot)
					set_fill_color(color[0],color[1],color[2])
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

def drawCar(car):
	myCoordinates=car.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	y_coor = y_coor*ROAD_SECTION_HEIGHT
	x_coor = x_coor*ROAD_SECTION_WIDTH


	enable_stroke()
	set_stroke_width(2)
	if (car.wantsToPark):
		color = colors.hex2color(Theme.Car_Parking)
		set_fill_color(color[0],color[1],color[2])
		set_stroke_color(color[0],color[1],color[2])
	else:
		color = colors.hex2color(Theme.Car_Done)
		set_fill_color(color[0],color[1],color[2])
		set_stroke_color(color[0],color[1],color[2])
	if(car.direction == Direction.North):
		x_coor = x_coor+(ROAD_SECTION_WIDTH/2)+(ROAD_SECTION_WIDTH/5)
		y_coor = y_coor + (ROAD_SECTION_HEIGHT/2)
	elif(car.direction == Direction.South):
		x_coor = x_coor+(ROAD_SECTION_WIDTH/2)-(ROAD_SECTION_WIDTH/5)
		y_coor = y_coor + (ROAD_SECTION_HEIGHT/2)

	elif(car.direction == Direction.West):
		y_coor = y_coor+(ROAD_SECTION_HEIGHT/2)+(ROAD_SECTION_HEIGHT/5)
		x_coor = x_coor + (ROAD_SECTION_WIDTH/2)
	elif(car.direction == Direction.East):
		y_coor = y_coor+(ROAD_SECTION_HEIGHT/2)-(ROAD_SECTION_HEIGHT/5)
		x_coor = x_coor + (ROAD_SECTION_WIDTH/2)
	

	draw_circle(x_coor,y_coor,ROAD_SECTION_WIDTH/4)
	disable_stroke()	

def update_progress(progress):
	barLength = 50 # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Done...\r\n"
	block = int(round(barLength*progress))
	text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
	sys.stdout.write(text)
	sys.stdout.flush()

if __name__ == '__main__':
	signal.signal(signal.SIGINT, signal_handler) #make sure log is written too even with ctl+c
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-m','--map',help="Path to city map",required=True)
	parser.add_argument('-o','--output',help="Path to file output",required=True)
	parser.add_argument('-g','--graphics',help="Run with graphics",action="store_true")
	parser.add_argument('-t','--time_length',help="Time between steps",default=0)
	parser.add_argument('-l','--canvas_length',help="Canvas Length",default=900)
	parser.add_argument('-w','--canvas_width',help="Canvas Width",default=900)
	parser.add_argument('-z','--zoom',help="Zoom: Best results in range 20(zoomed out)-50(zoomed in)",default=20)
	parser.add_argument('-c','--cars',help="Number of cars",default=1)
	parser.add_argument('-s','--smart',help="Percentage of smart cars: 100 for all smart, 0 for all dumb",default=0,type=int, choices=xrange(0,101),metavar='')
	parser.add_argument('-d','--destinations',help="Number of destinations each car should have",default=1,type=int)
	
	args = vars(parser.parse_args())

	logname = args["output"]
	cityFile = args["map"]
	CANVAS_HEIGHT = int(args["canvas_length"])
	CANVAS_WIDTH = int(args["canvas_width"])
	ROAD_SECTION_WIDTH=int(args["zoom"])
	ROAD_SECTION_HEIGHT=int(args["zoom"])
	STEP_LENGTH=float(args["time_length"])

	cityMap = loadCity(cityFile)
	carList = []

	percentSmart = float(args["smart"])/100
	#create cars
	for i in range(int(args["cars"])):
		if (i < percentSmart * int(args["cars"])):
			car = Car(env,i,cityMap,"smart")
		else:
			car = Car(env,i,cityMap,"dumb")
		car.randomlyPlaceCarOnRoads()
		car.generateDestinations(int(args["destinations"]))
		carList.append(car)
	#only done for graphic purposes
	if(args["graphics"]):
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				if roadSection.parkingRight.available == False:
					roadSection.parkingRight.isParkingSpot = False
				if roadSection.parkingLeft.available == False:
					roadSection.parkingLeft.isParkingSpot = False
	
		start_graphics(runGraphics,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)
	
	else:
		print("STARTING RUN: cars: %d destinations: %d map: %s output: %s" %(int(args["cars"]), int(args["destinations"]), cityFile, logname))
		while True:
			numDriving = len([car for car in carList if car.parkingSpot == None])
			for i in range(numDriving):
				env.step() 
			if numDriving == 0:
				env.step()
			sleep(STEP_LENGTH)

			update_progress(float(len([car for car in carList if len(car.destinations) == 0]))/float(len(carList)))
			if float(len([car for car in carList if len(car.destinations) == 0]))/float(len(carList)) > .97:
				sys.stdout.write("\n")
				print("Finished Simulation!")
				break


		fp=open(logname,"w")
		fp.write("Parking Log\n")
		total=0
		totalAverage = 0
		totalDistanceAverage = 0
		for car in carList:
			averageTime = (car.timeSpent / car.totalDestinations)
			averageDistance = (car.distanceFrom / car.totalDestinations)
			
			totalAverage += averageTime
			totalDistanceAverage += averageDistance
			
			total += car.timeSpent
			fp.write("Car: "+str(car.getCarID())+" Total Time Spent Searching: "+str(car.timeSpent)+ " Average Time Spent Searching: " + str(averageTime) + "For an average distance from destination of: " + str(averageDistance) + "\n")
		
		fp.write("Total Time Spent Looking for Parking by All Cars: "+str(total)+ " Average Time Spent Looking: " + str(totalAverage/len(carList)) + " Average Distance from destination: " + str(totalDistanceAverage/len(carList))+"\n")
		fp.close()
		print ("Total Time Spent Looking for Parking by All Cars: "+str(total)+ " Average Time Spent Looking: " + str(totalAverage/len(carList)) + " Average Distance from destination: " + str(totalDistanceAverage/len(carList))+"\n")
		sys.exit(0)

