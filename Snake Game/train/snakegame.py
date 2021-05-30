# Import Libraries
import pygame
import time
import random
import pandas as pd
from os import path

# Const Variable
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
SNAKESIZE = [10,10]

class Snake():
    def __init__(self,screenSize):
        self.headColor = RED
        self.bodyColor = GREEN
        self.size = [10,10]
        self.headfile = ""
        self.bodyfile = ""
        self.length = 1
        self.screenSize = screenSize
        self.position = [[screenSize[0]/2,screenSize[1]/2]]
        self.prePosition = self.position
        

    def predictPosition(self,direct): # Predict Move of Snake. Use later
        change_position = [0,0]
        temp = self.position[:]
        predict = temp[:]
        if direct == "left" :
            change_position[0] = -self.size [0]
        elif direct == "right":
            change_position[0] = self.size [0]
        elif direct == "up":
            change_position[1] = -self.size [1]
        elif direct == "down" :
            change_position[1] = self.size [1]
        
        if change_position != [0,0]: 
            predict[0] = [sum(x) for x in zip(temp[0], change_position)]
            predict[1:] = temp[:-1]
        return predict[:]

    def predictLoseMove(self,direct):
        isLose = False
        position = self.predictPosition(direct)[:]
        if position[0][0] >= self.screenSize[0] or position[0][0] < 0 or position[0][1] >= self.screenSize[1] or position[0][1] < 0:
            isLose = True
        elif (position[0]) in (position[1:]):
                    isLose = True
        return isLose
    
    def updatePosition(self,direct):
        predict = self.predictPosition(direct)
        self.prePosition = self.position[:]
        self.position = predict[:]

    def updateLengthSnake(self,foodPosition):
        head = [foodPosition[:]]
        body = self.prePosition
        head.extend(body)
        self.position = head[:]
        self.length = len(self.position)        

class Food():
    def __init__(self,screenSize,sizePlayable):
        self.color = WHITE
        self.size = [10,10]
        self.sizePlayable = sizePlayable
        self.screenSize = screenSize
        self.addFood()
    
    def addFood(self):
        foodx = round(random.randrange(self.sizePlayable[0], self.screenSize[0] - self.size [0]) / 10.0) * 10.0
        foody = round(random.randrange(self.sizePlayable[1], self.screenSize[1] - self.size [1]) / 10.0) * 10.0
        self.position = [foodx, foody]

class FileSave():
    def __init__(self,fileName):
        self.fileName = fileName
        self.highestScore = 0
        if path.exists(self.fileName) :
            with open(self.fileName,'r') as f:
                try :
                    df = pd.read_csv(f, usecols= ['Score'])
                    lst = df.values.tolist()
                    self.highestScore = max(lst)[0]
                except:
                    print("No column")
                f.close()

    def saveFileData(self,score):
        #df = pd.DataFrame([[list_direction,list_food,score]], columns = ['Direction', 'Food Position', 'Score'])
        df = pd.DataFrame([[score]], columns = ['Score'])
        if not path.exists(self.fileName) :
            with open(self.fileName,'w', newline='') as f:
                df.to_csv(f, index=False, encoding='utf-8',header=True)
                f.close()
        else:
            with open(self.fileName, 'a+', newline='') as f:
                df.to_csv(f, index=False, encoding='utf-8', mode='a',header=False)
                f.close()

class Enviroment():
    def __init__(self,scale):
        # Screen
        self.screenColor = BLACK
        self.screenScale = scale
        self.screenSize = (SNAKESIZE[0]*self.screenScale[0],SNAKESIZE[1]*self.screenScale[1])
        self.screenFps = 60
        self.caption = 'Snake game by TXDien'
        self.fontSizeScore = round(self.screenSize[0]/15)
        self.fontSize =  round(self.screenSize[0]/13)

        # Initalizing Screen for Game
        pygame.init()
        self.display = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption(self.caption)
        self.fontStyle = pygame.font.SysFont("bahnschrift", self.fontSize)
        self.fontStyleScore = pygame.font.SysFont("comicsansms", self.fontSizeScore )
        value = self.fontStyleScore .render("Your Score: " + str(0), True, YELLOW)
        self.sizePlayable = [value.get_width(),value.get_height()]
        self.clock = pygame.time.Clock()

        # Load from file
        self.fileName = FileSave('result.csv')
        # Setting new game
        self.reset()

    def direction(self,keyPressed):
        direct = ""
        if keyPressed == pygame.K_LEFT:
            direct = "left"
        elif keyPressed == pygame.K_RIGHT:
            direct = "right"
        elif keyPressed == pygame.K_UP:
            direct = "up"
        elif keyPressed == pygame.K_DOWN:
            direct = "down"
        return direct

    def displayBackground(self,mode="normal",screenName="playing"):
        if screenName == 'playing':
            color = self.screenColor
            background = ""
        elif screenName == 'gameover':
            color = self.screenColor
            background = ""
        elif screenName == 'playagain?':
            color = BLUE
            background = ""
        if mode == "normal" :
            self.display.fill(color)
        elif mode == "beautiful" :
            pass

    def displayElement(self):
        # Erase Screen
        self.displayBackground()
        # Display Score
        value = self.fontStyleScore.render("Your Score: " + str(self.score), True, YELLOW)
        self.display.blit(value, [0, 0])
        # Display Food
        temp_food = self.food.position+self.food.size
        pygame.draw.rect(self.display,self.food.color,temp_food)
        # Display Snake
        for i in range(self.snake.length):
            temp_snake = self.snake.position[i]+self.snake.size
            temp_color = self.snake.headColor if i==0 else self.snake.bodyColor
            temp_color_border = WHITE
            pygame.draw.rect(self.display,temp_color,temp_snake)
            pygame.draw.rect(self.display,temp_color_border,temp_snake,width=1)
        pygame.display.update()

    def displayMessage(self,color,*args):
        self.displayBackground()
        numberOfText = len(args)
        heightOfText = 0
        for index, text in enumerate(args) :
            mesg = self.fontStyle.render(text, True, color)
            x = (self.screenSize[0]-mesg.get_width())/2
            if index==0 :
                heightOfText = mesg.get_height()
                y = self.screenSize[1]/2 - heightOfText*(numberOfText//2)
                if numberOfText%2 > 0 :
                    y = y - heightOfText/2
            else:
                y = y + heightOfText
            textPosition = [x,y]
            self.display.blit(mesg,textPosition)
    
    def updateScore(self):
        self.score += 1
        self.snake.updateLengthSnake(self.food.position)
        while self.food.position in self.snake.position:
            self.food.addFood()

    def checkLose(self):
        isLose = False
        if self.snake.position[0][0] >= self.screenSize[0] or self.snake.position[0][0] < 0 or self.snake.position[0][1] >= self.screenSize[1] or self.snake.position[0][1] < 0:
            isLose = True
        elif (self.snake.position[0]) in (self.snake.position[1:]):
                    isLose = True
        self.isLose = isLose
        return isLose

    def askToQuit(self):
        self.displayBackground(screenName='playagain?')
        self.highestScore = max(self.score, self.highestScore)
        self.displayMessage(RED,"You Lost!",f"Your score: {self.score}",f"Hightest Score: {self.highestScore}","Press C-Play Again or Q-Quit")
        pygame.display.update()

        right_key = False
        isOver = False
        while not right_key :
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    isOver = True
                    right_key = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        isOver = True
                        right_key = True
                    elif event.key == pygame.K_c:
                        right_key = True
                        self.isNewgame= True
                        self.fileName.saveFileData(self.score)
        return isOver
        
    def reset(self):
        self.isNewgame = False # it already new game
        self.isLose = False
        self.food = Food(self.screenSize,self.sizePlayable)
        self.snake = Snake(self.screenSize)
        self.score = 0
        self.displayElement()

    def playGame(self):
        isOver = False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                isOver = True
            elif event.type == pygame.KEYDOWN:
                direct = self.direction(event.key)
                self.snake.updatePosition(direct)
                if self.snake.position[0] == self.food.position :
                    self.updateScore()
                self.displayElement()
                if self.checkLose() :
                    isOver = self.askToQuit()
                self.clock.tick(self.screenFps)
        if isOver :
            self.fileName.saveFileData(self.score)
            self.displayMessage(RED, "See you again")
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
        elif self.isNewgame :
            self.reset()
        return isOver

if __name__ == "__main__":
    env = Enviroment([20,20])
    isOver = False
    while not isOver:
        isOver = env.playGame()
