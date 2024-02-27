import pygame
from pygame.locals import *
import time


class Button:
    BUTTON_SIZE = (120, 120)

    def __init__(self, image_path, row, col):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, self.BUTTON_SIZE)
        self.rect = self.image.get_rect()

        total_width = 5 * (self.BUTTON_SIZE[0] + 20)
        total_height = 1 * (self.BUTTON_SIZE[1] + 20)

        start_x = (1000 - total_width) // 2
        start_y = (600 - total_height) // 2

        self.rect.topleft = (start_x + col * (self.BUTTON_SIZE[0] + 20), start_y + row * (self.BUTTON_SIZE[1] + 20))
        self.clicked = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class MainPage:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 600
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Minigames")
        self.background_image = pygame.image.load("bb.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.font = pygame.font.Font(None, 36)

        self.input_text = ""
        self.input_active = False
        self.message_text = ""
        self.message_surface = None
        self.name_submitted = False
        self.greeting_timer = None
        self.options_timer = None

        self.buttons = [
            Button("ball2.png", 0, 0),
            Button("archer.png", 0, 1),
            Button("cat2.png", 0, 2),
            Button("mine.png", 0, 3),
            Button("wordle.png", 0, 4)
        ]

    def show_options(self):
        self.surface.blit(self.background_image, (0, 0))
        options_text_surface = self.font.render("What do you want to play today?", True,
                                                (255, 255, 255))
        options_text_rect = options_text_surface.get_rect(center=(self.width // 2, 50))
        self.surface.blit(options_text_surface, options_text_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    for index, button in enumerate(self.buttons):
                        if button.is_clicked(event.pos):
                            # Check which button is clicked
                            if index == 0:
                                from football import Game
                                game1 = Game()
                                game1.run()

                            if index == 1:
                                from turtle import Main
                                game1 = Main()
                                game1.run()

                            if index == 2:
                                from catmenu import CatMenu
                                game1 = CatMenu()
                                game1.run()

                            if index == 3:
                                import minesweeper
                                minesweeper.run_game()

                            if index == 4:
                                import tkinter as tk
                                from wordle import WordleApp
                                options_root = tk.Tk()
                                options_root.destroy()
                                wordle_root = tk.Tk()
                                wordle_game = WordleApp(wordle_root)
                                wordle_root.mainloop()
                                wordle_game.reset_game()
                                wordle_root.destroy()

        for button in self.buttons:
            button.draw(self.surface)

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            self.surface.blit(self.background_image, (0, 0))

            if not self.name_submitted:
                static_text_surface = self.font.render("Hello player! Please enter your name:", True,
                                                       (255, 255, 255))
                static_text_rect = static_text_surface.get_rect(center=(self.width // 2, 50))
                self.surface.blit(static_text_surface, static_text_rect)

                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                        elif event.key == K_RETURN:
                            self.message_text = f'Hello, {self.input_text}!'
                            self.message_surface = self.font.render(self.message_text, True,
                                                                    (255, 255, 255))
                            self.input_text = ""
                            self.name_submitted = True
                            self.greeting_timer = time.time()  # Start the greeting timer
                        elif event.key == K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            self.input_text += event.unicode

                color = (0, 0, 0) if self.input_active else (255, 255, 255)
                pygame.draw.rect(self.surface, color, (100, 80, 800, 40), 2)
                input_surface = self.font.render(self.input_text, True, (255, 255, 255))
                self.surface.blit(input_surface, (110, 85))
            else:
                if self.greeting_timer is not None and time.time() - self.greeting_timer < 2:
                    self.surface.blit(self.message_surface,
                                      (self.width // 2 - self.message_surface.get_width() // 2, 50))
                else:
                    self.show_options()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            pygame.time.Clock().tick(30)


class OptionsPage:
    def __init__(self):
        pygame.init()
        self.width = 1000
        self.height = 600
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mini Games")
        self.background_image = pygame.image.load("bb.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.font = pygame.font.Font(None, 36)

        self.buttons = [
            Button("ball2.png", 0, 0),
            Button("archer.png", 0, 1),
            Button("cat2.png", 0, 2),
            Button("mine.png", 0, 3),
            Button("wordle.png", 0, 4)
        ]

    def run(self):
        running = True

        while running:
            self.surface.blit(self.background_image, (0, 0))

            options_text_surface = self.font.render("What would you like to play today?", True,
                                                    (255, 255, 255))
            options_text_rect = options_text_surface.get_rect(center=(self.width // 2, 50))
            self.surface.blit(options_text_surface, options_text_rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for index, button in enumerate(self.buttons):
                            if button.is_clicked(event.pos):  # Check if the button is clicked
                                if index == 0:  # Football game
                                    from football import Game
                                    game = Game()
                                    game.run()
                                elif index == 1:  # Archer game
                                    from turtle import Main
                                    game = Main()
                                    game.run()
                                elif index == 2:  # Cat game
                                    from catmenu import CatMenu
                                    game = CatMenu()
                                    game.run()
                                elif index == 3:  # Minesweeper
                                    import minesweeper
                                    minesweeper.run_game()
                                elif index == 4:  # Wordle
                                    import tkinter as tk
                                    from wordle import WordleApp
                                    options_root = tk.Tk()
                                    options_root.destroy()
                                    wordle_root = tk.Tk()
                                    wordle_game = WordleApp(wordle_root)
                                    wordle_root.mainloop()
                                    wordle_game.reset_game()
                                    wordle_root.destroy()

            for button in self.buttons:
                button.draw(self.surface)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            pygame.time.Clock().tick(30)


if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()
