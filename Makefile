
LENGTH = 10
WIDTH = 10

#CITIES
CITY_THREE = cities/grid_$(LENGTH)x$(WIDTH)_three.xml
CITY_FIVE = cities/grid_$(LENGTH)x$(WIDTH)_five.xml
CITY_TEN = cities/grid_$(LENGTH)x$(WIDTH)_ten.xml
CITY_TWENTY = cities/grip_$(LENGTH)x$(WIDTH)_twenty.xml

generate:
	python generate.py -s 100 -l 10 -w 10 -o 3 -f $(CITY_THREE)
	python generate.py -s 100 -l 10 -w 10 -o 3 -f $(CITY_FIVE)
	python generate.py -s 100 -l 10 -w 10 -o 3 -f $(CITY_TEN)
	python generate.py -s 100 -l 10 -w 10 -o 3 -f $(CITY_TWENTY)

run:
	# python run.py