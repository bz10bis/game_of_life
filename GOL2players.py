import pygame
import copy
from pygame.locals import *

class Cell:
	def __init__(self, coordinates, owner=0, alive=False):
		self.next_state = None
		self.pressed = False
		self.alive = alive
		self.coordinates = coordinates
		self.owner = owner

class Board:
	def __init__(self, board_sizes):
		self.array_of_cells = []
		self.board_sizes = board_sizes
		self.board_x_size = board_sizes[0]
		self.board_y_size = board_sizes[1]

	def fill(self):
		for i in range(self.board_x_size):
			self.array_of_cells.append([])
			for j in range(self.board_y_size):
				self.array_of_cells[i].insert(j, Cell((i,j)))

	def get_surrounding(self, cell_position):
		values = self.check_out_of_range(cell_position, self.board_x_size)
		number_of_neighbour = 0
		number_of_player1_neighbour = 0
		number_of_player2_neighbour = 0
		column = values[0]
		next_column = column + 2
		row = values[1]
		for i in range(column - 1, next_column):
			if i >= 0 and i < self.board_x_size:
				if self.array_of_cells[i][row].alive == True and i != column:
					if self.array_of_cells[i][row].owner == 2:
						number_of_player2_neighbour += 1
					elif self.array_of_cells[i][row].owner == 1:
						number_of_player1_neighbour += 1
				if row - 1 >= 0:
					if self.array_of_cells[i][row - 1].alive == True:
						if self.array_of_cells[i][row].owner == 2:
							number_of_player2_neighbour += 1
						elif self.array_of_cells[i][row].owner == 1:
							number_of_player1_neighbour += 1
				if row + 1 < self.board_x_size:
					if self.array_of_cells[i][row + 1].alive == True:
						if self.array_of_cells[i][row].owner == 2:
							number_of_player2_neighbour += 1
						elif self.array_of_cells[i][row].owner == 1:
							number_of_player1_neighbour += 1		
		return number_of_player1_neighbour,number_of_player2_neighbour

	def get_surrounding_cell(self, cell_position):
		number_of_player1_neighbour = 0
		number_of_player2_neighbour = 0
		if(self.is_valid(cell_position[0] - 1) and self.is_valid(cell_position[1] - 1)):
			if self.array_of_cells[cell_position[0] - 1][cell_position[1] - 1].alive:
				if self.array_of_cells[cell_position[0] - 1][cell_position[1] - 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] - 1][cell_position[1] - 1].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0]) and self.is_valid(cell_position[1] - 1)):
			if self.array_of_cells[cell_position[0]][cell_position[1] - 1].alive:
				if self.array_of_cells[cell_position[0]][cell_position[1] - 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0]][cell_position[1] - 1].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0] + 1) and self.is_valid(cell_position[1] - 1)):
			if self.array_of_cells[cell_position[0] + 1][cell_position[1] - 1].alive:
				if self.array_of_cells[cell_position[0] + 1][cell_position[1] - 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] + 1][cell_position[1] - 1].owner == 2:
					number_of_player2_neighbour += 1									
		if(self.is_valid(cell_position[0] - 1) and self.is_valid(cell_position[1])):
			if self.array_of_cells[cell_position[0] - 1][cell_position[1]].alive:
				if self.array_of_cells[cell_position[0] - 1][cell_position[1]].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] - 1][cell_position[1]].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0] + 1) and self.is_valid(cell_position[1])):
			if self.array_of_cells[cell_position[0] + 1][cell_position[1]].alive:
				if self.array_of_cells[cell_position[0] + 1][cell_position[1]].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] + 1][cell_position[1]].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0] - 1) and self.is_valid(cell_position[1] + 1)):
			if self.array_of_cells[cell_position[0] - 1][cell_position[1] + 1].alive:
				if self.array_of_cells[cell_position[0] - 1][cell_position[1] + 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] - 1][cell_position[1] + 1].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0]) and self.is_valid(cell_position[1] + 1)):
			if self.array_of_cells[cell_position[0]][cell_position[1] + 1].alive:
				if self.array_of_cells[cell_position[0]][cell_position[1] + 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0]][cell_position[1] + 1].owner == 2:
					number_of_player2_neighbour += 1
		if(self.is_valid(cell_position[0] + 1) and self.is_valid(cell_position[1] + 1)):
			if self.array_of_cells[cell_position[0] + 1][cell_position[1] + 1].alive:
				if self.array_of_cells[cell_position[0] + 1][cell_position[1] + 1].owner == 1:
					number_of_player1_neighbour += 1
				if self.array_of_cells[cell_position[0] + 1][cell_position[1] + 1].owner == 2:
					number_of_player2_neighbour += 1																					
		
		return number_of_player1_neighbour, number_of_player2_neighbour

	def is_valid(self, x):
		if x < 0 or x >= self.board_x_size or x >= self.board_y_size:
			return False
		else:
			return True

	def check_out_of_range(self,values, limit):
		new_values = []
		for v in values:
			if(v >= limit):
				v = limit - 1
			if(v < 0):
				v = 0
			new_values.append(v)
		return new_values

class Game:
	def __init__(self, image_size, board_sizes, speed=1):
		self.image_size = image_size
		self.board_sizes = board_sizes
		self.board_x_size = board_sizes[0]
		self.board_y_size = board_sizes[1]
		self.board_width = self.board_x_size * self.image_size
		self.board_heigth = self.board_y_size * self.image_size
		self.window_size = self.board_width, self.board_heigth
		self.board = Board(self.board_sizes)
		self.clock = pygame.time.Clock()
		self.board.fill()
		self.iteration = 0
		self.speed = speed
		self.window = None
		self.image_alive_player1 = None
		self.image_alive_player2 = None
		self.image_dead = None
		self.previous_board = None

	def initialize_window(self):
		self.window = pygame.display.set_mode(self.window_size, HWSURFACE|DOUBLEBUF|RESIZABLE)
		self.image_alive_player1 = pygame.image.load("alive.png").convert()
		self.image_alive_player2 = pygame.image.load("alive2.png").convert()
		self.image_dead = pygame.image.load("dead.png").convert()

	def draw_board(self):
		for i in range(self.board_x_size):
			for j in range(self.board_y_size):
				oneCell = self.board.array_of_cells[i][j]
				coordinates = oneCell.coordinates
				if oneCell.alive:
					if oneCell.owner == 2:
						self.window.blit(self.image_alive_player2, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))    
					elif oneCell.owner == 1:
						self.window.blit(self.image_alive_player1, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))
				else:
					self.window.blit(self.image_dead, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))    
		pygame.display.flip()

	def get_cells_location(self):
		cells_location = [];
		for i in range(self.board_x_size):
			cells_location.append([])
			for j in range(self.board_y_size):
				cells_location[i].append((self.board.array_of_cells[i][j].coordinates[0] * self.image_size, self.board.array_of_cells[i][j].coordinates[1] * self.image_size))
		return cells_location

	def is_inside_area(self, position, area):
		if position[0] >= area[0] and position[0] < area[0] + self.image_size and position[1] >= area[1] and position[1] < area[1] + self.image_size:
			return True
		return False

	def next_step(self):
		for i in range(self.board_x_size):
			for j in range(self.board_y_size):
				oneCell = self.board.array_of_cells[i][j]
				number_of_player1_neighbour, number_of_player2_neighbour = self.board.get_surrounding_cell(oneCell.coordinates)
				number_of_neighbour = number_of_player1_neighbour + number_of_player2_neighbour
				if (number_of_neighbour == 2 or number_of_neighbour == 3) and oneCell.alive == True:
					oneCell.next_state = True
				elif number_of_neighbour == 3 and oneCell.alive == False:
					oneCell.next_state = True
					if number_of_player1_neighbour > number_of_player2_neighbour:
						oneCell.owner = 1
					elif number_of_player1_neighbour < number_of_player2_neighbour:
						oneCell.owner = 2
				else:
					oneCell.next_state = False
		for i in range(self.board_x_size):
			for j in range(self.board_y_size):
				oneCell = self.board.array_of_cells[i][j]
				if oneCell.next_state == True:
					oneCell.next_state = False
					oneCell.alive = True
				else:
					oneCell.next_state = False
					oneCell.alive = False
		self.draw_board()

	def run(self):
		self.initialize_window()
		self.draw_board()
		done = False
		run = False
		elapsed_time = 0
		while done != True:
			ticks = self.clock.tick(60)
			elapsed_time += ticks
			for event in pygame.event.get():
				if event.type == QUIT:
					done = True
				elif event.type == KEYUP:
					if event.key == K_SPACE:
						self.next_step()
					elif event.key == K_c:
						print('Clear')
						for i in range(self.board_x_size):
							for j in range(self.board_y_size):
								self.board.array_of_cells[i][j].alive = False
						self.draw_board()
					elif event.key == K_l:
						self.load_board()
						self.draw_board()
					elif event.key == k_s:
						self.save_board()
					elif event.key == k_r:
						run = not run
						self.iteration = 0
						if(run):
							self.save_board()
			mouse = pygame.mouse.get_pressed()
			mouse_position = pygame.mouse.get_pos()
			if mouse[0]:
				cells_location = self.get_cells_location()
				for i in range(self.board_x_size):
					for j in range(self.board_y_size):
						oneCell = self.board.array_of_cells[i][j]
						if self.is_inside_area(mouse_position, cells_location[i][j]):
							if oneCell.alive != True:
								oneCell.alive = True
								oneCell.pressed = True
								oneCell.owner = 1
							if oneCell.alive == True and oneCell.owner == 2:
								oneCell.owner = 1
				self.draw_board()
			if mouse[1]:
				cells_location = self.get_cells_location()
				for i in range(self.board_x_size):
					for j in range(self.board_y_size):
						oneCell = self.board.array_of_cells[i][j]
						if self.is_inside_area(mouse_position, cells_location[i][j]):
							if oneCell.alive != True:
								oneCell.alive = True
								oneCell.pressed = True
								oneCell.owner = 2
							if oneCell.alive == True and oneCell.owner == 1:
								oneCell.owner = 2								
				self.draw_board()
			if mouse[2]:
				cells_location = self.get_cells_location()
				for i in range(self.board_x_size):
					for j in range(self.board_y_size):
						oneCell = self.board.array_of_cells[i][j]
						if self.is_inside_area(mouse_position, cells_location[i][j]):
							if oneCell.alive == True:
								oneCell.alive = False
								oneCell.pressed = False
								oneCell.owner = 0
				self.draw_board()				

			if run and elapsed_time >= 1000/self.speed:
				elapsed_time = 0
				self.iteration += 1
				self.next_step()


if __name__ == '__main__':
	pygame.init()
	newGame = Game(16, (50,50))
	newGame.run()
	pygame.quit()