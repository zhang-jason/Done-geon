import pygame
import math
from Entities.entity import Entity
from os.path import join
from os.path import dirname


class Projectile(Entity):
    # Team is whether Player or Enemy used projectile, Ability is type of projectile (e.g. fireball, arrow, etc.)
    def __init__(self, startPosition, endPosition, friendly, ability, TILE_SIZE):
        super(Projectile, self).__init__()

        # Math Stuff
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.speed = 2
        self.canMove = 0
        angle = math.atan2(endPosition[1] - startPosition[1], endPosition[0] - startPosition[0])
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.x = startPosition[0]
        self.y = startPosition[1]
        self.type = friendly  # True for Friendly Projectile, false for Enemy; useful for hit detection

        self.collidable = False # with tiles
        self.damage = 1

        # Image and Animations
        self.sprites = []
        for i in range(1, 30, 1):
            image = pygame.transform.scale(pygame.image.load(
                join(dirname(dirname(__file__)), f'assets/projectiles/{ability}', f'{i}.png')), (TILE_SIZE*3//4, TILE_SIZE*3//4))
            image = pygame.transform.rotate(image, math.degrees(-angle))
            self.sprites.append(image)

        trans_image = pygame.image.load(
            join(dirname(dirname(__file__)), 'assets/projectiles/Fireball', '1.png'))
        trans_color = trans_image.get_at((0, 0))
        for x in self.sprites:
            x.set_colorkey(trans_color)

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = startPosition

    # Override
    def update(self):
        # Update Sprite Animation
        self.current_sprite += 0.05
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]

        # Update Math
