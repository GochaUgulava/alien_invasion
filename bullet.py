import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ class for bullet """
    def __init__(self, game_set, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, game_set.bullet_width, game_set.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = game_set.bullet_color
        self.speed = game_set.bullet_speed

    def update(self):
        """  bullet move  """
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        """ drawing bullet """
        pygame.draw.rect(self.screen, self.color, self.rect)
