from cs1lib import *
from roadmap import *
from simulation import *
import simpy

CANVAS_WIDTH=1000
CANVAS_HEIGHT=1000
ROAD_SECTION_WIDTH=20
ROAD_SECTION_HEIGHT=20
STEP_LENGTH = .5

#cityMap = loadCity("cities/grid100_1.xml")


def runGraphics():
	print("in main")
	set_clear_color(1,1,1)
	clear()

	#Grass
	disable_stroke()
	set_fill_color(0,0.5,0) #Green
	draw_rectangle(0,0,CANVAS_WIDTH,CANVAS_HEIGHT)

	env = simpy.Environment()

	# roadMap = loadCity("cities/city1.xml")
	# roadMap = loadCity("cities/city3.xml")
	cityMap = loadCity("cities/grid100_3.xml")
	carList = []
	for i in range(100):
		car = Car(env,i,cityMap)
		car.randomlyPlaceCarOnRoads()
		carList.append(car)

	while not window_closed():
		numDriving = len([car for car in carList if car.parkingSpot == None])
		for i in range(numDriving):
			env.step()
		if numDriving == 0:
			print("Everything parked")
			env.step()
		for road in cityMap.roads:
			for roadSection in road.roadSections:
				#print "drawing road section"
				drawRoadSection(roadSection)
		for car in carList:
			drawCar(car)
		# drawRoads(cityMap)
		request_redraw()
		sleep(STEP_LENGTH)



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
			set_stroke_color(1,1,1) #white
			draw_line(x_coor+ROAD_SECTION_WIDTH/2,y_coor,x_coor+ROAD_SECTION_WIDTH/2,y_coor+ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_WIDTH/4,ROAD_SECTION_HEIGHT)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
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
			set_stroke_color(1,1,1) #white
			draw_line(x_coor,y_coor+ROAD_SECTION_WIDTH/2,x_coor+ROAD_SECTION_HEIGHT,y_coor+ROAD_SECTION_WIDTH/2)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(1)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingLeft.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor,ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
			disable_stroke()

			
			enable_stroke()
			set_stroke_width(2)
			set_stroke_color(1,1,0) #Yellow
			if (roadSection.parkingRight.available==True):
				set_fill_color(0,0.9,0)
			else:
				set_fill_color(0.9,0,0)
			draw_rectangle(x_coor,y_coor+((3*(ROAD_SECTION_WIDTH))/4),ROAD_SECTION_HEIGHT,ROAD_SECTION_WIDTH/4)
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
	set_fill_color(1,0,0.7) #Blue
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
	'''
	canvas = create_canvas("simulation",CANVAS_WIDTH,CANVAS_HEIGHT,True)
	def wrapped_user_fn():
		runGraphics()
        
        if window_closed():
            cs1_quit()

	
	canvas.start_thread(wrapped_user_fn)
	exit(app.exec_())
	
	for road in cityMap.roads:
		for roadSection in road.roadSections:
			#print "drawing road section"
			drawRoadSection(roadSection)
	for i in range(1):
		car = Car(env,i,cityMap)
		car.coordinates = Coord(0,5)
		car.direction = Direction.North
		drawCar(car)
		print car
		'''
		
	start_graphics(runGraphics,"SmartParking",CANVAS_WIDTH,CANVAS_HEIGHT, True)
	