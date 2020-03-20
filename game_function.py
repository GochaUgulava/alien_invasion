import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_events(game_set, screen, stats, sb, play_button, ship, aliens, bullets):
    """ handle events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, game_set, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_set, screen, ship, stats, sb, aliens,
                              bullets, play_button, mouse_x, mouse_y)


def check_play_button(game_set, screen, ship, stats, sb, aliens,
                      bullets, play_button, mouse_x, mouse_y):
    """ initialize new game when play button pushed """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        game_set.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(game_set, screen, ship, aliens)
        ship.center_ship()


def check_keydown_event(event, game_set, screen, ship, bullets):
    """ handle key down event"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_set, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_event(event, ship):
    """  handle key uo events  """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(game_set, screen, stats, sb, ship, aliens, bullets, play_button):
    """ updates display after each iteration of main loop"""
    screen.fill(game_set.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def fire_bullet(game_set, screen, ship, bullets):
    """  shot bullet from ship if there are bullet limits """
    if len(bullets) < game_set.bullets_allowed:
        new_bullet = Bullet(game_set, screen, ship)
        bullets.add(new_bullet)


def update_bullets(game_set, screen,  stats, sb, ship, aliens, bullets):
    """ move bullet, remove it if is out of screen top and call check collision"""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(game_set, screen,  stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(game_set, screen, stats, sb, ship, aliens, bullets):
    """   check bullets collisions with aliens, if there are no aliens starts new level"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, 1, 1)
    if collisions:
        for aliens in collisions.values():
            stats.score += game_set.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        game_set.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(game_set, screen, ship, aliens)


def create_fleet(game_set, screen, ship, aliens):
    """ create fleet from aliens """
    alien = Alien(game_set, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(game_set, alien_width)
    number_rows = get_number_rows(game_set, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_set, screen, aliens, alien_number, row_number)


def get_number_aliens_x(game_set, alien_width):
    """  calculate how many aliens fit on screen width  """
    available_space_x = game_set.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_set, ship_height, alien_height):
    """  calculate how many aliens fit on screen height  """
    available_space_y = (game_set.screen_height - game_set.free_space_y_factor
                         * alien_height - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_set, screen, aliens, alien_number, row_number):
    """  create alien and add it into group """
    alien = Alien(game_set, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = (alien.rect.height + 30) + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)


def update_aliens(game_set, stats, sb, ship, screen, aliens, bullets):
    """  check if aliens are in screen borders and not hit ship, else call handlers"""
    check_fleet_edges(game_set, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_set, stats, sb, ship, screen, aliens, bullets)
    check_aliens_bottom(game_set, stats, sb, ship, screen, aliens, bullets)


def ship_hit(game_set, stats, sb, ship, screen, aliens, bullets):
    """  restart when hit the ship """
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(game_set, screen, ship, aliens)
        ship.center_ship()
        sleep(1.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(game_set, stats, sb, ship, screen, aliens, bullets):
    """  control if aliens reach the bottom of screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(game_set, stats, sb, ship, screen, aliens, bullets)
            break


def check_fleet_edges(game_set, aliens):
    """  hold aliens within the screen """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_set, aliens)
            break


def change_fleet_direction(game_set, aliens):
    """  change fleet direction flag  """
    for alien in aliens.sprites():
        alien.rect.y += game_set.fleet_drop_speed_factor
    game_set.fleet_direction_flag *= -1


def check_high_score(stats, sb):
    """ change high score when current score is more"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
