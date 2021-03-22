import pygame
import socket
import time
import pickle

pygame.init()

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

display_width = 800
display_height = 600

clock = pygame.time.Clock()

game_display = pygame.display.set_mode((display_width, display_height))

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("192.168.1.10", 5050))




def recieve_data():
    data = clientsocket.recv(1024)
    data = pickle.loads(data)

    return data

def draw_paddles(x,y,p):
    if p == 1:
        pygame.draw.rect(game_display, RED, [x, y, 10, 80])
    if p == 2:
        pygame.draw.rect(game_display, GREEN, [x, y, 10, 80])

def draw_ball(x,y):
    pygame.draw.circle(game_display, WHITE, [x,y], 5)

def update_screen(l_score, r_score):
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    game_display.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    game_display.blit(label2, (470, 20)) 

    pygame.display.update()

def display():
    run = False
    data = []
    key_up = False
    key_down = False

    game_display.fill(BLACK)

    while run == False:
        info = recieve_data()

        game_display.fill(BLACK)

        draw_paddles(10, info[0], 1)
        draw_paddles(display_width-20, info[1], 2)
        draw_ball(info[3], info[2])

        update_screen(info[4], info[5])

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    key_up = True
                if event.key == pygame.K_DOWN:
                    key_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    key_up = False
                if event.key == pygame.K_DOWN:
                    key_down = False

        arr = [key_up, key_down]
        data_arr = pickle.dumps(arr)
        clientsocket.send(data_arr)

display()