# Import Libraries
import pygame
import time
import random
import pyautogui
import pandas as pd
from os import path

# Const Variable
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255,0,0)
red_border = (213, 50, 80)
green = (0, 255, 0)
green_border = (50, 213, 80)
blue = (0,0,255)
blue_border = (50, 153, 213)

screen_color = black
snake_head_color = red
snake_color = green
food_color = white

snake_head_size = [10,10]
food_size = [10,10]
scale_size = [20,20]
screen_size = (snake_head_size[0]*scale_size[0],snake_head_size[1]*scale_size[1])
score_font_size = round(screen_size[0]/15)
font_size =  round(screen_size[0]/13)

snake_speed = 60
file_name = 'result.csv'

# Create the Screen
def init_game():
    pygame.init()
    global dis, font_style, score_font, screen_playable, highest
    dis = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Snake game by TXDien')
    # font_style = pygame.font.SysFont(None,50)
    font_style = pygame.font.SysFont("bahnschrift", font_size)
    score_font = pygame.font.SysFont("comicsansms", score_font_size )
    value = score_font.render("Your Score: " + str(0), True, yellow)
    screen_playable = [value.get_width(),value.get_height()]
    highest = 0
    if path.exists(file_name) :
        with open(file_name,'r') as f:
            try :
                df = pd.read_csv(f, usecols= ['Score'])
                lst = df.values.tolist()
                highest = max(lst)[0]
            except:
                print("No column")
            f.close()
            


# Create Score 
def show_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Create the element (Snake, Food and Score)
def create_element(snake_pos,food_pos,score):
    dis.fill(screen_color)
    show_score(score)
    temp_food = food_pos+food_size
    pygame.draw.rect(dis,food_color,temp_food)
    snake_len = len(snake_pos)
    for i in range(snake_len):
        temp_snake = snake_pos[i]+snake_head_size
        temp_color = snake_head_color if i==0 else snake_color
        temp_color_border = white
        pygame.draw.rect(dis,temp_color,temp_snake)
        pygame.draw.rect(dis,temp_color_border,temp_snake,width=1)
    pygame.display.update()
    
# Adding the Food
def add_food():
    foodx = round(random.randrange(screen_playable[0], screen_size[0] - snake_head_size [0]) / 10.0) * 10.0
    foody = round(random.randrange(screen_playable[1], screen_size[1] - snake_head_size [1]) / 10.0) * 10.0
    return [foodx, foody]

# Create a random key_press
def key_press_simulate(snake_pos, food_pos):
    Controller = {0 : "left",1 : "right",2 : "up",3 : "down"}
    is_over = True
    pos_chose = [0,0,0,0]
    #temp = random.randint(0,99)%4
    while is_over :
        if (not pos_chose[0]) and (snake_pos[0][0] > food_pos[0]):
            temp = 0
        elif (not pos_chose[1]) and (snake_pos[0][0] < food_pos[0]):
            temp = 1
        elif (not pos_chose[2]) and (snake_pos[0][1] > food_pos[1]):
            temp = 2
        elif (not pos_chose[3]) and (snake_pos[0][1] < food_pos[1]):
            temp = 3 
        else:
            i = 0
            while (i<4) and (pos_chose[i] == 1):
                i+=1
            temp = i if (0 in pos_chose) else 1
        pos_chose[temp] = 1
        key_random = Controller[temp]
        snake = move_snake(key_random,snake_pos)
        is_over = you_lose(snake)
        if is_over and pos_chose == [1,1,1,1]:
            is_over = False 
    return key_random

# new Game
def new_game():
    snake_head_pos = [[screen_size[0]/2,screen_size[1]/2]]
    score = 0
    food_pos = add_food()
    create_element(snake_head_pos,food_pos, score)
    is_newgame = False
    return snake_head_pos, food_pos, score, is_newgame

# Read Position in keyboard
def direction(key_pressed):
    direct = ""
    if key_pressed == pygame.K_LEFT:
        direct = "left"
    elif key_pressed == pygame.K_RIGHT:
        direct = "right"
    elif key_pressed == pygame.K_UP:
        direct = "up"
    elif key_pressed == pygame.K_DOWN:
        direct = "down"
    return direct
    
# Moving the Snake, return new position
def move_snake(direct,position):
    change_position = [0,0]
    temp = position[:]
    if direct == "left" :
        change_position[0] = -snake_head_size [0]
    elif direct == "right":
        change_position[0] = snake_head_size [0]
    elif direct == "up":
        change_position[1] = -snake_head_size [1]
    elif direct == "down" :
        change_position[1] = snake_head_size [1]
    
    if change_position != [0,0]: 
        temp[0] = [sum(x) for x in zip(position[0], change_position)]
        temp[1:] = position[:-1]
    return temp[:]

# Increasing the Length of the Snake
def increase_length_snake(pre_snake_pos,food_pos):
    temp = [food_pos[:]]
    temp.extend(pre_snake_pos)
    return temp[:]

# Calculating if Score
def  game_score(pre_pos,food_pos,score):
    score += 1
    snake_pos = increase_length_snake(pre_pos,food_pos)
    while food_pos in snake_pos:
        food_pos = add_food()
    return snake_pos, food_pos,score

# Close Game when Hit Q or Play Again when hit C
def game_close(score):
    dis.fill(blue)
    global highest
    highest = max(score, highest)
    message(red,"You Lost!",f"Your score: {score}",f"Hightest Score: {highest}","Press C-Play Again or Q-Quit")
    pygame.display.update()

    right_key = False
    while not right_key :
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                is_newgame = False
                right_key = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    is_newgame = False
                    right_key = True
                elif event.key == pygame.K_c:
                    right_key = True
                    is_newgame = True
    
    return is_newgame

# Check if you lose or not
def you_lose(snake_pos):
    game_over = False
    if snake_pos[0][0] >= screen_size[0] or snake_pos[0][0] < 0 or snake_pos[0][1] >= screen_size[1] or snake_pos[0][1] < 0:
        game_over = True
    elif (snake_pos[0]) in (snake_pos[1:]):
                game_over = True
    return game_over

# Save data to csv file
def save_data(list_direction, list_food, score):
    df = pd.DataFrame([[list_direction,list_food,score]], columns = ['Direction', 'Food Position', 'Score'])
    if not path.exists(file_name) :
        with open(file_name,'w', newline='') as f:
            df.to_csv(f, index=False, encoding='utf-8',header=True)
            f.close()
    else:
        with open(file_name, 'a+', newline='') as f:
            df.to_csv(f, index=False, encoding='utf-8', mode='a',header=False)
            f.close()

# Game Over when Snake hits the boundaries
def game_over(snake_pos,score):
    game_over = you_lose(snake_pos)
    is_newgame = False
    if game_over :
        is_newgame = game_close(score)
        if is_newgame :
            game_over = False
    return game_over, is_newgame
    
# Message for Game
def message(color,*args):
    dis.fill((0,0,0))
    number = len(args)
    height_of_text = 0
    for index, text in enumerate(args) :
        mesg = font_style.render(text, True, color)
        x = (screen_size[0]-mesg.get_width())/2
        if index==0 :
            height_of_text = mesg.get_height()
            y = screen_size[1]/2 - height_of_text*(number//2)
            if number%2 > 0 :
                y = y - height_of_text/2
        else:
            y = y + height_of_text
        temp = [x,y]
        dis.blit(mesg,temp)

# Game Play
def game_play():
    clock = pygame.time.Clock()
    is_over = False
    snake_pos, food_pos, score, is_newgame = new_game()
    list_direction = []
    list_food = []
    while not is_over:
        if is_newgame :
            save_data(list_direction, list_food, score)
            snake_pos, food_pos, score, is_newgame = new_game()
            list_direction = []
            list_food = []
        pre_position = snake_pos[:]
        key_press = key_press_simulate(snake_pos,food_pos)
        pyautogui.press(key_press)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                is_over = True
            elif event.type == pygame.KEYDOWN:
                direct = direction(event.key)
                snake_pos = move_snake(direct,snake_pos)
                list_direction.append(direct)
                list_food.append(food_pos)
                if snake_pos[0] == food_pos :
                    snake_pos,food_pos,score = game_score(pre_position,food_pos,score)
        if not is_over :
            is_over, is_newgame = game_over(snake_pos,score)
            create_element(snake_pos, food_pos,score)
        clock.tick(snake_speed)
        
    save_data(list_direction, list_food, score)
    message(red, "See you again")
    pygame.display.update()
    time.sleep(2)

    pygame.quit()
    quit()

# Main
if __name__ == "__main__" :
    init_game()
    game_play()