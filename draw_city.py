from __future__ import division
from cs1lib import *
from roadmap import *
from simulation import *
import simpy
import sys


CANVAS_WIDTH=2000
CANVAS_HEIGHT=1000
ROAD_SECTION_WIDTH=21
ROAD_SECTION_HEIGHT=21
STEP_LENGTH = 0.05
FILENAME = "cities/grid100_3.xml"
LOGNAME = "logs/ParkingLog.log"
toHoursFactor=1/3600 #convert seconds to hours
AvgMPH=30 #average mph of a car driving in a city
AvgMPG=20 #average mpg of a car driving in a city
AvgCarbonEmissions=18 #average CO2 emissions in lbs per gallon of gas

def runGraphics():
	set_clear_color(1,1,1)
	clear()

	#Grass
	disable_stroke()
	set_fill_color(0,0.5,0) #Green
	draw_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)

	env = simpy.Environment()

	cityMap = loadCity(FILENAME)
	carList = []
	for i in range(1000):
		car = Car(env,i,cityMap)
		car.randomlyPlaceCarOnRoads()
		Destination=car.generateRandomDestinations(1,100)
		ParkingBlock=car.getParkingSpotsDistance(Destination)
		print("----------------")
		print(Destination)
		print(ParkingBlock.__str__())
		print("----------------")
		car.generateRandomDestinations(2,100) #100 for map size, not good way to get map size progromatically
		carList.append(car)
	for road in cityMap.roads:
			for roadSection in road.roadSections:
				if roadSection.parkingRight.available == False:
					roadSection.parkingRight.isParkingSpot = False
				if roadSection.parkingLeft.available == False:
					roadSection.parkingLeft.isParkingSpot = False

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
		# drawRoads(cityMap)
		request_redraw()
		sleep(STEP_LENGTH)

		if is_key_pressed("p"):
			while 1:
				if is_key_pressed("r"):
					break;
				sleep(0.1)

	fp=open(LOGNAME,"w")
	fp.write("Parking Log\n")
	totalDrivingTime=0;
	for car in carList:
		totalDrivingTime=totalDrivingTime+car.getTime()
		fp.write("Car: "+str(car.getCarID())+" Time Spent Driving: "+str(car.getTime())+"\n")

	fp.write("Total Time Spent Looking for Parking by All Cars: "+str(totalDrivingTime)+" seconds\n")
	#Computation for Carbon Emissions
		#~18 lbs of CO2 emitted per gallon of gas
		#Drivers driving for x seconds
		#Driving ~30 miles per hour on city streets
		#Average car gets ~20 MPG
	CarbonEmissions=(totalDrivingTime*toHoursFactor*AvgMPH*(1/AvgMPG)*AvgCarbonEmissions)
	fp.write("Predicted Total Carbon Emissions: "+ str(CarbonEmissions)+" lbs\n")
	fp.close()



def drawRoadSection(roadSection):
	myCoordinates=roadSection.coordinates
	x_coor=myCoordinates.x
	y_coor=myCoordinates.y
	y_coor = y_coor*ROAD_SECTION_HEIGHT
	x_coor = x_coor*ROAD_SECTION_WIDTH
	if (roadSection.intersection==True):
		enable_stroke()
		set_stroke_width(2)
		set_stroke_color(1,1,0) #Yellow
		set_fill_color(0.5,0.5,0.5) #Gray
		draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_WIDTH)
		disable_stroke()
	else:
		if (roadSection.direction==Direction.North):
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH,ROAD_SECTION_HEIGHT)
			enable_stroke()
			set_stroke_width(2)
			if(roadSection.crossable == True):
				set_stroke_color(1,1,1) #white
			else:
				set_stroke_color(1,1,0) #white
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingLeft.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor+((3*(ROAD_SECTION_WIDTH))/4),y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()


		if (roadSection.direction==Direction.East):
			
			disable_stroke()
			set_fill_color(0.5,0.5,0.5)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH)
			enable_stroke()
			set_stroke_width(2)
			if(roadSection.crossable == True):
				set_stroke_color(1,1,1) #white
			else:
				set_stroke_color(1,1,0) #white
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(1)
			if (roadSection.parkingLeft.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingLeft.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			if (roadSection.parkingRight.isParkingSpot == True):
				set_stroke_color(1,1,0) #Yellow
			else:
				set_stroke_color(0,0.5,0) #Green
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				if (roadSection.parkingRight.isParkingSpot == False):
					set_fill_color(0,0.5,0) #Green
				else:
					set_fill_color(0.9,0,0)
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
	set_stroke_color(1,0,0.7) #Yellow
	if (car.wantsToPark):
		set_fill_color(1,0,0.7) #Blue
	else:
		set_fill_color(0,0,1)
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


if __name__ == '__main__':
	if(len(sys.argv) > 1):
		FILENAME = sys.argv[1]
	if(len(sys.argv) > 2):
		LOGNAME = sys.argv[2]
	start_graphics(runGraphics,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)

	