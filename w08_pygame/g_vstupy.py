import pygame
from pygame.locals import *

class Bullet:
    def __init__(self, image, velocity_x, velocity_y, position_x, position_y):
        self.image = image
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.position_x = 0
        self.position_y = 0

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self.size = self.weight, self.height = 640, 400
        self._display_surf = None
        self._clock = None
        self._fps = 60
        self._star_position_x = 0
        self._star_position_y = 0
        self._star_velocity_x = 0
        self._star_velocity_y = 0
        self._bullets = []
        self._bullet_surf = None;
        self._last_key = None
 
    def on_init(self):
        # inicializace PyGame modulů
        pygame.init()   
        # nastavení velikosti okna, pokus o nastavení HW akcelerace, pokud nelze, použije se DOUBLEBUF
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._bullet_surf = pygame.image.load("../resources/missile.png").convert()
        self._running = True
        self._clock = pygame.time.Clock()
        # načtení obrázku
        self._image_surf = pygame.image.load("../resources/craft.png").convert()

    def on_loop(self):
        self._star_position_x += self._star_velocity_x
        self._star_position_y += self._star_velocity_y

        for bullet in self._bullets:
            bullet.position_x += bullet.velocity_x
            bullet.position_y += bullet.velocity_y

        self._clock.tick(self._fps)

    def on_input_focus(self):
        pass
    def on_input_blur(self):
        pass
    def on_key_down(self, event):
        print("key down...")
        print(event)
        if event.key == pygame.K_LEFT:
            self._star_velocity_x = -2
            self._last_key = pygame.K_LEFT
        if event.key == pygame.K_RIGHT:
            self._star_velocity_x = 2
            self._last_key = pygame.K_RIGHT
        if event.key == pygame.K_UP:
            self._star_velocity_y = -2
            self._last_key = pygame.K_UP
        if event.key == pygame.K_DOWN:
            self._star_velocity_y = 2
            self._last_key = pygame.K_DOWN

        if event.key == pygame.K_SPACE:
            self.spawn_bullet()


    def spawn_bullet(self):
        if self._last_key == pygame.K_LEFT:
            self._bullets.append(Bullet(self._bullet_surf, -10, 0, self._star_position_x, self._star_position_y))
        if self._last_key == pygame.K_RIGHT:
            self._bullets.append(Bullet(self._bullet_surf, 10, 0, self._star_position_x, self._star_position_y))
        if self._last_key == pygame.K_UP:
            self._bullets.append(Bullet(self._bullet_surf, 0, -10, self._star_position_x, self._star_position_y))
        if self._last_key == pygame.K_DOWN:
            self._bullets.append(Bullet(self._bullet_surf, 0, 10, self._star_position_x, self._star_position_y))

    def on_key_up(self, event):
        print("key up...")
        print(event)
        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self._star_velocity_x = 0

        if event.key in (pygame.K_UP, pygame.K_DOWN):
            self._star_velocity_y = 0
    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_mouse_move(self, event):
        pass
    def on_mouse_wheel(self, event):
        pass
    def on_lbutton_up(self, event):
        pass
    def on_lbutton_down(self, event):
        pass
    def on_rbutton_up(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_mbutton_up(self, event):
        pass
    def on_mbutton_down(self, event):
        pass
    def on_minimize(self):
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass
    def on_exit(self):
        pass
    def on_user(self,event):
        pass
    def on_joy_axis(self,event):
        pass
    def on_joybutton_up(self,event):
        pass
    def on_joybutton_down(self,event):
        pass
    def on_joy_hat(self,event):
        pass
    def on_joy_ball(self,event):
        pass
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
            #self.on_exit()
 
        elif event.type >= USEREVENT:
            self.on_user(event)
 
        elif event.type == VIDEOEXPOSE:
            self.on_expose()
 
        elif event.type == VIDEORESIZE:
            self.on_resize(event)
 
        elif event.type == KEYUP:
            self.on_key_up(event)
 
        elif event.type == KEYDOWN:
            self.on_key_down(event)
 
        elif event.type == MOUSEMOTION:
            self.on_mouse_move(event)
 
        elif event.type == MOUSEBUTTONUP:
            if event.button == 0:
                self.on_lbutton_up(event)
            elif event.button == 1:
                self.on_mbutton_up(event)
            elif event.button == 2:
                self.on_rbutton_up(event)
 
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 0:
                self.on_lbutton_down(event)
            elif event.button == 1:
                self.on_mbutton_down(event)
            elif event.button == 2:
                self.on_rbutton_down(event)
 
        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()

    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self._display_surf.blit(self._image_surf, (self._star_position_x, self._star_position_y))
        for bullet in self._bullets:
            self._display_surf.blit(bullet.image, (bullet.position_x, bullet.position_y))
        pygame.display.flip()
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        self.on_init()
        # game loop
        while( self._running ):
            # zpracování všech typů událostí
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()