# Fire Simulation Model

This repository contains a simulation model for fire spread and mitigation using various adjustable parameters.

---

## Default Settings
By default, the power plant is the only fire starting location, and the parameters are set as follows:
- `canWaterDrop`: `False`
- `waterPosLowerBound`: `burningPowerPlant`
- `waterPosUpperBound`: `burntPowerPlant`
- `canWindAffect`: `False`
- `windDirection`: `'N'`
- `numberGenerations`: `200`

---

## Adjusting Fire Start Locations
To adjust the starting point of a fire, modify the `caconfig.py` file:

### Incinerator
Edit the number inside `self.states[]` on line 65 to:
- `81`: Fire does **not** start at the incinerator.
- `82`: Fire **does** start at the incinerator.

### Power Plant
Edit the number inside `self.states[]` on line 68 to:
- `69`: Fire does **not** start at the power plant.
- `70`: Fire **does** start at the power plant.

---

## Adjusting for Wind Direction
For the model to be affected by wind:
1. Set `canWindAffect` (line 63 in `fire2d.py`) to `True`.
2. Assign a wind direction (`'N'`, `'E'`, `'S'`, `'W'`) to `windDirection` on line 64.

### Example:
If `windDirection = 'N'`, the fire will spread more likely in a northerly direction and less likely in a southerly direction.

---

## Adjusting for a Water Drop
To enable water drops:
1. Set `canWaterDrop` (line 58 in `fire2d.py`) to `True`.
2. Adjust `waterPosLowerBound` and `waterPosUpperBound` (lines 59 and 60) as needed.

### Example:
If:
- `waterPosLowerBound = burningPowerPlant`
- `waterPosUpperBound = burntPowerPlant`

Then a water drop will occur at the power plant when it starts burning.

To delay the water drop by 3 generations:
- `waterPosLowerBound = burningPowerPlant + 2`

### Location Adjustment:
Modify `water_drop(x, y)` (line 103 in `fire2d.py`) to specify the exact coordinates.

---

## Generating Results Affected by Wind
To generate results related to wind directions:
1. Ensure default variables are correctly set.
2. Adjust fire start locations as per [Adjusting Fire Start Locations](#adjusting-fire-start-locations).
3. Configure wind directions as per [Adjusting for Wind Direction](#adjusting-for-wind-direction).
4. Adjust `numberGenerations` (line 68 in `fire2d.py`) as follows:
   - `windDirection = 'N'`: `numberGenerations = 550`
   - `windDirection = 'E'`: `numberGenerations = 400`
   - `windDirection = 'S'`: `numberGenerations = 250`
   - `windDirection = 'W'`: `numberGenerations = 525`

---

## Generating Results Affected by Water Being Dropped
To generate results related to water drops:
1. Ensure default variables are correctly set.
2. Adjust fire start locations as per [Adjusting Fire Start Locations](#adjusting-fire-start-locations).
3. Configure water drop parameters as follows:

### For Water Near the Power Plant:
- `waterPosLowerBound = burningPowerPlant + 2`
- `waterPosUpperBound = burntPowerPlant`
- `water_drop(x + 2, y + 2)`

### For Water Near the Incinerator:
- `waterPosLowerBound = burningIncinerator + 4`
- `waterPosUpperBound = burntIncinerator`
- `water_drop(x + 4, y - 2)`

In both cases, the lower bound is increased to allow the fire to spread from its initial state.

---

## Notes
- Ensure all parameters are appropriately adjusted before running simulations to achieve desired results.
- Document any changes made to the configuration files for reproducibility.
