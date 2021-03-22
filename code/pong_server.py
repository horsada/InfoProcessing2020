import socket
import time
import pickle
import random

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(("192.168.1.10", 5050))
serversocket.listen(2)

arr = [400,400,400,400,0,0]

connection = []

ball_y_speed = 1
ball_x_speed = 1

def process_positions(array, player_1, player_2):
    global ball_y_speed, ball_x_speed


    #Moving the paddles
    if player_1[0] == True:
        array[0]-=3
    else:
        array[0] = array[0]

    if player_1[1] == True:
        array[0]+=3
    else:
        array[0] = array[0]

    if player_2[0] == True:
        array[1]-=3
    else:
        array[1] = array[1]

    if player_2[1] == True:
        array[1]+=3
    else:
        array[1] = array[1]

    #setting borders for the paddles
    if array[0]<0:
        array[0] = 0
    elif array[0] > 540:
        array[0] = 540

    if array[1]<0:
        array[1] = 0
    elif array[1] > 540:
        array[1] = 540

    #Ball moving
    array[2] += round(ball_y_speed)
    array[3] += round(ball_x_speed)

    if array[2] < 0 or array[2] > 595:
        ball_y_speed *= -1


    #Ball bouncing form the paddles
    if array[3]<20 and (array[0]<array[2] and array[0]+60>array[2]):
        ball_x_speed *= -1

    if array[3]>780 and (array[1]<array[2] and array[1]+60>array[2]):
        ball_x_speed *= -1

    #Ball scoring
    if array[3] < 5 :
        array[3] = 400
        array[2] = 300
        ball_x_speed = 1
        ball_y_speed = -1
        array[4] += 1

    if array[3] > 795 :
        array[3] = 400
        array[2] = 300
        ball_x_speed = -1
        ball_y_speed = 1
        array[5] += 1

    return array

def waiting_for_connections():
    while len(connection)<2:
        conn, addr = serversocket.accept()
        connection.append(conn)
        print(conn)
        print(connection)

def recieve_information():
    player_1_info = pickle.loads(connection[0].recv(1024))
    player_2_info = pickle.loads(connection[1].recv(1024))

    return player_1_info, player_2_info


while True:
    waiting_for_connections()

    data_arr = pickle.dumps(arr)
    print(data_arr)
    connection[0].send(data_arr)
    connection[1].send(data_arr)

    player1, player2 = recieve_information()

    arr = process_positions(arr,player1, player2)