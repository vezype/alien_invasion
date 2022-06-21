class Settings:
    def __init__(self):
        # Экран.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Корабль.
        self.ship_speed = 2.5
        self.ship_limit = 3

        # Стрельба.
        self.bullet_speed = 3.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Пришельцы.
        self.alien_speed = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 - движение направо, а -1 движение налево.
