# Name: Conway's game of life
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, CAConfig, randomise2d
import capyle.utils as utils
import numpy as np
import random
import math


# Constant variables used to indicate different terrain types and identify burning times
burnt = 0

canyonScrubland = 1
burningCanyonScrubland = 2
burntCanyonScrubland = 12

chaparral = 13
burningChaparral = 14
burntChaparral = 34

denseForest = 35
burningDenseForest = 36
burntDenseForest = 66

lake = 67
town = 68

powerPlant = 69
burningPowerPlant = 70
burntPowerPlant = 80

incinerator = 81
burningIncinerator = 82
burntIncinerator = 92

dampCanyonScrubland = 93
dampChaparral = 94
dampDenseForest = 95
dampPowerPlant = 96
dampIncinerator = 97

# Used to create an array for every state and state colour (if the highest possible state changes, this will also need changing)
highestState = dampIncinerator + 1

# Used to activate/deactivate whether a water drop happens within the model and the condition for this occuring (e.g. for when the power plant starts burning, lower bound = burningPowerPlant and upper bound = burntPowerPlant)
canWaterDrop = False
waterPosLowerBound = burningPowerPlant
waterPosUpperBound = burntPowerPlant

# Used to activate/deactivate whether a wind direction affects the fire spreading within the model and the direction that is being affected
canWindAffect = False
windDirection = 'N'

# Used to modify the basic configurement of the CA
STATES = np.arange(burnt, highestState, 1)
numberGenerations = 200
gridLength = 200

def transition_func(grid, neighbourstates, neighbourcounts):    
    # Used to check if water has been dropped, by default this is not turned on
    isWaterDropped = False
    
    # For every cell in the grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # If any cell is damp, then set isWaterDropped to true
            if (grid[i][j] == dampCanyonScrubland or grid[i][j] == dampChaparral or grid[i][j] == dampDenseForest or grid[i][j] == dampPowerPlant or grid[i][j] == dampIncinerator) and canWaterDrop:
                isWaterDropped = True
            # If the cell is in a burning state
            if grid[i][j] != burnt and grid[i][j] != canyonScrubland and grid[i][j] != chaparral and grid[i][j] != denseForest and grid[i][j] != lake and grid[i][j] != town and grid[i][j] != powerPlant and grid[i][j] != incinerator and grid[i][j] != dampCanyonScrubland and grid[i][j] != dampChaparral and grid[i][j] != dampDenseForest:
                # Add 1 to the cell state
                grid[i][j] += 1
                # If the cell state reaches it's predetermined burning time, it will be set to 'burnt'
                if grid[i][j] == burntCanyonScrubland or grid[i][j] == burntChaparral or grid[i][j] == burntDenseForest or grid[i][j] == burntPowerPlant or grid[i][j] == burntIncinerator:
                    grid[i][j] = 0
            
    # Need lists to update after the following for loop to ensure multiple steps don't occur at the same time
    listOfCellsToUpdateBurning = []
    listOfNewDampCells = []

    # For every cell in the grid
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            """
            To add a water drop feature, please edit the line with ### at the beginning
            To update the placement of this feature, please edit the x and y values accordingly in water_drop(x,y)
            """
            # If a fire has started at the incinerator and no water has been dropped yet
            if not isWaterDropped and (grid[x][y] > waterPosLowerBound and grid[x][y] < waterPosUpperBound) and canWaterDrop:
                # Get a list of cells that need to be updated with a damp state
                listOfNewDampCells = water_drop(x, y)
                # Ensure's water isn't dropped multiple times
                isWaterDropped = True
            else:
                # Get a list containing what state all neighbouring cells are in
                neighbouringBurningStates = burning_neighbour_states(grid, x, y)
                # If, by probability, the fire spreads then the cell location is noted
                # Can change the wind direction by changing the last parameter to one of N, E, S, W
                if spread_fire(grid[x][y], neighbouringBurningStates):
                    listOfCellsToUpdateBurning.append((x, y))       

    update_grid(grid, listOfCellsToUpdateBurning, listOfNewDampCells)

    return grid

def burning_neighbour_states(grid, cellXValue, cellYValue):
    """
    This function takes in a 2D array (grid), and the x and y values of a cell's position.

    Creates a list of numbers describing the state of the neighbouring cells, either -1.0, 0.0 or 1.0. 
    -1.0 = cell out of bounds or current cell position, 0.0 = cell not burning and 1.0 = cell is burning.

    These are added to the list in the following order (based of of a 3x3 representation):
        1 | 2 | 3;
        4 | 5 | 6;
        7 | 8 | 9.
    Where 5 is the cell's position based on the x and y values.

    returns listOfBurningStates (list)
    """
    
    # Get a list of the state's around the cell
    listOfBurningStates = []

    # For all neighbouring cells
    for y in range(cellYValue + 1, cellYValue - 2, -1):
        for x in range(cellXValue - 1, cellXValue + 2):
            # If the cell is not outside of the grid boundary and is not the current cell
            if not (x < 0 or x > gridLength - 1 or y < 0 or y > gridLength - 1) and not (cellXValue == x and cellYValue == y):
                # And if the cell is not burning, add '0.0' to the list 
                if grid[x][y] == canyonScrubland or grid[x][y] == chaparral or grid[x][y] == denseForest or grid[x][y] == lake or grid[x][y] == town or grid[x][y] == powerPlant or grid[x][y] == incinerator or grid[x][y] == burnt:
                    listOfBurningStates.append(0.0)
                # Or if the cell is damp, add '0.0' to the list
                elif grid[x][y] == dampCanyonScrubland or grid[x][y] == dampChaparral or grid[x][y] == dampDenseForest or grid[x][y] == dampPowerPlant or grid[x][y] == dampIncinerator:
                    listOfBurningStates.append(0.0)
                # Or if the cell is burning, add '1.0' to the list
                else:
                    listOfBurningStates.append(1.0)
            # Otherwise, if the cell is out of bounds or is the current cell, add '-1.0' to the list
            else:
                listOfBurningStates.append(-1.0)

    return listOfBurningStates

def water_drop(cellXValue, cellYValue):
    """
    This function takes in the location of the cell and identifies the neighbouring cells that will be used to create a circle.

    The dimensions of the circle is limited so that the equivalent of approximately 12.5km^2 is used.
    
    returns listOfCellsToUpdate (list)
    """
    listOfCellsToUpdate = []

    for y in range(4, -5, -1):
        for x in range(-4, 5):
            positiveX = math.sqrt(x * x)
            positiveY = math.sqrt(y * y)

            if not ((positiveX == 1 and positiveY > 3) or (positiveX == 2 and positiveY > 2) or (positiveX == 3 and positiveY > 1) or (positiveX == 4 and positiveY > 0)):
                if not (cellXValue + x < 0 or cellXValue + x > gridLength - 1 or cellYValue + y < 0 or cellYValue + y > gridLength - 1):
                    listOfCellsToUpdate.append((cellXValue + x, cellYValue + y))

    return listOfCellsToUpdate

def update_grid(grid, newBurningCells, newDampCells):
    """
    This function takes in a 2D array (grid), a list of cells that become burning and a list of cells that become damp.

    Using both lists, the cells will be assigned their new state value within the grid.

    returns grid (2D array)
    """
    # For all of the cells that begin burning, update their state by adding 1
    for cell in range(len(newBurningCells)):
        xValue = newBurningCells[cell][0]
        yValue = newBurningCells[cell][1]
        
        # If the cell is damp, assign it the corrosponding burning state of its terrain
        if grid[xValue][yValue] == dampCanyonScrubland:
            grid[xValue][yValue] = burningCanyonScrubland
        elif grid[xValue][yValue] == dampChaparral:
            grid[xValue][yValue] = burningChaparral
        elif grid[xValue][yValue] == dampDenseForest:
            grid[xValue][yValue] = burningDenseForest
        elif grid[xValue][yValue] == dampPowerPlant:
            grid[xValue][yValue] = burningPowerPlant
        elif grid[xValue][yValue] == dampIncinerator:
            grid[xValue][yValue] = burningIncinerator
        else:           
            # Otherwise, increase the state by 1
            grid[xValue][yValue] += 1

    # For all of the cells that become damp, assign it the corrosponding damp state of its terrain
    for cell in range(len(newDampCells)):
        xVal = newDampCells[cell][0]
        yVal = newDampCells[cell][1]
        if grid[xVal][yVal] >= canyonScrubland and grid[xVal][yVal] < burntCanyonScrubland:
            grid[xVal][yVal] = dampCanyonScrubland
        elif grid[xVal][yVal] >= chaparral and grid[xVal][yVal] < burntChaparral:
            grid[xVal][yVal] = dampChaparral
        elif grid[xVal][yVal] >= denseForest and grid[xVal][yVal] >= burntDenseForest:
            grid[xVal][yVal] = dampDenseForest
        elif grid[xVal][yVal] >= powerPlant and grid[xVal][yVal] < burntPowerPlant:
            grid[xVal][yVal] = dampPowerPlant
        elif grid[xVal][yVal] >= incinerator and grid[xVal][yVal] < burntIncinerator:
            grid[xVal][yVal] = dampIncinerator
    
    return grid

def spread_fire(currentState, neighbourStates):
    """
    This function determines if a cell begins to burn based off of random probability and wind direction factors and takes in the following:
    An integer: currentState = 67
    A character: windDirection = "N"
    A list: neighbourStates = [1.0, 0.0, 1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0] which follows this order:
        
        6 | 3 | 0;
        7 | 4 | 1;
        8 | 5 | 2        
    Where 4 is the cell's position based on the x and y values.

    returns spread (boolean)
    """

    # Used to either reduce or increase the chance of fire spreading based off of wind directions 
    lowFactor = 0.5
    highFactor = 1.5
    
    if canWindAffect:
        # Applies the wind factors to the list of neighbour states
        neighbourStatesFactors = apply_factors(neighbourStates, windDirection, lowFactor, highFactor)
    else:
        neighbourStatesFactors = neighbourStates
    
    neighbourStatesFiltered = []

    # For every state in neighbourStatesFactors
    for i in range(len(neighbourStatesFactors)):
        # Add float values that are greater than 0 to filter out cells that caused a negative state e.g. cells out of bound
        if neighbourStatesFactors[i] > 0:
            neighbourStatesFiltered.append(neighbourStatesFactors[i])

    burningThreshold = find_threshold(currentState)
    rand_no = generate_random_number()
    sumNeighbourStates = sum(neighbourStatesFiltered) * rand_no

    # If the factors of wind direction, random probability and burning neighbours is greater than the terrain threshold, then return true
    if sumNeighbourStates > burningThreshold:
        spread = True
    else:
        spread = False
        
    return spread

def generate_random_number():
    rand_no = random.uniform(0.5, 1.5)
    return rand_no
    
def find_threshold(currentState):
    """
    If statement of threshold resistances to fire spread for each non burning terrain type and takes in the following:
    An integer: currentState = 67

    If the current state of the cell doesn't align with one of these then it is either burning or burnt.
    These cells must have a high threshold so their burning time isn't updated twice in transition_func.

    returns threshold (integer)
    """

    if currentState == canyonScrubland:
        threshold = 1
    elif currentState == chaparral:
        threshold = 2
    elif currentState == denseForest:
        threshold = 2.8
    elif currentState == lake:
        threshold = 50
    elif currentState == town or currentState == powerPlant or currentState == incinerator:
        threshold = 1
    elif currentState == dampCanyonScrubland:
        threshold = 6
    elif currentState == dampChaparral:
        threshold = 7
    elif currentState == dampDenseForest:
        threshold = 7.5
    elif currentState == dampPowerPlant or currentState == dampIncinerator:
        threshold = 6
    else:
        threshold = 50
    return threshold
        
    
def apply_factors(neighbourStates, windDirection, lowFactor, highFactor):
    """
    This function applies wind direction factors to neighbouring cell states by multiplying the currect value with a factor.
    The factor used is dependant on which direction the wind is travelling from and takes in the following:
    A list: neighbourStates = [1, 1, 0, 1, -1, 0, 0, 0, 0]
    A character: windDirection = "N"
    Two floats: lowFactor = 0.5 and highFactor = 1.5

    returns neighbourStates (list)
    """
    if windDirection == "N":
        neighbourStates = apply_to_S_states(neighbourStates, highFactor)
        neighbourStates = apply_to_N_states(neighbourStates, lowFactor)   
    elif windDirection == "E":
        neighbourStates = apply_to_W_states(neighbourStates, highFactor)
        neighbourStates = apply_to_E_states(neighbourStates, lowFactor)
    elif windDirection == "S":
        neighbourStates = apply_to_N_states(neighbourStates, highFactor)
        neighbourStates = apply_to_S_states(neighbourStates, lowFactor)
    elif windDirection == "W":
        neighbourStates = apply_to_E_states(neighbourStates, highFactor)
        neighbourStates = apply_to_W_states(neighbourStates, lowFactor)
    return neighbourStates

def apply_to_N_states(neighbourStates, factor):
    neighbourStates[0] *= factor
    neighbourStates[3] *= factor
    neighbourStates[6] *= factor
    return neighbourStates

def apply_to_E_states(neighbourStates, factor):
    neighbourStates[0] *= factor
    neighbourStates[1] *= factor
    neighbourStates[2] *= factor
    return neighbourStates

def apply_to_S_states(neighbourStates, factor):
    neighbourStates[2] *= factor
    neighbourStates[5] *= factor
    neighbourStates[8] *= factor
    return neighbourStates

def apply_to_W_states(neighbourStates, factor):
    neighbourStates[6] *= factor
    neighbourStates[7] *= factor
    neighbourStates[8] *= factor
    return neighbourStates



def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16)/256 for i in (0, 2, 4))

def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Forest Fire"
    config.dimensions = 2
    config.states = STATES
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = np.zeros((highestState,3))
    config.state_colors[0] = hex_to_rgb('#460c00') # Burnt
    config.state_colors[1] = hex_to_rgb('#DDF507') # Canyon Scrubland
    config.state_colors[2:13] = hex_to_rgb('#f59407') # Burning Scrubland
    config.state_colors[13] = hex_to_rgb('#B5B407') # Chaparral
    config.state_colors[14:35] = hex_to_rgb('#b55b07') # Burning Chaparral
    config.state_colors[35] = hex_to_rgb('#4a8135') # Dense Forest
    config.state_colors[36:67] = hex_to_rgb('#d8772b') # Burning Forest
    config.state_colors[67] = hex_to_rgb('#1EADE3') # Lake
    config.state_colors[68] = hex_to_rgb('#000000') # Town
    config.state_colors[69] = hex_to_rgb('#5a00ff') # Power Plant
    config.state_colors[70:81] = hex_to_rgb('#ffe000') # Burning Power Plant
    config.state_colors[81] = hex_to_rgb('#0058ff') # Incinerator
    config.state_colors[82:93] = hex_to_rgb('#ff2900') # Burning Incinerator
    config.state_colors[93:98] = hex_to_rgb('#003aff') # Damp Terrain

    config.num_generations = numberGenerations
    config.grid_dims = (gridLength,gridLength)
    config.wrap = False

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config  

def main():
    # Open the config object
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, transition_func)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)


if __name__ == "__main__":
    main()