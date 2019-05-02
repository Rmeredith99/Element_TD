import numpy as np 
import pygame
from towers import *
from math import ceil, floor
from scipy.spatial.distance import cdist
from queue import PriorityQueue as MinHeap
from random import uniform
pygame.font.init()










# a_1 = Air_Tower(0,0, level=1)
# a_2 = Air_Tower(0,0, level=2)
# a_3 = Air_Tower(0,0, level=3)

# w_1 = Water_Tower(0,0, level=1)
# w_2 = Water_Tower(0,0, level=2)
# w_3 = Water_Tower(0,0, level=3)

# e_1 = Earth_Tower(0,0, level=1)
# e_2 = Earth_Tower(0,0, level=2)
# e_3 = Earth_Tower(0,0, level=3)

# f_1 = Fire_Tower(0,0, level=1)
# f_2 = Fire_Tower(0,0, level=2)
# f_3 = Fire_Tower(0,0, level=3)

# m_1 = Magic_Tower(0,0, level=1)
# m_2 = Magic_Tower(0,0, level=2)
# m_3 = Magic_Tower(0,0, level=3)

# s_1 = Spirit_Tower(0,0, level=1)
# s_2 = Spirit_Tower(0,0, level=2)
# s_3 = Spirit_Tower(0,0, level=3)

# t = [a_1, a_2, a_3, w_1, w_2, w_3, e_1, e_2, e_3, f_1, f_2, f_3, m_1, m_2, m_3, s_1, s_2, s_3]
# for i in range(len(t)):
# 	if i%3==0:
# 		print("new_tower")
# 	print(t[i].get_cost())











########################################


# Initializing enemy graphics
enemy_width = 65

# First enemy
enemy1 = pygame.image.load("game_art/enemy1.png")
enemy1 = pygame.transform.scale(enemy1, (enemy_width, enemy_width))

enemy1_1 = pygame.transform.rotate(enemy1, 270)
enemy1_2 = pygame.transform.rotate(enemy1, 0)
enemy1_3 = pygame.transform.rotate(enemy1, 90)
enemy1_4 = pygame.transform.rotate(enemy1, 180)

# Second enemy
enemy2 = pygame.image.load("game_art/enemy2.png")
enemy2 = pygame.transform.scale(enemy2, (enemy_width, enemy_width))

enemy2_1 = pygame.transform.rotate(enemy2, 270)
enemy2_2 = pygame.transform.rotate(enemy2, 0)
enemy2_3 = pygame.transform.rotate(enemy2, 90)
enemy2_4 = pygame.transform.rotate(enemy2, 180)

# Third enemy
enemy3 = pygame.image.load("game_art/enemy3.png")
enemy3 = pygame.transform.scale(enemy3, (enemy_width, enemy_width))

enemy3_1 = pygame.transform.rotate(enemy3, 270)
enemy3_2 = pygame.transform.rotate(enemy3, 0)
enemy3_3 = pygame.transform.rotate(enemy3, 90)
enemy3_4 = pygame.transform.rotate(enemy3, 180)

# Fourth enemy
enemy4 = pygame.image.load("game_art/enemy4.png")
enemy4 = pygame.transform.scale(enemy4, (enemy_width, enemy_width))

enemy4_1 = pygame.transform.rotate(enemy4, 270)
enemy4_2 = pygame.transform.rotate(enemy4, 0)
enemy4_3 = pygame.transform.rotate(enemy4, 90)
enemy4_4 = pygame.transform.rotate(enemy4, 180)


# Classes and function for graph traversal
#########################################################
class Node:
	def __init__(self, index, neighbors, x=0, y=0):
		"""
		index: int representing the node
		neighbors: list of tuples (neighbor index, length of path)
		"""
		self.index = index
		self.neighbors = neighbors
		self.x = x
		self.y = y

class Graph:
	def __init__(self, node_list):
		"""
		nodes: hashmap from node index to node object
		"""
		self.nodes = node_list

def a_star_search(graph, start, end):
	"""
	[a_star_search] takes a graph and determines the shortest path from
		[start] to [end].
	"""
	# Maps node index to shortest path distance
	path_weight = {start:0}
	# Maps node index to previous node according to current shortest path
	previous = {start:None}
	# Min Heap of unsettled nodes (frontier nodes) sorted by shortest distance
	remaining = MinHeap()
	remaining.put((0,start))
	# Set of all nodes which have a determined shortest distance
	settled = set()

	# Used to find distance for A* search
	final_node = graph.nodes[end]
	finished = False

	while (not remaining.empty()):
		val, current_index = remaining.get()
		current_node = graph.nodes[current_index]
		if current_index == end:
			finished = True
			break
		if current_index not in settled:
			settled.add(current_index)

			for neighbor, weight in current_node.neighbors:
				# actual neighbor node object
				neighbor_node = graph.nodes[neighbor]
				# distance from neighbor node to right side of screen
				a_star_dist = abs(neighbor_node.x - final_node.x) + abs(neighbor_node.y - final_node.y)
				randomizer = uniform(0.0, 0.001)
				new_weight = path_weight[current_index] + weight + a_star_dist + randomizer
				if (neighbor not in path_weight) or (new_weight < path_weight[neighbor]):
					path_weight[neighbor] = new_weight
					remaining.put((new_weight, neighbor))
					previous[neighbor] = current_index

	# there is no path to the end
	if not finished:
		return None
	else:
		path = [end]
		prev_node = previous[end]
		while prev_node != None:
			path.append(prev_node)
			prev_node = previous[prev_node]

		path.reverse()
		# cutting out the imaginary start and end nodes
		return path


def map_to_graph(map_array, no_go_value=2):
	"""
	[map_to_graph] takes in a map array with locations that can't be visited,
		as marked by [no_go_value] and returns a graph corresponding to the map.
	"""
	# array dimensions
	h = len(map_array)
	w = len(map_array[0])

	# Indexes by essentially flattening array (f: Z^2 -> Z)
	def coords_to_index(i, j):
		return w*j + i

	# all viable neighbors in the four cardinal directions
	def neighbors(i, j):
		neighbors = []
		for new_j in range(max(0, j - 1), min(h - 1, j + 1) + 1):
			for new_i in range(max(0, i - 1), min(w - 1, i + 1) + 1):
				if (abs(new_j - j) + abs(new_i - i) == 1) and (map_array[new_j][new_i] != no_go_value):
					neighbors.append(coords_to_index(new_i, new_j))
		return neighbors

	# conversion of map to graph, stored in graph_dict
	graph_dict = {}
	for i in range(w):
		for j in range(h):
			if map_array[j][i] != no_go_value:
				index = coords_to_index(i, j)
				connections = list(map((lambda n : (n, 1)), neighbors(i, j)))
				# # adding auxilary nodes as start and end points
				# if i == 0:
				# 	connections.append((-1, 0))
				# elif i == w - 1:
				# 	connections.append((w*h, 0))
				node = Node(index, connections, x=i, y=j)
				graph_dict[index] = node

	# adding start and end nodes to graph
	# connect only nodes that don't have towers
	# start_connections = []
	# for j in range(h):
	# 	if map_array[j][0] != no_go_value:
	# 		start_connections.append((w*j, 1))

	# end_connections = []
	# for j in range(h):
	# 	if map_array[j][w-1] != no_go_value:
	# 		end_connections.append((w*j + w - 1, 1))

	# graph_dict[-1] = Node(-1, start_connections)
	# graph_dict[h*w] = Node(h*w, end_connections)

	return Graph(graph_dict)

def get_path(map_array):
	"""
	[get_path] takes in a map and returns a list of coordinates
		of the new path. If no path can be found, returns None.
	"""
	graph = map_to_graph(map_array)
	start = 0
	end = (len(map_array)) * (len(map_array[0])) - 1
	return a_star_search(graph, start, end)

#########################################################


class Notification:
	def __init__(self, text, duration = 2.3):
		"""
		This class handles all in-game notifications. Notifications are
			displayed on the screen for a given amount of time.
		"""
		self.duration = duration
		self.text = text
		self.time = 0.0
		self.active = True

	def draw(self, screen):
		text_length = 9.75 * len(self.text)
		
		w = text_length + 40
		h = 80

		x = 1050 - 10 - w
		y = 700 - 10 - h
		
		pygame.draw.rect(screen, (200, 200, 200), [x, y, w, h])
		pygame.draw.rect(screen, (0, 200, 200), [x + 10, y + 10, w - 20, h - 20])
		write_text(screen, self.text, x + w // 2 - int(text_length / 2.0), y + h // 2 - 15, (0,0,0), 20)
	
	def update(self, time_delta):
		self.time += time_delta
		if self.time > self.duration:
			self.active = False



class Animation:
	def __init__(self, start_x, start_y, end_x, end_y, draw_function_sequence, animation_time = 0.3):
		"""
		This class handles animations, particularly attack animations.
			[draw_function_sequence] is the main argument. It is a list
				of functions that take in (x,y) coords as arguments and
				draw a given image with those coordinates as the center.
				This functions as sprite animations and each tower will
				have their own unique animation sequence.
		"""

		self.start_x = start_x 
		self.start_y = start_y
		self.end_x = end_x
		self.end_y = end_y
		
		self.current_x = start_x
		self.current_y = start_y
		self.duration = 0.0

		self.speed = 1000
		norm_factor = 1.0 / ((end_x - start_x)**2 + (end_y - start_y)**2)**0.5
		self.direction = ((end_x - start_x) * norm_factor, (end_y - start_y) * norm_factor)

		self.last_distance = float("inf")

		self.is_done = False

		# self.index is a float so it can account for partial progress in the sequence
		self.index = 0
		self.num_animations_start = len(draw_function_sequence[0])
		self.num_animations_end = len(draw_function_sequence[1])
		self.animation_time = draw_function_sequence[2]
		self.total_time = draw_function_sequence[3]

		self.frame_rate_start = self.num_animations_start / float(animation_time)
		self.frame_rate_end = self.num_animations_end / float(animation_time)

		self.draw_function_sequence_start = draw_function_sequence[0]
		self.draw_function_sequence_end = draw_function_sequence[1]

		self.end_animation = False
		self.end_distance = 100

	def update(self, time_delta):
		"""
		[update] progresses an animation by a given amount of time and 
			redraws the current frame.
		"""
		if not self.end_animation:
			self.index = (self.index + self.frame_rate_start * time_delta) % self.num_animations_start
		else:
			self.index = (self.index + self.frame_rate_end * time_delta) % self.num_animations_end
		self.current_x += self.direction[0] * self.speed * time_delta
		self.current_y += self.direction[1] * self.speed * time_delta

		# Updating run-time
		self.duration += time_delta

		distance = ((self.current_x - self.end_x)**2 + (self.current_y - self.end_y)**2)**0.5

		# If the animation has reached its target and it's a "bullet" type animation
		# meaning it's not based on time, but rather distance
		if distance > self.last_distance and self.total_time == None:
			if self.num_animations_end == 0:
				self.is_done = True
			else:
				self.duration = 0
				self.total_time = self.animation_time
				self.end_animation = True
				self.index = 0
		# If the animation is based on time and time is up
		elif self.total_time != None and self.duration > self.total_time:
			self.is_done = True 

		self.last_distance = distance

		# If it's time for the end animation, reset self.index
		# if self.last_distance < self.end_distance and self.num_animations_end > 0:
		#     self.end_animation = True
		#     # Slows the speed down so the explosion animation can take place
		#     self.speed = 200
		#     self.index = 0

	def draw(self, screen):
		"""
		[draw] is the method that actually draws the current animation
			frame on the provided screen.
		"""
		if not self.end_animation:#self.last_distance > self.end_distance or len(self.draw_function_sequence_end) == 0:
			self.draw_function_sequence_start[int(self.index)](screen, self.current_x, self.current_y)
			
		else:
			self.draw_function_sequence_end[int(self.index)](screen, self.current_x, self.current_y)



class Enemy:
	def __init__(self, path, hp, speed, reward, type=1):
		self.original_hp = hp
		self.hp = hp
		self.x = 100
		self.y = 200
		self.direction = (1, 0)
		self.speed = speed
		self.color = (255, 0, 0)
		self.path = path
		self.target_index = 0
		self.out_of_bounds = False
		self.half_width = 25
		self.reward = reward
		# So towers can hit the first enemy
		self.dist_traveled = 0
		self.last_distance = float('inf')

		# Effects from attacks
		self.effect_start = None
		self.effect_middle = None
		self.effect_end = None
		self.effect_duration = 0

		# Animation type
		self.type = type
		self.enemy_name = ["Tank", "Fighter Jet", "Missile", "Helicopter"][self.type - 1]

		# Immunity
		immunities = ["AIR", "WATER", "EARTH", "FIRE"]
		self.immunity = immunities[self.type - 1]


	def draw(self, screen):
		"""
		[draw] draws the enemy on the provided screen
		"""
		if self.type == 1:
			# Tank
			if self.direction[0] > 0.5:
				screen.blit(enemy1_1, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] < -0.5:
				screen.blit(enemy1_2, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[0] < -0.5:
				screen.blit(enemy1_3, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] > 0.5:
				screen.blit(enemy1_4, (self.x - enemy_width // 2, self.y - enemy_width // 2))
		elif self.type == 2:
			# Fighter jet
			if self.direction[0] > 0.5:
				screen.blit(enemy2_1, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] < -0.5:
				screen.blit(enemy2_2, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[0] < -0.5:
				screen.blit(enemy2_3, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] > 0.5:
				screen.blit(enemy2_4, (self.x - enemy_width // 2, self.y - enemy_width // 2))
		elif self.type == 4:
			# Helicopter
			if self.direction[0] > 0.5:
				screen.blit(enemy3_1, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] < -0.5:
				screen.blit(enemy3_2, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[0] < -0.5:
				screen.blit(enemy3_3, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] > 0.5:
				screen.blit(enemy3_4, (self.x - enemy_width // 2, self.y - enemy_width // 2))
		elif self.type == 3:
			# Missile vehicle
			if self.direction[0] > 0.5:
				screen.blit(enemy4_1, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] < -0.5:
				screen.blit(enemy4_2, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[0] < -0.5:
				screen.blit(enemy4_3, (self.x - enemy_width // 2, self.y - enemy_width // 2))
			elif self.direction[1] > 0.5:
				screen.blit(enemy4_4, (self.x - enemy_width // 2, self.y - enemy_width // 2))

	def draw_health_bar(self, screen):
		"""
		[draw_health_bar] takes care of drawing the health bar so that
			the health bar can always be visible (above the enemies).
		"""
		hp_frac = max(0.0, self.hp / float(self.original_hp))
		bar_width = 40
		bar_height = 5
		green = [0, 255, 0]
		red = [255, 0, 0]
		pygame.draw.rect(screen, green, 
		[int(self.x) - bar_width // 2, int(self.y) - self.half_width - bar_height * 2, int(ceil(hp_frac * bar_width)), bar_height])
		if hp_frac < 1.0:
			pygame.draw.rect(screen, red, 
			[int(self.x) - bar_width // 2 + (int(hp_frac * bar_width)), int(self.y) - self.half_width - bar_height * 2, 
			bar_width - int(floor(hp_frac * bar_width)), bar_height])

	def draw_info(self, screen, top_left_corner):
		"""
		[draw_info] draws enemy info in the sidebar
		"""
		corner_x, corner_y = top_left_corner

		h = 20
		spacing = 30
		w = 10
		size = 15
		
		write_text(screen, str(self.enemy_name), corner_x + w, corner_y + h, (0,0,0), size + 5)
		write_text(screen, "Hitpoints: " + str(int(self.hp)), corner_x + w, corner_y + h+spacing, (0,0,0), size)
		write_text(screen, "Speed: " + str(int(self.speed)), corner_x + w, corner_y + h+2*spacing, (0,0,0), size)
		write_text(screen, "Immunity: " + str(self.immunity), corner_x + w, corner_y + h+3*spacing, (0,0,0), size)
		write_text(screen, "Reward: " + str(int(self.reward)), corner_x + w, corner_y + h+4*spacing, (0,0,0), size)


	def update(self, time_delta):
		"""
		[update] advances the enemy forward and changes attributes
			as necessary. Depends on how much time has passed. This
			is given by [time_delta].
		"""
		v_x, v_y = self.direction[0] * self.speed, self.direction[1] * self.speed
		self.x += v_x * time_delta
		self.y += v_y * time_delta
		target_x, target_y = self.path[self.target_index]

		self.dist_traveled += ((v_x * time_delta)**2 + (v_y * time_delta)**2)**0.5

		distance = ((self.x - target_x)**2 + (self.y - target_y)**2)**0.5

		if distance > self.last_distance:
			self.target_index += 1
			new_target_x, new_target_y = self.path[self.target_index]
			d_x = new_target_x - self.x
			d_y = new_target_y - self.y
			norm_factor = (d_x**2 + d_y**2)**0.5
			self.direction = (d_x / float(norm_factor), d_y / float(norm_factor))
			self.last_distance = float('inf')
		else:
			self.last_distance = distance

		# Effects
		if self.effect_middle != None:
			if self.effect_duration <= 0:
				# End effect
				self.effect_end(self)
				# Reset the effect data
				self.effect_duration = 0
				self.effect_start = None
				self.effect_middle = None
				self.effect_end = None
			else: # Effect is still lasting
				# Effect takes place
				self.effect_duration -= time_delta
				self.effect_middle(self, time_delta)

	def predict_coords(self, time_delta):
		"""
		[predict_coords] is used to estimate the location of the enemy
			for when the attack actually arrives. Purely for aesthetic reasons.
		"""
		pass

	def set_effect(self, effect):
		"""
		[set_effect] initializes an effect from an attack
		"""
		# Ends previous effect
		if self.effect_end != None:
			self.effect_end(self)
		# Initializes new effect
		start, middle, end, duration = effect
		start(self)
		self.effect_start = start
		self.effect_middle = middle
		self.effect_end = end
		self.effect_duration = duration

class Round:
	def __init__(self, path, round_number, difficulty):
		self.path = path
		self.round_number = round_number
		self.difficulty = difficulty # 1, 2, 3 for easy, medium, hard
		self.enemies = self.get_enemies()
		self.release_delay = self.get_release_delay()

	def get_enemies(self):
		"""
		[get_enemies] returns a list of Enemy objects which constitutes
			a wave.
		"""
		constant = 0.1
		a = .02 * self.difficulty
		hp = ceil((a * self.round_number ** 3 + 0.09 * self.round_number**2 + 1*self.round_number + 12) / constant)
		# hp = ceil((0.25 * self.round_number**2 + 10*self.round_number + 4.666) / constant)
		speed = 100 + self.round_number * 1.5 * (self.difficulty)
		reward = int(self.round_number**0.9)
		num_enemies = 10 + self.round_number - 1
		enemies = []
		for i in range(num_enemies):
			animation_type = (self.round_number - 1) % 4 + 1
			enemy = Enemy(self.path, hp, speed, reward, type=animation_type)
			# First four rounds have no immunity
			if self.round_number <= 4:
				enemy.immunity = None
			enemies.append(enemy)

		return enemies

	def get_release_delay(self):
		"""
		[get_release_delay] is the amount of time in between releasing
			one enemy and the next one. Should decrease as difficulty 
			increases.
		""" 
		return 1 / float(self.difficulty * self.round_number / 4.0)**0.25


class State:
	def __init__(self):
		# create your own path boolean
		self.own_path = False

		self.lives = 10
		self.gold = 100
		self.end_of_round_bonus = 50
		self.score = 0
		self.map_width, self.map_height = 1050, 700
		self.map = None
		self.set_map(1)
		self.spawn_point = (-100, 35)
		length = int(self.map_height / len(self.map))
		for i in range(len(self.map)):
			if self.map[i][0] == 1:
				self.spawn_point = (-100, i * length + length // 2)
				break
		self.points = None
		self.towers = []
		self.enemies = []
		self.tower_selected = None
		self.enemy_selected = None
		self.tower_colors = [(217, 229, 247),(9, 85, 198),(19, 160, 45),(196, 14, 1),(114, 5, 173),(120, 120, 120)]
		self.tower_types = [Air_Tower, Water_Tower, Earth_Tower, Fire_Tower, Magic_Tower, Spirit_Tower]

		# Pertaining to rounds
		self.difficulty = 1
		self.round_number = 1
		self.round = None #Rounds are created later
		self.end_of_round = True
		self.time_since_last_spawn = float('inf')
		self.spawned_this_round = 0

		self.attack_animations = []

		self.add_tower_buttons = [False, False, False, False, False, False]
		self.add_tower_button = False

		self.paused = False

		# Keeping track of all notifications
		self.notification = None


	def set_map(self, difficulty):
		"""
		[get_map] returns an array that denotes the map. Each index
			will either have a 1 (path) or 0 (building land).
		"""
		if not self.own_path:
			if difficulty == 3:
				arr = [
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,1,1,1,1,1,1,0,0],
					[0,0,0,0,0,0,0,1,0,0,0,0,1,1,1],
					[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
					[0,0,1,1,1,1,1,1,0,0,0,0,0,0,0],
					[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
				]
			elif difficulty == 2:
				arr = [
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
					[0,1,0,0,1,0,0,0,0,0,0,1,1,1,1],
					[1,1,0,0,1,0,0,0,0,0,0,1,0,0,0],
					[0,0,0,0,1,0,0,0,1,1,1,1,0,0,0],
					[0,0,0,0,1,0,0,0,1,0,0,0,0,0,0],
					[0,0,0,0,1,1,1,1,1,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				]
			else:
				arr = [
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,1,1,1,1,1,1,1,0,0,0,0],
					[1,1,0,0,1,0,0,0,0,0,1,0,0,0,0],
					[0,1,0,0,1,0,0,0,0,0,1,0,0,0,0],
					[0,1,0,0,1,1,1,0,0,0,1,0,0,0,0],
					[0,1,0,0,0,0,1,0,0,0,1,1,1,0,0],
					[0,1,0,0,0,0,1,0,0,0,0,0,1,0,0],
					[0,1,1,1,1,1,1,0,0,0,0,0,1,1,1],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
					[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
				]
			self.map = arr
			self.set_points()
		else:
			self.map = [[0 for i in range(15)] for j in range(10)]


	def set_points(self):
		"""
		[get_points] returns a list of checkpoints that the
			enemies will use to determine where to go in order
			to follow the path.
		"""
		x = 0
		y = 0
		for i in range(len(self.map)):
			if self.map[i][0] == 1:
				y = i
				break
		points = [(x,y)]

		map_h = len(self.map) - 1
		map_w = len(self.map[0]) - 1

		def neighbors(x, y, r=1):
			neighbors = []
			for y_loc in range(max(0,y-r), min(map_h,y+r) + 1):
				for x_loc in range(max(0,x-r), min(map_w,x+r) + 1):
					if abs(y_loc - y) + abs(x_loc - x) == 1:
						neighbors.append((x_loc, y_loc))
			return neighbors

		visited = set([(x,y)])

		while x < len(self.map[0]) - 1:
			n = neighbors(x,y)
			for new_x, new_y in n:
				if self.map[new_y][new_x] == 1 and (new_x, new_y) not in visited:
					x, y = new_x, new_y
					points.append((x, y))
					visited.add((x, y))
					break

		points.append((x + 3, y))

		length = int(self.map_height / len(self.map))
		pixel_points = list(map(lambda v : (v[0] * length + length // 2, v[1] * length + length // 2), points))

		self.points = pixel_points

		# Setting the spawn point
		for i in range(len(self.map)):
			if self.map[i][0] == 1:
				self.spawn_point = (-100, i * length + length // 2)
				break


	def draw(self, screen):
		"""
		[draw] draws all towers and enemies currently on the map.
		"""
		if self.tower_selected != None:
			self.tower_selected.draw_circle(screen)
			# If you're in the middle of placing a tower
			if self.add_tower_button:
				self.tower_selected.draw(screen)
		for t in self.towers:
			t.draw(screen)
		for e in self.enemies:
			e.draw(screen)
		for e in self.enemies:
			e.draw_health_bar(screen)
		for a in self.attack_animations:
			a.draw(screen)
		if self.notification != None:
			self.notification.draw(screen)

	def draw_sidebar(self, screen, top_left_corner):
		"""
		[draw_sidebar] draws the information outside of the 
			actual game area.
		"""
		corner_x, corner_y = top_left_corner
		width = corner_x // 6

		# Details
		h = 5
		write_text(screen, "         : " + str(self.lives), corner_x + 40, corner_y + h, (0,0,0), 20)
		write_text(screen, "         : " + str(self.gold) + " ", corner_x + 40, corner_y + h+27, (0,0,0), 20)
		write_text(screen, "Score: " + str(self.score) + " ", corner_x + 40, corner_y + h+54, (0,0,0), 20)
		write_text(screen, "Round: " + str(self.round_number), corner_x + 40, corner_y + h+81, (0,0,0), 20)

		# Pause button
		w = 20
		h = 125
		if self.paused:
			pygame.draw.rect(screen, (50,50,50), [corner_x + w, corner_y + h, width - 2*w, 70])
		else:    
			pygame.draw.rect(screen, (150,150,150), [corner_x + w, corner_y + h, width - 2*w, 70])
		pygame.draw.rect(screen, (200,0,0), [corner_x + w+5, corner_y + h+5, width - 2*(w+5), 60])
		if self.end_of_round:
			write_text(screen, "Next Round", corner_x + 32, corner_y + h+20, (255,255,255), 20)
		else:  
			write_text(screen, "Pause/Play", corner_x + 40, corner_y + h+20, (255,255,255), 20)

		# Partition line
		pygame.draw.rect(screen, (0,0,0), [corner_x + 10, corner_y + 206, width - 20, 3])

		# Add Tower Buttons
		for i in range(6):
			w = 20
			h = 220 + i*80
			color = self.tower_colors[i]
			if i == 0:
				font_color = (0,0,0)
			elif i == 5:
				font_color = (209, 205, 0)
			else:
				font_color = (255,255,255)
			if self.add_tower_buttons[i]:
				pygame.draw.rect(screen, (50,50,50), [corner_x + w, corner_y + h, width - 2*w, 70])
			else:
				pygame.draw.rect(screen, (150,150,150), [corner_x + w, corner_y + h, width - 2*w, 70])
			pygame.draw.rect(screen, color, [corner_x + w+5, corner_y + h+5, width - 2*(w+5), 60])
			if self.add_tower_buttons[i]:
				write_text(screen, "Cancel", corner_x + 57, corner_y + h+20, font_color, 20)
			else:
				write_text(screen, "Add Tower", corner_x + 35, corner_y + h+20, font_color, 20)

	def draw_sidebar_2(self, screen, top_left_corner):
		"""
		[draw_sidebar_2] fills the second side bar with tower information, etc.
		"""
		# Selected Tower info
		if self.tower_selected != None:
			purchased = not self.add_tower_button
			tower = self.tower_selected
			tower.draw_info(screen, top_left_corner, purchased=purchased)
		
		# Selected enemy info
		elif self.enemy_selected != None:
			enemy = self.enemy_selected
			enemy.draw_info(screen, top_left_corner)

	def update(self, time_delta):
		"""
		[update] advances all enemies on the map by updating
			their positions. Once an enemy leaves the map, it is
			removed from the map and a life is subtracted.
		"""
		# Updating Towers
		for t in self.towers:
			t.update(time_delta)

		# Updating Animations
		done_indices = set()
		for i, a in enumerate(self.attack_animations):
			a.update(time_delta)
			if a.is_done:
				done_indices.add(i)
		
		# Deleting animations that have finished
		new_animation_list = []
		for i, animation in enumerate(self.attack_animations):
			if i not in done_indices:
				new_animation_list.append(animation)
		self.attack_animations = new_animation_list

		# Determines if an enemy has finished the course
		def out_of_bounds(enemy):
			if enemy.x - enemy.half_width > self.map_width:
				return True
			return False

		# Updating Enemies
		out_indices = set()
		for i, e in enumerate(self.enemies):
			e.update(time_delta)
			if out_of_bounds(e):
				out_indices.add(i)
				self.lives -= 1
			if e.hp <= 0:
				out_indices.add(i)
				self.gold += e.reward
				self.score += e.reward

		# Deleting selected enemy if it has run out of hp
		if (self.enemy_selected != None) and (self.enemy_selected.hp <= 0):
			self.enemy_selected = None

		# Delete finished enemies in reverse order to not mess up ordering
		new_enemies_list = []
		for i, enemy in enumerate(self.enemies):
			if i not in out_indices:
				new_enemies_list.append(enemy)
		self.enemies = new_enemies_list

		# If game is not paused, run attacks
		if not self.paused:
			self.initiate_attacks()

		# Determining if a round is done
		# Only needs to be calculated when end_of_round is false
		if len(self.enemies) == 0 and (self.round != None) and (len(self.round.enemies) == self.spawned_this_round) and (not self.end_of_round):
			self.end_of_round = True
			self.gold += self.end_of_round_bonus
			self.end_round()

		# If round isn't done and there are still enemies to spawn
		elif (self.round != None) and (len(self.round.enemies) > self.spawned_this_round):
			self.spawn_next()

		# Updating time since last spawn
		self.time_since_last_spawn += time_delta

		# Updating location of soon-to-be placed tower
		if (self.tower_selected != None) and (self.add_tower_button):
			x, y = pygame.mouse.get_pos()
			self.tower_selected.x = x
			self.tower_selected.y = y

		# Updating notification
		if self.notification != None:
			self.notification.update(time_delta)
			if not self.notification.active:
				self.notification = None

	def end_round(self):
		"""
		[end_round] makes adjustments to the map after the round is over
			in order to get it ready for next round.
		"""
		# Resets the path if it's a create your own path game
		if self.own_path:
			for j in range(len(self.map)):
				for i in range(len(self.map[0])):
					# Re-setting path squares
					if self.map[j][i] == 1:
						self.map[j][i] = 0

		# Announcing the enemy immunity for next round
		next_round_number = self.round_number + 1
		if next_round_number > 4:
			immunity = ["Air", "Water", "Earth", "Fire"]
			note = Notification("Next level's immunity: " + immunity[next_round_number % 4 - 1], duration=3.5)
			self.notification = note


	def spawn_next(self):
		"""
		[spawn_next] creates a new enemy at the spawning point (the
			start of the path). The enemy is the next in line according
			to the current round.
		"""
		# If it's been long enough to spawn another
		if (self.time_since_last_spawn >= self.round.release_delay):
			x, y = self.spawn_point
			enemy = self.round.enemies[self.spawned_this_round]
			enemy.x = x
			enemy.y = y
			self.enemies.append(enemy)
			self.spawned_this_round += 1
			self.time_since_last_spawn = 0

	def add_tower(self, x, y):
		"""
		[add_tower] creates a tower at the proper location for 
			when a click occurs at (x, y).
		"""
		box_size = self.map_height // len(self.map)
		i, j = x // box_size, y // box_size

		# If it's a create-you-own-path game, we need to make sure the 
		# tower doesn't block the enemy path
		if (self.own_path) and (self.end_of_round) and (not self.verify_placement(i, j)):
			self.tower_selected = None
			self.add_tower_button = False
			self.add_tower_buttons = [False] * 6
			note = Notification("You can't block the enemies' path")
			self.notification = note
			return None
		
		elif self.map[j][i] == 0:
			x, y = i * box_size + box_size // 2, j * box_size + box_size // 2 
			# Changed so tower follows cursor
			tower = self.tower_selected
			tower.x = x
			tower.y = y
			self.tower_selected
			if tower.cost > self.gold:
				note = Notification("You can't afford that tower")
				self.notification = note
				self.add_tower_button = False
				self.add_tower_buttons = [False] * 6
				return None
			self.towers.append(tower)
			self.map[j][i] = 2
			self.gold -= tower.cost
		else:
			note = Notification("You can't place a tower there")
			self.notification = note

		self.add_tower_button = False
		self.add_tower_buttons = [False] * 6

	def select_tower(self, x, y):
		"""
		[select_tower] is called when a square in the tower area is
			clicked but the add-tower button is not selected.
			This adds the selected tower to self.tower_selected.
		"""
		box_size = self.map_height // len(self.map)
		i, j = x // box_size, y // box_size
		if self.map[j][i] == 2:
			x, y = i * box_size + box_size // 2, j * box_size + box_size // 2 
			tower = None
			for t in self.towers:
				if t.x == x and t.y == y:
					tower = t
					break
			# If it's a click on the currently selected tower
			if self.tower_selected == tower:
				self.tower_selected = None
			else:
				self.tower_selected = tower
			# Un-selecting an enemy when a tower is selected
			self.enemy_selected = None

		else:
			self.tower_selected = None
			self.enemy_selected = None

	def select_enemy(self, x, y):
		"""
		[select_enemy] is called when a click on a square in the path.
		"""
		# If this particular click selected an enemy
		selected = False
		for enemy in self.enemies:
			dist = ((x - enemy.x)**2 + (y - enemy.y)**2)**0.5
			if dist < 25:
				if enemy != self.enemy_selected:
					self.enemy_selected = enemy
					selected = True
				else: # if it's the same enemy as already selected
					self.enemy_selected = None
				# Un-selecting an enemy when a tower is selected
				self.tower_selected = None
				
		if not selected:
			self.tower_selected = None
			self.enemy_selected = None

	def initiate_attacks(self):
		"""
		[initiate_attacks] finds all towers that can attack and
			attacks the furthest along enemy
		"""
		tower_list = list(filter(lambda x : x.can_attack(), self.towers))
		if len(tower_list) == 0 or len(self.enemies) == 0:
			# No tower can/enemy to attack, so it's not worth doing the rest of the calculations
			return None
		tower_coords = list(map(lambda v : (v.x, v.y), tower_list))
		enemy_coords = list(map(lambda v : (v.x, v.y), self.enemies))
		distances = cdist(tower_coords, enemy_coords)
		
		for i in range(len(tower_list)):
			tower = tower_list[i]
			# Allows towers to target any number of enemies
			for j in range(len(distances[i])):
				# If enemy is immune, range is set to 'inf' so it can't be attacked
				if self.enemies[j].immunity == tower.type:
					distances[i][j] = float('inf')
			attack_indices = tower.get_attack_indices(distances[i], self.enemies)

			for index in attack_indices:   
				enemy = self.enemies[index]
				enemy.hp = max(enemy.hp - tower.damage, 0)
				tower.attack()
				effect = tower.get_effect()
				if effect[3] != 0:
					enemy.set_effect(effect)
				kwargs = [tower.x, tower.y, enemy.x, enemy.y]
				animation = Animation(tower.x, tower.y, enemy.x, enemy.y, tower.get_animation_sequence(kwargs=kwargs))
				self.attack_animations.append(animation)

	def start_next_round(self):
		"""
		[start_next_round] begins the next wave of enemies and creates
			new map based on the current tower configuration.
		"""
		# If there's no defined path, set the new path
		if self.own_path:
			# Creating a new map
			path = get_path(self.map)
			for index in path:
				i = index % len(self.map[0])
				j = index // len(self.map[0])
				self.map[j][i] = 1
			self.set_points()
		
		# Initiating the round
		if self.round_number > 1 or self.round != None:
			self.round_number += 1
		self.round = Round(self.points, self.round_number, self.difficulty)
		self.end_of_round = False
		self.spawned_this_round = 0

	def verify_placement(self, i, j):
		"""
		[verify_placement] returns a bool that says whether or not a
			tower placement is valid, meaning it doesn't prevent enemies
			from traversing the graph.
		"""
		if (i == 0 and j == 0) or (i == len(self.map[0]) - 1 and j == len(self.map) - 1):
			return False

		# temporarily adding a tower to the map
		temp_value = self.map[j][i]
		self.map[j][i] = 2

		#calculating shortest path if there is any
		path = get_path(self.map)

		# removing temporary tower
		self.map[j][i] = temp_value

		# returns true if path exists
		return path != None


	def click(self, x, y):
		"""
		[click] is called when there's a click on the screen.
			This checks the click against all buttons.
		"""
		# "Add Tower" Button
		for i in range(6):
			w = 20
			h = 220 + i*80
			if (x > self.map_width + w) and (x < self.map_width * 7/6. -2*w) and (y > h) and (y < h+70):
				if not self.add_tower_button:
					self.add_tower_button = True
					self.add_tower_buttons[i] = True
					tower = self.tower_types[i](x, y)
					self.tower_selected = tower
				# Cancelling a tower once selected
				else:
					self.add_tower_button = False
					self.add_tower_buttons = [False] * 6
					self.tower_selected = None

				# So the other location checks don't take place
				# Necessary since the 'for' loop doesn't allow for use of elif later
				return None

		# Pause/Start round button
		w = 20
		h = 125
		if (x > self.map_width + w) and (x < self.map_width * 7/6. -2*w) and (y > h) and (y < h+70):
			# If there is no current wave
			if self.end_of_round:
				self.start_next_round()
			else:
				self.paused = not self.paused

		# Adding a tower when the add tower button is pressed
		elif (x < self.map_width) and self.add_tower_button:
			self.add_tower(x, y)
			self.tower_selected = None

		# Selecting a tower/enemy
		elif (x < self.map_width):
			box_size = self.map_height // len(self.map)
			i, j = x // box_size, y // box_size
			# not on the path
			if self.map[j][i] != 1:
				self.select_tower(x, y)
			else: # on the path
				self.select_enemy(x, y)

		# Upgrading a tower
		elif (x > self.map_width * 7/6. + 20) and (x < self.map_width * 8/6. -2*20) and (y > 380 + 206) and (y < 380+70 + 206):
			# If a tower can be upgraded
			# If the tower has been purchased, it's not at max level
			if (self.tower_selected != None) and (not self.add_tower_button) and (self.tower_selected.level < self.tower_selected.max_level): 
				# If there's enough money
				if self.gold >= self.tower_selected.upgrade_cost[self.tower_selected.level - 1]:
					self.gold -= self.tower_selected.upgrade_cost[self.tower_selected.level - 1]
					self.tower_selected.upgrade()
				else:
					note = Notification("You don't have enough money to upgrade that tower")
					self.notification = note

		# Selling a tower
		elif (x > self.map_width * 7/6. + 20) and (x < self.map_width * 8/6. -2*20) and (y > 300 + 206) and (y < 300+70+206):
			if (self.tower_selected != None):
				# Finding the tower selected
				tower_index = -1
				for i, tower in enumerate(self.towers):
					if self.tower_selected == tower:
						tower_index = i
						break

				# Adding back the money
				self.gold = int(self.gold + self.tower_selected.sell_back_rate * self.tower_selected.sunk_cost())

				# Deleting the tower
				del(self.towers[tower_index])

				# Resetting map placements
				box_size = self.map_height // len(self.map)
				i, j = self.tower_selected.x // box_size, self.tower_selected.y // box_size
				self.map[j][i] = 0

				self.tower_selected = None

		# Click elsewhere
		else:    
			self.enemy_selected = None
			self.tower_selected = None

		
