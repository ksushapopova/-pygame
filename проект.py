import os
import pygame
import sys
import random


def load_image(name, color_key=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_color_key(color_key)
    else:
        image = image.convert_alpha()

    return image


class Play(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.width = size[0]
        self.height = 50
        self.image = load_image("10.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (0, 400)
        self.step = 30

    def update(self, *args):
        if self.rect.left < 650:
            self.rect.left += self.step


def terminate():
    pygame.quit()
    sys.exit()


def main():
    size = 1500, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maze')
    fon = pygame.transform.scale(load_image('fone.jpg'), (size[0], size[1]))
    screen.blit(fon, (0, 0))
    all_sprites = pygame.sprite.Group()
    Play(all_sprites, size)
    fps = 10
    clock = pygame.time.Clock()
    mp = pygame.mouse.get_pos()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                return

        fon = pygame.transform.scale(load_image('fone.jpg'), (size[0], size[1]))
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()


PINK = (230, 150, 215)
WHITE = (255, 255, 255)
BLUE = (30, 35, 75)


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800
FPS = 40


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img='cat.png'):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0
        self.walls = None

        self.coins = None
        self.collected_coins = 0

        self.enemies = pygame.sprite.Group()
        self.alive = True

    def update(self):
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        coins_hit_list = pygame.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.collected_coins += 1
            coin.kill()

        # if pygame.sprite.spritecollideany(self, self.enemies, False):
            # self.alive = False


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img='crocodile.png'):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direction = -1

    def update(self):
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        self.rect.x += self.direction * 2


pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Maze')

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall_coords = [
    [0, 0, 10, 600],
    [790, 0, 10, 600],
    [10, 0, 790, 10],
    [0, 200, 100, 10],
    [0, 590, 600, 10],
    [450, 400, 10, 200],
    [550, 450, 250, 10]
]
for coord in wall_coords:
    wall = Wall(coord[0], coord[1], coord[2], coord[3])
    wall_list.add(wall)
    all_sprite_list.add(wall)

coins_list = pygame.sprite.Group()
coins_coord = [[100, 140], [236, 50], [400, 234]]

for coord in coins_coord:
    coin = Coin(coord[0], coord[1])
    coins_list.add(coin)
    all_sprite_list.add(coin)

enemies_list = pygame.sprite.Group()
enemies_coord = [[10, 500], [400, 50]]

for coord in enemies_coord:
    enemy = Enemy(coord[0], coord[1])
    enemies_list.add(enemy)
    all_sprite_list.add(enemy)


player = Player(50, 50)
player.walls = wall_list
all_sprite_list.add(player)

player.coins = coins_list

player.enemies = enemies_list

font = pygame.font.SysFont('Arial', 24, True)
text = font.render('Game over', True, WHITE)
text_vin = font.render('Winner', True, WHITE)

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.change_x = -3
            elif event.key == pygame.K_RIGHT:
                player.change_x = 3
            elif event.key == pygame.K_UP:
                player.change_y = -3
            elif event.key == pygame.K_DOWN:
                player.change_y = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.change_x = 0
            elif event.key == pygame.K_RIGHT:
                player.change_x = 0
            elif event.key == pygame.K_UP:
                player.change_y = 0
            elif event.key == pygame.K_DOWN:
                player.change_y = 0

    screen.fill(PINK)

    if not player.alive:
        screen.blit(text, (100, 100))
    else:
        all_sprite_list.update()
        all_sprite_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()