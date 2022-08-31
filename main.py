import random
import sys
import time

import pygame


def another_ball():
    while True:
        if random.randint(0, 9) != 7:
            type_ = "piggy"
            body = pygame.image.load("pic/pig.png")
        else:
            type_ = "dollar"
            body = pygame.image.load("pic/dollar.png")
        body = pygame.transform.scale(body, (40, 40))
        rect = body.get_rect()
        rect.right = width
        rect.top = random.randint(0, height - rect.height)
        new_ball = {"body": body, "rect": rect, "type": type_}
        yield new_ball


def show_final_text():
    font = pygame.font.SysFont("YaHei", 60)
    str_tip = "Final: %s" % scores
    font_color = (200, 30, 30)
    bmp_game_over = font.render(str_tip, False, font_color)
    bmp_rect = bmp_game_over.get_rect()
    screen.blit(bmp_game_over, (width / 2 - bmp_rect.width / 2, height / 2 - bmp_rect.height / 2))
    game_over_sound.play()
    game_over_sound.set_volume(0.3)


def show_current_score():
    font_color = (255, 255, 255)
    str_tip = "Current:%s" % scores
    font = pygame.font.SysFont("YaHei", 40)
    bmp_tips = font.render(str_tip, False, font_color)
    screen.blit(bmp_tips, (10, 10))


pygame.init()
clock = pygame.time.Clock()
width, height = 800, 600

screen = pygame.display.set_mode((width, height))
background_color = [(0, 0, 0),
                    (128, 128, 33),
                    (33, 33, 128),
                    (255, 255, 255)]

background_color_idx = 0
bird = pygame.image.load("pic/angry-birds.png")
bird = pygame.transform.scale(bird, (60, 60))
bird_rect = bird.get_rect()
bird_rect.top, bird_rect.left = width / 2, height / 2
x_step = 0
y_step = 0
mouse_down = False
cur_pos = 50, 50
last_time = time.time()
game_over = False
ball_list = []
dollar_list = []
scores = 0
speed = 2.0
press_dict = {pygame.K_w: (0, -speed), pygame.K_a: (-speed, 0), pygame.K_s: (0, speed), pygame.K_d: (speed, 0)}
ball_generator = another_ball()

pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("sound/game_over.ogg")
eat_coin = pygame.mixer.Sound("sound/add_score.mp3")
pygame.mixer.music.load("sound/Ari Pulkkinen - Title Theme.mp3")
pygame.mixer.music.play(-1, 0)
pygame.mixer.music.set_volume(0.3)

while not game_over:

    b_quit = False
    this_time = time.time()
    clock.tick(400)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                game_over = True
            elif event.key == pygame.K_1:
                background_color_idx = (background_color_idx + 1) % len(background_color)
            if event.key in press_dict:
                x_step, y_step = x_step + press_dict.get(event.key)[0], y_step + press_dict.get(event.key)[1]
        if event.type == pygame.KEYUP:
            if event.key in press_dict:
                x_step, y_step = x_step - press_dict.get(event.key)[0], y_step - press_dict.get(event.key)[1]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bird_rect.collidepoint(event.pos):
                mouse_down = True
                cur_pos = event.pos
        if event.type == pygame.MOUSEMOTION:
            if mouse_down:
                cur_pos = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
    screen.fill(background_color[background_color_idx])

    # mouse motion

    if mouse_down:
        bird_rect.left, bird_rect.top = cur_pos
        bird_rect.left, bird_rect.top = bird_rect.left - bird_rect.width / 2, bird_rect.top - bird_rect.height / 2

    bird_rect.right += x_step
    bird_rect.top += y_step

    if x_step == speed and bird_rect.right >= width:
        bird_rect.right += -speed
    if x_step == -speed and bird_rect.left <= 0:
        bird_rect.right += speed
    if y_step == speed and bird_rect.bottom >= height:
        bird_rect.top += -speed
    if y_step == -speed and bird_rect.bottom <= 0:
        bird_rect.top += speed

    screen.blit(bird, bird_rect)

    # if time elapsed more than 0.5 second
    # then add another pig
    if last_time < this_time - 0.3:
        last_time = this_time
        ball_list.append(next(ball_generator))

    for ball in ball_list:
        ball_rect = ball["rect"]
        if ball_rect.left < 0:
            ball_list.remove(ball)
            scores += 10
        else:
            ball["rect"] = ball_rect.move(-1, 0)
            screen.blit(ball["body"], ball["rect"])

        if bird_rect.colliderect(ball_rect):
            ball_list.remove(ball)
            if ball["type"] == "piggy":
                game_over = True
            else:
                scores += 50
                eat_coin.play()
                eat_coin.set_volume(0.3)

    if game_over:
        show_final_text()
    else:
        show_current_score()
    pygame.display.flip()

pygame.mixer.music.stop()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
