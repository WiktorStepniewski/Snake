# Snake GAME - click 'Space' button and play. 
import numpy as np
import pygame as pg
from tkinter import *
from tkinter import messagebox

class Menu():
    def __init__(self):
        self.textStart = '''Welcome! Click "_"  button!'''
        self.textLose = '''Click "_"  button!'''
        
    def show_start_message(self):
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Snake...", self.textStart)
        root.destroy()

    def show_lose_message(self, score):
        self.score = score
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Snake...", self.textLose + '\nYour score: ' + str(self.score))
        root.destroy()

class Environment():
    def __init__(self, waitTime,score):
        
        # Defining the parameters
        self.width = 880            # width of the game window
        self.height = 880           # height of the game window
        self.nRows = 20             # number of rows in our board
        self.nColumns = 20          # number of columns in our board
        self.initSnakeLen = 2       # initial length of the snake
        self.waitTime = waitTime    # slowdown after taking an action
        self.score = score
        if self.initSnakeLen > self.nRows / 2:
            self.initSnakeLen = int(self.nRows / 2)
        
        self.screen = pg.display.set_mode((self.width, self.height))
        
        self.snakePos = list()
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.5       
        self.applePos = self.placeApple()   
        self.drawScreen() 
        self.collected = False
        self.lastMove = 0
    def placeApple(self):
        posx = np.random.randint(0, self.nColumns)
        posy = np.random.randint(0, self.nRows)
        while self.screenMap[posy][posx] == 0.5:
            posx = np.random.randint(0, self.nColumns)
            posy = np.random.randint(0, self.nRows)
        
        self.screenMap[posy][posx] = 1
        
        return (posy, posx)
   

    def drawScreen(self):
        
        self.screen.fill((0, 0, 0))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.screenMap[i][j] == 0.5:
                    pg.draw.rect(self.screen, (255, 255, 255), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 1:
                    pg.draw.rect(self.screen, (255, 0, 0), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
        
                    
                 
        
        
        pg.display.flip()
    def moveSnake(self, nextPos, col):
        
        self.snakePos.insert(0, nextPos)
        
        if not col:
            self.snakePos.pop(len(self.snakePos) - 1)
        
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(len(self.snakePos)):
            self.screenMap[self.snakePos[i][0]][self.snakePos[i][1]] = 0.5
        
        if col:
            self.score +=1
            self.applePos = self.placeApple()
            self.collected = True
            if self.waitTime>100:
                self.waitTime -= 10
            elif self.waitTime <=100 & self.waitTime > 45:
                self.waitTime -= 5
            elif self.waitTime <=45 & self.waitTime > 1:
                self.waitTime -= 1
                
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1
    def step(self, action):

        # Resetting these parameters
        gameOver = False

        self.collected = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        snakeX = self.snakePos[0][1]
        snakeY = self.snakePos[0][0]

        if action == 1 and self.lastMove == 0:
            action = 0
        if action == 0 and self.lastMove == 1:
            action = 1
        if action == 3 and self.lastMove == 2:
            action = 2
        if action == 2 and self.lastMove == 3:
            action = 3

        if action == 0:
            if snakeY > 0:
                if self.screenMap[snakeY - 1][snakeX] == 0.5:
                    gameOver = True
                elif self.screenMap[snakeY - 1][snakeX] == 1:                  
                    self.moveSnake((snakeY - 1, snakeX), True)
                elif self.screenMap[snakeY - 1][snakeX] == 0:
                    self.moveSnake((snakeY - 1, snakeX), False)
            else:
                gameOver = True
                
                
        elif action == 1:
            if snakeY < self.nRows - 1:
                if self.screenMap[snakeY + 1][snakeX] == 0.5:
                    gameOver = True
                    
                elif self.screenMap[snakeY + 1][snakeX] == 1:
                    
                    self.moveSnake((snakeY + 1, snakeX), True)
                elif self.screenMap[snakeY + 1][snakeX] == 0:
                    self.moveSnake((snakeY + 1, snakeX), False)
            else:
                gameOver = True
                
                
        elif action == 2:
            if snakeX < self.nColumns - 1:
                if self.screenMap[snakeY][snakeX + 1] == 0.5:
                    gameOver = True
                    
                elif self.screenMap[snakeY][snakeX + 1] == 1:
                    
                    self.moveSnake((snakeY, snakeX + 1), True)
                elif self.screenMap[snakeY][snakeX + 1] == 0:
                    self.moveSnake((snakeY, snakeX + 1), False)
            else:
                gameOver = True
               
        
        elif action == 3:
            if snakeX > 0:
                if self.screenMap[snakeY][snakeX - 1] == 0.5:
                    gameOver = True
                    
                elif self.screenMap[snakeY][snakeX - 1] == 1:
                    
                    self.moveSnake((snakeY, snakeX - 1), True)
                elif self.screenMap[snakeY][snakeX - 1] == 0:
                    self.moveSnake((snakeY, snakeX - 1), False)
            else:
                gameOver = True
                
        self.drawScreen()
        
        self.lastMove = action
        
        pg.time.wait(self.waitTime)
        
        # Returning the new frame of the game, the reward obtained and whether the game has ended or not
        return self.screenMap, gameOver
    
    # function that resets the environment
    def reset(self):
        self.screenMap  = np.zeros((self.nRows, self.nColumns))
        self.snakePos = list()
        self.waitTime = 200
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.001
        
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1
        
        self.lastMove = 0




if __name__ == '__main__':     
    
    env = Environment(200,0)
    menu = Menu()
    menu.show_start_message()
    ShownScore = False
    
    start = False
    direction = 0
    gameOver = False
    while True:
        state = env.screenMap
        pos = env.snakePos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameOver = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not start:
                    start = True
                if event.key == pg.K_UP and direction != 1:
                    direction = 0
                elif event.key == pg.K_RIGHT and direction != 3:
                    direction = 2
                elif event.key == pg.K_LEFT and direction != 2:
                    direction = 3
                elif event.key == pg.K_DOWN and direction != 0:
                    direction = 1
        if start:
            _,  gameOver = env.step(direction)
            ShownScore = False
        if gameOver:
            env.reset()
            direction = 0
            if ShownScore != True:
                menu.show_lose_message(env.score)
                env.score = 0
                ShownScore = True
            start = False
            
            
        



