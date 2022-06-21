from pygame.mixer import music


class Sounds:
    """Класс для управления звуками в игре."""

    def __init__(self):
        """Инициализация звуков."""
        self.path_background_game = 'sounds/Brian Tyler - Battle Los Angeles Main Titles.mp3'
        self.path_background_pause = 'sounds/Brian Tyler - We Are Still Here.mp3'

    def start_background_game(self):
        """Загружает и запускает фоновую песню в момент игры."""
        music.load(self.path_background_game)
        music.set_volume(0.1)
        music.play(loops=-1)

    def start_background_pause(self):
        """Загружает и запускает фоновую песню в паузы."""
        music.load(self.path_background_pause)
        music.set_volume(0.15)
        music.play(loops=-1)
