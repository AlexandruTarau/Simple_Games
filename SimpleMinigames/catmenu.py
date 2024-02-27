import pygame
import sys


class CatMenu:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 1000, 600
        self.BUTTON_WIDTH, self.BUTTON_HEIGHT = 200, 50
        self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT = 100, 30
        self.BUTTON_COLOR = (50, 205, 50)
        self.BACK_BUTTON_COLOR = (255, 0, 0)
        self.BUTTON_TEXT_COLOR = (255, 255, 255)
        self.MESSAGE_COLOR = (255, 255, 255)

        # Load background image
        self.background_image = pygame.image.load('green4.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        # Initialize the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Catch the Cat")

        # Font for button text and message
        self.font = pygame.font.Font(None, 36)

        # Initialize buttons
        self.create_buttons()

    def create_buttons(self):
        # Button for 1 Player
        self.button_1_player = pygame.Rect((self.WIDTH - self.BUTTON_WIDTH) // 2, 200, self.BUTTON_WIDTH,
                                           self.BUTTON_HEIGHT)

        # Button for 2 Players
        self.button_2_players = pygame.Rect((self.WIDTH - self.BUTTON_WIDTH) // 2, 300, self.BUTTON_WIDTH,
                                            self.BUTTON_HEIGHT)

        # Back button
        self.button_back = pygame.Rect(20, self.HEIGHT - 60, self.BACK_BUTTON_WIDTH, self.BACK_BUTTON_HEIGHT)

    def draw_buttons(self):
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.button_1_player)
        pygame.draw.rect(self.screen, self.BUTTON_COLOR, self.button_2_players)
        pygame.draw.rect(self.screen, self.BACK_BUTTON_COLOR, self.button_back)

        # Draw text on buttons
        text_1_player = self.font.render("1 Player", True, self.BUTTON_TEXT_COLOR)
        text_rect_1_player = text_1_player.get_rect(center=self.button_1_player.center)
        self.screen.blit(text_1_player, text_rect_1_player)

        text_2_players = self.font.render("2 Players", True, self.BUTTON_TEXT_COLOR)
        text_rect_2_players = text_2_players.get_rect(center=self.button_2_players.center)
        self.screen.blit(text_2_players, text_rect_2_players)

        text_back = self.font.render("Back", True, self.BUTTON_TEXT_COLOR)
        text_rect_back = text_back.get_rect(center=self.button_back.center)
        self.screen.blit(text_back, text_rect_back)

    def draw_message(self, message):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the message above the buttons
        message_text = self.font.render(message, True, self.MESSAGE_COLOR)
        message_rect = message_text.get_rect(center=(self.WIDTH // 2, 100))
        self.screen.blit(message_text, message_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_1_player.collidepoint(event.pos):
                        self.start_game(1)
                    elif self.button_2_players.collidepoint(event.pos):
                        self.start_game(2)
                    elif self.button_back.collidepoint(event.pos):
                        from main import OptionsPage
                        menu = OptionsPage()
                        menu.run()
                        pygame.quit()

            self.draw_message("Choose game mode:")
            self.draw_buttons()

            pygame.display.flip()

    def start_game(self, num_players):
        pygame.quit()

        if num_players == 1:
            from cat1 import Game1
            game = Game1()
            game.run()
        elif num_players == 2:
            from cat2 import Game2
            game = Game2()
            game.run_game()


# Run the main menu
main_menu = CatMenu()
main_menu.run()
