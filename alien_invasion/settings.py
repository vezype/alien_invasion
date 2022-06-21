class Settings:
    def __init__(self):
        """Инициализирует статические настройки игры."""
        # Экран.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Корабль.
        self.ship_limit = 3

        # Стрельба.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Пришельцы.
        self.fleet_drop_speed = 10

        # Темп ускорения игры.
        self.speedup_scale = 1.1

        # Темп роста стоимости пришельцев.
        self.score_scale = 1.5

        self.initalize_dynamic_settings()

    def initalize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 2.5
        self.bullet_speed = 3.5
        self.alien_speed = 1

        # Подсчёт очков.
        self.alien_points = 50

        self.fleet_direction = 1  # 1 - движение направо, а -1 движение налево.

    def increase_speed(self):
        """Увеличивает настройки скорости и стоимость пришельцев."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

