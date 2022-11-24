import pygame
from pygame.locals import *

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((350,350), pygame.HWSURFACE)
        self._running = True
        # načtení obrázku
        self._image_surf = pygame.image.load("../resources/star.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        # metoda blit vykreslí do paměti obrázek na dané pozici, lze vykreslit i než část pomocí
        # self.display_surf.blit(self._image_surf,, (0,0) , rect_containing_coordinates_to_draw)
        self._display_surf.blit(self._image_surf,(0,0))
        color = (255,0,0)
        # vykreslení plného obdelníku červenou barvou
        pygame.draw.rect(self._display_surf, color, pygame.Rect(40, 40, 50, 50))
        # vykreslení obdelníku červenou barvou čárou tloušťky 10
        pygame.draw.rect(self._display_surf, color, pygame.Rect(100, 40, 50, 50), 10)
        # vykreslení trojúhelníku
        pygame.draw.polygon(self._display_surf, color, [[150, 150], [50, 250], [250, 250]], 1)

        # Metoda flip zobrazí obrázek z paměti na obrazovku
        pygame.display.flip()

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