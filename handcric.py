# sample basic logic behind the  hand cricket battle game
import cv2
import time
import handdetector as htm
import random
import numpy as np

cTime = 0
pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.HandDect()
res = 0
score = 0
computer_move=0
comp_score = 0
chance = 0
moves = [0,1,2,3,4,5,6]
bat_bowl = ["Batting", "Bowling"]
while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    cv2.putText(img,f'You are {bat_bowl[chance]}!',(10,100), cv2.FONT_HERSHEY_SIMPLEX,1,
                (0,255,0),2)
    img = detector.findHands(img)
    lm_list = detector.findPosition(img)
    #if len(lm_list) != 0:
    #    print(lm_list)
    tips = [8,12,16,20]
    finger_up = []
    if len(lm_list) != 0:
        if lm_list[4][1] < lm_list[4-2][1]:
            finger_up.append(1)
        else:
            finger_up.append(0)
        for tip in tips:
            if lm_list[tip][2] < lm_list[tip-2][2]:
                finger_up.append(1)
            else:
                finger_up.append(0)
    #print(finger_up)
    if finger_up:
        t,i,m,r,p = finger_up
        if t == 1 and i == 0 and m == 0 and r == 0 and p == 0:
            res = 6
        else:
            res = finger_up.count(1)

        computer_move = random.choice(moves)
        print(f'{computer_move=}, {res=}')
        cv2.putText(img,f'You: {res} | Computer: {computer_move}',
                (10,30), cv2.FONT_HERSHEY_SIMPLEX,1,
                (255,0,255),2)
        if chance == 0:
            if res != computer_move:
                score += res
                print(score)
            else:
                print(f'{score=}')
                chance = 1
                img_black = np.zeros_like(img)
                cv2.putText(img_black,f"You are OUT!",(0,50), 
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.putText(img_black,f"Computer Needs {score} to win!",(0,80), 
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.putText(img_black,f"You are now Bowling!",
                (0,110), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.putText(img_black,f"Press any button to continue!",
                (0,140), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
                cv2.imshow("Image",img_black)
                cv2.waitKey(0)
                
        else:
            if res != computer_move:
                comp_score += computer_move
                print(comp_score)
                if comp_score > score:
                    break
            else:
                print(f'{comp_score=}')
                break


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    #cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
    #            (255,0,255),3)
    cv2.putText(img,f'Score: {score} | {comp_score}',
                (10,65), cv2.FONT_HERSHEY_SIMPLEX,1,
                (255,0,255),2)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(2)

def black_screen(flag):
    if flag == "comp":
        wins = "COMPUTER WINS"
    else:
        wins = "PLAYER WINS"
    img_black = np.zeros_like(img)
    cv2.putText(img_black,f"{wins}",
                (50,200), cv2.FONT_HERSHEY_SIMPLEX,2,
                (255,255,255),5)
    cv2.putText(img_black,f"Player Score:{score}, Computer Score:{comp_score}",
                (50,400), cv2.FONT_HERSHEY_SIMPLEX,1,
                (255,255,255),1)
    cv2.putText(img_black,f"Press any key to exit!",
                (50,430), cv2.FONT_HERSHEY_SIMPLEX,1,
                (255,255,255),1)
    cv2.imshow("Image", img_black)
    cv2.waitKey(0)

print(f'{comp_score=},{score=}')
if comp_score > score:
    black_screen("comp")
    print("COMPUTER WINS")
else:
    black_screen("player")
    print("PLAYER WINS")