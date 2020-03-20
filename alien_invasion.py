import pygame
from pygame.sprite import Group

import game_function as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """  initialize and main loop for game  """
    pygame.init()
    game_set = Settings()
    screen = pygame.display.set_mode((game_set.screen_width, game_set.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(game_set, screen, "Play")
    stats = GameStats(game_set)
    sb = Scoreboard(game_set, screen, stats)
    ship = Ship(game_set, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(game_set, screen, ship, aliens)
    while True:
        gf.check_events(game_set, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update_pos()
            gf.update_bullets(game_set, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(game_set, stats, sb, ship, screen, aliens, bullets)
        gf.update_screen(game_set, screen, stats, sb, ship, aliens, bullets, play_button)


if __name__ == "__main__":
    run_game()
