import pygame
import sys
import random
from PIL import Image


class Game2:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 600, 600
        self.CELL_SIZE = 30
        self.GRID_SIZE = self.WIDTH // self.CELL_SIZE
        self.GRID_SIZEX = 1000 // self.CELL_SIZE
        self.GRID_SIZEY = self.WIDTH // self.CELL_SIZE

        # Colors
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        # Load images
        cell_width, cell_height = self.CELL_SIZE, self.CELL_SIZE

        self.player1_image = Image.open('player1.png').resize((cell_width, cell_height))
        self.player2_image = Image.open('player2.png').resize((cell_width, cell_height))
        self.cat_image = Image.open('cat.png').resize((cell_width, cell_height))
        self.wall_image = Image.open('wall.png').resize((cell_width, cell_height))
        self.background_image = Image.open('background.png').resize((1000, self.HEIGHT))

        self.player1_image = pygame.image.fromstring(self.player1_image.tobytes(), self.player1_image.size,
                                                     self.player1_image.mode)
        self.player2_image = pygame.image.fromstring(self.player2_image.tobytes(), self.player2_image.size,
                                                     self.player2_image.mode)
        self.cat_image = pygame.image.fromstring(self.cat_image.tobytes(), self.cat_image.size, self.cat_image.mode)
        self.wall_image = pygame.image.fromstring(self.wall_image.tobytes(), self.wall_image.size, self.wall_image.mode)
        self.background_image = pygame.image.fromstring(self.background_image.tobytes(), self.background_image.size,
                                                        self.background_image.mode)

        # Game variables
        self.player1_pos = [self.GRID_SIZEX // 3, self.GRID_SIZEY // 2]
        self.player2_pos = [2 * self.GRID_SIZEX // 3, self.GRID_SIZEY // 2]
        self.cat_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZEY - 1)]
        self.walls = [[random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZEY - 1)] for _ in
                      range(55)]
        self.player1_wins = 0
        self.player2_wins = 0

        menu_background_image = Image.open('green4.jpg').resize((1000, self.HEIGHT))
        menu_background_image = pygame.image.fromstring(menu_background_image.tobytes(), menu_background_image.size,
                                                        menu_background_image.mode)

        # Initialize the screen
        self.screen = pygame.display.set_mode((1000, self.HEIGHT))
        pygame.display.set_caption("Capture the Cat - 2 Players")

        # Font for displaying scores
        self.font = pygame.font.Font(None, 36)

        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def handle_movement(self):
        keys = pygame.key.get_pressed()

        # Handle player 1 movement
        if keys[pygame.K_UP] and self.player1_pos[1] > 0 and [self.player1_pos[0],
                                                              self.player1_pos[1] - 1] not in self.walls:
            self.player1_pos[1] -= 1
        if keys[pygame.K_DOWN] and self.player1_pos[1] < self.GRID_SIZE - 1 and [self.player1_pos[0],
                                                                                 self.player1_pos[
                                                                                     1] + 1] not in self.walls:
            self.player1_pos[1] += 1
        if keys[pygame.K_LEFT] and self.player1_pos[0] > 0 and [self.player1_pos[0] - 1,
                                                                self.player1_pos[1]] not in self.walls:
            self.player1_pos[0] -= 1
        if keys[pygame.K_RIGHT] and self.player1_pos[0] < self.GRID_SIZEX - 1 and [self.player1_pos[0] + 1,
                                                                                   self.player1_pos[
                                                                                       1]] not in self.walls:
            self.player1_pos[0] += 1

        # Handle player 2 movement
        if keys[pygame.K_w] and self.player2_pos[1] > 0 and [self.player2_pos[0],
                                                             self.player2_pos[1] - 1] not in self.walls:
            self.player2_pos[1] -= 1
        if keys[pygame.K_s] and self.player2_pos[1] < self.GRID_SIZE - 1 and [self.player2_pos[0], self.player2_pos[
                                                                                                       1] + 1] not in self.walls:
            self.player2_pos[1] += 1
        if keys[pygame.K_a] and self.player2_pos[0] > 0 and [self.player2_pos[0] - 1,
                                                             self.player2_pos[1]] not in self.walls:
            self.player2_pos[0] -= 1
        if keys[pygame.K_d] and self.player2_pos[0] < self.GRID_SIZEX - 1 and [self.player2_pos[0] + 1,
                                                                               self.player2_pos[1]] not in self.walls:
            self.player2_pos[0] += 1

    def move_cat(self):
        cat_moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        random.shuffle(cat_moves)
        for move in cat_moves:
            new_cat_pos = [self.cat_pos[0] + move[0], self.cat_pos[1] + move[1]]
            if 0 <= new_cat_pos[0] < self.GRID_SIZEX and 0 <= new_cat_pos[
                        1] < self.GRID_SIZE and new_cat_pos not in self.walls:
                self.cat_pos = new_cat_pos
                break

    def check_win_condition(self):
        if self.player1_wins >= self.player2_wins + 5:
            winner_text = "Player 1 Wins!"
            self.display_winner(self.player1_image, winner_text)
            self.reset_game()
        elif self.player2_wins >= self.player1_wins + 5:
            winner_text = "Player 2 Wins!"
            self.display_winner(self.player2_image, winner_text)
            self.reset_game()

    def display_winner(self, winner_image, winner_text):
        self.screen.blit(winner_image, (0, 0))

        # Load the image for the green background
        background_image = Image.open('green4.jpg').resize((1000, self.HEIGHT))
        background_image = pygame.image.fromstring(background_image.tobytes(), background_image.size,
                                                   background_image.mode)

        self.screen.blit(background_image, (0, 0))

        # Render the winner text
        font = pygame.font.Font(None, 72)
        text = font.render(winner_text, True, self.GREEN)
        text_rect = text.get_rect(center=(1000 // 2, self.HEIGHT // 2))

        self.screen.blit(text, text_rect)

        # Create buttons
        button_rect_menu = pygame.Rect(1000 // 2 - 145, self.HEIGHT // 2 + 50, 300, 50)
        button_rect_change_mode = pygame.Rect(1000 // 2 - 145, self.HEIGHT // 2 + 120, 300, 50)
        button_rect_play_again = pygame.Rect(1000 // 2 - 145, self.HEIGHT // 2 + 190, 300, 50)

        pygame.draw.rect(self.screen, (0, 205, 0), button_rect_menu)
        pygame.draw.rect(self.screen, (255, 0, 0), button_rect_change_mode)
        pygame.draw.rect(self.screen, (0, 0, 255), button_rect_play_again)

        # Render button texts
        font = pygame.font.Font(None, 36)
        text_menu = font.render("Go Back to Menu", True, self.WHITE)
        text_change_mode = font.render("Change Game Mode", True, self.WHITE)
        text_play_again = font.render("Play Again", True, self.WHITE)

        # Blit button texts
        self.screen.blit(text_menu, (1000 // 2 - 90, self.HEIGHT // 2 + 65))
        self.screen.blit(text_change_mode, (1000 // 2 - 115, self.HEIGHT // 2 + 135))
        self.screen.blit(text_play_again, (1000 // 2 - 60, self.HEIGHT // 2 + 205))

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Check if buttons are clicked
                    if button_rect_menu.collidepoint(mouse_pos):
                        from main import OptionsPage
                        menu = OptionsPage()
                        menu.run()
                        pygame.quit()
                        sys.exit()

                    elif button_rect_change_mode.collidepoint(mouse_pos):
                        from cat1 import Game1
                        game1 = Game1()
                        game1.run()

                    elif button_rect_play_again.collidepoint(mouse_pos):
                        game1 = Game2()
                        game1.run_game()

            pygame.time.Clock().tick(30)

    def reset_game(self):
        self.player1_pos = [self.GRID_SIZE // 3, self.GRID_SIZE // 2]
        self.player2_pos = [2 * self.GRID_SIZE // 3, self.GRID_SIZE // 2]
        self.cat_pos = [random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.walls = [[random.randint(0, self.GRID_SIZE - 1), random.randint(0, self.GRID_SIZE - 1)] for _ in range(15)]

    def run_game(self):
        while True:
            self.handle_events()
            self.handle_movement()
            self.move_cat()

            # Check if either player caught the cat
            if self.player1_pos == self.cat_pos:
                self.player1_wins += 1
                print("Player 1 caught the cat!")
                self.reset_game()

            elif self.player2_pos == self.cat_pos:
                self.player2_wins += 1
                print("Player 2 caught the cat!")
                self.reset_game()

            # Draw the background
            self.screen.blit(self.background_image, (0, 0))

            # Draw the walls
            for wall in self.walls:
                self.screen.blit(self.wall_image, (wall[0] * self.CELL_SIZE, wall[1] * self.CELL_SIZE))

            # Draw Player 1
            self.screen.blit(self.player1_image,
                             (self.player1_pos[0] * self.CELL_SIZE, self.player1_pos[1] * self.CELL_SIZE))

            # Draw Player 2
            self.screen.blit(self.player2_image,
                             (self.player2_pos[0] * self.CELL_SIZE, self.player2_pos[1] * self.CELL_SIZE))

            # Draw the cat
            self.screen.blit(self.cat_image, (self.cat_pos[0] * self.CELL_SIZE, self.cat_pos[1] * self.CELL_SIZE))

            # Display scores
            score_text1 = self.font.render(f"Player 1 Wins: {self.player1_wins}", True, self.WHITE)
            score_text2 = self.font.render(f"Player 2 Wins: {self.player2_wins}", True, self.WHITE)
            self.screen.blit(score_text1, (10, 10))
            self.screen.blit(score_text2, (10, 50))

            self.check_win_condition()

            pygame.display.flip()
            self.clock.tick(10)  # Adjust the speed of the game


# Run the game
game = Game2()
game.run_game()
