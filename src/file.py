import itertools
import random

import numpy as np

MAZE_SIZE = [6, 8]  # X, Y


class WallEncoding:
	"""
	Small class to keep a state of a wall. If the value is "W" then wall exists, 
	if the value is "S" the wall does not exist, and it is a viable path.
	"""
	
	def __init__(self, value):
		self.value = value
	
	def __bool__(self):
		return self._is_a_wall()
	
	def __str__(self):
		return self.value
	
	def __repr__(self):
		return self.value
	
	def __eq__(self, other):
		if isinstance(other, WallEncoding):
			return self.value == other.value
		return False
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def flip(self):
		return "W" if self.value == "S" else "S"
	
	def _is_a_wall(self):
		return self.value == "W"


class GenerateMaze:
	
	def __init__(self, *args):
		self.shape = list(args)
		self.starting_pos = None
		self.maze_grid = None
		self.walls_encoding = {}
		
		self.backtrack_path = []
		
		if args:
			self.starting_pos = [0] * len(args)
			self.generate_grid()
			self.generate_walls_encodings()
		
		return
	
	def generate_grid(self):
		"""
		Generate basic maze structure with given shape (X, Y) and fill it with 0.
		Which translates to a grid with every cell classed of.
		:return: None
		"""
		self.maze_grid = np.zeros(self.shape[::])
	
	def generate_walls_encodings(self):
		"""
		For simplicity to represent wall I give each cell a number representing on witch side it has walls.
		
		For example:
		
		0 - Walls everywhere
		
		1 - Walls on SEW no walls on N
		
		...
		
		
			Representation in code for storing where walls exist and where not would be a string with W or S:
		
		0 - WWWW
		
		1 - SWWW
		
		...
		
		:return: dictionary connecting a number with wall that exist or not
		:rtype: dict
		"""
		
		n_dimensions = len(self.shape)
		# Every dimension has M = N*2 walls
		n_walls = n_dimensions * 2
		
		elements = [WallEncoding("W"), WallEncoding("S")]
		length = n_walls
		
		# Generate all combinations
		combinations = itertools.product(elements, repeat=length)
		
		self.walls_encoding = list(combinations)
	
	@staticmethod
	def update_wall_encoding(tuple_data, index):
		"""
		To simplify this function will change the value of wall ending tuple on given index
		
		:param tuple_data: Tuple containing walls
		:type tuple_data: tuple[WallEncoding]
		:param index: index on which to change the value
		:type index: int
		:return: updated tuple_data
		:rtype: tuple[WallEncoding]
		"""
		if index < 0 or index >= len(tuple_data):
			print("Invalid index!")
			return tuple_data
		
		updated_list = list(tuple_data)
		updated_list[index] = WallEncoding(updated_list[index].flip())
		updated_tuple = tuple(updated_list)
		return updated_tuple
	
	@staticmethod
	def generate_possible_neighbours(pos):
		positions = []
		for dim in range(len(pos)):
			pos_plus = pos.copy()
			pos_plus[dim] += 1
			
			pos_minus = pos.copy()
			pos_minus[dim] -= 1
			
			positions.extend([pos_plus, pos_minus])
		
		return positions
	
	def _possible_routes(self, pos):
		"""
		In generating a maze using Depth-First Search (DFS) a route is considered possible
		if it leads to a cell which was not yet visited.
		:return: None
		"""
		# Define the indexes of neighboring cells
		indexes = self.generate_possible_neighbours(pos)
		
		encoding = []
		for possible_index in indexes:
			if all([0 <= v < self.shape[i] for i, v in enumerate(possible_index)]):
				if self.maze_grid.item(*possible_index) == 0:
					encoding.append(WallEncoding("S"))
				else:
					encoding.append(WallEncoding("W"))
			else:
				encoding.append(WallEncoding("W"))
		
		encoding = tuple(encoding)
		return encoding
	
	@staticmethod
	def pick_route_index(walls_encoding):
		open_routes_indexes = [i for i, wall in enumerate(walls_encoding) if not wall]
		
		return random.choice(open_routes_indexes)
	
	@staticmethod
	def new_position(curr_pos, route_index):
		possible_neighbours = GenerateMaze.generate_possible_neighbours(curr_pos)
		new_pos = possible_neighbours[route_index]
		
		return new_pos
	
	def _update_cell(self, cell_pos, route_index):
		curr_wall_int = int(self.maze_grid.item(*cell_pos))
		curr_wall_encoding = self.walls_encoding[curr_wall_int]
		
		new_wall_encoding = self.update_wall_encoding(curr_wall_encoding, route_index)
		new_wall_int = self.walls_encoding.index(new_wall_encoding)
		
		# Because np is stupid
		flattened_index = np.ravel_multi_index(tuple(cell_pos), self.maze_grid.shape)
		flattened_arr = self.maze_grid.flatten()
		flattened_arr[flattened_index] = new_wall_int
		self.maze_grid = flattened_arr.reshape(self.maze_grid.shape)
		
	def generate_maze(self):
		if self.starting_pos is None:
			self.starting_pos = [0] * len(self.shape)
		
		self.backtrack_path.append(self.starting_pos)
		
		while len(self.backtrack_path) > 0:
			curr_pos = self.backtrack_path[-1]
			
			possible_routes = self._possible_routes(curr_pos)
			if all([wall for wall in possible_routes]):
				self.backtrack_path.pop()
				continue
			
			picked_route_index = self.pick_route_index(possible_routes)
			self._update_cell(curr_pos, picked_route_index)
			
			new_pos = self.new_position(curr_pos, picked_route_index)
			reverse_picked_index = int(not bool(picked_route_index % 2)) + (picked_route_index // 2) * 2
			self._update_cell(new_pos, reverse_picked_index)
			
			self.backtrack_path.append(new_pos)
		
		pass


if __name__ == '__main__':
	maze = GenerateMaze(*MAZE_SIZE)
	maze.generate_maze()
	
	np.save("assets/maze.npy", maze.maze_grid)
