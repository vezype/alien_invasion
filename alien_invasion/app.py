import pygame

import sys
from time import sleep

from settings import Settings
from game_stats import GameStats
from button import Button

import ship
import bullet
import alien


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN
        )
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption('Инопланетное вторжение. Часть 1.')

        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)

        self.ship = ship.Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Играть.
        self.play_button = Button(self, 'Play')

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left.
            self.stats.ships_left -= 1

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал между соседними пришельцами равен ширине пришельца.
        new_alien = alien.Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size
        available_space_x = self.settings.screen_width - (2 * new_alien_width)
        number_aliens_x = available_space_x // (2 * new_alien_width)

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * new_alien_height) - ship_height)
        number_rows = available_space_y // (2 * new_alien_height)

        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        new_alien = alien.Alien(self)
        new_alien_width, new_alien_height = new_alien.rect.size
        new_alien.x = new_alien_width + 2 * new_alien_width * alien_number
        new_alien.rect.x = new_alien.x
        new_alien.rect.y = new_alien.rect.height + 2 * new_alien.rect.height * row_number
        self.aliens.add(new_alien)

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = bullet.Bullet(self)
            self.bullets.add(new_bullet)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(
            self.settings.bg_color  # При каждом проходе цикла перерисовывается экран.
        )
        self.ship.blitme()

        for bullet_now in self.bullets.sprites():
            bullet_now.draw_bullet()
        self.aliens.draw(self.screen)

        # Кнопка Играть отображает в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  # Отображение последнего прорисованного экрана.

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые."""
        # Обновление позиции снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet_now in self.bullets.copy():
            if bullet_now.rect.bottom <= 0:
                self.bullets.remove(bullet_now)

        self._check_bullet_allien_collisions()

    def _check_bullet_allien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Проверка попаданий в пришельцев.
        # При обнаружении попадания удаляем пришельца и пулю.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Уничтожение существующих снарядом и создание нового флота.
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """
        Проверяет, достиг ли флот края экрана, с последующим
        обновлением позиций всех пришельцев во флоте.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельец края экрана."""
        for current_alien in self.aliens.sprites():
            if current_alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление."""
        for current_alien in self.aliens.sprites():
            current_alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for current_alien in self.aliens.sprites():
            if current_alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же самое, что и при столкновении с кораблём.
                self._ship_hit()
                break

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
