import pygame
from random import randrange
import sys

RES = 800
размер = 25  # Уменьшил размер ячейки для создания более плотной сетки

x, y = randrange(0, RES, размер), randrange(0, RES, размер)
яблоко = randrange(0, RES, размер), randrange(0, RES, размер)
направления = {'w': True, 's': True, 'a': True, 'd': True}
длина = 1
змея = [(x, y)]
dx, dy = 0, 0
очки = 0
fps = 15  # Увеличил FPS для более плавного движения
в_меню = True
конец_игры = False

pygame.init()
экран = pygame.display.set_mode((RES, RES))
часы = pygame.time.Clock()
шрифт_очков = pygame.font.SysFont('Arial', 26, bold=True)
шрифт_конца = pygame.font.SysFont('Arial', 20, bold=True)
шрифт_меню = pygame.font.SysFont('Arial', 50, bold=True)

def рисовать_меню():
    экран.fill(pygame.Color('blue'))
    рендер_меню = шрифт_меню.render('Игра Змейка', 1, pygame.Color('yellow'))
    экран.blit(рендер_меню, (RES // 4, RES // 3))
    pygame.display.flip()

def рисовать_меню_конца():
    экран.fill(pygame.Color('blue'))
    рендер_конец = шрифт_конца.render('Игра окончена', 1, pygame.Color('brown'))
    экран.blit(рендер_конец, (RES // 2 - 200 // 3, RES // 2))
    рендер_повтора = шрифт_очков.render('Нажмите R для повтора, Q для возврата в главное меню', 1, pygame.Color('yellow'))
    экран.blit(рендер_повтора, (RES // 4, RES // 2 + 50))
    pygame.display.flip()

def игровое_меню():
    global в_меню
    рисовать_меню()
    while в_меню:
        for событие in pygame.event.get():
            if событие.type == pygame.QUIT:
                sys.exit()
            if событие.type == pygame.KEYDOWN:
                if событие.key == pygame.K_RETURN:
                    в_меню = False

в_меню = True
игровое_меню()

while True:
    экран.fill(pygame.Color('blue'))

    for событие in pygame.event.get():
        if событие.type == pygame.QUIT:
            sys.exit()
        if not в_меню and not конец_игры:
            if событие.type == pygame.KEYDOWN:
                if событие.key == pygame.K_w and направления['w']:
                    dx, dy = 0, -1
                    направления = {'w': True, 's': False, 'a': True, 'd': True}
                elif событие.key == pygame.K_s and направления['s']:
                    dx, dy = 0, 1
                    направления = {'w': False, 's': True, 'a': True, 'd': True}
                elif событие.key == pygame.K_a and направления['a']:
                    dx, dy = -1, 0
                    направления = {'w': True, 's': True, 'a': True, 'd': False}
                elif событие.key == pygame.K_d and направления['d']:
                    dx, dy = 1, 0
                    направления = {'w': True, 's': True, 'a': False, 'd': True}
            elif событие.type == pygame.KEYDOWN and событие.key == pygame.K_q:
                в_меню = True
        elif конец_игры:
            if событие.type == pygame.KEYDOWN:
                if событие.key == pygame.K_r:
                    x, y = randrange(0, RES, размер), randrange(0, RES, размер)
                    яблоко = randrange(0, RES, размер), randrange(0, RES, размер)
                    направления = {'w': True, 's': True, 'a': True, 'd': True}
                    длина = 1
                    змея = [(x, y)]
                    dx, dy = 0, 0
                    очки = 0
                    fps = 15
                    конец_игры = False
                elif событие.key == pygame.K_q:
                    в_меню = True

    if not в_меню and not конец_игры:
        # рисуем змейку и яблоко
        for i, j in змея:
            pygame.draw.rect(экран, pygame.Color('green'), (i, j, размер, размер))
        pygame.draw.rect(экран, pygame.Color('red'), (*яблоко, размер, размер))

        # надпись
        рендер_очков = шрифт_очков.render(f'Счет: {очки}', 1, pygame.Color('yellow'))
        экран.blit(рендер_очков, (5, 5))

        # движение змейки
        x += dx * размер
        y += dy * размер
        змея.append((x, y))
        змея = змея[-длина:]

        # хаваем яблоко
        if змея[-1] == яблоко:
            яблоко = randrange(0, RES, размер), randrange(0, RES, размер)
            длина += 1
            очки += 1

        # когда соснул стенку или себе
        if x < 0 or x > RES - размер or y < 0 or y > RES - размер or len(змея) != len(set(змея)):
            конец_игры = True

        # отрисовка экрана конца игры
        if конец_игры:
            рисовать_меню_конца()

    pygame.display.flip()
    часы.tick(fps)
