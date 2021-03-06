import pygame
import copy
from pygame.locals import *

class cell(object):

    def __init__(self, coordinates, alive=False):
        self.next_state = None
        self.pressed = False
        self.alive = alive
        self.coordinates = coordinates
        self.player2 = False

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
        number_of_player1_neighbour = 0
        number_of_player2_neighbour = 0
        column = values[0]
        next_column = column + 2
        row = values[1]
        for i in range(column - 1, next_column):
            #print("Board Size: " + str(self.board_size) + " i: " + str(i) + " row: " + str(row) + " column " + str(column))
            if i >= 0 and i < self.board_size:
                if self.array_of_cells[i][row].alive == True and i != column:
                    if self.array_of_cells[i][row].player2:
                        number_of_player2_neighbour += 1
                    else:
                        number_of_player1_neighbour += 1
                if row - 1 >= 0:
                    if self.array_of_cells[i][row - 1].alive == True:
                        if self.array_of_cells[i][row].player2:
                            number_of_player2_neighbour += 1
                        else:
                            number_of_player1_neighbour += 1
                if row + 1 < self.board_size:
                    if self.array_of_cells[i][row + 1].alive == True:
                        if self.array_of_cells[i][row].player2:
                            number_of_player2_neighbour += 1
                        else:
                            number_of_player1_neighbour += 1

        return number_of_player1_neighbour,number_of_player2_neighbour

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

    def __init__(self,image_size, board_size, speed=1):
        self.image_size = image_size
        self.board_size = board_size
        self.board_width = board_size * image_size
        self.board_height = board_size * image_size
        self.window_size = self.board_width , self.board_height + 100
        print(self.window_size)
        self.board = board(self.board_size)
        self.clock = pygame.time.Clock()
        self.speed = speed
        self.board.fill()
        self.window = None
        self.image_alive = None
        self.image_dead = None
        self.iteration = 0
        self.previous_board = None

    def initialize_window(self):
        self.window = pygame.display.set_mode(self.window_size, HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.image_alive = pygame.image.load("alive.png").convert()
        self.image_alive_2 = pygame.image.load("alive2.png").convert()
        self.image_dead = pygame.image.load("dead.png").convert()
        self.image_running = pygame.image.load("red_light.png").convert()
        self.window.blit(self.image_running, (10, self.board_height))

    def draw_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                oneCell = self.board.array_of_cells[i][j]
                coordinates = oneCell.get_coordinates()
                if oneCell.alive:
                    if oneCell.player2:
                        self.window.blit(self.image_alive_2, (coordinates[0] * self.image_size, coordinates[1] * self.image_size))    
                    else:
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
        for i in range(self.board_size):
            for j in range(self.board_size):
                oneCell = self.board.array_of_cells[i][j]
                number_of_player1_neighbour, number_of_player2_neighbour = self.board.get_surrounding(oneCell.coordinates)
                number_of_neighbour = number_of_player1_neighbour + number_of_player2_neighbour            
                if (number_of_neighbour == 2 or number_of_neighbour == 3) and oneCell.alive == True:
                    oneCell.next_state = True                    
                elif number_of_neighbour == 3 and oneCell.alive == False:
                    oneCell.next_state = True
                    print("Number of p1: " + str(number_of_player1_neighbour))
                    print("Number of p2: " + str(number_of_player2_neighbour))
                    if number_of_player1_neighbour > number_of_player2_neighbour:
                        oneCell.player2 = False
                    elif number_of_player1_neighbour < number_of_player2_neighbour:
                        oneCell.player2 = True
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

    def save_board(self):
        self.previous_board = copy.deepcopy(self.board.array_of_cells)
        print(self.board.array_of_cells[0][0].alive)

    def load_board(self):
        if(self.previous_board != None):
            self.board.array_of_cells = self.previous_board
            print(self.board.array_of_cells[0][0].alive)
            self.draw_board()

    def run(self):
        self.initialize_window()
        self.draw_board()
        elapsed_time = 0
        run = False
        done = False
        while done != True:
            milliseconde = self.clock.tick(60)
            elapsed_time += milliseconde
            for event in pygame.event.get():

                if event.type == QUIT:
                    done = True 

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        self.next_step() 

                    elif event.key == K_c:
                        print("Clear")
                        for i in range(self.board_size):
                            for j in range(self.board_size):
                                self.board.array_of_cells[i][j].alive = False
                        self.draw_board()

                    elif event.key == K_l:
                        print("Load last save state")
                        self.load_board()
                        self.draw_board()

                    elif event.key == K_s:
                        print("Saving")
                        self.save_board()

                    elif event.key == K_r:
                        run = not run
                        self.iteration = 0
                        if(run):
                            print("Start")
                            self.save_board()
                            self.image_running = pygame.image.load("green_light.png").convert()
                        else:
                            self.image_running = pygame.image.load("red_light.png").convert()
                            print("Stop")
                        self.window.blit(self.image_running, (10, self.board_height))
                        pygame.display.update()

            mouse = pygame.mouse.get_pressed()
            mouse_position = pygame.mouse.get_pos()
            if mouse[0]:
                cells_location = self.get_cells_location()
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        oneCell = self.board.array_of_cells[i][j]
                        if self.is_inside_area(mouse_position, cells_location[i][j]):
                            if oneCell.alive != True:
                                oneCell.alive = True
                                oneCell.pressed = True
                self.draw_board()

            if mouse[1]:
                cells_location = self.get_cells_location()
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        oneCell = self.board.array_of_cells[i][j]
                        if self.is_inside_area(mouse_position, cells_location[i][j]):
                            if oneCell.alive != True:
                                oneCell.alive = True
                                oneCell.pressed = True
                                oneCell.player2 = True
                self.draw_board()

            if mouse[2]:
                cells_location = self.get_cells_location()
                for i in range(self.board_size):
                    for j in range(self.board_size):
                        oneCell = self.board.array_of_cells[i][j]
                        if self.is_inside_area(mouse_position, cells_location[i][j]):
                            if oneCell.alive == True:
                                oneCell.alive = False
                                oneCell.pressed = False
                                oneCell.player2 = False
                self.draw_board()

            if run and elapsed_time >= 1000/self.speed:
                elapsed_time = 0
                self.iteration += 1
                print(self.iteration)
                self.next_step()
                                          
        return True            

if __name__ == "__main__":
    pygame.init()
    newGame = game(16, 51, 3)
    newGame.run()
    pygame.quit()