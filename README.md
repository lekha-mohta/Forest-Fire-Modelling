By default, the power plant is the only fire starting location and the parameters are set to:  
canWaterDrop = False
waterPosLowerBound = burningPowerPlant
waterPosUpperBound = burntPowerPlant
canWindAffect = False
windDirection = 'N'
numberGenerations = 200.



ADJUSTING FIRE START LOCATIONS  
To be able to adjust the starting point of a fire, you will need to enter the caconfig.py file and adjust the initial starting state for the incinerator and/or the power plant.

To do this for the incinerator, edit the number inside self.states[] on line 65 to be one of the following:  
	- 81 (meaning a fire does not start at the incinerator)
	- 82 (meaning a fire does start at the incinerator)

Similarly, for the power plant, you will need to edit the number inside self.states[] on line 68 to be one of the following:  
	- 69 (meaning a fire does not start at the power plant)
	- 70 (meaning a fire does start at the power plant)



ADJUSTING FOR WIND DIRECTION
For the model to be affected by a wind direction, the boolean canWindAffect on line 63 (fire2d.py) will need to be set to true, as when it is false no wind will affect the model.

If canWindAffect = True, a wind direction of N, E, S or W can be assigned to the variable windDirection on line 64. This will result in the fire being more likely to spread in its respective wind direction. 

For example, if windDirection = 'N' then the fire is more likely to spread in a northerly direction and less likely to spread in a southerly direction.



ADJUSTING FOR A WATER DROP
To be able to drop a pre-determined amount of water (an area of 12.5km squared), you will need to enter the fire2d.py and change the boolean canWaterDrop on line 58 (fire2d.py) to be true, as when it is false this function will not be actioned.

When canWaterDrop = True, the condition for when and where this will happen can be adjusted using waterPosLowerBound and waterPosUpperBound on lines 59 and 60. 

For example, if waterPosLowerBound = burningPowerPlant and waterPosUpperBound = burntPowerPlant then a water drop will occur at the location of the power plant when this begins to burn. If you want a water drop to occur after 3 generations of the power plant being burning, then waterPosLowerBound = burningPowerPlant + 2.

Additionally, to better control the location for the water drop, you can change the x and y values within water_drop(x, y) on line 103 (fire2d.py) accordingly.



GENERATING RESULTS AFFECTED BY WIND
To generate all of our results related to wind directions, you will need to do the following:
	- Ensure any variables that you do not need to change are set to their defaults as listed above.
	- For when the fire starts at either the incinerator or power plant, follow the directions in section ADJUSTING FIRE START LOCATIONS to start the fire at the correct location.
	- For all wind directions, follow the directions in section ADJUSTING FOR WIND DIRECTION to accurately set the wind direction
	- We recommend adjusting the variable numberGenerations on line 68 (fire2d.py) depending on the wind direction to ensure repeatability and for the fire spread to be witnessed reaching the town by using these values:
		- If windDirection = 'N', set numberGenerations = 550
		- If windDirection = 'E', set numberGenerations = 400
		- If windDirection = 'S', set numberGenerations = 250
		- If windDirection = 'W', set numberGenerations = 525



GENERATING RESULTS AFFECTED BY WATER BEING DROPPED
To generate all of our results related to water being dropped, you will need to do the following:
	- Ensure any variables that you do not need to change are set to their defaults as listed above.
	- For when the fire starts at either the incinerator or power plant, follow the directions in section ADJUSTING FIRE START LOCATIONS to start the fire at the correct location.
	- For when the water drops near the power plant, follow the directions in section ADJUSTING FOR A WATER DROP using these values:
		- waterPosLowerBound = burningPowerPlant + 2
		- waterPosUpperBound = burntPowerPlant
		- water_drop(x + 2, y + 2)
	- For when the water drops the near the incinerator, follow the directions in section ADJUSTING FOR A WATER DROP using these values:
		- waterPosLowerBound = burningIncinerator + 4
		- waterPosUpperBound = burntIncinerator
		- water_drop(x + 4, y - 2)
	- In both of these, the lower bound is increased to allow the fire to spread from the initial starting state.
