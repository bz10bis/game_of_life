import pygame
from pygame.locals import *

class cell(object):

    def __init__(self, coordinates, alive=False):
        self.next_state = None
        self.pressed = False
        self.alive = alive
        self.coordinates = coordinates

    def get_coordinates(self):
        return self.coordinates

class board(object):

    def __init__(self,board_size):
        self.array_of_cells = []
        self.board_size = board_size

    def fill(self):
        for i in range(self.board_size):
            self.array_of_cells.append([])
            for j in range(self.board_size):
                self.array_of_cells[i].insert(j, cell((i,j)))

    def get_surrounding(self, cell_position):
        values = self.check_out_of_range(cell_position, self.board_size)
        number_of_neighbour = 0
        column = values[0]
        next_column = column + 2
        row = values[1]
        for i in range(column - 1, next_column):
            #print("Board Size: " + str(self.board_size) + " i: " + str(i) + " row: " + str(row) + " column " + str(column))
            if i >= 0 and i < self.board_size:
                if self.array_of_cells[i][row].alive == True and i != column:
                    number_of_neighbour += 1
                if row - 1 >= 0:
                    if self.array_of_cells[i][row - 1].alive == True:
                        number_of_neighbour += 1
                if row + 1 < self.board_size:
                    if self.array_of_cells[i][row + 1].alive == True:
                        number_of_neighbour += 1

        return number_of_neighbour

    def check_out_of_range(self,values, limit):
        new_values = []
        for v in values:
            if(v >= limit):
                v = limit - 1
            if(v < 0):
                v = 0
            new_values.append(v)
        return new_values

class game(object):

    def __init__(self,image_size, board_size):
        self.image_size = image_size
        self.board_size = board_size
        self.board_width = board_size * image_size
        self.board_height = board_size * image_size
        self.window_size = self.board_width, self.board_height
        print(self.window_size)
        self.board = board(self.board_size)
        self.board.fill()
        self.window = None
        self.image_alive = None
        self.image_dead = None
        

    def initialize_window(self):
        self.window = pygame.display.set_mode(self.window_size)
        self.image_alive = pygame.image.load("alive.png").convert()
        self.image_dead = pygame.image.load("dead.png").convert()

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                oneCell = self.board.array_of_cells[i][j]
                coordinates = oneCell.get_coordinates()
                if oneCell.alive:
                    self.window.blit(self.image_alive, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))
                else:
                    self.window.blit(self.image_dead, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))    
        pygame.display.flip()

    def get_cells_location(self):
        cells_location = [];
        for i in range(self.board_size):
            cells_location.append([])
            for j in range(self.board_size):
                cells_location[i].append((self.board.array_of_cells[i][j].coordinates[0] * self.image_size, self.board.array_of_cells[i][j].coordinates[1] * self.image_size))
        return cells_location       

    def is_inside_area(self, position, area):
        if position[0] >= area[0] and position[0] < area[0] + self.image_size and position[1] >= area[1] and position[1] < area[1] + self.image_size:
            return True
        return False

    def next_step(self):
        print("Next Step")
        for i in range(self.board_size):
            for j in range(self.board_size):
                oneCell = self.board.array_of_cells[i][j]
                number_of_neighbour = self.board.get_surrounding(oneCell.coordinates)
                if (number_of_neighbour == 2 or number_of_neighbour == 3) and oneCell.alive == True:
                    oneCell.next_state = True
                elif number_of_neighbour == 3 and oneCell.alive == False:
                    oneCell.next_state = True
                else:
                    oneCell.next_state = False
        for i in range(self.board_size):
            for j in range(self.board_size):
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
        while done != True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True 

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.next_step() 

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos() 
                    cells_location = self.get_cells_location()
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            oneCell = self.board.array_of_cells[i][j]
                            if self.is_inside_area(mouse_position, cells_location[i][j]):
                                if oneCell.alive:
                                    oneCell.alive = False
                                    oneCell.pressed = False
                                else:                           
                                    oneCell.alive = True
                                    oneCell.pressed = True
                                    number_of_neighbour = self.board.get_surrounding(oneCell.coordinates)
                                self.draw_board()
                            
        return True            

if __name__ == "__main__":
    pygame.init()
    newGame = game(16, 32)
    newGame.run()
    pygame.quit()