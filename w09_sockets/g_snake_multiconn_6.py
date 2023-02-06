# inspirace: https://zetcode.com/javagames/snake/

# Síťová verze hry snake - díky selektorům se může k serveru připojit více klientů.
# Ukol:
# - rozšiřte hrací plochu
# - do třídy Snake přidejte instanční proměnnou jména hráče (hada)
# - vytvořte pole (napravo od hrací plochy) s legendou jednotlivých hráčú
#   (had dané barvy + jméno hráče).

import pygame
from enum import Enum
from pygame.locals import *
from random import randrange
import sys
import socket
import pickle
import uuid
import selectors
import types



class Movement(Enum):
    LEFT   = 1 
    RIGHT  = 2 
    UP     = 3
    DOWN   = 4 



class Snake:
    # šířka hada
    DOT_SIZE = 10
    # délka hada při startu (počet stavebních kamenů)
    N_DOTS = 3
    # délka překážky
    N_OBSTACLE_DOTS = 3
    # max pozice jablka v libovolné ose
    APPLE_MAX_POS = 89
    OBSTACLES =[
            [[10,10], [10,11], [10,12]],
            [[24,24], [25,24], [26,24]],
            [[13,12], [13,13], [13,14], [12,13], [14,13]]
        ]

    def __init__(self, y_init, body_color, player_name = "Snake"):
        # unikátní id instance hada uuid4 <=> random 
        self._uuid = str(uuid.uuid4())
        # body = tělo hada, reprezentované seznamem bodů (n-tic) jednotlivých stavebních kamenů o šířce Snake.DOT_SIZE
        self._body = []
        # aktuální pohyb
        self._name = player_name
        self._movement = Movement.RIGHT
        self._is_apple_consumed = False
        
        self._y_init = y_init

        # had nezemřel
        self._is_alive = True

        self._body_color = body_color
        # had
        self.init_snake()
    
    @property
    def uuid(self):
        return self._uuid
    
    @property
    def is_apple_consumed(self):
        return self._is_apple_consumed

        
    def init_snake(self):
        for z in range(Snake.N_DOTS):
            self._body.append([50 - z * Snake.DOT_SIZE, self._y_init])
        #self._image_head = pygame.image.load("../resources/head.png").convert()
        #self._image_body = pygame.image.load("../resources/dot.png").convert()
        
    @property
    def movement(self):
        return self._movement

    def setMovement(self, movement):
        self._movement = movement
    
    
    def getScore(self):
        return len(self._body) - Snake.N_DOTS


class Game:
    SCORE_SCREEN_HEIGHT = 40   
    def __init__(self):
        # instance hráčú
        self.snakes = {}
        # pozice jablka
        self.apple_position = []

        # hra neskončena
        self._running = True 
        self.speed = App.INITIAL_SPEED
        self.level = 1
        
        # inicializace PyGame modulů
        pygame.init()
        # nastavení velikosti okna, pokus o nastavení HW akcelerace, pokud nelze, použije se DOUBLEBUF
        #self._snake = Snake(self, 50)
        #App.play_music(self.level)

        
    def get_bodies(self):
        bodies = []
        for snake in self.snakes.values():
            bodies += snake._body
        return bodies

    def respawn_apple(self):
        while True:
            self.apple_position = [randrange(1,Snake.APPLE_MAX_POS-1)*Snake.DOT_SIZE,
                                    randrange(int(Game.SCORE_SCREEN_HEIGHT/Snake.DOT_SIZE + 1), Snake.APPLE_MAX_POS-1)*Snake.DOT_SIZE]
            if self.apple_position not in self.get_bodies() and self.apple_position not in sum(Snake.OBSTACLES[:self.level-1],[]):
                break

class App:
    B_WIDTH  = 900
    B_HEIGHT = 900

    INITIAL_SPEED = 7
    SPEED_LEVEL_LIMIT = 10

    d_level_mid = {
        1: "../resources/tetris.mid",
        2: "../resources/mortal_kombat.mid",
        3: "../resources/popcorn.mid",
        4: "../resources/beat_it.mid",
    }
    _display_surf = pygame.display.set_mode((B_WIDTH, B_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
    _clock = pygame.time.Clock()
    _image_apple = pygame.image.load("../resources/apple.png").convert()
    _client_snake_uuidake = None
    _game = None
    _is_server_mode = False
        
    

    @staticmethod
    def init(isServer=False):
        App._is_server_mode = isServer
        pygame.font.init()
        if App._is_server_mode:
            App._game = Game()
            App._game.respawn_apple()
        else:
            pygame.mixer.init()
        

    @staticmethod
    def setGame(game):
        App._game = game
    
    @staticmethod
    def setSnake(snake):
        App._client_snake_uuid = snake.uuid
        #App._client_snake = snake
        #App._game.snakes.clear()
        App._game.snakes[snake.uuid] = snake

    @staticmethod
    def get_client_snake():
        return App._game.snakes[App._client_snake_uuid]
    @staticmethod
    def is_server_mode():
        return App._is_server_mode

    @staticmethod
    def play_music(level):
        if not App.is_server_mode():
            pygame.mixer.music.stop()
            pygame.mixer.music.load(App.d_level_mid.get(level))
            pygame.mixer.music.play()

    @staticmethod
    def snake_move(snake, movement):
        snake._is_apple_consumed = False
        head = [snake._body[0][0], snake._body[0][1]]
        if movement == Movement.LEFT:
            head[0] -= Snake.DOT_SIZE
        if movement == Movement.RIGHT:
            head[0] += Snake.DOT_SIZE
        if movement == Movement.UP:
            head[1] -= Snake.DOT_SIZE
        if movement == Movement.DOWN:
            head[1] += Snake.DOT_SIZE
        if head == App._game.apple_position:
            snake._body = [head] + snake._body
            snake._is_apple_consumed = True
        else:
            snake._body = [head] + snake._body[:-1]
    
    @staticmethod
    def is_snake_collided(snake):
        # možné body kolize sám se sebou a spoluhráči
        bodies = App._game.get_bodies()
        print(f'bodies:{bodies}, body:{snake._body[0]}')
        bodies.remove(snake._body[0])
        # S koncem obrazovky
        if (snake._body[0][0] == 0
            or snake._body[0][0] == App.B_WIDTH-Snake.DOT_SIZE
            or snake._body[0][1] == Game.SCORE_SCREEN_HEIGHT
            or snake._body[0][1] == App.B_HEIGHT-Snake.DOT_SIZE
            # sám se sebou, či s ostatními
            or snake._body[0] in bodies
            # s překážkami:
            or snake._body[0] in map(
                lambda p: [p[0] * Snake.DOT_SIZE, p[1] * Snake.DOT_SIZE], 
                sum(Snake.OBSTACLES[:App._game.level-1],[]))):
            snake._is_alive = False

    @staticmethod
    def snake_draw_obstacles(surface):
        cnt = 0
        for obstacle in Snake.OBSTACLES:
            cnt += 1
            if cnt == App._game.level:
                break
            for p in obstacle:
                pygame.draw.rect(surface, (0,0,255), pygame.Rect(
                    Snake.DOT_SIZE * p[0], Snake.DOT_SIZE * p[1], Snake.DOT_SIZE, Snake.DOT_SIZE), 3)
            
    @staticmethod
    def snake_draw(snake, surface):
        #draw apple
        surface.blit(App._image_apple, App._game.apple_position)
        #draw snake
        pygame.draw.rect(surface, (255,0,0), pygame.Rect(
                snake._body[0][0], snake._body[0][1], Snake.DOT_SIZE, Snake.DOT_SIZE))
        #draw obstacles
        App.snake_draw_obstacles(surface)
        
        for i in range(len(snake._body) - 1):
            pygame.draw.rect(surface, snake._body_color, pygame.Rect(
                snake._body[i+1][0], snake._body[i+1][1], Snake.DOT_SIZE, Snake.DOT_SIZE))
    
    @staticmethod
    def game_over():
        if not App.is_server_mode():
            pygame.mixer.music.stop()
        #pygame.font.init()
        App._display_surf.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 50)
        font2 = pygame.font.SysFont("Arial", 20)
        render = font.render("Game Over", 1, (255, 0, 0))
        render2 = font2.render("Score: {}".format(App.get_client_snake().getScore()), 1, (0, 255, 0))
        App._display_surf.blit(render, (App.B_WIDTH/2 - render.get_width()/2, App.B_WIDTH/2 - render.get_height()/2))
        App._display_surf.blit(render2, (App.B_WIDTH/2 - render2.get_width()/2, App.B_WIDTH/2 - render2.get_height()/2 + 35))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == pygame.K_SPACE:
                    App.on_cleanup()
    @staticmethod
    def draw_score_screen():
        font = pygame.font.SysFont("Arial", 25 )
        render = font.render("Score: {}".format(App.get_client_snake().getScore()), 1, (255, 0, 0))
        App._display_surf.blit(render, (20, App._game.SCORE_SCREEN_HEIGHT/2 - render.get_height()/2))
        
        render = font.render("Speed: {}".format(App._game.speed), 1, (0, 255, 0))
        App._display_surf.blit(render, (100, App._game.SCORE_SCREEN_HEIGHT/2 - render.get_height()/2))
        
        render = font.render("Level: {}".format(App._game.level), 1, (0, 0, 255))
        App._display_surf.blit(render, (200, App._game.SCORE_SCREEN_HEIGHT/2 - render.get_height()/2))
    
    #Dodělat!
    @staticmethod
    def draw_legend_screen():
        y = 20
        if(App._game):
            for snake in App._game.snakes.values():
                print(snake._name)
                y += 20
                font = pygame.font.SysFont("Arial", 20)
                render = font.render(snake._name, 1, (snake._body_color))
                App._display_surf.blit(render, (App.B_WIDTH - 100, y ))
            
    @staticmethod    
    def on_render(snake):
        #App._display_surf.fill((0, 0, 0))
        App.draw_score_screen()
        App.draw_legend_screen()
        App.snake_draw(snake, App._display_surf)
        pygame.draw.rect(App._display_surf, (255,0,0), pygame.Rect(
            0, Game.SCORE_SCREEN_HEIGHT, App.B_WIDTH, App.B_HEIGHT-Game.SCORE_SCREEN_HEIGHT), 10)
        pygame.display.flip()
    
    @staticmethod
    def on_input_focus():
        pass

    @staticmethod
    def on_key_down(snake, event):
        if event.key == pygame.K_LEFT:
            snake.setMovement(Movement.LEFT)
        if event.key == pygame.K_RIGHT:
            snake.setMovement(Movement.RIGHT)
        if event.key == pygame.K_UP:
            snake.setMovement(Movement.UP)
        if event.key == pygame.K_DOWN:
            snake.setMovement(Movement.DOWN)
        if event.key == pygame.K_q:
            snake._is_alive = False

    @staticmethod
    def on_event(snake, event):
        if event.type == QUIT:
            App._game._running = False
        elif event.type == KEYDOWN:
            App.on_key_down(snake, event)

    @staticmethod
    def on_loop(snake):
        App._clock.tick(App._game.speed)
        App.snake_move(snake, snake.movement)
        App.is_snake_collided(snake)

    @staticmethod
    def on_cleanup(self):
        pygame.quit()

    @staticmethod
    def processAi():
        snake = App.get_client_snake()
        snake._body[0]
        if snake._movement==Movement.RIGHT and (
            snake._body[0][0]==App.B_WIDTH-2*Snake.DOT_SIZE
            or
            snake._body[0][0]==App._game.apple_position[0]   
        ):
            snake._movement=Movement.DOWN
        elif snake._movement==Movement.DOWN and (
            snake._body[0][1]==App._game.apple_position[1]
            or
            snake._body[0][1]==App.B_HEIGHT-2*Snake.DOT_SIZE
        ):
            snake._movement=Movement.LEFT
        elif snake._movement==Movement.LEFT and (
            snake._body[0][0]==App._game.apple_position[0]
            or
            snake._body[0][0]==Snake.DOT_SIZE
        ):
            snake._movement=Movement.UP
        elif snake._movement==Movement.UP and (
            snake._body[0][1]==App._game.apple_position[1]
            or
            snake._body[0][1]==Game.SCORE_SCREEN_HEIGHT+Snake.DOT_SIZE
        ):
            snake._movement=Movement.RIGHT
    @staticmethod
    def on_execute():
        # game loop
        if App._game._running:
            App._display_surf.fill((0, 0, 0))
            # zpracování všech typů událostí (netýká se serveru, resp. pozorovtele - observer)
            if not App.is_server_mode():
                if len(sys.argv) > 1 and sys.argv[1] == "a":
                    App.processAi()
                else:    
                    for event in pygame.event.get():
                        App.on_event(App.get_client_snake(), event)
                App.on_loop(App.get_client_snake())
                App.on_render(App.get_client_snake())
        else:
            App.game_over()
        for snake in App._game.snakes.values():   
            print(f"processing snake: position: {snake._body[0]}, length: {len(snake._body)}")
            #print(f"processing snake: {snake.uuid}")
            if snake.is_apple_consumed:
                App._game.respawn_apple()
                App._game.speed += 0.5
                if App._game.speed >= App.SPEED_LEVEL_LIMIT:
                    App._game.level += 1
                    App.play_music(App._game.level)
                    App._game.speed = App.INITIAL_SPEED
            App.on_render(snake)

        if not App.is_server_mode() and not App.get_client_snake()._is_alive:
            App.game_over()

class Network:
    HOST_CLIENT = "192.168.5.132"  # Standard loopback interface address (localhost)
    HOST_SERVER = "0.0.0.0"
    PORT = 65434  # Port to listen on (non-privileged ports are > 1023)
    MAX_MESSAGE_LENGTH = 20000
    sel = selectors.DefaultSelector()

    @staticmethod
    def server_accept_wrapper(sock):
        conn, addr = sock.accept()  # Should be ready to read
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        outb = pickle.dumps(App._game)
        #data = types.SimpleNamespace(addr=addr, inb=b"", outb=outb, msg_total=len(outb), recv_total=0)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=outb)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        Network.sel.register(conn, events, data=data)

    @staticmethod
    def server_service_connection(key, mask):
        sock = key.fileobj
        data = key.data

        if mask & selectors.EVENT_WRITE:
            if data.outb:
                game = pickle.loads(data.outb)
                print(f"Sending {type(game)}, snakes: {game.snakes.keys()} to {data.addr}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                #TODO: finish multiple receive in client side
                data.outb = b""

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(Network.MAX_MESSAGE_LENGTH)  # Should be ready to read
            if recv_data:
                #data.inb += recv_data
                data.inb = recv_data
            # všechna data přenesena
            #else:
                print(f"received:{data.inb}")
                snake = pickle.loads(data.inb)
                App.setSnake(snake)
                if snake._is_alive:
                    pass
                else:
                    #App._game.snakes.pop(snake._uuid)
                    del App._game.snakes[snake._uuid]
                    Network.sel.unregister(sock)
                    sock.close()
                App.on_execute()
                # odstranění z monitoringu selectů
                #Network.sel.unregister(sock)
                #Network.server_register_data_to_send(sock, data.addr)
                data.outb = pickle.dumps(App._game)
                #sock.close()

    # inicializace spojení
    @staticmethod
    def client_start_connection():
        server_addr = (Network.HOST_CLIENT, Network.PORT)
        print(f"Starting connection to {server_addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # každý socket nastaven do neblokujícího módu
        sock.setblocking(False)
        # rozdíl oproti connect(addr): connect(addr) může vyhodit výjimku BlockingIOError exception,
        # connect_ex(addr) pouze může vrátit indikátor chyby errno.EINPROGRESS
        sock.connect_ex(server_addr)
        #outb = pickle.dumps(snake)
        #data = types.SimpleNamespace(addr=None, inb=b"", outb=outb, msg_total=len(outb), recv_total=0)
        data = types.SimpleNamespace(addr=None, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        Network.sel.register(sock, events, data=data)

    @staticmethod
    def client_service_connection(key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(Network.MAX_MESSAGE_LENGTH)  # Should be ready to read
            if recv_data:
                #data.recv_total += len(recv_data)
                #data.inb += recv_data
                data.inb = recv_data
                #print(f"total:{data.recv_total}, msg:{data.msg_total}, Received {recv_data!r} from server")
                
            #if not recv_data or data.recv_total == data.msg_total:
                print(f"delka prijatych dat: {len(data.inb)}")
                createSnake = True if App._game is None else False
                App.setGame(pickle.loads(data.inb))
                # v první iteraci vytvoříme hada
                if createSnake:
                    App.setSnake(Snake(60, (100,55,0), 'Lojza'))
                print(f" create:{createSnake} snakes:{App._game.snakes.keys()}")
                print(f"delka pred:{len(App.get_client_snake()._body)}")
                #pohneme s hadem
                App.on_execute()
                #pošleme hada
                print(f"delka po:{len(App.get_client_snake()._body)}")
                # odstranění z monitoringu selectů
                #sock.close()
                data.outb = pickle.dumps(App.get_client_snake())
                #Network.sel.unregister(sock)

        if mask & selectors.EVENT_WRITE:
            #if not data.outb and data.messages:
            #    data.outb = data.messages.pop(0)
            if data.outb:
                print(f"Sending {data.outb!r} to server.")
                sent = sock.send(data.outb)  # Should be ready to write
                #data.outb = data.outb[sent:]
                data.outb = b""

if __name__ == "__main__" :
    #server
    if len(sys.argv) > 1 and sys.argv[1] == "s":
        App.init(True)
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((Network.HOST_SERVER, Network.PORT))
        lsock.listen()
        print(f"Listening on {(Network.HOST_SERVER, Network.PORT)}")
        lsock.setblocking(False)
        Network.sel.register(lsock, selectors.EVENT_READ, data=None)
        try:
            while True:
                #blokující operace, pro každý socket vrací danou n-tici
                events = Network.sel.select(timeout=None)
                for key, mask in events:
                    # je událost od naslouchajícího socketu?
                    if key.data is None:
                        Network.server_accept_wrapper(key.fileobj)
                    # socket již byl akceptován
                    else:
                        Network.server_service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            Network.sel.close()
    else:
        App.init()
        Network.client_start_connection()
        try:
            while True:
                events = Network.sel.select(timeout=10)
                if events:
                    for key, mask in events:
                        Network.client_service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not Network.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            Network.sel.close()