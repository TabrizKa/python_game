import pygame
from random import randint as ri

timer= pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((1700 , 900)) # размеры окна
pygame.display.set_caption("My Demon") # название игры
icon= pygame.image.load('images/main_pic.png') #добавляем картинку в программу
pygame.display.set_icon(icon)

score=0
myfont=pygame.font.Font('font/BrokenConsoleBold.ttf', 60)
menufont=pygame.font.Font('font/BrokenConsoleBold.ttf', 55)
menutext=menufont.render('press "ENTER" to start game',True, 'White')
bg= pygame.image.load('images/bg.png').convert() #фон
bg_x=0
#изображения спрайта для анимации движения
walk_right= [pygame.image.load('images/herosprite/Rright1.gif').convert_alpha(),
             pygame.image.load('images/herosprite/Rright2.gif').convert_alpha(),
             pygame.image.load('images/herosprite/Rright3.gif').convert_alpha()]
hero_die=pygame.image.load('images/herosprite/Rred.gif').convert_alpha()
walk_left= [ pygame.image.load('images/herosprite/Rleft1.gif').convert_alpha(),
             pygame.image.load('images/herosprite/Rleft2.png').convert_alpha(),
             pygame.image.load('images/herosprite/Rleft3.gif').convert_alpha()]
enemy= [ pygame.image.load('images/enemysprite/enemy1.png').convert_alpha(),
         pygame.image.load('images/enemysprite/enemy2.png').convert_alpha(),
         pygame.image.load('images/enemysprite/enemy3.png').convert_alpha()]
enemy_die=[ pygame.image.load('images/enemysprite/die1.png').convert_alpha(),
         pygame.image.load('images/enemysprite/die2.png').convert_alpha(),
         pygame.image.load('images/enemysprite/die3.png').convert_alpha()]
enemy_x=1720
enemy_list=[]
fireball= [pygame.image.load('images/fireballs/fr1.png'),
pygame.image.load('images/fireballs/fr2.png'),
pygame.image.load('images/fireballs/fr3.png'),
]
fireballs=[]
hero_speed = 20
hero_x= 100
hero_y=550
jumping= False
jumping_height = 14 #высота прыжка
animate_count=0
menu= True
running = False
#музыка
if menu ==True:
    bg_menu_sound = pygame.mixer.Sound('music/menu.wav')
    bg_menu_sound.play(-1)
#меню
while menu:
    screen.blit(bg, (bg_x, 0))  # прорисовка фона  #для бесконечного фона
    screen.blit(bg, (bg_x + 1700, 0))
    screen.blit(menutext, (400, 550))
    if bg_x <= -1700:
        bg_x = 0

    menu_key = pygame.key.get_pressed()
    if menu_key[pygame.K_RETURN]:
        running = True
        pygame.mixer.stop()
        menu = False

    pygame.display.update()
    for event in pygame.event.get():  # чтобы окно закрывалось
        if event.type == pygame.QUIT:
            menu = False
            pygame.quit()
if running== True:
    bg_sound = pygame.mixer.Sound('music/main.wav')
    bg_sound.play(-1)
while running:
    timer.tick(10) #скорость анимации
    keys = pygame.key.get_pressed()

    screen.blit(bg, (bg_x,0)) #прорисовка фона  #для бесконечного фона
    screen.blit(bg, (bg_x + 1700, 0))
    #система очков
    score_text = myfont.render('SCORE: ' + str(score), True, 'White')
    score += 1
    screen.blit(score_text, (1300, 25))
    # условные текстуры для героя
    hero_rect = walk_left[0].get_rect(topleft=(hero_x, hero_y))
    # рисуем врагов
    chek = ri(0,30) # чем меньше диапазон, тем чаще будут появляться враги
    if chek == 1: # здесь должно быть чисто в заданном диапазоне ri()
        enemy_list.append(enemy[animate_count].get_rect(topleft=(enemy_x,550)))
    if enemy_list:
        for (i, i_idx) in enumerate(enemy_list):
            screen.blit(enemy[animate_count], i_idx) #рисуем врага
            i_idx.x -= 15  # анимация движения врагов
            if i_idx.x < 0: #исчезновение врагов за пределами игры
                enemy_list.pop(i)

            # реация при соприкосновении
            if hero_rect.colliderect(i_idx):
                screen.blit(hero_die, (hero_x, hero_y))  # игрок во время смерти
                end_of_game = True
                while end_of_game:
                    end_text = myfont.render('you lose', True, 'White')
                    end_sc_text = myfont.render('your score: ' + str(score), True, 'White')
                    screen.blit(end_text, (690, 300))
                    screen.blit(end_sc_text, (600, 400))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    pygame.display.update()

    # реакция на нажатие кнопок
    if keys[pygame.K_LEFT]:
        screen.blit(walk_left[animate_count], (hero_x, hero_y))
    else:
        screen.blit(walk_right[animate_count], (hero_x, hero_y))
    #реализация снарядов
    if keys[pygame.K_SPACE]:
        fireballs.append(fireball[animate_count].get_rect(topleft=(hero_x+150,hero_y+20)))
    if fireballs:
        for (d,fireball_index) in enumerate(fireballs):
            screen.blit(fireball[animate_count],fireball_index)
            fireball_index.x += 40
            if fireball_index.x > 1701:  # исчезновение патрона за пределами игры
                fireballs.pop(d)
            if enemy_list:
                for (d2,enemy_idx) in enumerate(enemy_list):
                    if fireball_index.colliderect(enemy_idx):  #смерть врагов
                        score += 100
                        screen.blit(enemy_die[animate_count],enemy_idx) #анимация смерти врагов
                        fireballs.pop(d)
                        enemy_list.pop(d2)

    if keys[pygame.K_LEFT] and hero_x > 20:
        hero_x -= hero_speed
    elif keys[pygame.K_RIGHT] and hero_x < 1500:
        hero_x += hero_speed
    # анимация прыжка
    if not jumping:
        if keys[pygame.K_UP]:
            jumping = True
    else:
        if jumping_height >= -14:
            if jumping_height > 0:
                hero_y -= (jumping_height ** 2) / 2
            else:
                hero_y += (jumping_height ** 2) / 2
            jumping_height -= 2
        else:
            jumping = False
            jumping_height = 14
    #пауза в игре
    if keys[pygame.K_p]:
        paused = True
        while paused:
            screen.blit(menutext, (420, 400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused = False
            pygame.display.update()
            timer.tick(1000)
#анимация движения всех персонажей
    if animate_count == 2:
        animate_count = 0
    else:
        animate_count += 1
    #скорость движения фона
    bg_x -= 11
    if bg_x <= -1700:
        bg_x = 0

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # чтобы окно закрывалось
            running = False
            pygame.quit()





