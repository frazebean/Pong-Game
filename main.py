import sys
import random
import pygame
from math import sqrt

pygame.init()
clock = pygame.time.Clock()

# Functions concerned with MOVING anything.
# --------------------------------------------------------------------------------- #
def move_player_paddle(keys):
    if keys[pygame.K_s] and player_rect.bottom <= SCREEN_HEIGHT:
        player_rect.y = player_rect.y + PADDLE_VEL
    if keys[pygame.K_w] and player_rect.top >= 0:
        player_rect.y = player_rect.y - PADDLE_VEL

def move_second_paddle(single_player_chosen, two_player_chosen, ball_vel_y):
    if single_player_chosen:
        single_player(ball_vel_y)
    elif two_player_chosen:
        two_player()

# FINALLY MADE THE AI WORK
def single_player(ball_vel_y):
    # NOTE: PADDLE_VEL is for hardest difficulty (8 velocity)

    if abs(ball_vel_y) < abs(PADDLE_VEL):  # The paddle exactly follows ball speeds less than PADDLE_VEL, to eliminate stuttering/jittering
        enemy_rect.y = enemy_rect.y + ball_vel_y
    else:
        if ball_rect.bottom < enemy_rect.top:
            enemy_rect.y = enemy_rect.y - PADDLE_VEL  # Change paddle_vel for difficulty (PADDLE_VEL is most difficult)
        if ball_rect.top > enemy_rect.bottom:
            enemy_rect.y = enemy_rect.y + PADDLE_VEL  # Change paddle_vel for difficulty (PADDLE_VEL is most difficult)

    # This section is responsible for not allowing the enemy paddle to exceed the screen.
    if enemy_rect.bottom > SCREEN_HEIGHT:
        enemy_rect.bottom = SCREEN_HEIGHT
    if enemy_rect.top < 0:
        enemy_rect.top = 0

def two_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and enemy_rect.bottom <= SCREEN_HEIGHT:
        enemy_rect.y = enemy_rect.y + PADDLE_VEL
    if keys[pygame.K_UP] and enemy_rect.top >= 0:
        enemy_rect.y = enemy_rect.y - PADDLE_VEL

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
    # NOTE: The ball's speed when facing any direction is sqrt(200)

    if ball_rect.colliderect(player_rect):
        discrepancy = (ball_rect.center[1] - player_rect.center[1])
    elif ball_rect.colliderect(enemy_rect):
        discrepancy = (ball_rect.center[1] - enemy_rect.center[1])

    ball_vel_y = (discrepancy * ANGLE_FACTOR)  # Change the angle of ball based on where it hits paddle

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


# Functions concerned with the main and pause menu.
# ---------------------------------------------------------------------------------------------------- #
def button_rect(text, position):
    text_surf = score_font.render(text, False, BLACK)
    text_rect = text_surf.get_rect(center = position)

    rect_width = text_rect.width + 20
    rect_height = text_rect.height + 20

    bg_rect = pygame.Rect(text_rect.left, text_rect.top, rect_width, rect_height)
    bg_rect.center = text_rect.center

    pygame.draw.rect(SCREEN, WHITE, bg_rect)
    SCREEN.blit(text_surf, text_rect)

    return bg_rect

def one_player_text():
    bg_rect = button_rect("One Player", (SCREEN_WIDTH * 0.25, SCREEN_HEIGHT // 2))

    return bg_rect

def two_player_text():
    bg_rect = button_rect("Two Player", (SCREEN_WIDTH * 0.75, SCREEN_HEIGHT // 2))

    return bg_rect

def divider_line():
    divider_rect = pygame.Rect(SCREEN_WIDTH // 2, 0, DIVIDER_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, divider_rect)

def pause_bg():
    pause_bg_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, TURQUOISE, pause_bg_rect)

def resume_button():
    bg_rect = button_rect("RESUME", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    return bg_rect

def restart_button():
    bg_rect = button_rect("RESTART", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    return bg_rect

def quit_button():
    bg_rect = button_rect("QUIT", (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
    
    return bg_rect

def mouse_pos_in(rect, pos):
    mouse_in_rect = False
    if (pos[0] >= rect.left and pos[0] <= rect.right) and (pos[1] >= rect.top and pos[1] <= rect.bottom):
        mouse_in_rect = True

    return mouse_in_rect
# ---------------------------------------------------------------------------------------------------- #


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
ANGLE_FACTOR = 0.125  # Constant responsible for ball angles.

DIVIDER_WIDTH = 10

score_font = pygame.font.Font("GamerFont/gamer_font.ttf", 50)

player_rect = pygame.Rect(20, (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
enemy_rect = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH - 20), (SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2), PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pygame.Rect((SCREEN_WIDTH // 2 - BALL_WIDTH // 2), (SCREEN_HEIGHT // 2 - BALL_HEIGHT // 2), BALL_WIDTH, BALL_HEIGHT)
# ------------------------------------------------------------------------------------------------------------------------------------------- #

def main():
    reset_player_pos()
    reset_enemy_pos()
    reset_ball_pos()

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

    single_player_chosen = False
    two_player_chosen = False

    # Main menu loop.
    # ------------------------------------------------------------------------------------------------ #
    while menu_runs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if mouse_pos_in(one_player_text(), pos):
                    if pygame.mouse.get_pressed()[0]:
                        single_player_chosen = True
                        menu_runs = False
                
                if mouse_pos_in(two_player_text(), pos):
                    if pygame.mouse.get_pressed()[0]:
                        two_player_chosen = True
                        menu_runs = False

        # Background colour of the main menu.
        SCREEN.fill(TURQUOISE)
        # Display the option for one player
        one_player_text()
        # Display the option for two player
        two_player_text()
        # Draw a divider line in the middle of the screen
        divider_line()
        
        pygame.display.update()
        clock.tick(FPS)
    # ------------------------------------------------------------------------------------------------ #


    # Main game loop.
    # ------------------------------------------------------------------------------------------------ #
    while game_runs:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause
            elif event.type == pygame.MOUSEBUTTONDOWN and pause == True:
                pos = pygame.mouse.get_pos()

                if mouse_pos_in(resume_button(), pos):
                    if pygame.mouse.get_pressed()[0]:
                        pause = not pause

                if mouse_pos_in(restart_button(), pos):
                    if pygame.mouse.get_pressed()[0]:
                        reset_player_pos()
                        reset_enemy_pos()
                        reset_ball_pos()
                        player_score = 0
                        enemy_score = 0
                        round_starts = True

                        pause = not pause

                if mouse_pos_in(quit_button(), pos):
                    if pygame.mouse.get_pressed()[0]:
                        main()  # Calling the main function again means the whole 'game' restarts.


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
            move_player_paddle(keys)
            move_second_paddle(single_player_chosen, two_player_chosen, ball_vel_y)
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
            pause_bg()  # Display the colour of the pause menu background (turquoise)
            resume_button()
            restart_button()
            quit_button()

        pygame.display.update()
        clock.tick(FPS)
    # ------------------------------------------------------------------------------------------------ #
    
    pygame.quit()


if __name__ == "__main__":
    main()