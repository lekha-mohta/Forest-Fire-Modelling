import sys
import numpy as np
from capyle.utils import save, get_metadata, scale_array, gens_to_dims
from capyle.ca import Neighbourhood


class CAConfig(object):
    ROOT_PATH = sys.path[0]

    def __init__(self, filepath):
        self.filepath = filepath
        # parse the file for the best guess of the dimensions and name
        self.title, self.dimensions = get_metadata(filepath)
        self.states = None
        self.grid_dims = None
        self.rule_num = None
        self.state_colors = None
        self.num_generations = None
        self.nhood_arr = None
        self.initial_grid = None
        # default wrapping behaviour is True
        self.wrap = True
        self.default_paths()

    def fill_in_defaults(self):
        """ if any of the fields are not filled in in description
        they are filled in with defaults here """
        # rule number
        self.rule_num = 0 if self.rule_num is None else self.rule_num
        # number of generations
        if self.num_generations is None:
            self.num_generations = 100

        # grid dimensions
        if self.grid_dims is None:
            if self.dimensions == 2:
                self.grid_dims = (200, 200)
            else:
                self.grid_dims = gens_to_dims(self.num_generations)

        # initial grid
        if self.initial_grid is None:
            fillstate = self.states[13] if self.states is not None else 0
            self.initial_grid = np.zeros(self.grid_dims, dtype=type(fillstate))
            self.initial_grid.fill(fillstate)
            
            ###### setting initial grid
            
            ###town
            self.initial_grid[135:145, 95 :105] = self.states[68]
            
            ###dense forest
            self.initial_grid[30 :40 , 0  :40 ] = self.states[35]
            self.initial_grid[30 :160, 40 :80 ] = self.states[35]
            self.initial_grid[60 :80 , 120:170] = self.states[35]

            ###canyon
            self.initial_grid[90 :100, 100:170] = self.states[1]
        
            ###lake
            self.initial_grid[160:170, 60 :120] = self.states[67]
            self.initial_grid[110:160, 170:180] = self.states[67]

            ###incinerator
            self.initial_grid[0:2, 197:200] = self.states[81]

            ###power plant
            self.initial_grid[60:62, 18:20] = self.states[70]

        # neighbourhood array
        if self.nhood_arr is None:
            if self.dimensions == 2:
                self.nhood_arr = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
            else:
                self.nhood_arr = np.array([1, 1, 1])

    def default_paths(self):
        self.path = self.ROOT_PATH + '/temp/config.pkl'
        self.timeline_path = self.ROOT_PATH + '/temp/timeline.pkl'

    def neighbourhood(self):
        if self.nhood_arr is None:
            self.nhood_arr = [0, 1, 0]
        return Neighbourhood(self.nhood_arr, dims=self.dimensions)

    def save(self):
        save(self, self.path)

    def set_grid_dims(self, dims=None, num_generations=None):
        if dims is not None:
            i = dims[0] if dims[0] > 2 else 3
            j = dims[1] if dims[1] > 2 else 3
            self.grid_dims = i, j
        else:
            if num_generations < 1:
                num_generations = 1
            self.num_generations = num_generations
            self.grid_dims = gens_to_dims(self.num_generations)
        if self.initial_grid is not None:
            self.initial_grid = scale_array(self.initial_grid, *self.grid_dims)
        else:
            self.intitial_grid = np.zeros(self.grid_dims)

    def set_initial_grid(self, grid):
        if grid.shape[0] == 1:
            self.initial_grid[0] = np.copy(grid[0])
        else:
            self.initial_grid = np.copy(grid)
