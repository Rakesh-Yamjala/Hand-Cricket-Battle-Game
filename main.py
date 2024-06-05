# Importing necessary Libraries
import random,time
import sys
import cv2
import handdetector as htm
import pygame.constants as const
import pymsgbox
import numpy as np
from pygame.locals import *
import pygame
from pygame import mixer

# Initializing Pygame and setting up the background screen
pygame.init()
detector = htm.HandDect()
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('bk_gnd1.png')
background = pygame.transform.scale(background, (800, 600))
# font = pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('freesansbold.ttf', 32)

# For Background music
# mixer.music.load('ipl_stadium.wav')
# mixer.music.play(-1)

# Setting up the Icon and the name of Window
pygame.display.set_caption('Hand Cricket Battle')
icon = pygame.image.load('icon1.png')
pygame.display.set_icon(icon)

# Initializing the player_score and Computer_score to 0
player_score,comp_score,res,num = 0,0,0,0
# Chance represents the Batting or Bowling of player, default option is Batting by player
chance = 0

# Camera Setup and Working Logic of Hand cricket
def camera():
    global comp_score,res,player_score,running,chance,num
    cam = cv2.VideoCapture(0)
    while True:
        ret,frame = cam.read()
        frame = cv2.flip(frame,1)
        frame = detector.findHands(frame)
        detect_list = detector.findPosition(frame)
        tips = [8,12,16,20] # keypoints of Finger tips
        finger_up = []
        if len(detect_list) != 0:
            if detect_list[4][1] < detect_list[4-2][1]:
                finger_up.append(1)
            else:
                finger_up.append(0)
            for tip in tips:
                if detect_list[tip][2] < detect_list[tip-2][2]:
                    finger_up.append(1)
                else:
                    finger_up.append(0)
        if finger_up:
            t,i,m,r,p = finger_up
            if t == 1 and i == 0 and m == 0 and r == 0 and p == 0:
                res = 6
            else:
                res = finger_up.count(1)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame=pygame.transform.scale(frame, (300,200))
        screen.blit(frame,(100,250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break   
            elif event.type == rand:
                numbers = ['0.png','1.png','2.png','3.png','4.png','5.png','6.png']
                q = True
                while q and len(detect_list)!=0:
                    num=random.choice(range(0,7))
                    if num in range(0,7):
                        q=False
                    img = pygame.image.load(numbers[num])
                    img = pygame.transform.scale(img,(250,200))
                    screen.blit(img,(450,250))
                    pygame.display.flip()
                    pygame.display.update()
                
        pygame.display.update()

        if chance == 0:
            playerscore = font.render(f'Player Score : {player_score}',player_score,True,(255,255,255))
            if res != num and len(detect_list)!=0:
                player_score += res
                screen.blit(playerscore,(125,450))
                pygame.display.update() 
            else:
                chance = 1
                pymsgbox.alert(f'your are BOWLING now , computer target is {player_score}', '2nd Innings')   
        else:
            if res!=num and len(detect_list)!=0 and player_score>comp_score:
                compscore = font.render(f'Computer Score : {comp_score}',comp_score,True,(255,255,255))
                comp_score+=num
                screen.blit(compscore,(465,450))
                pygame.display.update()
            else:
                if player_score>comp_score:
                    pymsgbox.alert('PLAYER WON','RESULT')
                else:
                    pymsgbox.alert('COMPUTER WON','RESULT')
                time.sleep(7)
                pygame.quit()
                sys.exit()
                
        time.sleep(1.2)
 
def set_background():
    global background
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
def game_input():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        
rand = const.USEREVENT + 1
pygame.time.set_timer(rand,2000)

running = True
while running:
    set_background()
    game_input()
    camera()
    pygame.display.update()
