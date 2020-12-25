import pygame
import os


pygame.init()
size = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Инициализация игры')
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)


def load_image(name, color_key=None):
    fullname = os.path.join('data1', name)
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


class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Lab1(object):
    wall_list = None
    enemy_sprites = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()


class FirstLvl(Lab1):
    def __init__(self):
        super().__init__()

        walls = [[0, 0, 20, 100, PURPLE],
                 [0, 200, 20, 600, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                 ]

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        for x in range(0, 900, 200):
            for y in range(0, 550, 300):
                x += 110
                wall = Wall(x, y, 10, 400, PURPLE)
                self.wall_list.add(wall)


def main():
    pygame.init()
    rooms = []
    room = FirstLvl()
    rooms.append(room)
    current_room_no = 0
    current_room = rooms[current_room_no]
    all_sprites = pygame.sprite.Group()
    hero = pygame.sprite.Sprite(all_sprites)
    hero.image = load_image('coin.png')
    hero.rect = hero.image.get_rect()
    step = 10

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                hero.rect.top += step
            elif key[pygame.K_UP]:
                hero.rect.top -= step
            elif key[pygame.K_RIGHT]:
                hero.rect.left += step
            elif key[pygame.K_LEFT]:
                hero.rect.left -= step


        screen.fill((255, 182, 193))
        all_sprites.draw(screen)
        current_room.wall_list.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
