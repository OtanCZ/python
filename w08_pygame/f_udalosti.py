import pygame
from pygame.locals import *
 
class App:
    # Statická proměnná FRAME třídy App. USEREVENT je globální proměnná z PyGame. 
    # Je celočíselná a hodnoty nad ní můžeme libovolně využívat pro svou potřebu.
    # Zde použito pro vykreslení jednotlivých framů.
    FRAME = USEREVENT + 1
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._clock = None
        self._star_position_x = 0
        self._star_position_y = 0
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((350,350), pygame.HWSURFACE)
        self._running = True
        # načtení obrázku
        self._image_surf = pygame.image.load("../resources/star.png").convert()
        pygame.time.set_timer(App.FRAME, 60)


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        if event.type == App.FRAME:
            self._star_position_x += 1
            self._star_position_y += 1

    def on_loop(self):
        pass
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
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