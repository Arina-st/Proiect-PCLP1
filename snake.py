import pygame
import sys
import random
from pygame.math import Vector2
class SNAKE:
    def __init__(self):
        self.body= [Vector2(5,10),Vector2(6,10),Vector2(7,10)]
        self.direction = Vector2(1,0)
        self.newblock = False

        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()


        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()
    

    def draw_snake(self):
        self.update_head_graphics()

        #pentru marimea snake-ului
        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            #directia sarpelui
            if index == 0:
                screen.blit(self.head,block_rect)
            else:
                pygame.draw.rect(screen,(150,100,100),block_rect)
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down


    def move_snake(self):
        #se creste sarpele miscandu-l cu o pozitie in directie fara sa se taie ultimul vector
        if self.newblock == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newblock = False
        else:
        #se misca sarpele miscandu-l cu o pozitie in directie dar se taie utlima pozitie pentru a pastra marimea
           body_copy = self.body[:-1]
           body_copy.insert(0,body_copy[0] + self.direction)
           self.body = body_copy[:]
    def grow(self):
        self.newblock = True

class FRUCT:
    def __init__(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number- 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
        #se alege pozitia x si y -> vector 2D
    #functie care deseneaza patratul(fructul)
    def draw_fruit(self):
        #pygame.Rect are nevoie de int dar ii dam float(valorile dintr-un vector sunt de tip float)
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y *cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        #pygame.draw.rect(screen,(255,0,0),fruit_rect)
    #se aleg x,y(coordonate dintr-un vector) la intamplare
    def randomize(self):
        self.x = random.randint(1,cell_number - 3)
        self.y = random.randint(1,cell_number- 3)
        self.pos = pygame.math.Vector2(self.x,self.y)
class MAIN:
    #folosita pentru ca codul sa arate mai bine + snake si fruct in aceeasi metoda -> mai usor sa realizez munch
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUCT()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    def check_collision(self):
        #daca fructul si capul sunt pe aceeasi pozitie,atunci munch
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow()

pygame.init()
cell_size = 40
cell_number = 20
#variabila care tine fereastra in care jocul se va intampla
screen = pygame.display.set_mode((cell_number*cell_size ,cell_number*cell_size ))
#clock este folosit pentru a stabiliza frame-rate-ul(la 60)
clock = pygame.time.Clock()
#graficile marului
apple = pygame.image.load('graphics/apple.png').convert_alpha()
#un while care merge permanent,trebuie inchis dinauntru
SCREEN_UPDATE = pygame.USEREVENT
#this event will trigger every 150ms
pygame.time.set_timer(SCREEN_UPDATE,150)
main_game = MAIN()
while True:
    #daca ceva se intampla 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #daca ce s-a intamplat e sa dai pe X,quit.
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                main_game.snake.direction = (Vector2(0,-1))
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = (Vector2(0,1))
            if event.key == pygame.K_RIGHT:
               main_game.snake.direction = (Vector2(1,0))
            if event.key == pygame.K_LEFT:
               main_game.snake.direction = Vector2(-1,0)
    screen.fill((175,220,80))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)