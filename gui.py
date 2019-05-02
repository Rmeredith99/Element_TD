import pygame
import math
from td import State
from pygame.locals import *
from time import time
pygame.font.init()
flags = DOUBLEBUF

# The game state where everything is run
state = State()

# Setting up parameters for the board and the screen
board_height = 700
board_width = int(board_height * 1.5)
side_bar_size = int(board_width / 6)
square_size = int(math.ceil(board_height / 10.0))
squares = len(state.map)

pygame.init()
screen = pygame.display.set_mode((board_width + side_bar_size*2, board_height), flags)
clock = pygame.time.Clock()

done = False


# Colors
white = (255, 255, 255)
light_gray = (200, 200, 200)
dark_gray = (100, 100, 100)
black = (0, 0, 0)
red = (170, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 170)
yellow = (255, 255, 0)
dark_brown = (100, 70, 33)
light_brown = (170, 133, 60)

# Artwork
corner_art = pygame.image.load("game_art/corner_art.png")
background = pygame.image.load("game_art/background.png")
how_to_play = pygame.image.load("game_art/how_to_play.png")
lives_art = pygame.image.load("game_art/lives_art.png")
lives_art = pygame.transform.scale(lives_art, (70, 70))
gold_art = pygame.image.load("game_art/gold_art.png")
gold_art = pygame.transform.scale(gold_art, (70, 70))

# Path Art
straight_path_1_h = pygame.image.load("game_art/path/straight_1.png")
straight_path_1_h = pygame.transform.scale(straight_path_1_h, (square_size, square_size))
straight_path_2_h = pygame.image.load("game_art/path/straight_2.png")
straight_path_2_h = pygame.transform.scale(straight_path_2_h, (square_size, square_size))
straight_path_3_h = pygame.image.load("game_art/path/straight_3.png")
straight_path_3_h = pygame.transform.scale(straight_path_3_h, (square_size, square_size))
straight_path_1_v = pygame.transform.rotate(straight_path_1_h, 90)
straight_path_2_v = pygame.transform.rotate(straight_path_2_h, 90)
straight_path_3_v = pygame.transform.rotate(straight_path_3_h, 90)

corner_path_1_q2 = pygame.image.load("game_art/path/corner_1.png")
corner_path_1_q2 = pygame.transform.scale(corner_path_1_q2, (square_size, square_size))
corner_path_2_q2 = pygame.image.load("game_art/path/corner_2.png")
corner_path_2_q2 = pygame.transform.scale(corner_path_2_q2, (square_size, square_size))

corner_path_1_q1 = pygame.transform.rotate(corner_path_1_q2, -90)
corner_path_1_q3 = pygame.transform.rotate(corner_path_1_q2, 90)
corner_path_1_q4 = pygame.transform.rotate(corner_path_1_q2, 180)

corner_path_2_q1 = pygame.transform.rotate(corner_path_2_q2, -90)
corner_path_2_q3 = pygame.transform.rotate(corner_path_2_q2, 90)
corner_path_2_q4 = pygame.transform.rotate(corner_path_2_q2, 180)

# Saving path images to save computation time
path_array = [[None for i in range(int(1.5*squares))] for j in range(squares)]
path_screen = pygame.display.set_mode((board_width  + side_bar_size*2, board_height), flags)
path_initiated = False

def get_path_corner(number, quandrant):
	"""
	[get_path_corner] returns an image for a corner for a 
		given quadrant. Different [number]s return slightly
		different images, but with the same angles.
	"""
	q1 = [corner_path_1_q1, corner_path_2_q1]
	q2 = [corner_path_1_q2, corner_path_2_q2]
	q3 = [corner_path_1_q3, corner_path_2_q3]
	q4 = [corner_path_1_q4, corner_path_2_q4]
	if quandrant == 1:
		return q1[number - 1]
	elif quandrant == 2:
		return q2[number - 1]
	elif quandrant == 3:
		return q3[number - 1]
	elif quandrant == 4:
		return q4[number - 1]

def get_path_straight(number, vert=False):
	"""
	[get_path_straight] returns an image for a straight path
		with the angle depending on whether [vert] (vertical)
		is true or false. Different [number]s return slightly
		different images, but with the same angles.
	"""
	h = [straight_path_1_h, straight_path_2_h, straight_path_3_h]
	v = [straight_path_1_v, straight_path_2_v, straight_path_3_v]
	if vert:
		return v[number - 1]
	else:
		return h[number - 1]


def write_text(screen, text, x, y, color, size, font="Comic Sans Ms"):
    """
    [write_text] is an encapsulation of the text-writing process using
        the blit function on the given screen. Function parameters define
        the look of the text.
    """
    myfont = pygame.font.SysFont(font, size)
    textsurface = myfont.render(text, False, color)
    screen.blit(textsurface,(x, y))

def draw_grid_square(x, y, color):
	length = int(board_height / squares)
	buffer = int(length / 20)
	small_length = length - buffer * 2
	pygame.draw.rect(screen, color, [x + buffer, y + buffer, small_length, small_length])

def draw_grid():
	"""
	[draw_grid] creates a grid that overlays the map so that
		it's easier to see where towers are placed
	"""
	w = 3
	for j in range(squares):
		y = j * square_size
		for i in range(int(squares*1.5)):
			x = i * square_size
			# horizontal line
			if j != 0:
				pygame.draw.rect(screen, light_gray, [x + 10, y-w//2, square_size - 20, w])
			# vertical line
			if i != 0:
				pygame.draw.rect(screen, light_gray, [x - w//2, y +10, w, square_size - 20])


def draw_sidebar(state):
	pygame.draw.rect(screen, (255,255,255), [board_width, 0, side_bar_size * 2, board_height])
	pygame.draw.rect(screen, (0,0,0), [board_width + side_bar_size - 1, 0, 2, board_height])
	state.draw_sidebar(screen, (board_width, 0))
	# For the game logo
	pygame.draw.rect(screen, (100,100,100), [board_width*7/6, 0, side_bar_size, 206])
	state.draw_sidebar_2(screen, (board_width + side_bar_size, 206))
	animation = pygame.transform.scale(corner_art, (175, 206))
	screen.blit(animation, (board_width + side_bar_size, 0))

	# Lives and gold art
	screen.blit(lives_art, (board_width + 25, -15))
	screen.blit(gold_art, (board_width + 25, 15))
		
def draw_state(state, time_delta):
	"""
	[draw_state] is a void function that draws the
		given state on the local screen
	"""
	# pygame.draw.rect(screen, dark_gray, [0, 0, board_width, board_height])
	# length = int(board_height / squares)
	# board_map = state.map
	# for y in range(squares):
	# 	for x in range(int(squares * 1.5)):
	# 		value = board_map[y][x]
	# 		if value == 1:
	# 			draw_grid_square(x * length, y * length, (124, 95, 0))
	# 		else:
	# 			draw_grid_square(x * length, y * length, (40, 180, 70))

	# state.update(time_delta)
	# state.draw(screen)
	# return None

	# The length of one grid square
	length = int(board_height / squares)

	global path_initiated
	global path_screen

	screen.blit(background, (0, 0))
	if path_initiated and not state.end_of_round:
		for y in range(squares):
			for x in range(int(1.5*squares)):
				img = path_array[y][x]
				if img != None:
					screen.blit(img, (x * length, y * length))
	else:
		path_initiated = False
		for y in range(squares):
			for x in range(int(squares * 1.5)):
				value = state.map[y][x]
				if value == 1:
					# top
					try:
						# fixes roll-over issue with -1 index
						top = (state.map[y - 1][x] == 1) and (y - 1 >= 0)
					except:
						top = 0
					# right
					try:
						right = (state.map[y][x + 1] == 1)
					except:
						right = 0
					# bottom
					try:
						bottom = (state.map[y + 1][x] == 1)
					except:
						bottom = 0
					# left
					try:
						left = (state.map[y][x - 1] == 1)  and (x - 1 >= 0)
					except:
						left = 0
					
					if (left + right + top + bottom) == 1:
						if left or right:
							straight = True
							vertical = False
						elif x == 0:
							if top:
								quad = 2
								straight = False
							else:
								quad = 3
								straight = False
						elif x == len(state.map[0]) - 1:
							if top:
								quad = 1
								straight = False
							else:
								quad = 4
								straight = False

					else:
						if right and left:
							straight = True
							vertical = False
						elif top and bottom:
							straight = True
							vertical = True
						else:
							straight = False
							if right and top:
								quad = 1
							elif top and left:
								quad = 2
							elif left and bottom:
								quad = 3
							else:
								quad = 4
					if straight:
						img = get_path_straight((x + y) % 3 + 1, vert=vertical)
					else:
						img = get_path_corner((x + y) % 2 + 1, quad)
					
					path_array[y][x] = img
					screen.blit(img, (x * length, y * length))
	
	# grid when adding a tower
	if state.add_tower_button:
		draw_grid()

	state.update(time_delta)
	state.draw(screen)

def write_high_scores(names, scores, difficulty):
	"""
	[write_high_scores] adds data to the high scores
	"""
	with open('high_scores_' + difficulty + '.txt', 'w') as F:
		for i in range(len(names)):
			s = names[i] + "\t" + str(scores[i]) + "\n"
			F.write(s)

def get_high_scores(difficulty):
	"""
	[get_high_scores] retrieves the high scores
	"""
	with open('high_scores_' + difficulty + '.txt', 'r') as F:
		s = F.read().strip()
		entries = s.split("\n")
		names = []
		scores = []
		for i in entries:
			if i == "":
				return [], []
			name, score = i.split("\t")
			names.append(name)
			scores.append(score)
	return names, scores

def start_screen(state, page=1, click=None):
	"""
	[start_screen] displays the initial start screen which 
		includes difficulty selection
	"""
	# Opening screen
	if page == 1:
		h = 180
		w = 270
		buffer = 20
		width = int(board_width/6)
		pygame.draw.rect(screen, light_gray, [w, h, board_width - 2*w, board_height - 2*h])
		pygame.draw.rect(screen, dark_gray, [w + buffer, h + buffer, board_width - 2*(w+buffer), board_height - 2*(h+buffer)])
		
		# Drawing game logo
		scale = 1.35
		animation = pygame.transform.scale(corner_art, (int(side_bar_size * scale), int(206 * scale)))
		screen.blit(animation, (w + 30, h + 30))

		# Text
		font = "DroidSans"
		x = 65
		y = 45
		increment = 35
		size = 50
		x_adj = [3, 62, 5, 55]
		write_text(screen, "Welcome", w + side_bar_size * scale + x + x_adj[0], h + y, black, size, font=font)
		write_text(screen, "to", w + side_bar_size * scale + x + x_adj[1], h + y + increment, black, size, font=font)
		write_text(screen, "Element", w + side_bar_size * scale + x + x_adj[2], h + y + 2 * increment, black, size, font=font)
		write_text(screen, "TD", w + side_bar_size * scale + x + x_adj[3], h + y + 3 * increment, black, size, font=font)

		# Continue button
		font_color = (255,255,255)
		width = int(board_width/6)
		x = 320
		y = 220
		pygame.draw.rect(screen, (0,0,0), [w + x, h + y, width - 2*20, 70])
		pygame.draw.rect(screen, (0, 100, 200), [w + x+5, h + y+5, width - 2*(20+5), 60])
		write_text(screen, "Continue", w + x + 55 - 4*8, h + y+25, font_color, 30, font = "DroidSans")

		# Handling clicking the continue button
		if click != None:
			click_x, click_y = click
			x = 320
			y = 220
			if (click_x > w+x) and (click_x < w+x+ width - 2*20) and (click_y > h+y) and (click_y < h+y+70):
				return 2

		return page
	
	# Selecting a difficulty
	elif page == 2:
		h = 180
		w = 270
		buffer = 20
		width = int(board_width/6)
		pygame.draw.rect(screen, light_gray, [w, h, board_width - 2*w, board_height - 2*h])
		pygame.draw.rect(screen, dark_gray, [w + buffer, h + buffer, board_width - 2*(w+buffer), board_height - 2*(h+buffer)])

		write_text(screen, "Select a difficulty", w + 140, h + 60, (0,0,0), 40, font = "DroidSans")

		difficulties = ["EASY", "MEDIUM", "HARD"]
		colors = [(0,220,0), (220,220,0), (220,0,0)]
		for i, difficulty in enumerate(difficulties):
			font_color = (0,0,0)
			width = int(board_width/6)
			x = 37 + 150 * i
			y = 220
			pygame.draw.rect(screen, (0,0,0), [w + x, h + y, width - 2*20, 70])
			pygame.draw.rect(screen, colors[i], [w + x+5, h + y+5, width - 2*(20+5), 60])
			write_text(screen, difficulty, w + x + 55 - 4*len(difficulty), h + y+25, font_color, 30, font = "DroidSans")

		# How to play button
		x = 187
		y = 125
		pygame.draw.rect(screen, (0,0,0), [w+x, h+y, width - 2*20, 70])
		pygame.draw.rect(screen, (0,200,200), [w + x+5, h + y+5, width - 2*(20+5), 60])
		write_text(screen, "How to play", w + x + 55 - 4*11, h + y+25, font_color, 30, font = "DroidSans")

		if click != None:
			click_x, click_y = click
			# Difficulties
			for i in range(3):
				x = 37 + 150 * i
				y = 220
				if (click_x > w+x) and (click_x < w+x+ width - 2*20) and (click_y > h+y) and (click_y < h+y+70):
					state.difficulty = i + 1
					state.set_map(i+1)
					return 4

			# How to play screen
			x = 187
			y = 125
			if (click_x > w+x) and (click_x < w+x+ width - 2*20) and (click_y > h+y) and (click_y < h+y+70):
				return 3
		return page

	# How to play screen
	elif page == 3:
		screen.blit(how_to_play, (0, 0))

		# Back button
		x = 900
		y = 620
		h = 70
		w = 130
		pygame.draw.rect(screen, (0,0,0), [x, y, w, h])
		pygame.draw.rect(screen, (200,0,0), [x+5, y+5, w-10, h-10])
		write_text(screen, "Back", x + 30, y + 23, (0,0,0), 40, font = "DroidSans")

		if click != None:
			click_x, click_y = click
			if (click_x > x) and (click_x < x + w) and (click_y > y) and (click_y < y + h):
				# Covering up the 'how to play' screen behind the new window
				draw_state(state, 0)
				draw_sidebar(state)
				return 2 # returns to previous page

		return page

def game_over(state, page=1, click=None, name_string=""):
	"""
	[game_over] displays the game over graphics including displaying data,
		entering a high score, and displaying current high_scores.
	"""

	h = 180
	w = 270
	buffer = 20
	pygame.draw.rect(screen, light_gray, [w, h, board_width - 2*w, board_height - 2*h])
	pygame.draw.rect(screen, dark_gray, [w + buffer, h + buffer, board_width - 2*(w+buffer), board_height - 2*(h+buffer)])

	if state.difficulty == 1:
		difficulty = "easy"
	elif state.difficulty == 2:
		difficulty = "medium"
	else:
		difficulty = "hard"

	# Original Game Over screen
	if page == 1:
		write_text(screen, "GAME OVER", w + 45, h + 45, (200,0,0), 100, font="DroidSans")
		write_text(screen, "Score: " + str(state.score), w + 55, h + 130, (255,255,255), 35, font="DroidSans")
		# Correcting for when round 
		r = state.round_number
		if r == None:
			r = 1
		write_text(screen, "Rounds Completed: " + str(r - 1), w + 55, h + 170, (255,255,255), 35, font="DroidSans")

		# Next screen button
		font_color = (255,255,255)
		width = int(board_width/6)
		x = 320
		y = 220
		pygame.draw.rect(screen, (255,255,255), [w + x, h + y, width - 2*20, 70])
		pygame.draw.rect(screen, (0,0,0), [w + x+5, h + y+5, width - 2*(20+5), 60])
		write_text(screen, "Next", w + x + 45, h + y+25, font_color, 30, font = "DroidSans")

		if click != None:
			click_x, click_y = click
			if (click_x > w+x) and (click_x < w+x+ width - 2*20) and (click_y > h+y) and (click_y < h+y+70):
				page = 2

	# Enter High Score
	elif page == 2:
		
		names, scores = get_high_scores(difficulty)
		if len(names) < 10 or state.score > int(scores[9]):
			write_text(screen, "Congratulations!", w + 50, h + 50, (255,255,255), 30, font="DroidSans")
			write_text(screen, "You have achieved a high score.", w + 50, h + 90, (255,255,255), 30, font="DroidSans")
			write_text(screen, "Type your name and then hit 'Enter'.", w + 50, h + 130, (255,255,255), 30, font="DroidSans")
			# Partition line
			buffer = 30
			pygame.draw.rect(screen, (200,200,200), [w + buffer, h + 165, board_width - 2*w - 2*buffer, 5])
			# If the name has been entered
			if name_string.count("\r") > 0 and len(name_string) > 0:
				name_string = name_string[:-1]

				# Iterate through scores to find where new score places
				index = 0
				new_score = state.score
				for score in scores:
					if int(new_score) <= int(score):
						index += 1
				scores.insert(index, new_score)
				names.insert(index, name_string)

				write_high_scores(names[:10], scores[:10], difficulty)
				page = 3
			else:
				write_text(screen, "Name: " + name_string, w + 50, h + 190, (255,255,255), 35, font="DroidSans")
		else:
			page = 3

	# Leaderboard
	elif page == 3:
		names, scores = get_high_scores(difficulty)
		write_text(screen, "Leaderboard: " + difficulty.upper(), w + 130, h + 40, (255,255,255), 35, font="DroidSans")
		# Partition line
		buffer = 30
		pygame.draw.rect(screen, (200,200,200), [w + buffer, h + 70, board_width - 2*w - 2*buffer, 5])
		for i in range(len(names)):
			y = 22 * (i + 1)
			write_text(screen, str(i+1) + ") " + names[i], w + 50, h + 60 + y, (255,255,255), 30, font="DroidSans")
			write_text(screen, scores[i], w + 350, h + 60 + y, (255,255,255), 30, font="DroidSans")

	return page


def run_gui():
	"""
	[run_gui] is the main game loop
	"""
	
	global state, done
	max_frame_rate = 60
	counter = 0
	last_time = 0
	time_delta = 0
	elapsed_time = 0 # used for displaying framerate
	frame_rate = 0

	# Initiating the game graphics
	draw_state(state, time_delta)
	draw_sidebar(state)
	
	page = 1
	while not done:
		#### Start of event section
		click_pos = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				click = pygame.mouse.get_pressed()
				click_pos = pygame.mouse.get_pos()
		#### End of event section

		page = start_screen(state, page=page, click=click_pos)

		if page > 3:
			done = True

		clock.tick(max_frame_rate)
		pygame.display.flip()


	# Main Game Loop
	done = False
	while not done:
		if time_delta != 0:
			counter +=1

		# Adjusts the time_delta when paused
		if state.paused:
			time_delta = 0
			new_time = time()
			last_time = new_time

		else:
			new_time = time()
			time_delta = new_time - last_time
			last_time = new_time

		# Calculating frame rate for display purposes
		if counter % 5 == 0 and counter > 0:
			try:
				frame_rate = 5.0 / elapsed_time
			except:
				frame_rate = 1
			elapsed_time = 0
		else:
			elapsed_time += time_delta

		#### Start of event section
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				click = pygame.mouse.get_pressed()
				x, y = pygame.mouse.get_pos()

				# If a mouse click occurs
				if click[0] == 1:
					# State.click handles all events in the state class
					state.click(x, y)
							
		#### End of event section


		# Updating state graphics
		draw_state(state, time_delta)
		draw_sidebar(state)
		write_text(screen, str(int(frame_rate)), board_width + side_bar_size + 5, board_height - 30, (0,0,0), 20)
		
		# Updates screen
		clock.tick(max_frame_rate)
		pygame.display.flip()

		if state.lives == 0:
			done = True

	# Game-Over Sequence
	done = False
	page = 1
	name_string = ""
	while not done:

		#### Start of event section
		click_pos = None
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				click = pygame.mouse.get_pressed()
				click_pos = pygame.mouse.get_pos()
			elif event.type == pygame.KEYDOWN:
				if page == 2:
					key = event.unicode
					if key == "\b":
						if len(name_string) > 0:
							name_string = name_string[:-1]
					elif key == "\r" and len(name_string) == 0:
						pass
					else:
						name_string += event.unicode

				if page == 3:
					key = event.unicode
					if key == "\r":
						# Start over game
						state = State()
						run_gui()
						done = True

			

		#### End of event section

		page = game_over(state, page=page, click=click_pos, name_string=name_string)

		clock.tick(max_frame_rate)
		pygame.display.flip()

		
if __name__ == "__main__":
	run_gui()
	