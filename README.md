# Parking Simulation  

## To Run:  
- Enter Virtual Environment: `source venv/bin/activate`
- Generate a Map: `python generate.py -m <map size> -l <block length> -w <block width> -o <percent open> -f <file to write to>`
- Run Simulation: `python run.py -h` for full options
- Exit venv: `deactivate`

## Cities:
- Multiple pre-created cities are included
	- Use `<city1,city2,city3>.xml` for debugging purposes
	- Use `grid100_<number>.xml` for running tests

## Color Chart
- Cars
  - Orange = want to park
  - Blue = done parking
- Parking Spots
  - Dark Green = always unavailable
  - Yellow = open
  - Red = occupied
