from random import randrange

import pygame
from pygame.locals import *
 
class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._clock = None
        self._star_position_x = 0
        self._star_position_y = 0
        self._star_velocity_x = 5
        self._star_velocity_y = 5
        self._fps = 60
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((696, 420), pygame.HWSURFACE)
        # třída Clock slouží pro sledování času
        self._clock = pygame.time.Clock()
        self._running = True
        # načtení obrázku
        self._image_surf = pygame.image.load("../resources/suck.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        if self._star_position_x > self._display_surf.get_width() - self._image_surf.get_width():
            self._star_velocity_x *= -1
        if self._star_position_x < 0:
            self._star_velocity_x *= -1
        if self._star_position_y > self._display_surf.get_height() - self._image_surf.get_height():
            self._star_velocity_y *= -1
        if self._star_position_y < 0:
            self._star_velocity_y *= -1

        self._star_position_x += self._star_velocity_x
        self._star_position_y += self._star_velocity_y
        # čekáme, dokud od posledního volání metody tick neuběhlo 60 ms
        self._clock.tick(self._fps)
    def on_render(self):
        # smazat obrazovku
        self._display_surf.fill((0, 0, 0))
        # metoda blit vykreslí obrázek na dané pozici, lze vykreslit i než část pomocí
        # self.display_surf.blit(self._image_surf,, (0,0) , rect_containing_coordinates_to_draw)
        self._display_surf.blit(self._image_surf, (self._star_position_x, self._star_position_y))
        pygame.display.flip()
        #pygame.display.update()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()