import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos_x, self.pos_y = pos_x, pos_y

    def move(self, motion):
        if motion == 'left' and self.pos_x - 1 > -1 and \
                level_map[self.pos_y][self.pos_x - 1] != '#':
            self.rect.x -= tile_width
            self.pos_x -= 1
        elif motion == 'right' and self.pos_x + 1 < len(level_map[0]) and \
                level_map[self.pos_y][self.pos_x + 1] != '#':
            self.rect.x += tile_width
            self.pos_x += 1
        elif motion == 'up' and self.pos_y - 1 > -1 and \
                level_map[self.pos_y - 1][self.pos_x] != '#':
            self.rect.y -= tile_height
            self.pos_y -= 1
        elif motion == 'down' and self.pos_y + 1 < len(level_map) and \
                level_map[self.pos_y + 1][self.pos_x] != '#':
            self.rect.y += tile_height
            self.pos_y += 1


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x + 1, y + 1


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    intro_text = ["Заставка", "",
                  "Перемещение",
                  "героя"]
    font = pygame.font.Font(None, 30)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = 50
level_name = input('Введите имя файла с уровнем\n')
running = True
try:
    level_map = load_level(level_name)
    player, level_x, level_y = generate_level(load_level(level_name))

    pygame.init()
    size = width, height = tile_width * level_x, tile_height * level_y
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Mario')
    start_screen()
except FileNotFoundError:
    print(f"Файл с картой уровня '{level_name}' не найден")
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move('left')
            elif event.key == pygame.K_RIGHT:
                player.move('right')
            elif event.key == pygame.K_UP:
                player.move('up')
            elif event.key == pygame.K_DOWN:
                player.move('down')
    player_group.update()
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()