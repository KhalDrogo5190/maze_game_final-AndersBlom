# Imports
import pygame
import intersects

# Initialize game engine
pygame.init()

# Window
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
TITLE = "Cooperative Fun Puzzle Maze"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

#Sound
coin = pygame.mixer.Sound("sound/coin.ogg")

#Picture
banjo = pygame.image.load("pictures/banjo.png")

# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 150, 175)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
PINK = (255, 0, 220)


# Fonts
MY_FONT = pygame.font.Font(None, 36)

# make walls

wall1 =  [0, 0, 800, 25]
wall2 =  [0, 25, 25, 550]
wall3 =  [0, 575, 800, 25]
wall4 =  [775, 25, 25, 550]
wall5 =  [362.5, 25, 25, 550]
wall6 = [75, 287.5, 650, 25]
wall7 = [25, 362.5, 270, 25]
wall8 = [450, 362.5, 350,25]
wall9 = [270, 387.5,25,125]
wall10 = [450, 387.5, 25, 125]
wall11= [25, 200, 150, 25]
wall12 = [450, 500, 150, 25]


walls = [wall1, wall2, wall3,wall4, wall5 ,wall6, wall7, wall8, wall9, wall10, wall11, wall12]


# Make coins
coin1 = [200, 500, 25, 25]
coin2 = [400, 250, 25, 25]
coin3 = [250, 150, 25, 25]
coin4 = [550, 330, 25, 25]
coin5 = [575, 450, 25, 25]

coins = [coin1, coin2, coin3, coin4, coin5]

 #Make gates blue
gate1 = [25, 287.5 ,50, 25]
gate2 = [725, 287.5, 50, 25]

gate3 = [295, 362.5,  65, 25]
gate4 = [386, 362.5, 65, 25]

gates_a = [gate1, gate2]
gates_b = [gate3, gate4]

#Make switches
switch1 = [150, 175, 25, 25]
switch2 = [500, 470, 25, 25]
switch3 = [500,  330, 25, 25]
switch4 = [150, 330, 25, 25]

switchs_a = [switch1, switch3 ]
switchs_b = [switch2, switch4]

# stages
START = 0
PLAYING = 1
END = 2
PAUSE = 3


def setup():
    global player1, vel1, score1, player2, vel2, score2, stage, grav, gate_open

    player1 =  [100, 150, 25, 25]
    vel1 = [0, 0]
    score1 = 0

    player2 =  [500, 150, 25, 25]
    vel2 = [0, 0]
    score2 = 0

    grav = 5
    stage = START
    gate_open = True

def on_switch_a():
    for s in switchs_a:
        if intersects.rect_rect(player1, s):
            return True
        elif intersects.rect_rect(player2,s):
            return True

    return False

def on_switch_b():
    for s in switchs_b:
        if intersects.rect_rect(player1, s):
            return True
        elif intersects.rect_rect(player2, s):
            return True

    return False

# Game loop
setup()
win = 0
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            
             if stage == START:
                 if event.key == pygame.K_SPACE:
                     stage = PLAYING
                    
                 elif stage == PLAYING:
                     if event.key == pygame.K_SPACE:
                         stage = PAUSE

                 elif stage == END:
                     if event.key == pygame.K_SPACE:
                         setup()       
                 elif stage == PAUSE:
                    if event.key == pygame.K_SPACE:
                         stage = PLAYING          
                
                    

    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

       
        up1 = pressed[pygame.K_w]
        down1 = pressed[pygame.K_s]
        left1 = pressed[pygame.K_a]
        right1 = pressed[pygame.K_d]
        up2 = pressed[pygame.K_UP]
        down2 = pressed[pygame.K_DOWN]
        left2 = pressed[pygame.K_LEFT]
        right2 = pressed[pygame.K_RIGHT]
        

        if left1:
            vel1[0] = -5
        elif right1:
            vel1[0] = 5
        else:
            vel1[0] = 0
        if up1:
            vel1[1] = -5
        elif down1:
            vel1[1] = 5
        else:
            vel1[1] = 0
            

        if left2:
            vel2[0] = -5
        elif right2:
            vel2[0] = 5
        else:
            vel2[0] = 0
        if up2:
            vel2[1] = -5
        elif down2:
            vel2[1] = 5
        else:
            vel2[1] = 0


    # Game logic (Check for collisions, update points, etc.)
    gate_open_a = on_switch_a()
    gate_open_b = on_switch_b()

    
    ''' move the player in horizontal direction '''
    player1[0] += vel1[0]
    
    player2[0] += vel2[0]


    ''' resolve collisions'''
    collidables = []
    if gate_open_a and gate_open_b:
        collidables = walls
    elif gate_open_a and not gate_open_b:
        collidables = walls + gates_b
    elif gate_open_b and not gate_open_a:
        collidables = walls + gates_a
    else:
        collidables = walls + gates_a + gates_b
        
    '''horizontally '''
    for c in collidables:
        if intersects.rect_rect(player1, c):        
            if vel1[0] > 0:
                player1[0] = c[0] - player1[2]
            elif vel1[0] < 0:
                player1[0] = c[0] +c[2]

        if intersects.rect_rect(player2, c):        
            if vel2[0] > 0:
                player2[0] = c[0] - player2[2]
            elif vel2[0] < 0:
                player2[0] = c[0] + c[2]

            
    ''' move the player in vertical direction '''
    player1[1] += vel1[1] 
    
    player2[1] += vel2[1]
    
    '''vertically '''
    for c in collidables:
        if intersects.rect_rect(player1, c):                    
            if vel1[1] > 0:
                player1[1] = c[1] - player1[3] 
            if vel1[1]< 0:
                player1[1] = c[1] + c[3]


        if intersects.rect_rect(player2, c):                    
            if vel2[1] > 0:
                player2[1] = c[1] - player2[3] 
            if vel2[1]< 0:
                player2[1] = c[1] +c[3]


    ''' here is where you should resolve player collisions with screen edges '''
    left1 = player1[0]
    right1 = player1[0] + player1[2]
    top1 = player1[1]
    bottom1 = player1[1] +player1[3]

    if left1 < 0:
        player1[0] = 0
    elif right1 > WIDTH:
        player1[0] = WIDTH - player1[2]

    if top1 < 0:
        player1[1] = 0
    elif bottom1 > HEIGHT:
        player1[1] = HEIGHT - player1[3]

    left2 = player2[0]
    right2 = player2[0] + player2[2]
    top2 = player2[1]
    bottom2 = player2[1] +player2[3]

    if left2 < 0:
        player2[0] = 0
    elif right2 > WIDTH:
        player2[0] = WIDTH - player2[2]

    if top2 < 0:
        player2[1] = 0
    elif bottom2 > HEIGHT:
        player2[1] = HEIGHT - player2[3]

    ''' get the coins'''
    hit_list1 = []
    hit_list2 = []
    
    
    hit_list1 = [c for c in coins if intersects.rect_rect(player1, c)]
    
    for hit in hit_list1:
        coins.remove(hit)
        score1 += 1
        coin.play()
            
    hit_list2 = [c for c in coins if intersects.rect_rect(player2, c)]
    
    for hit in hit_list2:
        coins.remove(hit)
        score2 += 1
        coin.play()



        
    #win situations
    if len(coins) == 0:

        win = 1

        stage = END

    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, player1)

    pygame.draw.rect(screen, RED, player2)
    
    for w in walls:
        pygame.draw.rect(screen, CYAN, w)
         
    for g in gates_a:
        if not gate_open_a :
            pygame.draw.rect(screen, PINK, g)

    for s in switchs_a:
        pygame.draw.rect(screen, PINK, s)

    for g in gates_b:
        if not gate_open_b :
            pygame.draw.rect(screen, GREEN, g)

    for s in switchs_b:
        pygame.draw.rect(screen, GREEN, s)

    for c in coins:
        pygame.draw.rect(screen, WHITE, c)
        

    if win == 1:
        text = MY_FONT.render("You Win!", 1, GREEN)
        screen.blit(text, [350, 100])

    

    #begin/end game text
    if stage == START:
        screen.blit(banjo, (0, 0))
        text1 = MY_FONT.render("Mazish", True, WHITE)
        text2 = MY_FONT.render("(Press SPACE to play.)", True, WHITE)
        screen.blit(text1, [350, 150])
        screen.blit(text2, [275, 200])
    elif stage == END:
        text1 = MY_FONT.render("Game Over", True, WHITE)
        text2 = MY_FONT.render("(Press SPACE to restart.)", True, WHITE)
        screen.blit(text1, [310, 150])
        screen.blit(text2, [210, 200])
    elif stage == PAUSE:
        text1 = MY_FONT.render("Pause", True, WHITE)
        text2 = MY_FONT.render("(Press SPACE to continue.)", True, WHITE)
        screen.blit(text1, [310, 150])
        screen.blit(text2, [210, 200])
        


    #scoring text cooperative
    score_text = MY_FONT.render("Score: " + str(score1 + score2), 1, WHITE)
    screen.blit(score_text, [10, 25])

    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
