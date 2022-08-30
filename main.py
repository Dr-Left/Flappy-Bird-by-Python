import random
import time

import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
width, height = 800, 600

press_dict = {pygame.K_w: (0, -1), pygame.K_a: (-1, 0), pygame.K_s: (0, 1), pygame.K_d: (1, 0)}

screen = pygame.display.set_mode((width, height))
background_color = [(0, 0, 0),
                    (128, 128, 33),
                    (33, 33, 128), ]

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
cnt = 0

while not game_over:

    b_quit = False
    this_time = time.time()
    clock.tick(500)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                b_quit = True
                pass
            elif event.key == pygame.K_1:
                background_color_idx = (background_color_idx + 1) % len(background_color)

            cur_key = event.key
            if cur_key in press_dict:
                x_step, y_step = x_step + press_dict.get(cur_key)[0], y_step + press_dict.get(cur_key)[1]

        if event.type == pygame.KEYUP:
            cur_key = event.key
            if event.key in press_dict:
                x_step, y_step = x_step - press_dict.get(cur_key)[0], y_step - press_dict.get(cur_key)[1]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if bird_rect.collidepoint(event.pos):
                mouse_down = True
                cur_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if mouse_down:
                cur_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    if b_quit:
        break
    screen.fill(background_color[background_color_idx])

    # mouse motion

    if mouse_down:
        bird_rect.left, bird_rect.top = cur_pos
        bird_rect.left, bird_rect.top = bird_rect.left - bird_rect.width / 2, bird_rect.top - bird_rect.height / 2

    if x_step == 1.0 and bird_rect.right >= width:
        bird_rect.right += -1.0
    if x_step == -1.0 and bird_rect.left <= 0:
        bird_rect.right += 1.0
    if y_step == 1.0 and bird_rect.bottom >= height:
        bird_rect.top += -1.0
    if y_step == -1.0 and bird_rect.bottom <= 0:
        bird_rect.top += 1.0

    bird_rect.right += x_step
    bird_rect.top += y_step

    screen.blit(bird, bird_rect)

    # if time elapsed more than 0.5 second
    # then add another pig
    if last_time < this_time - 0.3:
        last_time = this_time
        cnt += 1
        ball_body = pygame.image.load("pic/pig.png")
        ball_body = pygame.transform.scale(ball_body, (40, 40))
        ball_rect = ball_body.get_rect()
        ball_rect.right = width
        ball_rect.top = random.randint(0, height - ball_rect.height)
        ball = {"body": ball_body, "rect": ball_rect}
        ball_list.append(ball)

    for ball in ball_list:
        ball_rect = ball["rect"]
        if ball_rect.left < 0:
            ball_list.remove(ball)
        else:
            ball["rect"] = ball_rect.move(-1, 0)
            screen.blit(ball["body"], ball["rect"])

        if bird_rect.colliderect(ball_rect):
            game_over = True

    # if time elapsed more than 0.5 second
    # then add another dollar
    if cnt >= 10:
        cnt = 0
        last_time = this_time
        dollar_body = pygame.image.load("pic/dollar.png")
        dollar_body = pygame.transform.scale(dollar_body, (40, 40))
        dollar_rect = dollar_body.get_rect()
        dollar_rect.right = width
        dollar_rect.top = random.randint(0, height - dollar_rect.height)
        dollar = {"body": dollar_body, "rect": dollar_rect}
        dollar_list.append(dollar)

    for dollar in dollar_list:
        dollar_rect = dollar["rect"]
        if dollar_rect.left < 0:
            dollar_list.remove(dollar)
        else:
            dollar["rect"] = dollar_rect.move(-1, 0)
            screen.blit(dollar["body"], dollar["rect"])

        if bird_rect.colliderect(dollar_rect):
            scores += 100
            dollar_list.remove(dollar)

    if game_over:
        font = pygame.font.SysFont("YaHei", 60)
        str_tip = "Final: %s" % scores
        font_color = (200, 30, 30)
        bmp_game_over = font.render(str_tip, False, font_color)
        bmp_rect = bmp_game_over.get_rect()
        screen.blit(bmp_game_over, (width / 2 - bmp_rect.width / 2, height / 2 - bmp_rect.height / 2))
    else:
        font_color = (255, 255, 255)
        str_tip = "Current:%s" % scores
        font = pygame.font.SysFont("YaHei", 40)
        bmp_tips = font.render(str_tip, False, font_color)
        screen.blit(bmp_tips, (10, 10))

    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
pygame.quit()
