import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ class for  ship """
    def __init__(self, game_set, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.game_set = game_set
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update_pos(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_set.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_set.ship_speed
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx
