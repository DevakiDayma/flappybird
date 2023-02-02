import random   #for generating random numbers
import sys      #sys.exit is for exit from the program
import pygame
from pygame.locals import *

# globle variable which we will use
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT * 0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='images/bird.jpg.png'
BACKGROUND='images/bg.jpg.jpeg'
PIPE='images/pipe.jpg.jpeg'

def welcomeScreen():
    "Showes welcome image to the screen"
    playreX = int(SCREENWIDTH/5)
    playrey = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messegex= int((SCREENWIDTH-GAME_SPRITES['messege'].get_width())/1.5)
    messegey= int(SCREENHEIGHT * 0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()
            # if the user press space or up key,start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playreX,playrey))
                SCREEN.blit(GAME_SPRITES['messege'],(messegex,messegey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
def mainGame():
    score=0
    playerX=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0
    #crete new pipes for blitting
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']},
    ]
    #my list of lower pipes
    lowerPipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']},
    ]

    pipeVelX=-4
    playerVelY=-9
    playerMaxVelY=10
    playerMinY=-8
    playerAccY=1

    playerFlapAccv=-8   #veloity while flapping
    playerFlapped=False#it is true only when the player is flapping

    while True:
        for event in pygame.event.get():
            if event.type==QUIT or (event.type==KEYDOWN and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playerVelY=playerFlapAccv
                    playerFlapped=True
                    GAME_SOUNDS['ice'].play()
        crashTest = isCollide(playerX,playery,upperPipes,lowerPipes)#this function will return true if function crashed
        if crashTest:
            return
        #check for score
        playerMidPos=playerX+GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos= pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
                print(f"your score is {score}")
                GAME_SOUNDS['ice'].play()


        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped=False
        playerHeight= GAME_SPRITES['player'].get_height()
        playery=playery+min(playerVelY,GROUNDY-playery-playerHeight)


        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
        # Add a new pipe when the first pipe is about cross the leftmost part of the screen
        if 0< upperPipes[0]['x']<5:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

         # if the pipe is out of the screen,remove
        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)




        #lets blit your sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(upperPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerX,playery))
        myDigits = [int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset=(SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)




def isCollide(playerX,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['ice'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['ice'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['ice'].play()
            return True

    return False
def getRandomPipe():
    """generate position of two pipes(one bottom starith and one top rotated) for blitting on screen"""
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset),int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x': pipeX,'y':-y1}, #upperpipe
        {'x':pipeX,'y':y2}  #lowerpipe

    ]
    return pipe



    




if __name__ == "__main__":
    #this will be the main point from where our game start
    pygame.init() #initialise all module of pygame module
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('flappy bird by @devakidayma')
    GAME_SPRITES['numbers']=(
        pygame.image.load('images/10.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/1.jpg.png').convert_alpha(),
        pygame.image.load('images/2.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/3.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/4.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/5.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/6.jpg.jpeg').convert_alpha(),
        pygame.image.load('images/7.jpg.png').convert_alpha(),
        pygame.image.load('images/0.jpg.png').convert_alpha(),
        pygame.image.load('images/9.jpg.jpeg').convert_alpha(),
    

    )
    GAME_SPRITES['messege']=pygame.image.load('images/messenger.jpg.jpeg').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('images/base.jpg.jpeg').convert_alpha()
    GAME_SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),pygame.image.load(PIPE).convert_alpha()
    )

    #game sounds
    GAME_SOUNDS['ice']=pygame.mixer.Sound('sound\Ice & Fire - King Canyon.mp3')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #showes the screen until press a button
        mainGame()  #this is the main game function

