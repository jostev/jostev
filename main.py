# unoptimised, could run iteration over each snake section only once, hard to identify snake's body shape
import pygame
import random

pygame.init()

SCREEN_WIDTH = 360
SCREEN_HEIGHT = 360
clock = pygame.time.Clock()
dt = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def updateBG():
    for x in range(0, 18):
        for y in range(0, 18):
            tile = pygame.Rect((x * 20, y * 20, 19, 19))
            pygame.draw.rect(screen, (19, 77, 51), tile)

input_x = -20
input_y = 0
pos_x = 180
pos_y = 180
food_x = 0
food_y = 0

snake = [pos_x, pos_y, pos_x + 20, pos_y]

def renderSnake(list):
    for i in range(0, len(list) - 1, 2):
        pygame.draw.rect(screen, (0, 199, 86), pygame.Rect((list[i], list[i+1], 20, 20)))

def updateFoodPos():
    food_x = random.randint(0, 17) * 20
    food_y = random.randint(0, 17) * 20
    for i in range(0, len(snake) - 1):
            if snake[i] == food_x and snake[i + 1] == food_y:
                updateFoodPos()
    return [food_x, food_y]

new_food = updateFoodPos()
food_x = new_food[0]
food_y = new_food[1]

def updateFood():
    food = pygame.Rect((food_x, food_y, 20, 20))
    pygame.draw.rect(screen, (77, 19, 51), food)

food_exists = False

game_over = False
run = True
while run:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((0, 0, 0))
    updateBG()
    
    # movement
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        if snake[2] != pos_x - 20:
            input_x = -20
            input_y = 0
    elif key[pygame.K_d] == True:
        if snake[2] != pos_x + 20:
            input_x = 20
            input_y = 0
    elif key[pygame.K_w] == True:
        if snake[3] != pos_y - 20:
            input_x = 0
            input_y = -20
    elif key[pygame.K_s] == True:
        if snake[3] != pos_y + 20:
            input_x = 0
            input_y = 20
    
    pos_x += input_x
    pos_y += input_y
    
    #Game Over
    for i in range(4, len(snake) - 1, 2):
        if snake[i] == pos_x and snake[i + 1] == pos_y:
            game_over = True
    
    if pos_x < 0 or pos_x >= 360 or pos_y < 0 or pos_y >= 360:
        game_over = True
    
    while game_over:
        screen.fill((19, 77, 51))
        text_sf = pygame.font.SysFont(None, 70).render('GAME OVER', False, (255, 255, 255))
        screen.blit(text_sf, (30,100))
        pygame.display.update()
        
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                run = False
                game_over = False
            # restart
            if event.type == pygame.KEYDOWN:
                # NOT WORKING
                pos_x = 180
                pos_y = 180
                snake = [pos_x, pos_y, pos_x + 20, pos_y]
                screen.fill((0, 0, 0))
                updateBG()
                game_over = False
    
    if len(snake) == 648 or key[pygame.K_l]:
        screen.fill((19, 77, 51))
        text_sf = pygame.font.SysFont(None, 70).render('YOU WIN!', False, (255, 255, 255))
        screen.blit(text_sf, (30,100))
        pygame.display.update()
        
        # winning
        while run:
            text = ['YOU WIN!']
            text_sf = pygame.font.SysFont(None, 20).render(text[random.randint(0, len(text) - 1)], False, (255, 255, 255))
            screen.blit(text_sf, (random.randint(0, 360), random.randint(0, 360)))
            
            clock.tick(3)
            pygame.display.update()
            
            for event in pygame.event.get():
                # quit
                if event.type == pygame.QUIT:
                    run = False
    
    # eating
    if snake[0] == food_x and snake[1] == food_y:
        snake.append(snake[len(snake)-2])
        snake.append(snake[len(snake)-2])
        food_exists = False
        new_food = updateFoodPos()
        food_x = new_food[0]
        food_y = new_food[1]
        updateFood()
    
    if food_exists == False:
        updateFoodPos()
        updateFood()
        food_exists = True
    
    # update snake
    i = len(snake) - 1
    while i > 2:
        snake[i] = snake[i-2]
        snake[i-1] = snake[i-3]
        i -= 2
    
    
    if key[pygame.K_p] == True:
        length = len(snake)
        snake.append(snake[length-2])
        snake.append(snake[length-1])
    
    snake[0] = pos_x
    snake[1] = pos_y
    
    
    
    updateFood()
    renderSnake(snake)
    
    pygame.display.update()
    
    clock.tick(5) # fps

pygame.quit()