import sys
import random
import pygame
from math import sqrt

pygame.init()
clock = pygame.time.Clock()


# Functions concerned with MOVING anything.
# --------------------------------------------------------------------------------- #
def move_paddle(keys):
    # Move the player.
    # -------------------------------------- #
    if keys[pygame.K_s] and player_rect.bottom <= SCREEN_HEIGHT:
        player_rect.y = player_rect.y + PADDLE_VEL
    if keys[pygame.K_w] and player_rect.top >= 0:
        player_rect.y = player_rect.y - PADDLE_VEL
    # -------------------------------------- #

    # Move the enemy.
    # -------------------------------------- #
    if keys[pygame.K_DOWN] and enemy_rect.bottom <= SCREEN_HEIGHT:         
        enemy_rect.y = enemy_rect.y + PADDLE_VEL
    if keys[pygame.K_UP] and enemy_rect.top >= 0:                   
        enemy_rect.y = enemy_rect.y - PADDLE_VEL                
    # -------------------------------------- #

def move_ball_horizontally(ball_vel_x, ball_vel_y):
    # This code randomly chooses where the ball goes to initially.
    ball_vel_x_list = [6, -6]
    ball_vel_x = random.choice(ball_vel_x_list)
    ball_rect.x = ball_rect.x + ball_vel_x
    ball_vel_y = 0  # y-velocity is zero because to make it easier at the start of each round.

    ball_velocities = (ball_vel_x, ball_vel_y)

    return ball_velocities

def move_ball_at_angle(ball_vel_x, ball_vel_y):
    # After the ball bounces of a paddle it does so at certain angles.
    ball_rect.x = ball_rect.x + ball_vel_x
    ball_rect.y = ball_rect.y + ball_vel_y
# --------------------------------------------------------------------------------- #


# Functions concerned with checking if a paddle wins the game. 
# ----------------------------------------------------------------- #
def check_player_win():
    player_win = False
    if ball_rect.left > (SCREEN_WIDTH + 10):
        player_win = True

    return player_win

def check_enemy_win():
    enemy_win = False
    if ball_rect.right < -10:
        enemy_win = True

    return enemy_win
# ----------------------------------------------------------------- #


# Functions concerned with resetting game state.
# ----------------------------------------------------------------- #
def reset_player_pos():
    player_rect.left = 20
    player_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

def reset_enemy_pos():
    enemy_rect.left = (SCREEN_WIDTH - PADDLE_WIDTH - 20)
    enemy_rect.top = (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)

def reset_ball_pos():
    ball_rect.left = (SCREEN_WIDTH // 2 - BALL_WIDTH // 2)
    ball_rect.top = (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2)
# ----------------------------------------------------------------- #


# Functions that are concerned with ball COLLISIONS with paddles or walls.
# ---------------------------------------------------------------------------------------------------- #
def wall_collision(ball_vel_y):
    if (ball_rect.bottom >= SCREEN_HEIGHT) or (ball_rect.top <= 0):

        # In case ball bottom/top exceeds the screen, place it so that it can bounce correctly.
        if ball_rect.bottom >= SCREEN_HEIGHT:
            ball_rect.bottom = SCREEN_HEIGHT
        elif ball_rect.top <= 0:
            ball_rect.top = 0

        ball_vel_y = ball_vel_y * -1

    return ball_vel_y

def paddle_collision(ball_vel_x, ball_vel_y):
    if ball_rect.colliderect(player_rect):
        discrepancy = (ball_rect.center[1] - player_rect.center[1])
    elif ball_rect.colliderect(enemy_rect):
        discrepancy = (ball_rect.center[1] - enemy_rect.center[1])

    ball_vel_y = (discrepancy * DISCREPANCY_FACTOR)  # Change the angle of ball based on where it hits paddle

    ball_vel_x = sqrt(((10 * sqrt(2)) ** 2) - ((ball_vel_y) ** 2))  # Adjust ball x-velocity so that ball is always fast

    # If ball collides with enemy its x-velocity must become negative to reflect.
    if ball_rect.colliderect(enemy_rect):
        ball_vel_x = ball_vel_x * -1

    ball_velocities = (ball_vel_x, ball_vel_y)

    return ball_velocities
# ---------------------------------------------------------------------------------------------------- #


# Functions concerned with the player score.
# ---------------------------------------------------------------------------------------------------- #
def display_player_score(player_score):
    score_surf = score_font.render(f"{player_score}", False, GREEN)
    score_rect = score_surf.get_rect(center = (320, 50))
    SCREEN.blit(score_surf, score_rect)

def display_enemy_score(enemy_score):
    score_surf = score_font.render(f"{enemy_score}", False, RED)
    score_rect = score_surf.get_rect(center = (960, 50))
    SCREEN.blit(score_surf, score_rect)
# ---------------------------------------------------------------------------------------------------- #


# Functions concerned with the main menu.
# ---------------------------------------------------------------------------------------------------- #
def one_player_text():
    text_surf = score_font.render("One Player", False, BLACK)
    text_rect = text_surf.get_rect(midleft = (150, 350))

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 20

    new_rect = pygame.Rect(text_rect.left, text_rect.top, rect_width, rect_height)
    new_rect.center = text_rect.center

    pygame.draw.rect(SCREEN, WHITE, new_rect)
    SCREEN.blit(text_surf, text_rect)


def two_player_text():
    text_surf = score_font.render("Two Player", False, BLACK)
    text_rect = text_surf.get_rect(midright = (1130, 350))

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 20

    new_rect = pygame.Rect(text_rect.left, text_rect.top, rect_width, rect_height)
    new_rect.center = text_rect.center

    pygame.draw.rect(SCREEN, WHITE, new_rect)
    SCREEN.blit(text_surf, text_rect)


# This block of code is for the screen.
# --------------------------------------------------- #
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong Game")
# --------------------------------------------------- #


# This block of code is for the colours.
# ------------------------------------- #
GREY = "#363738"
GREEN = "#7fdb98"
RED = "#cf624c"
PEARL_WHITE = "#cacccf"
WHITE = "#f5f5f5"
TURQUOISE = "#64c5e8"
BLACK = "#000000"
# ------------------------------------- #


# This block of code is for declaring the object rects.
# ------------------------------------------------------------------------------------------------------------------------------------------- #
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VEL = 40, 150, 8
BALL_WIDTH, BALL_HEIGHT = 25, 25
DISCREPANCY_FACTOR = 0.125  # Constant responsible for ball angles.

score_font = pygame.font.Font("GamerFont/gamer_font.ttf", 50)

player_rect = pygame.Rect(20, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
enemy_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH - 20), (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect((SCREEN_WIDTH // 2 - BALL_WIDTH // 2), (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2), BALL_WIDTH, BALL_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------- #

def main():
    ball_vel_x = 0
    ball_vel_y = 0  # Initialise the y-velocity.

    round_starts = True

    player_win = False
    player_score = 0
    enemy_win = False
    enemy_score = 0

    menu_runs = True  # Boolean that controls the main menu loop.
    game_runs = True  # Boolean that controls the main game loop.
    pause = False

    # Main menu loop.
    while menu_runs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Background colour of the main menu.
        SCREEN.fill(TURQUOISE)
        # Display the option for one player
        one_player_text()
        # Display the option for two player
        two_player_text()
        # Draw a line in the middle of the screen
        pygame.draw.rect(SCREEN, BLACK, (640,0,10,1000))
        
        pygame.display.update()
        clock.tick(FPS)


    # Main game loop.
    while game_runs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause

        # If pause == False means if the player did not click 'ESC' to pause the game.
        if pause == False:
            # Code responsible for drawing objects on the screen.
            # --------------------------------------------------- #
            SCREEN.fill(GREY)
            pygame.draw.rect(SCREEN, GREEN, player_rect)
            pygame.draw.rect(SCREEN, RED, enemy_rect)
            pygame.draw.ellipse(SCREEN, PEARL_WHITE, ball_rect)
            # --------------------------------------------------- #


            # Code responsible for moving the player and enemy paddles vertically.
            # ------------------------------------------------------------------- #
            keys = pygame.key.get_pressed()
            move_paddle(keys)
            # ------------------------------------------------------------------- #


            # Code responsible for moving the ball and its related physics.
            # ------------------------------------------------------------------- #
            if round_starts:
                # If the round starts, the ball is moved horizontally to either paddle or player.
                ball_vel_x, ball_vel_y = move_ball_horizontally(ball_vel_x, ball_vel_y)
                round_starts = False
            else:
                # After the ball hits any paddle horizontally, it will bounce at a certain angle.
                move_ball_at_angle(ball_vel_x, ball_vel_y)
            # ------------------------------------------------------------------- #


            # Check if ball collides with the top/bottom walls and bounce it.
            # -------------------------------------------------------------- #
            ball_vel_y = wall_collision(ball_vel_y)
            # -------------------------------------------------------------- #


            # Responsible for ball angles when colliding with player or enemy paddle.
            # ----------------------------------------------------------------------------------------------------------------------------- #
            if ball_rect.colliderect(player_rect) or ball_rect.colliderect(enemy_rect):
                ball_vel_x, ball_vel_y = paddle_collision(ball_vel_x, ball_vel_y)
                round_starts = False
            # ----------------------------------------------------------------------------------------------------------------------------- #


            # Check if the ball passes either paddles (player/enemy wins).
            # ------------------------------------------------------------ #
            player_win = check_player_win()
            enemy_win = check_enemy_win()
            # ------------------------------------------------------------ #


            # Code responsible for the player and enemy scores.
            # ------------------------------------------------- #
            display_player_score(player_score)
            display_enemy_score(enemy_score)
            # ------------------------------------------------- #


            # Code executed if either player or enemy wins
            # ------------------------------------------------------- #
            if player_win or enemy_win:
                if player_win:
                    player_score = player_score + 1
                elif enemy_win:
                    enemy_score = enemy_score + 1

                reset_player_pos()
                reset_enemy_pos()
                reset_ball_pos()

                round_starts = True
            # ------------------------------------------------------- #
        else:
            pass

        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()


if __name__ == "__main__":
    main()