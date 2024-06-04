import pygame, random

#Initialize pygame
pygame.init()

#Create display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tap the Ball")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

#Set constants
BORDER_THICKNESS = 5
BALL_INITIAL_RADIUS = 20
BALL_INITIAL_VELOCITY = 5
BALL_INTIAL_ACCELERATION = .5
BALL_INITIAL_INCREMENT = .5

#Set variables
ball_x = WINDOW_WIDTH//2
ball_y = WINDOW_HEIGHT//2
ball_dx = random.choice([-1, 1])
ball_dy = random.choice([-1, 1])
ball_radius = BALL_INITIAL_RADIUS
ball_velocity = BALL_INITIAL_VELOCITY
wall_hit = False
score = 0

#Set colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Set shapes
ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)

#Set font
font = pygame.font.Font("Franxurter.ttf", 96)

#Set text
score_text = font.render("Score: " + str(score), True, WHITE)
score_rect = score_text.get_rect()
score_rect.center = (WINDOW_WIDTH//2, 96)

#Set sounds
collide_sound = pygame.mixer.Sound("sounds/collide.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")
miss_sound.set_volume(.1)

#Set tail
trail_color = BLACK
trail = []

#Main game loop
running = True
while running:
    #Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Click the ball
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            if ball_rect.collidepoint(mouse_x, mouse_y):
                collide_sound.play()
                score += 1
                ball_velocity += BALL_INTIAL_ACCELERATION

                #Move the ball in a new direction
                previous_dx = ball_dx
                previous_dy = ball_dy
                while (previous_dx == ball_dx and previous_dy == ball_dy):
                    ball_dx = random.choice([-1, 1])
                    ball_dy = random.choice([-1, 1])
            else:
                if (ball_velocity >= BALL_INITIAL_VELOCITY * 2):
                    ball_velocity -= BALL_INTIAL_ACCELERATION * 2
                miss_sound.play()

    #Update the score
    score_text = font.render("Score: " + str(score), True, WHITE)

    #Move the ball
    ball_rect.x += ball_dx * ball_velocity
    ball_rect.y += ball_dy * ball_velocity

    #Bounce the ball
    if ball_rect.left <= BORDER_THICKNESS or ball_rect.right >= WINDOW_WIDTH - BORDER_THICKNESS:
        wall_hit = True
        ball_dx = ball_dx * -1
    if ball_rect.top <= BORDER_THICKNESS or ball_rect.bottom >= WINDOW_HEIGHT - BORDER_THICKNESS:
        wall_hit = True
        ball_dy = ball_dy * -1

    if wall_hit:
        wall_hit = False
        score += 1
        collide_sound.play()
        ball_radius += BALL_INITIAL_INCREMENT
        ball_velocity += BALL_INTIAL_ACCELERATION

        #Set trail color
        if ball_rect.left <= BORDER_THICKNESS:
            trail_color = GREEN
        if ball_rect.right >= WINDOW_WIDTH - BORDER_THICKNESS:
            trail_color = BLUE
        if ball_rect.top <= BORDER_THICKNESS:
            trail_color = RED
        if ball_rect.bottom >= WINDOW_HEIGHT - BORDER_THICKNESS:
            trail_color = YELLOW

    #Add trail
    trail.append((trail_color, ball_rect.center, ball_radius))
    
    #Clear the display
    display_surface.fill(BLACK)

    #Draw the trail
    for color, position, radius in trail:
        pygame.draw.circle(display_surface, color, position, radius)

    #Draw the ball
    pygame.draw.circle(display_surface, WHITE, ball_rect.center, ball_radius)

    #Draw the border
    pygame.draw.line(display_surface, GREEN, (0, 0), (0, WINDOW_HEIGHT), BORDER_THICKNESS)
    pygame.draw.line(display_surface, BLUE, (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT), BORDER_THICKNESS)
    pygame.draw.line(display_surface, RED, (0, 0), (WINDOW_WIDTH, 0), BORDER_THICKNESS)
    pygame.draw.line(display_surface, YELLOW, (0, WINDOW_HEIGHT), (WINDOW_WIDTH, WINDOW_HEIGHT), BORDER_THICKNESS)

    #Blit the score
    display_surface.blit(score_text, score_rect)

    #Update display
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()
