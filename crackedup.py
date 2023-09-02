##################################################################
# Imports                                                        #
##################################################################
from cmu_112_graphics_openCV import *
from crackedupclasses import *
import mediapipe as mp
import numpy as np
import math
import random


##################################################################
# App Started                                                    #
##################################################################


def appStarted(app):
    app.mode = "homeScreen" #start at the Home Screen mode when the app starts


##################################################################
# Home Screen Mode                                               #
##################################################################


def homeScreen_keyPressed(app, event):
    #if the Q key is pressed
    if event.key == "q":
        #switch to run game mode 1
        app.mode = "homeScreen1"
        gameMode1_appStarted(app)
    #if the W key is pressed
    elif event.key == "w":
        #switch to run game mode 2
        app.mode = "homeScreen2"
        gameMode2_appStarted(app)
    #if the E key is pressed
    elif event.key == "e":
        #switch to run game mode 3
        app.mode = "homeScreen3"
        gameMode3_appStarted(app)

def homeScreen_redrawAll(app, canvas):
    #creates Welcome text
    canvas.create_text(app.width/2, 0, text="Welcome to Cracked Up!", font="Helvetica 36",
                       anchor="n")
    #creates instructions to play which game mode
    canvas.create_text(app.width/2, app.height*3/10, text="press 'q' for for game mode 1",
                       font="Helvetica 20")
    canvas.create_text(app.width/2, app.height*5/10, text="press 'w' for for game mode 2",
                       font="Helvetica 20")
    canvas.create_text(app.width/2, app.height*7/10, text="press 'e' for for game mode 3",
                       font="Helvetica 20")


##################################################################
# Game Mode 1 Home Screen                                        #
##################################################################


def homeScreen1_appStarted(app):
    app.key = ""

def homeScreen1_keyPressed(app, event):
    #if the L key is pressed
    if event.key == "l":
        app.key = event.key
        app.mode = "gameMode1"
        gameMode1_appStarted(app) #run game mode 1
    #if the F key is pressed
    elif event.key == "f":
        app.key = event.key
        app.mode = "gameMode1" #run game mode 1
        gameMode1_appStarted(app)
    #if the H key is pressed
    elif event.key == "h":
        app.mode = "homeScreen" #go back to the home screen

def homeScreen1_redrawAll(app, canvas):
    #creates game mode label
    canvas.create_text(app.width/2, 0, text="Game Mode: Dodge", font="Helvetica 30",
                       anchor="n")
    #instructions for how to play game mode 1
    canvas.create_text(app.width/2, app.height/2, text="Dodge the incoming obstacles until it reaches the black line to gain points!\n" +
                       "If the ball hits an obstacle, you lose a life.\nThe game ends when you have 0 lives left.",
                       font="Helvetica 20")
    #opencv ball control options
    canvas.create_text(app.width/2, app.height*2/3, text="Press 'l' to play and control the ball with light.\n" +
                       "Press 'f' to play and control the ball with your finger.",
                       font="Helvetica 18", anchor="s")


##################################################################
# Game Mode 1 (Dodge) Mode                                       #
##################################################################


def gameMode1_appStarted(app):
    app.obStartHeight = 5/12
    #creates ball object for user to control
    app.ball = Ball(app.width/2, app.height/2, 20)
    #creates 3 obstacles (one blue, one purple, one green)
    app.obs1 = [Obstacle(app.width/2, app.height*app.obStartHeight-10, 
                       app.width/2, app.height*app.obStartHeight-10, 10, 10, "blue", "rect"),
                Obstacle(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 8, 8, "purple", "rect"),
                Obstacle(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 12, 12, "green", "circle")]
    newObstacle1(app)
    newSecObstacle1(app)
    app.lives = 5
    app.score1 = 0
    app.inside = False
    app.gameOver = False

def newObstacle1(app):
    #chooses random obstacle from list of obsatcle "designs"
    randomIndex = random.randint(0, len(app.obs1)-1)
    app.ob1 = app.obs1[randomIndex]

    #iniates random obstacle starting position on the path
    app.ob1.cx = app.ob1.initialX+random.randrange(-90,90)
    app.ob1.cy = app.ob1.initialY
    app.ob1.insideCounter = 0

def newSecObstacle1(app):
    #chooses random obstacle from list of obsatcle "designs"
    randomIndex2 = random.randint(0, len(app.obs1)-1)
    app.obc1 = app.obs1[randomIndex2]

    #iniates random obstacle starting position on the path
    app.obc1.cx = app.obc1.initialX+random.randrange(-90,90)
    app.obc1.cy = app.obc1.initialY
    app.obc1.insideCounter = 0



def gameMode1_cameraFired(app):
    app.frame = cv2.flip(app.frame, 1) #flips camera for easier user experience

    #if F key was pressed, use finger detection
    if app.key == "f":
        #heavily referenced from: https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils
        
        app.frame = cv2.resize(app.frame, None, None, fx=0.5, fy=0.5)
        imgRGB = cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = app.frame.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    if id == 8: #8 is the id for the tip of pointer finger
                        app.ball.cx = cx
                        app.ball.cy = cy
                        cv2.circle(app.frame, (cx,cy), 3, (255,0,255), cv2.FILLED)

    #if L key was pressed, used light detection (brightest spot on screen)
    elif app.key == "l":
        #get data from sub window on screen
        app.frame = cv2.resize(app.frame, None, None, fx=0.75, fy=0.75)
        # cv2.rectangle(app.frame, (400,100), (1200,700), (0,255,0), 0)
        # crop_img = app.frame[100:700, 400:1200]

        grey = cv2.cvtColor(app.frame, cv2.COLOR_BGR2GRAY) #converts to grayscale

        #collaboration with Ethan Huang
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey) #finds brightest point on screen
        
        #sets ball coordinates to coordinates of brightest point
        app.ball.cx = maxLoc[0]
        app.ball.cy = maxLoc[1]

    cv2.imshow("Camera", app.frame) #displays camera windows


'''
def gameMode1_mouseMoved(app, event):
    app.ball.cx = event.x
    app.ball.cy = event.y

'''

def gameMode1_keyPressed(app, event):
    #if R key is pressed
    if event.key == "r":
        gameMode1_appStarted(app) #rerun game mode 1
    #if H key is pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

#calculates the distance between 2 points
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5 #distance formula

def gameMode1_drawNewObstacle(app, canvas):
    #if the obstacle is a rectangle type, draw as rectangle
    if app.ob1.shape == "rect":
        canvas.create_rectangle(app.ob1.cx-app.ob1.r, app.ob1.cy-app.ob1.r,
                                app.ob1.cx+app.ob1.r, app.ob1.cy+app.ob1.r,
                                fill=app.ob1.color)
    #if the obstacle is a circle type, draw as circle
    elif app.ob1.shape == "circle":
        canvas.create_oval(app.ob1.cx-app.ob1.r, app.ob1.cy-app.ob1.r,
                                app.ob1.cx+app.ob1.r, app.ob1.cy+app.ob1.r,
                                fill=app.ob1.color)

def gameMode1_drawNewSecObstacle(app, canvas):
    #if the obstacle is a rectangle type, draw as rectangle
    if app.obc1.shape == "rect":
        canvas.create_rectangle(app.obc1.cx-app.obc1.r, app.obc1.cy-app.obc1.r,
                                app.obc1.cx+app.obc1.r, app.obc1.cy+app.obc1.r,
                                fill=app.obc1.color)
    #if the obstacle is a circle type, draw as circle
    elif app.obc1.shape == "circle":
        canvas.create_oval(app.obc1.cx-app.obc1.r, app.obc1.cy-app.obc1.r,
                                app.obc1.cx+app.obc1.r, app.obc1.cy+app.obc1.r,
                                fill=app.obc1.color)

def gameMode1_timerFired(app):
    #if the obstacle passes the black line
    if app.ob1.cy+app.ob1.r >= app.height-100:
        #set obstacle r, cx, and cy back to initial values
        app.ob1.r = app.ob1.initialR
        app.ob1.cx = app.ob1.initialX
        app.ob1.cy = app.ob1.initialY
        #if obstacle did not get hit, increase score
        if (app.ob1.insideCounter == 0):
            app.score1 += 10
        #spawn in new obstacle
        newObstacle1(app)
    
    #otherwise, increase obsatcle radius and y position
    else:
        app.ob1.r += 0.5
        app.ob1.cy += 1

        #if the obstacle gets hit
        if distance(app.ball.cx, app.ball.cy, app.ob1.cx, app.ob1.cy) <= app.ob1.r:
            #if the obstacle was hit once 
            if not app.inside and app.ob1.insideCounter < 1:
                app.lives -= 1 #player loses a life
                app.ob1.insideCounter += 1
                app.inside = True
                #if player has no lives left, switch to game over screen
                if app.lives <= 0:
                    app.mode = "gameOver1"
        else:
            app.inside = False

    #if the obstacle passes the black line
    if app.obc1.cy+app.obc1.r >= app.height-100:
        #set obstacle r, cx, and cy back to initial values
        app.obc1.r = app.obc1.initialR
        app.obc1.cx = app.obc1.initialX
        app.obc1.cy = app.obc1.initialY
        #if obstacle did not get hit, increase score
        if (app.obc1.insideCounter == 0):
            app.score1 += 10
         #spawn in new obstacle
        newSecObstacle1(app)
    
    #otherwise, increase obsatcle radius and y position
    else:
        app.obc1.r += 0.5
        app.obc1.cy += 1

        #if the obstacle gets hit
        if distance(app.ball.cx, app.ball.cy, app.obc1.cx, app.obc1.cy) <= app.obc1.r:
            #if the obstacle was hit once 
            if not app.inside and app.obc1.insideCounter < 1:
                app.lives -= 1 #player loses a life
                app.obc1.insideCounter += 1
                app.inside = True
                #if player has no lives left, switch to game over screen
                if app.lives <= 0:
                    app.mode = "gameOver1"
        else:
            app.inside = False
     
def gameMode1_redrawAll(app, canvas):
    #displays number of lives left
    canvas.create_text(app.width/2, 0, text=f"{app.lives} lives left", 
                        anchor="n")
    #displays current score
    canvas.create_text(app.width/2, 20, text=f"score: {app.score1}", 
                        anchor="n")
    #displays middle path
    canvas.create_polygon(app.width/2-100, app.height*app.obStartHeight, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, app.width, app.height,
                          0, app.height, 0, app.height-100, fill="lightblue")
    #displays left wall
    canvas.create_polygon(0, 0, app.width/2-100, 0, app.width/2-100, app.height*app.obStartHeight,
                          0, app.height-100, fill="darkgrey")
    #displays right wall
    canvas.create_polygon(app.width, 0, app.width/2+100, 0, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, fill="darkgrey")
    #displays black line
    canvas.create_line(0, app.height-100, app.width, app.height-100, width=2)
    #draws first obstacle
    gameMode1_drawNewSecObstacle(app, canvas)
    #draws second obstacle
    gameMode1_drawNewObstacle(app, canvas)
    #draws ball
    canvas.create_oval(app.ball.cx-app.ball.r, app.ball.cy-app.ball.r,
                       app.ball.cx+app.ball.r, app.ball.cy+app.ball.r,
                       fill="grey")


##################################################################
# Game Mode 2 Home Screen                                        #
##################################################################


def homeScreen2_appStarted(app):
    app.key = ""

def homeScreen2_keyPressed(app, event):
    #if the L key is pressed
    if event.key == "l":
        app.key = event.key
        app.mode = "gameMode2" 
        gameMode2_appStarted(app) #run game mode 2
    #if the F key is pressed
    elif event.key == "f":
        app.key = event.key
        app.mode = "gameMode2" #fun game mode 2
        gameMode2_appStarted(app)
    #if the H key is pressed
    elif event.key == "h":
        app.mode = "homeScreen" #go back to home screen

def homeScreen2_redrawAll(app, canvas):
    #creates game mode label
    canvas.create_text(app.width/2, 0, text="Game Mode: Break", font="Helvetica 30",
                       anchor="n")
    #instructions for how to play
    canvas.create_text(app.width/2, app.height/2, text="Break the incoming obstacles before it reaches the black line to gain points!\n" +
                       "If you fail to break an obstacle, the game ends.",
                       font="Helvetica 20")
    #opencv ball control options
    canvas.create_text(app.width/2, app.height*2/3, text="Press 'l' to play and control the ball with light.\n" +
                       "Press 'f' to play and control the ball with your finger.",
                       font="Helvetica 18", anchor="s")


##################################################################
# Game Mode 2 (Break) Mode                                       #
##################################################################


def gameMode2_appStarted(app):
    app.obStartHeight = 5/12
    #creates ball object for user control
    app.ball = Ball(app.width/2, app.height/2, 20)
    #creates 3 obstacles (one blue, one purple, one green)
    app.obs2 = [Breakable(app.width/2, app.height*app.obStartHeight-10, 
                       app.width/2, app.height*app.obStartHeight-10, 10, 10, "blue", "blue", "circle"),
               Breakable(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 8, 8, "purple", "purple", "rect"),
               Breakable(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 12, 12, "green", "green", "rect")]
    newObstacle2(app)
    app.score2 = 0
    app.inside = False
    app.cracked2 = False
    app.gameOver = False

def newObstacle2(app):
    #chooses random obstacle from list of obsatcle "designs"
    randomIndex = random.randint(0, len(app.obs2)-1)
    app.ob2 = app.obs2[randomIndex]

    #iniates random obstacle starting position on the path
    app.ob2.cx = app.ob2.initialX+random.randrange(-90,90)
    app.ob2.cy = app.ob2.initialY
    app.ob2.insideCounter = 0


def gameMode2_cameraFired(app):
    app.frame = cv2.flip(app.frame, 1) #flips camera for easier user experience

    #if F key was pressed, use finger detection
    if app.key == "f":
        #heavily referenced from: https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils
        
        app.frame = cv2.resize(app.frame, None, None, fx=0.5, fy=0.5)
        imgRGB = cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = app.frame.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    if id == 8: #8 is the id for the tip of pointer finger
                        app.ball.cx = cx
                        app.ball.cy = cy
                        cv2.circle(app.frame, (cx,cy), 3, (255,0,255), cv2.FILLED)

    #if L key was pressed, used light detection (brightest spot on screen)
    elif app.key == "l":
        #get data from sub window on screen
        app.frame = cv2.resize(app.frame, None, None, fx=0.75, fy=0.75)

        grey = cv2.cvtColor(app.frame, cv2.COLOR_BGR2GRAY) #converts to grayscale

        #collaboration with Ethan Huang
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey) #finds brightest point on screen
        
        #sets ball coordinates to coordinates of brightest point
        app.ball.cx = maxLoc[0]
        app.ball.cy = maxLoc[1]

    cv2.imshow("Camera", app.frame) #show camera window
  
'''

def gameMode2_mouseMoved(app, event):
    app.ball.cx = event.x
    app.ball.cy = event.y

'''

def gameMode2_keyPressed(app, event):
    #if R key was pressed
    if event.key == "r":
        gameMode2_appStarted(app) #rerun gamemode 2
    #if H key was pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def gameMode2_drawNewObstacle(app, canvas):
    #if obstacle is rectangle type, draw rectangle
    if app.ob2.shape == "rect":
        canvas.create_rectangle(app.ob2.cx-app.ob2.r, app.ob2.cy-app.ob2.r,
                                app.ob2.cx+app.ob2.r, app.ob2.cy+app.ob2.r,
                                fill=app.ob2.color)
    #if obstacle is circle type, draw circle
    elif app.ob2.shape == "circle":
        canvas.create_oval(app.ob2.cx-app.ob2.r, app.ob2.cy-app.ob2.r,
                                app.ob2.cx+app.ob2.r, app.ob2.cy+app.ob2.r,
                                fill=app.ob2.color)

def gameMode2_timerFired(app):
    #if obstacle reaches black line
    if app.ob2.cy+app.ob2.r >= app.height-100:
        #if obstacle did not "break", game is over
        if app.ob2.color == app.ob2.initialC:
            app.mode="gameOver2"
        #set obstacle r, cx, cy, and color back to initial values
        app.ob2.reset() 
        #spawn in new obstacle
        newObstacle2(app)
    
    #otherwise, increase obsatcle radius and y position
    else:
        app.ob2.r += 0.5
        app.ob2.cy += 1
    
        #if the obstacle gets "hit"
        if distance(app.ball.cx, app.ball.cy, app.ob2.cx, app.ob2.cy) <= app.ob2.r:
            #if the obstacle was hit once
            if not app.inside and app.ob2.insideCounter < 1:
                app.cracked2 = True
                app.score2 += 1 #increase player's score
                app.ob2.insideCounter += 1
                app.inside = True
        else:
            app.inside = False
            app.cracked2 = False

def gameMode2_redrawAll(app, canvas):
    #displays player's score
    canvas.create_text(app.width/2, 0, text=f"score: {app.score2}", 
                        anchor="n")
    #draws middle path
    canvas.create_polygon(app.width/2-100, app.height*app.obStartHeight, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, app.width, app.height,
                          0, app.height, 0, app.height-100, fill="lightblue")
    #draws left wall
    canvas.create_polygon(0, 0, app.width/2-100, 0, app.width/2-100, app.height*app.obStartHeight,
                          0, app.height-100, fill="darkgrey")
    #draws right wall
    canvas.create_polygon(app.width, 0, app.width/2+100, 0, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, fill="darkgrey")
    #draws black line
    canvas.create_line(0, app.height-100, app.width, app.height-100, width=2)
    #draws obstacle
    gameMode2_drawNewObstacle(app, canvas)
    #if the obstacle gets hit, turn color to transparent
    if app.cracked2:
        app.ob2.color = ""
        #canvas.create_oval()
    #draws ball for player control
    canvas.create_oval(app.ball.cx-app.ball.r, app.ball.cy-app.ball.r,
                       app.ball.cx+app.ball.r, app.ball.cy+app.ball.r,
                       fill="grey")


##################################################################
# Game Mode 3 Home Screen                                        #
##################################################################


def homeScreen3_appStarted(app):
    app.key = ""

def homeScreen3_keyPressed(app, event):
    #if L key pressed
    if event.key == "l":
        app.key = event.key
        app.mode = "gameMode3"
        gameMode3_appStarted(app) #run game mode 3
    #if F key pressed
    elif event.key == "f":
        app.key = event.key
        app.mode = "gameMode3" #run game mode 3
        gameMode3_appStarted(app)
    #if H key pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def homeScreen3_redrawAll(app, canvas):
    #creates game mode label
    canvas.create_text(app.width/2, 0, text="Game Mode: Combo", font="Helvetica 30",
                       anchor="n")
     #instructions for how to play
    canvas.create_text(app.width/2, app.height/2, text="Break the incoming circles before it reaches the black line to gain points!\n" +
                       "If you fail to dodge a square, you lose a life.\nIf you fail to break an obstacle, the game ends.",
                       font="Helvetica 20")
    #opencv ball control options
    canvas.create_text(app.width/2, app.height*2/3, text="Press 'l' to play and control the ball with light.\n" +
                       "Press 'f' to play and control the ball with your finger.",
                       font="Helvetica 18", anchor="s")


##################################################################
# Game Mode 3 (Comb) Mode                                        #
##################################################################


def gameMode3_appStarted(app):
    app.obStartHeight = 5/12
    #creates ball object for user control
    app.ball = Ball(app.width/2, app.height/2, 20)
    #creates 3 obstacles (one blue, one purple, one green)
    app.obs3 = [Breakable(app.width/2, app.height*app.obStartHeight-10, 
                       app.width/2, app.height*app.obStartHeight-10, 10, 10, "blue", "blue", "circle"),
               Breakable(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 8, 8, "purple", "purple", "rect"),
               Breakable(app.width/2, app.height*app.obStartHeight-10,
                       app.width/2, app.height*app.obStartHeight-10, 12, 12, "green", "green", "rect")]
    newObstacle3(app)
    app.score3 = 0
    app.lives3 = 3
    app.inside = False
    app.cracked3 = False
    app.gameOver = False

def newObstacle3(app):
    #chooses random obstacle from list of obsatcle "designs"
    randomIndex = random.randint(0, len(app.obs3)-1)
    app.ob3 = app.obs3[randomIndex]

    #iniates random obstacle starting position on the path
    app.ob3.cx = app.ob3.initialX+random.randrange(-90,90)
    app.ob3.cy = app.ob3.initialY
    app.ob3.insideCounter = 0


def gameMode3_cameraFired(app):
    app.frame = cv2.flip(app.frame, 1) #flips camera for easier user experience

    #if F key was pressed, use finger detection
    if app.key == "f":
        #heavily referenced from: https://www.analyticsvidhya.com/blog/2021/07/building-a-hand-tracking-system-using-opencv/
        mpHands = mp.solutions.hands
        hands = mpHands.Hands(static_image_mode=False,
                            max_num_hands=2,
                            min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)
        mpDraw = mp.solutions.drawing_utils
        
        app.frame = cv2.resize(app.frame, None, None, fx=0.5, fy=0.5)
        imgRGB = cv2.cvtColor(app.frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = app.frame.shape
                    cx, cy = int(lm.x *w), int(lm.y*h)
                    if id == 8: #8 is the id for the tip of pointer finger
                        app.ball.cx = cx
                        app.ball.cy = cy
                        cv2.circle(app.frame, (cx,cy), 3, (255,0,255), cv2.FILLED)

    #if L key was pressed, used light detection (brightest spot on screen)
    elif app.key == "l":
        #get data from sub window on screen
        app.frame = cv2.resize(app.frame, None, None, fx=0.75, fy=0.75)

        grey = cv2.cvtColor(app.frame, cv2.COLOR_BGR2GRAY) #converts to grayscale

        #collaboration with Ethan Huang
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(grey) #finds brightest point on screen
        
        #sets ball coordinates to coordinates of brightest point
        app.ball.cx = maxLoc[0]
        app.ball.cy = maxLoc[1]

    cv2.imshow("Camera", app.frame) #show camera window

''' 

def gameMode3_mouseMoved(app, event):
    app.ball.cx = event.x
    app.ball.cy = event.y

''' 

def gameMode3_keyPressed(app, event):
    #if R key pressed
    if event.key == "r":
        gameMode3_appStarted(app) #rerun game mode 3
    #if H key pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def gameMode3_drawNewObstacle(app, canvas):
    #if obstacle is rectangle type, draw rectangle
    if app.ob3.shape == "rect":
        canvas.create_rectangle(app.ob3.cx-app.ob3.r, app.ob3.cy-app.ob3.r,
                                app.ob3.cx+app.ob3.r, app.ob3.cy+app.ob3.r,
                                fill=app.ob3.color)
    #if obstacle is circle type, draw circle
    elif app.ob3.shape == "circle":
        canvas.create_oval(app.ob3.cx-app.ob3.r, app.ob3.cy-app.ob3.r,
                                app.ob3.cx+app.ob3.r, app.ob3.cy+app.ob3.r,
                                fill=app.ob3.color)

def gameMode3_timerFired(app):
    #if obstacle reaches black line
    if app.ob3.cy+app.ob3.r >= app.height-100:
        #if obstacle is circle type
        if app.ob3.shape == "circle":
            #if obstacle did not "break", game is over
            if app.ob3.color == app.ob3.initialC:
                app.mode="gameOver3"
        #set obstacle r, cx, cy, and color back to initial values
        app.ob3.reset()
        #spawn in new obstacle
        newObstacle3(app)
    
    #otherwise, increase obsatcle radius and y position
    else:
        app.ob3.r += 0.5
        app.ob3.cy += 1
    
        #if the obstacle gets "hit"
        if distance(app.ball.cx, app.ball.cy, app.ob3.cx, app.ob3.cy) <= app.ob3.r:
            #if the obstacle was hit once
            if not app.inside and app.ob3.insideCounter < 1:
                #if the obstacle is a circle type
                if app.ob3.shape == "circle":
                    app.cracked3 = True
                    app.score3 += 10 #increment player score
                #if the obstacle is a rectangle type
                elif app.ob3.shape == "rect":
                    app.lives3 -= 1 #player loses life
                
                app.ob3.insideCounter += 1
                app.inside = True
                #if player has no lives left
                if app.lives3 <= 0:
                    app.mode = "gameOver3" #game over
                
        else:
            app.inside = False
            app.cracked3 = False

def gameMode3_redrawAll(app, canvas):
    #displays player's remaining lives
    canvas.create_text(app.width/2, 0, text=f"{app.lives3} lives left", 
                        anchor="n")
    #displays player's score
    canvas.create_text(app.width/2, 20, text=f"score: {app.score3}", 
                        anchor="n")
    #draws middle path
    canvas.create_polygon(app.width/2-100, app.height*app.obStartHeight, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, app.width, app.height,
                          0, app.height, 0, app.height-100, fill="lightblue")
    #draws left wall
    canvas.create_polygon(0, 0, app.width/2-100, 0, app.width/2-100, app.height*app.obStartHeight,
                          0, app.height-100, fill="darkgrey")
    #draws right wall
    canvas.create_polygon(app.width, 0, app.width/2+100, 0, app.width/2+100, app.height*app.obStartHeight,
                          app.width, app.height-100, fill="darkgrey")
    #draws black line
    canvas.create_line(0, app.height-100, app.width, app.height-100, width=2)
    #draws obstacle
    gameMode3_drawNewObstacle(app, canvas)
    #if the (circle) obstacle gets hit, turn color to transparent
    if app.cracked3:
        app.ob3.color = ""
    #draws ball
    canvas.create_oval(app.ball.cx-app.ball.r, app.ball.cy-app.ball.r,
                       app.ball.cx+app.ball.r, app.ball.cy+app.ball.r,
                       fill="grey")


##################################################################
# Game Over Modes                                                #
##################################################################


def gameOver1_keyPressed(app, event):
    #if R key pressed
    if event.key == "r":
        app.mode = "gameMode1"
        gameMode1_appStarted(app) #rerun game mode 1
    #if H key pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def gameOver1_redrawAll(app, canvas):
    #display game over text
    canvas.create_text(app.width/2, 0, text="Game Over", font="Helvetica 36",
                            fill="red", anchor="n")
    #display final player score
    canvas.create_text(app.width/2, 60, text=f"Final score: {app.score1}", font="Helvetica 25",
                           fill="green")
    #display next options
    canvas.create_text(app.width/2, app.height*3/8, text="press 'r' to restart",
                           font="Helvetica 20")
    canvas.create_text(app.width/2, app.height*5/8, text="press 'h' to go to home screen",
                           font="Helvetica 20")

def gameOver2_keyPressed(app, event):
    #if R key pressed
    if event.key == "r":
       app.mode = "gameMode2"
       gameMode2_appStarted(app) #rerun game mode 2
    #if H key pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def gameOver2_redrawAll(app, canvas):
    #display game over text
    canvas.create_text(app.width/2, 0, text="Game Over", font="Helvetica 36",
                            fill="red", anchor="n")
    #display final player score
    canvas.create_text(app.width/2, 60, text=f"Final score: {app.score2}", font="Helvetica 25",
                           fill="green")
    #display next options
    canvas.create_text(app.width/2, app.height*3/8, text="press 'r' to restart",
                           font="Helvetica 20")
    canvas.create_text(app.width/2, app.height*5/8, text="press 'h' to go to home screen",
                           font="Helvetica 20")

def gameOver3_keyPressed(app, event):
    #if R key pressed
    if event.key == "r":
        app.mode = "gameMode3"
        gameMode3_appStarted(app) #rerun game mode 3
    #if H key pressed
    elif event.key == "h":
        app.mode = "homeScreen" #return to home screen

def gameOver3_redrawAll(app, canvas):
    #display game over text
    canvas.create_text(app.width/2, 0, text="Game Over", font="Helvetica 36",
                            fill="red", anchor="n")
    #display final player score
    canvas.create_text(app.width/2, 60, text=f"Final score: {app.score3}", font="Helvetica 25",
                           fill="green")
    #display next options
    canvas.create_text(app.width/2, app.height*3/8, text="press 'r' to restart",
                           font="Helvetica 20")
    canvas.create_text(app.width/2, app.height*5/8, text="press 'h' to go to home screen",
                           font="Helvetica 20")


##################################################################
# Run Game                                                       #
##################################################################

def crackedAnimation():
    runApp(width=800, height=600)

crackedAnimation()
