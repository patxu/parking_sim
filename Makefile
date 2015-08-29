
# City generation parameters
CITY_DIR = cities/
LENGTH = 10
WIDTH = 10

PERCENT3 = 3
PERCENT5 = 5
PERCENT10 = 10
PERCENT20 = 20

CITY_THREE = percent$(PERCENT3)_$(LENGTH)x$(WIDTH).xml
CITY_FIVE = percent$(PERCENT5)_$(LENGTH)x$(WIDTH).xml
CITY_TEN = percent$(PERCENT10)_$(LENGTH)x$(WIDTH).xml
CITY_TWENTY = percent$(PERCENT20)_$(LENGTH)x$(WIDTH).xml

# Test and Log parameters
# log output format: smartXX_carsXX_destXX_PERCENTAGE
LOG_DIR = logs/

CARS100 = 100
CARS500 = 500
CARS1000 = 1000
CARS2500 = 2500
DESTINATIONS = 2

SMART100 = 100
SMART80 = 80
SMART60 = 60
SMART40 = 40
SMART20 = 20
SMART0 = 0

LOG_THREE = cars$(CARS)_dest$(DESTIONATIONS)_three.log
LOG_FIVE = cars$(CARS)_dest$(DESTIONATIONS)_five.log
LOG_TEN = cars$(CARS)_dest$(DESTIONATIONS)_ten.log
LOG_TWENTY = cars$(CARS)_dest$(DESTIONATIONS)_twenty.log

generate:
	python generate.py -s 100 -l 10 -w 10 -o $(PERCENT3) -f $(CITY_DIR)$(CITY_THREE)
	python generate.py -s 100 -l 10 -w 10 -o $(PERCENT5) -f $(CITY_DIR)$(CITY_FIVE)
	python generate.py -s 100 -l 10 -w 10 -o $(PERCENT10) -f $(CITY_DIR)$(CITY_TEN)
	python generate.py -s 100 -l 10 -w 10 -o $(PERCENT20) -f $(CITY_DIR)$(CITY_TWENTY)

#we don't loop through the smart-dumb ratios in a single command in order to be able to run the tests in parallel
smart100:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART100) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART100) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART100) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART100) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

smart80:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART80) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART80) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART80) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART80) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

smart60:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART60) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART60) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART60) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART60) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

smart40:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART40) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART40) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART40) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART40) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

smart20:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART20) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART20) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART20) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART20) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

smart0:
	for number in 100 500 1000 2500; do \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART0) -m $(CITY_DIR)$(CITY_THREE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_THREE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART0) -m $(CITY_DIR)$(CITY_FIVE) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_FIVE); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART0) -m $(CITY_DIR)$(CITY_TEN) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TEN); \
		python run.py -t 0 -d $(DESTINATIONS) -c $$number -s $(SMART0) -m $(CITY_DIR)$(CITY_TWENTY) -o $(LOG_DIR)cars$$number_smart$(SMART100)_$(LOG_TWENTY); \
	done

sphinxhtml:
	cd sphinx/; make html; cd ..
	rm -rf *.pyc