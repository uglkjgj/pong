import pygame, sys, random


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x  # Changes the position of the ball in each instance of the loop
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:  # Implements collision with top and bottom of the screen
        pygame.mixer.Sound.play(pong_sound)  # Plays sound
        ball_speed_y *= -1

    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:  # Checks if the ball collides with the rectangles
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.top -= opponent_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)
    player.center = (screen_width - 12, screen_height / 2)
    opponent.center = (10, screen_height / 2)

    # Displays a count down timer
    if current_time - score_time < 700:
        number_three = score_font.render("3", False, game_shape_color)
        screen.blit(number_three, (screen_width / 2 - 7, screen_height / 2 + 11))
    if 700 < current_time - score_time < 1400:
        number_two = score_font.render("2", False, game_shape_color)
        screen.blit(number_two, (screen_width / 2 - 7, screen_height / 2 + 11))
    if 1400 < current_time - score_time < 2100:
        number_one = score_font.render("1", False, game_shape_color)
        screen.blit(number_one, (screen_width / 2 - 7, screen_height / 2 + 11))

    # Resets the balls speed
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0


    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


# General Setup
pygame.mixer.pre_init(44100, -16, 2, 512)  # Ensures that the buffer before sounds is removed so there is no delay in
# sounds first 3 parameters are default the 4th is the one that has to be changed 512 is a safe bet
pygame.init()  # Initiates all the modules and required when starting pygame code
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))  # Sets up the screen with the width and height
pygame.display.set_caption("Pong")  # Title of the screen

# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 7.5, screen_height / 2 - 7.5, 15,
                   15)  # These variables simply create empty rectangles
player = pygame.Rect(screen_width - 15, screen_height / 2 - 35, 5, 70)  # They still have to be drawn
opponent = pygame.Rect(10, screen_height / 2 - 35, 5, 70)

# Colors
bg_color = (102, 0, 0)
shape_color = (255, 153, 51)

alt_bg = (255, 255, 255)
alt_shapes = (51, 153, 255)

game_bg_color = bg_color
game_shape_color = shape_color

# Game Variables
ball_speed_x = 7
ball_speed_y = 7
opponent_speed = 7
player_speed = 0

# Score Timer
score_time = True

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 20)
score_font = pygame.font.Font("freesansbold.ttf", 32)
start_page_font = pygame.font.Font("freesansbold.ttf", 40)

# Sound
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

# Check if the mouse has been clicked
click = False


def menu():
    global click, player_speed
    while True:
        settings_button = pygame.Rect(20, 20, 30, 30)
        game_start = pygame.Rect(0, 0, 640, 480)
        pygame.draw.rect(screen, game_bg_color, game_start)
        screen.fill(game_bg_color)
        pygame.draw.ellipse(screen, game_shape_color, settings_button)

        pygame.draw.rect(screen, game_shape_color, player)
        pygame.draw.rect(screen, game_shape_color, opponent)
        player_animation()
        text = start_page_font.render("Pong", False, game_shape_color)
        screen.blit(text, (270, 100))

        click_to_start = game_font.render("Click to start", False, game_shape_color)
        screen.blit(click_to_start, (255, 300))

        # Get mouse positions
        mx, my = pygame.mouse.get_pos()
        set_click = False
        if settings_button.collidepoint(mx, my):
            if click:
                set_click = True
                settings()
                click = False

        if set_click == False:
            if game_start.collidepoint(mx, my):
                if click:
                    game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks if the user quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player_speed += 7
                if event.key == pygame.K_w:
                    player_speed -= 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player_speed -= 7
                if event.key == pygame.K_w:
                    player_speed += 7

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()
        clock.tick(60)


def game():
    global player_speed
    running = True
    while running:  # Game Loop
        # Handling input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks if the user quit the game
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    player_speed += 7
                if event.key == pygame.K_w:
                    player_speed -= 7
                if event.key == pygame.K_SPACE:
                    running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    player_speed -= 7
                if event.key == pygame.K_w:
                    player_speed += 7

        ball_animation()
        player_animation()
        opponent_ai()

        # Visuals
        screen.fill(
            game_bg_color)  # Sets a background color for the screen, elements are drawn in the order they are written
        pygame.draw.rect(screen, game_shape_color, player)  # This draws the rectangle unto the screen
        pygame.draw.rect(screen, game_shape_color, opponent)
        pygame.draw.ellipse(screen, game_shape_color, ball)
        pygame.draw.aaline(screen, game_shape_color, (screen_width / 2, 0),
                           (screen_width / 2, screen_height))  # Draws the line that would divide the screen

        # Player Text
        player_text = game_font.render(f"{player_score}", False, game_shape_color)
        screen.blit(player_text, (330, 20))

        opponent_text = game_font.render(f"{opponent_score}", False, game_shape_color)
        screen.blit(opponent_text, (300, 20))

        if score_time:
            ball_restart()

        # Updating the window
        pygame.display.flip()
        clock.tick(60)


def settings():
    global click
    running = True
    while running:
        screen.fill(game_bg_color)

        color_1 = pygame.Rect(300, 120, 50, 50)
        color_2 = pygame.Rect(300, 200, 50, 50)
        pygame.draw.rect(screen, alt_shapes, color_2)
        pygame.draw.rect(screen, shape_color, color_1)

        text = start_page_font.render("Choose Game Theme", False, game_shape_color)
        screen.blit(text, (120, 50))

        # Get mouse positions
        mx, my = pygame.mouse.get_pos()
        if color_1.collidepoint(mx, my):
            if click:
                set_color_red()

        if color_2.collidepoint(mx, my):
            if click:
                set_color_blue()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Checks if the user quit the game
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.flip()
        clock.tick(60)


def set_color_red():
    global game_bg_color, game_shape_color
    game_bg_color = bg_color
    game_shape_color = shape_color


def set_color_blue():
    global game_bg_color, game_shape_color
    game_bg_color = alt_bg
    game_shape_color = alt_shapes


if __name__ == '__main__':
    menu()
