# Parking Simulation  


## Getting Started:  
- Enter Virtual Environment: `source venv/bin/activate`
- Generate a Map: `python generate.py -m <map size> -l <block length> -w <block width> -o <percent open> -f <file to write to>`
- Run Simulation: `python run.py -h` for full options
- Exit venv: `deactivate`

- Quick Run: `python run.py -g -c 40 -t 0.1 -m cities/smallCity.xml -o temp.log`

## Cities:
- Multiple pre-created cities are included in `cities/`
	- Use `<city1,city2,city3,city4>.xml` for debugging purposes
	- Use `<percent>_<length>x<width>.xml` for running tests

## Color Chart
- Cars
  - Orange = wants to park
  - Blue = done parking
- Parking Spots
  - Dark Green = always unavailable
  - Yellow = open
  - Red = occupied
