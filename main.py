import pygame
import math
import time
import random

# load alle sprites fra load_sprites.py
import load_sprites as spr

# variabler til styring af spillet
screenX, screenY = 650, 650
r = 18 # radius af cirklerne
grid_color = (230, 230, 230)
bg_color = (255, 255, 255)
player_color = (40, 240, 80)
segment_color = (30, 255, 70)
food_color = (240, 50, 35)
dead_color = (30, 185, 70)
dead_grid_color = (255, 255, 255)
gridX, gridY = math.floor(screenX/(2*r))-1, math.floor(screenY/(2*r))-1
player_pos = [math.floor(gridX/2), math.floor(gridY/2)] # [S. 2: (1)]
player_dir = "L" # L: left, R: right, U: up, D: down
player_speed = 130_000_000 # delay mellem trin i ns
food_pos = 0
points = 0
snake_segments = [] # liste af arrays [x, y] med slangens segmenter
keyboard_buffer = "" # [V1 S. 6: (1)]
alive = True

highscore = 0
def load_highscore():
    with open('hs.txt', "r") as hs:
        return int(hs.readline())
    
def write_highscore(score):
    with open("hs.txt", "w") as hs:
        hs.write(f"{score}")

def check_overlap():
    if player_pos in snake_segments[:-1]:
        return False
    return True

def is_alive():
    if player_pos[0] < 0 or player_pos[1] < 0:
        return False
    try:
        grid[player_pos[1]][player_pos[0]]
    except:
        return False
    return check_overlap()

# tilføjer et segment til slangen i den position hvor slangens hoved er
def segment_add():
    snake_segments.append([player_pos[0], player_pos[1]])

# gør ciklen i segmenternes position til farven gemt i variablen player_color [V1 S. 3: (2)]
def draw_segments():
    n = 1
    for i in snake_segments:
        n += 1
        if alive:
            grid[i[1]][i[0]] = segment_color
        else:
            grid[i[1]][i[0]] = dead_color

# fjern sidste segment og set et nyt i slangens position
def update_segments():
    if len(snake_segments) >= 1:
        snake_segments.pop(0)
        segment_add()

# sæt madens position til et tilfældigt sted på gitteret [V1 S. 3: (1)]
def random_food_position():
    global food_pos
    while food_pos == 0 or (food_pos in snake_segments or  food_pos == player_pos): # [V1 S. 5: (1-2)]
        food_pos = [random.randint(0, gridX-1), random.randint(0, gridY-1)]


# tjek om maden er på slangens hoved -> Bool [V1 S. 3: (3)]
def check_food():
    if food_pos == player_pos:
        return True
    return False

# gør ciklen i madens position til farven gemt i variablen food_color [V1 S. 2: (2)]
def draw_food():
    grid[food_pos[1]][food_pos[0]] = food_color

# pygame setup [S. 1: (1)]
pygame.init()
pygame.display.set_caption('SNAKE GAME')
screen = pygame.display.set_mode((screenX, screenY))
clock = pygame.time.Clock()
running = True
dt = 0

# gitter setup
grid = []
def grid_make():
    global grid
    grid = [[[] for x in range(screenX)] for y in range(screenY)]
grid_make()

# funktion til at tegne sprites på gitteret
def draw_grid(offsetX, offsetY, spacing, radius):
    spacing += radius*2
    n_y = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            rect = pygame.Rect((offsetX + x*2*radius, offsetY + y*2*radius))
            screen.blit(spr.apple, rect)

# gør ciklen i spillerens position til farven gemt i variablen player_color [V1 S. 2: (2)]
def draw_player():
    if alive:
        grid[player_pos[1]][player_pos[0]] = player_color
    else:
        grid[player_pos[1]][player_pos[0]] = dead_color

ns_last = time.time_ns()
snake_segments = []
random_food_position()

while running:
    # fang spillerens keyboardinput [V1 S. 2: (4)] & [S. 6: (3)]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and len(keyboard_buffer) < 3:
            if event.key == pygame.K_w and player_dir != "D":
                keyboard_buffer += "U"
            if event.key == pygame.K_s and player_dir != "U":
                keyboard_buffer += "D"
            if event.key == pygame.K_a and player_dir != "R":
                keyboard_buffer += "L"
            if event.key == pygame.K_d and player_dir != "L":
                keyboard_buffer += "R"
            if event.key == pygame.K_r:
                alive = False
                
    # flyt spillerens position i retningen spilleren har valgt [V1 S. 2: (4)]
    if time.time_ns() > player_speed + ns_last:
        update_segments()
        if len(keyboard_buffer) > 0:
            player_dir = keyboard_buffer[0]
            keyboard_buffer = keyboard_buffer[1:]
        if player_dir == "U":
            player_pos[1] -= 1
        elif player_dir == "D":
            player_pos[1] += 1
        elif player_dir == "L":
            player_pos[0] -= 1
        elif player_dir == "R":
            player_pos[0] += 1
        
        ns_last = time.time_ns()

    # tjek positionen af maden og sæt den til ny position hvis slangens hoved ligger på maden [V1 S. 3: (3)]
    if check_food():
        points += 1
        random_food_position()
        segment_add()

    alive = is_alive()
    
    # display points, highscore og navn af spillet
    pygame.display.set_caption(f'SNAKE GAME  |  Points: {points}  |  Highscore: {load_highscore()}')

    # fyld skærmen med farve til baggrunden
    if alive:
        screen.fill(bg_color)
    else:
        screen.fill((0, 0, 0))
    
    grid_make()
    draw_segments()
    draw_food()
    if alive: draw_player()

    # tegner gitteret og "flipper" skærmen for at vise næste frame
    draw_grid(6, 6, 0, r)
    pygame.display.flip()

    dt = clock.tick(60) / 1000  # sætter den maximale FPS til 60

    if not alive:
        time.sleep(2)
        snake_segments = []
        player_pos = [math.floor(gridX/2), math.floor(gridY/2)]
        food_pos = 0
        if points > load_highscore():
            write_highscore(points)
        points = 0
        random_food_position()
        alive = True

pygame.quit()
