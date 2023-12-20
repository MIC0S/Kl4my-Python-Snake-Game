import pygame as pg
from settings import *
from random import randint
from dataclasses import dataclass


@dataclass
class Pos:
    x: int = 0
    y: int = 0


pg.init()
screen = pg.display.set_mode((SCREEN_X // TILES_X * TILES_X, SCREEN_Y // TILES_Y * TILES_Y))
pg.display.set_caption(TITLE)
clock = pg.time.Clock()

TILE_SIZE_X = SCREEN_X // TILES_X
TILE_SIZE_Y = SCREEN_Y // TILES_Y
exitGame = False
ticks = 0


# Draw Function
def draw(position, color):
    pg.draw.rect(screen, color, [position.x * TILE_SIZE_X, position.y * TILE_SIZE_Y, TILE_SIZE_X, TILE_SIZE_Y])


facing = Pos()
head = Pos()
score = 0
isOver = False
food = Pos()
tail = []
last_update_food = False
for _ in range(TILES_X * TILES_Y + 2):
    tail.append(Pos())


def check_game_end():
    global head, tail
    if head.x >= TILES_X or head.y >= TILES_Y or head.x < 0 or head.y < 0:
        return True
    for i in range(score):
        tail_cell = tail[i]
        if head.x == tail_cell.x and head.y == tail_cell.y:
            return True
    return False


def spawn_food():
    global head, tail, food
    while True:
        spawn = Pos(randint(0, TILES_X - 1), randint(0, TILES_Y - 1))
        if spawn.x == head.x and spawn.y == head.y:
            continue
        valid_spawn = True
        for i in range(score):
            tail_cell = tail[i]
            if tail_cell.x == spawn.x and tail_cell.y == spawn.y:
                valid_spawn = False
                break
        if not valid_spawn:
            continue
        food.x = spawn.x
        food.y = spawn.y
        draw(spawn, FOOD_COLOR)
        break


def game_reset():
    global facing, isOver, score, head, food, tail, last_update_food
    facing = Pos()
    head = Pos()
    score = 0
    isOver = False
    last_update_food = False
    spawn_food()


def move():
    global head, facing, isOver, last_update_food, score
    old_head = Pos(head.x, head.y)
    head.x += facing.x
    head.y += facing.y
    if check_game_end():
        isOver = True
        return
    draw(head, HEAD_COLOR)
    if last_update_food:
        last_update_food = False
        draw(old_head, TAIL_COLOR)
        tail[score] = Pos(old_head.x, old_head.y)
        score += 1
        spawn_food()
    else:
        if score > 0:
            draw(tail[0], EMPTY_COLOR)
            tail[score].x = old_head.x
            tail[score].y = old_head.y
            draw(old_head, TAIL_COLOR)
            for i in range(score):
                tail[i].x = tail[i + 1].x
                tail[i].y = tail[i + 1].y
        else:
            if facing.x != 0 or facing.y != 0:
                draw(old_head, EMPTY_COLOR)
        if food.x == head.x and food.y == head.y:
            last_update_food = True


def inputs(ev):
    global facing
    if ev.key == pg.K_w:
        facing = Pos(0, -1)
    if ev.key == pg.K_a:
        facing = Pos(-1, 0)
    if ev.key == pg.K_s:
        facing = Pos(0, 1)
    if ev.key == pg.K_d:
        facing = Pos(1, 0)


while not exitGame:
    game_reset()
    ticks = 0

    while not isOver:
        pg.display.update()
        clock.tick(FPS)
        ticks += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exitGame = True
                break
            if event.type == pg.KEYDOWN:
                inputs(event)
        if exitGame:
            break
        if ticks >= FPS / SPEED:
            ticks = 0
            move()
    for _ in range(3):
        if exitGame:
            break
        screen.fill((125, 0, 0))
        pg.display.update()
        for _ in range(FPS // 2):
            clock.tick(FPS)
        screen.fill((0, 0, 0))
        pg.display.update()
        for _ in range(FPS // 2):
            clock.tick(FPS)


pg.quit()
quit()
