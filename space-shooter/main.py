import pygame, random

#Initialize pygame
pygame.init()

#Create a display surface
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 500
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
ALIEN_STARTING_VELOCITY = 10
ALIEN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100
BULLET_VELOCITY = 30

score = 0
player_lives = PLAYER_STARTING_LIVES
alien_velocity = ALIEN_STARTING_VELOCITY
bullet_active = False

#Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

#Set fonts
font = pygame.font.Font("Facon.ttf", 32)

#Set text
score_text = font.render("Score: " + str(score), True, WHITE)
score_rect = score_text.get_rect()
score_rect.topleft = (15, 15)

lives_text = font.render("Lives: " + str(player_lives), True, WHITE)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 15, 15)

game_over_text = font.render("GAMEOVER", True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, RED)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

#Set sounds and music
collide_sound = pygame.mixer.Sound("sounds/player_collide.wav")
alien_death_sound = pygame.mixer.Sound("sounds/alien_death.wav")
shoot_sound = pygame.mixer.Sound("sounds/player_fire.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
game_over_sound.set_volume(.5)
pygame.mixer.music.load("sounds/background_music.wav")

#Set images
player_image = pygame.image.load("images/spaceship.png")
player_rect = player_image.get_rect()
player_rect.left = 30
player_rect.centery = WINDOW_HEIGHT//2

alien_image = pygame.image.load("images/alien.png")
alien_rect = alien_image.get_rect()
alien_rect.right = WINDOW_WIDTH + BUFFER_DISTANCE
alien_rect.centery = random.randint(64, WINDOW_HEIGHT - 48)

background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (WINDOW_WIDTH, WINDOW_HEIGHT))
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

bullet_image = pygame.image.load("images/bullet.png")
bullet_rect = bullet_image.get_rect()

#The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        #Check if player wants to quit
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not bullet_active:
                #Fire bullet
                bullet_active = True
                bullet_rect.x = player_rect.right
                bullet_rect.centery = player_rect.centery
                shoot_sound.play()

    #Get the list of keys being pressed down
    keys = pygame.key.get_pressed()

    #Move the player continously
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_VELOCITY
    if keys[pygame.K_RIGHT] and player_rect.right < WINDOW_WIDTH:
        player_rect.x += PLAYER_VELOCITY
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    #Move the alien
    if alien_rect.x < 0:
        #Player missed the alien
        player_lives -= 1
        collide_sound.play()
        alien_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        alien_rect.y = random.randint(64, WINDOW_HEIGHT - 48)
    else:
        #Move the alien
        alien_rect.x -= alien_velocity

    #Move bullet
    if bullet_active:
        bullet_rect.x += BULLET_VELOCITY
        #Check if bullet is out of screen
        if bullet_rect.right > WINDOW_WIDTH:
            bullet_active = False

    #Check for collisions
    if player_rect.colliderect(alien_rect):
        # score += 1
        player_lives -= 1

        collide_sound.play()
        alien_velocity += ALIEN_ACCELERATION
        alien_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        alien_rect.y = random.randint(64, WINDOW_HEIGHT - 48)

    if bullet_active and alien_rect.colliderect(bullet_rect):
        score += 1
        alien_death_sound.play()
        alien_velocity += ALIEN_ACCELERATION
        alien_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        alien_rect.y = random.randint(64, WINDOW_HEIGHT - 48)
        bullet_active = False

    #Update HUD
    score_text = font.render("Score: " + str(score), True, WHITE)
    lives_text = font.render("Lives: " + str(player_lives), True, WHITE)

    #Check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game until player presses a key, then reset the game
        game_over_sound.play()
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    alien_velocity = ALIEN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                #The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #Blit the background
    display_surface.blit(background_image, background_rect)

    #Blit the HUD
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    #Blit the images
    display_surface.blit(player_image, player_rect)
    display_surface.blit(alien_image, alien_rect)

    #Blit the bullet if active
    if bullet_active:
        display_surface.blit(bullet_image, bullet_rect)

    #Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()
