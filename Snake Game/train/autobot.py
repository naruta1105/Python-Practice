# Import Libraries
import pyautogui
from snakegame import Enviroment

# Create a random key_press
def simulateKeyPress(env):
    controller = {0 : "left",1 : "right",2 : "up",3 : "down"}
    isFound = False
    posChose = [0,0,0,0]
    #temp = random.randint(0,99)%4
    while not isFound :
        if (not posChose[0]) and (env.snake.position[0][0] > env.food.position[0]):
            temp = 0
        elif (not posChose[1]) and (env.snake.position[0][0] < env.food.position[0]):
            temp = 1
        elif (not posChose[2]) and (env.snake.position[0][1] > env.food.position[1]):
            temp = 2
        elif (not posChose[3]) and (env.snake.position[0][1] < env.food.position[1]):
            temp = 3 
        else:
            i = 0
            while (i<4) and (posChose[i] == 1):
                i = i+1
            temp = i if (0 in posChose) else 1
        print(posChose)
        posChose[temp] = 1
        key_random = controller[temp]
        isLose = env.snake.predictLoseMove(key_random)
        if (not isLose) or (isLose and posChose == [1,1,1,1]) :
            isFound = True
    return key_random

if __name__ == "__main__":
    env = Enviroment([20,20])

    isOver = False
    while not isOver:
        keyPressed = simulateKeyPress(env)
        pyautogui.press(keyPressed)
        print(keyPressed)
        isOver = env.playGame()