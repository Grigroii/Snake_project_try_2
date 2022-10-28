import pygame
import sys
import random
import pygame_menu

pygame.init()
SIZE_BLOCK = 20  # размер блока
FRAME_COLOR = (0, 255, 204)  # цвет фоновый
WHITE = (255, 255, 255)
RED = (224, 0, 0)
BLUE = (204, 255, 255)
COUNT_BLOCKS = 20  # количество блоков
SNAKE_COLOR = (0, 102, 0) # цвет змейки
HEADER_COLOR = (0, 204, 152) # цвет верхней части где находится счёт и скорость
HEADER_MARGIN = 70 # отступ верхней части
MARGIN = 1

size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN] #размер игрового поля

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def get_random_empty_block():# получение рандомного блока , то есть яблока
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.Y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block


def draw_block(color, row, column):# функция рисующая поле
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN * (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK, SIZE_BLOCK])


snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]# наша змейка
apple = SnakeBlock(2, 5) #яблоко
d_row = buf_row = 0
d_col = buf_col = 1
total = 0
speed = 1

while True:

    for ev in pygame.event.get():# проверка , куда двигается змейка при нажатии клавиш
        if ev.type == pygame.QUIT:
            pygame.quit()
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP and d_col != 0:
                buf_row = -1
                buf_col = 0
            elif ev.key == pygame.K_DOWN and d_col != 0:
                buf_row = 1
                buf_col = 0
            elif ev.key == pygame.K_RIGHT and d_row != 0:
                buf_row = 0
                buf_col = 1
            elif ev.key == pygame.K_LEFT and d_row != 0:
                buf_row = 0
                buf_col = -1

    screen.fill(FRAME_COLOR)
    pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

    text_total = courier.render(f"Total: {total}", 5, WHITE)
    text_speed = courier.render(f"Speed: {speed}", 5, WHITE)
    screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
    screen.blit(text_speed, (SIZE_BLOCK + 250, SIZE_BLOCK))

    for row in range(COUNT_BLOCKS):# цикл для создания нашего игрового поля
        for column in range(COUNT_BLOCKS):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = WHITE
            draw_block(color, row, column)

    head = snake_blocks[-1]
    if not head.is_inside(): #проверка чтобы змейка не выходила за границы игрового поля
        pygame.quit()
        sys.exit()

    draw_block(RED, apple.x, apple.y)
    for block in snake_blocks:
        draw_block(SNAKE_COLOR, block.x, block.y)

    pygame.display.flip()


    if apple == head: # проверка для функционала нашей змейки
        total += 1
        speed = total // 5 + 1

        snake_blocks.append(apple)
        apple = get_random_empty_block()
    d_row = buf_row
    d_col = buf_col
    new_head = SnakeBlock(head.x + d_row, head.y + d_col)

    if new_head in snake_blocks: #проверка чтобы при столкновении змейки со своим телом игра заканчивалась
        pygame.quit()
        sys.exit()

    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    timer.tick(3 + speed)
