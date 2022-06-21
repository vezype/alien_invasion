from pygame.mixer import music
import pygame


class Sounds:
    """Класс для управления звуками в игре."""

    def __init__(self, ai_game):
        """Инициализация звуков."""
        self.settings = ai_game.settings

        self.path_background_game = 'sounds/Brian Tyler - Battle Los Angeles Main Titles.mp3'
        self.path_background_pause = 'sounds/Brian Tyler - We Are Still Here.mp3'

        self.shot_sound = pygame.mixer.Sound('sounds/shot.wav')
        self.boom_sound = pygame.mixer.Sound('sounds/boom.wav')
        self.huston_sound = pygame.mixer.Sound('sounds/hyuston-u-nas-problema.wav')

    def start_background_game(self):
        """Загружает и запускает фоновую песню в момент игры."""
        music.load(self.path_background_game)
        music.set_volume(self.settings.music_volume)
        music.play(loops=-1)

    def start_background_pause(self):
        """Загружает и запускает фоновую песню в паузы."""
        music.load(self.path_background_pause)
        music.set_volume(self.settings.music_volume)
        music.play(loops=-1)

    def shot(self):
        """Звук выстрела."""
        self.shot_sound.set_volume(self.settings.shot_volume)
        self.shot_sound.play()

    def boom(self):
        """Звука взрыва космического корабля."""
        self.boom_sound.set_volume(self.settings.boom_volume)
        self.boom_sound.play()

    def huston(self):
        """Звук, когда пришельцы доходят до края экрана или жизней больше нет!"""
        self.huston_sound.set_volume(self.settings.huston_volume)
        self.huston_sound.play()
