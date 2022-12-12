# inspirace: https://zetcode.com/javagames/snake/

# Snake is an older classic video game. 
# It was first created in late 70s. Later it was brought to PCs. In this game the player controls a snake. 
# The objective is to eat as many apples as possible. Each time the snake eats an apple its body grows.
# The snake must avoid the walls and its own body. This game is sometimes called Nibbles.

# 1. pomocí 2 obdelníků rozdělte obrazovku na herní část a informační část (score, speed, level),
# 2. v informační části zobrazte aktuální score, speed a level,
# 3. po snědení N jablek zvyšte rychlost hry,
# 4. připravte další 2 úrovně hry v podobě zvyšujícího se počtu překážek (seznam seznamů seznamu bodů),
# 5. naprogramujte hru tak, aby s překážkami bylo v kolizích počítáno.
import pygame
from enum import Enum
from pygame.locals import *
from random import randrange
import time

class Movement(Enum):
    LEFT   = 1 
    RIGHT  = 2 
    UP     = 3
    DOWN   = 4 

class Level:
    def __init__(self, level, color, obstacles):
        self.level = level
        self.color = color
        self.scoreGoal = level * 10
        self.obstacles = obstacles

    def init_level(self):
        self._image_obstacle = pygame.image.load("../resources/alien.png").convert()

    def draw(self, surface):
        for obstacle in self.obstacles:
            surface.blit(self._image_obstacle, obstacle)

class Snake:
    # šířka hada
    DOT_SIZE = 10
    # délka hada při startu (počet stavebních kamenů)
    N_DOTS = 3
    # max pozice jablka v libovolné ose
    APPLE_MAX_POS = 29
    def __init__(self):
        # body = tělo hada, reprezentované seznamem bodů (n-tic) jednotlivých stavebních kamenů o šířce Snake.DOT_SIZE
        self._body = []
        self._speed = 5
        # aktuální pohyb
        self._movement = Movement.RIGHT
        # pozice jablka
        self._apple_position = []
        self._respawn_apple()
        # hlava hada
        self._image_head = None
        # stav. kámen hada
        self._image_body = None
        # jablko
        self._image_apple = None
        # Snake running
        self._running = True

    def init_snake(self):
        for z in range(Snake.N_DOTS):
            self._body.append([50 - z * Snake.DOT_SIZE, 50])
        self._image_head = pygame.image.load("../resources/head.png").convert()
        self._image_body = pygame.image.load("../resources/dot.png").convert()
        self._image_apple = pygame.image.load("../resources/apple.png").convert()

    def pohyb(self, movement):
        head = [self._body[0][0], self._body[0][1]]
        if movement == Movement.LEFT:
            head[0] -= Snake.DOT_SIZE
        if movement == Movement.RIGHT:
            head[0] += Snake.DOT_SIZE
        if movement == Movement.UP:
            head[1] -= Snake.DOT_SIZE
        if movement == Movement.DOWN:
            head[1] += Snake.DOT_SIZE
        if head == self._apple_position:
            self._body = [head] + self._body
            self._speed += self._speed/10
            self._respawn_apple()
        else:
            self._body = [head] + self._body[:-1]
    def is_collided(self):
        # S koncem obrazovky
        if (self._body[0][0] == -Snake.DOT_SIZE
            or self._body[0][0] == App.B_WIDTH + Snake.DOT_SIZE
            or self._body[0][1] == -Snake.DOT_SIZE
            or self._body[0][1] == App.B_HEIGHT + Snake.DOT_SIZE
            or self._body[0] in self._body[1:]):
            self._running = False

    def _respawn_apple(self):
        while True:
            self._apple_position = [randrange(Snake.APPLE_MAX_POS)*Snake.DOT_SIZE,
                                    randrange(Snake.APPLE_MAX_POS)*Snake.DOT_SIZE]
            if self._apple_position not in self._body:
                break
    
    def draw(self, surface):
        #draw apple
        surface.blit(self._image_apple, self._apple_position)
        #draw snake
        surface.blit(self._image_head, self._body[0])
            
        for i in range(len(self._body) - 1):
            surface.blit(self._image_body, self._body[i + 1])

    def setMovement(self, movement):
        self._movement = movement
    
    def getScore(self):
        return len(self._body) - Snake.N_DOTS

class App:
    B_WIDTH  = 300
    B_HEIGHT = 300
    A_WIDTH = 300

    def __init__(self):
        # hra neskončena
        self._running = True 
        self._display_surf = None
        self._snake = Snake()
        self._levels = [Level(1, (0, 0, 0), [[1, 2], [2, 4], [8, 100]]), Level(2, (100, 255, 7), [[1, 2], [2, 4], [3, 6]]), Level(3, (255, 0, 0), [[1, 2], [2, 4], [3, 6], [4, 8]])]
        self._level = self._levels[0]
        self.size = self.width, self.height = App.B_WIDTH + App.A_WIDTH, App.B_HEIGHT
        self._clock = None

        # inicializace PyGame modulů
        pygame.init()
        # nastavení velikosti okna, pokus o nastavení HW akcelerace, pokud nelze, použije se DOUBLEBUF
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._image_obstacle = pygame.image.load("../resources/alien.png").convert()
        self._running = True
        self._clock = pygame.time.Clock()
    def on_input_focus(self):
        pass
    def on_key_down(self, event):
        if event.key == pygame.K_LEFT:
            self._snake.setMovement(Movement.LEFT)
        if event.key == pygame.K_RIGHT:
            self._snake.setMovement(Movement.RIGHT)
        if event.key == pygame.K_UP:
            self._snake.setMovement(Movement.UP)
        if event.key == pygame.K_DOWN:
            self._snake.setMovement(Movement.DOWN)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == KEYDOWN:
            self.on_key_down(event)
    def game_over(self):
        pygame.font.init()
        self._display_surf.fill((self._level.color))
        font = pygame.font.SysFont("Arial", 50)
        font2 = pygame.font.SysFont("Arial", 20)
        render = font.render("Game Over", 1, (255, 0, 0))
        render2 = font2.render("Score: {}".format(self._snake.getScore()), 1, (0, 255, 0))
        self._display_surf.blit(render, (self.B_WIDTH/2 - render.get_width()/2, self.B_WIDTH/2 - render.get_height()/2))
        self._display_surf.blit(render2, (self.B_WIDTH/2 - render2.get_width()/2, self.B_WIDTH/2 - render2.get_height()/2 + 35))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    self.on_cleanup()
    def on_loop(self):
        self._clock.tick(self._snake._speed)
        self._snake.pohyb(self._snake._movement)
        self._snake.is_collided()

    def on_render(self):
            self._display_surf.fill((self._level.color))
            self._snake.draw(self._display_surf)
            self._level.draw(self._display_surf)
            self.render_score(self._display_surf)
            pygame.display.flip()

    def render_score(self, display):
        font = pygame.font.SysFont("Arial", 20)
        pygame.draw.line(display, (255, 255, 255), (self.B_WIDTH, 0), (self.B_WIDTH, self.B_HEIGHT))
        render = font.render("Score: {}".format(self._snake.getScore()), 1, (255, 255, 255))
        display.blit(render, (self.B_WIDTH + self.A_WIDTH/2 - render.get_width()/2, self.B_WIDTH/10 - render.get_height()/2))
        render2 = font.render("Speed: {}".format(self._snake._speed), 1, (255, 255, 255))
        display.blit(render2, (self.B_WIDTH + self.A_WIDTH/2 - render2.get_width()/2, self.B_WIDTH/10 - render2.get_height()/2 + 20))
        render3 = font.render("Level: {}".format(self._level.level), 1, (255, 255, 255))
        display.blit(render3, (self.B_WIDTH + self.A_WIDTH/2 - render3.get_width()/2, self.B_WIDTH/10 - render3.get_height()/2 + 40))

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        # had
        self._snake.init_snake()
        self._level.init_level()
        # game loop
        while self._snake._running:
            # zpracování všech typů událostí
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.game_over()

 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()