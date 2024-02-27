import pygame
import sys
import random
from PIL import Image


class Player:
    def __init__(self, image_path, initial_pos):
        self.image = pygame.image.load(image_path)
        self.pos = initial_pos


class Game1:
    def __init__(self):
        pygame.init()

        # Constants
        self.WIDTH, self.HEIGHT = 600, 600
        self.CELL_SIZE = 30
        self.GRID_SIZE = self.WIDTH // self.CELL_SIZE
        self.GRID_SIZEX = 1000 // self.CELL_SIZE

        # Colors
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 165, 0)

        # Load images
        cell_width, cell_height = self.CELL_SIZE, self.CELL_SIZE

        self.player_image = Image.open('player1.png').resize((cell_width, cell_height))
        self.cat_image = Image.open('cat.png').resize((cell_width, cell_height))
        self.obstacle_image = Image.open('player2.png').resize((cell_width, cell_height))
        self.wall_image = Image.open('wall.png').resize((cell_width, cell_height))
        self.background_image = Image.open('background.png').resize((1000, 600))

        # Convert PIL images to Pygame surfaces
        self.player_image = pygame.image.fromstring(self.player_image.tobytes(), self.player_image.size,
                                                    self.player_image.mode)
        self.cat_image = pygame.image.fromstring(self.cat_image.tobytes(), self.cat_image.size, self.cat_image.mode)
        self.obstacle_image = pygame.image.fromstring(self.obstacle_image.tobytes(), self.obstacle_image.size,
                                                      self.obstacle_image.mode)
        self.wall_image = pygame.image.fromstring(self.wall_image.tobytes(), self.wall_image.size, self.wall_image.mode)
        self.background_image = pygame.image.fromstring(self.background_image.tobytes(), self.background_image.size,
                                                        self.background_image.mode)

        # Game variables
        self.player = Player('player1.png', [self.GRID_SIZE // 2, self.GRID_SIZE // 2])
        self.cat_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.obstacle1_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.obstacle2_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.walls = [[random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)] for _ in
                      range(55)]
        self.score = 0
        self.opponent_score = 0

        # Initialize the screen
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Catch the Cat - 1 Player")

    def reset_game(self):
        self.player.pos = [self.GRID_SIZEX // 2, self.GRID_SIZE // 2]
        self.cat_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.obstacle1_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.obstacle2_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
        self.walls = [[random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)] for _ in
                      range(55)]
        self.score = 0
        self.opponent_score = 0

    def check_win(self):
        return self.score >= 5

    def check_loss(self):
        return self.opponent_score >= 1

    def display_message(self, message, image_path, text_color):
        # Load the image for the background
        background_image = Image.open("green4.jpg").resize((1000, self.HEIGHT))
        background_image = pygame.image.fromstring(background_image.tobytes(), background_image.size,
                                                   background_image.mode)

        self.screen.blit(background_image, (0, 0))

        # Render the message text
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, text_color)
        text_rect = text.get_rect(center=(1000 // 2, self.HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)

        # Create buttons
        center_x = 1000 // 2
        center_y = self.HEIGHT // 2

        # Calculate positions for buttons
        button_width = 300
        button_height = 50
        button_spacing = 22

        button_rect_menu = pygame.Rect(center_x - button_width // 2, center_y + button_spacing, button_width,
                                       button_height)
        button_rect_change_mode = pygame.Rect(center_x - button_width // 2,
                                              center_y + 2 * button_spacing + button_height,
                                              button_width, button_height)
        button_rect_play_again = pygame.Rect(center_x - button_width // 2,
                                             center_y + 3 * button_spacing + 2 * button_height, button_width,
                                             button_height)

        pygame.draw.rect(self.screen, (0, 205, 0), button_rect_menu)
        pygame.draw.rect(self.screen, (255, 165, 0), button_rect_change_mode)
        pygame.draw.rect(self.screen, (0, 0, 255), button_rect_play_again)

        font = pygame.font.Font(None, 36)
        text_menu = font.render("Go Back to Menu", True, (255, 255, 255))
        text_change_mode = font.render("Change Game Mode", True, (255, 255, 255))
        text_play_again = font.render("Play Again", True, (255, 255, 255))

        # Center the text on the buttons
        text_rect_menu = text_menu.get_rect(center=button_rect_menu.center)
        text_rect_change_mode = text_change_mode.get_rect(center=button_rect_change_mode.center)
        text_rect_play_again = text_play_again.get_rect(center=button_rect_play_again.center)

        self.screen.blit(text_menu, text_rect_menu.topleft)
        self.screen.blit(text_change_mode, text_rect_change_mode.topleft)
        self.screen.blit(text_play_again, text_rect_play_again.topleft)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rect_menu.collidepoint(mouse_pos):
                        from main import OptionsPage
                        menu = OptionsPage()
                        menu.run()
                        pygame.quit()
                    elif button_rect_change_mode.collidepoint(mouse_pos):
                        pygame.quit()
                        from cat2 import Game2
                        game2 = Game2()
                        game2.run_game()
                    elif button_rect_play_again.collidepoint(mouse_pos):
                        # Play the game again
                        self.reset_game()
                        return

    def run(self):
        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.player.pos[1] > 0 and [self.player.pos[0],
                                                                 self.player.pos[1] - 1] not in self.walls:
                self.player.pos[1] -= 1
            if keys[pygame.K_DOWN] and self.player.pos[1] < self.GRID_SIZE - 1 and [self.player.pos[0], self.player.pos[
                                                                                                            1] + 1] not in self.walls:
                self.player.pos[1] += 1
            if keys[pygame.K_LEFT] and self.player.pos[0] > 0 and [self.player.pos[0] - 1,
                                                                   self.player.pos[1]] not in self.walls:
                self.player.pos[0] -= 1
            if keys[pygame.K_RIGHT] and self.player.pos[0] < self.GRID_SIZEX - 1 and [self.player.pos[0] + 1,
                                                                                      self.player.pos[
                                                                                          1]] not in self.walls:
                self.player.pos[0] += 1

            # Move the obstacles
            obstacle_moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            random.shuffle(obstacle_moves)

            for obstacle_pos in [self.obstacle1_pos, self.obstacle2_pos]:
                move = random.choice(obstacle_moves)
                new_obstacle_pos = [obstacle_pos[0] + move[0], obstacle_pos[1] + move[1]]
                if 0 <= new_obstacle_pos[0] < self.GRID_SIZEX and 0 <= new_obstacle_pos[
                    1] < self.GRID_SIZE and new_obstacle_pos not in self.walls:
                    obstacle_pos[:] = new_obstacle_pos

            # Move the cat
            cat_moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            random.shuffle(cat_moves)
            for move in cat_moves:
                new_cat_pos = [self.cat_pos[0] + move[0], self.cat_pos[1] + move[1]]
                if 0 <= new_cat_pos[0] < self.GRID_SIZEX and 0 <= new_cat_pos[
                    1] < self.GRID_SIZE and new_cat_pos not in self.walls:
                    self.cat_pos = new_cat_pos
                    break

            # Check if the player caught the cat
            if self.player.pos == self.cat_pos:
                self.score += 1
                print(f"Congratulations! You caught the cat. Score: {self.score}")
                self.cat_pos = [random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)]
                self.walls = [[random.randint(0, self.GRID_SIZEX - 1), random.randint(0, self.GRID_SIZE - 1)] for _ in
                              range(55)]

            # Check if the cat or an obstacle caught the player
            if self.player.pos == self.cat_pos or self.player.pos in [self.obstacle1_pos, self.obstacle2_pos]:
                self.opponent_score += 1
                print(
                    f"The cat or an obstacle caught you. Your Score: {self.score}, Opponent Score: {self.opponent_score}")

            self.screen.blit(self.background_image, (0, 0))

            # Draw the walls
            for wall in self.walls:
                self.screen.blit(self.wall_image, (wall[0] * self.CELL_SIZE, wall[1] * self.CELL_SIZE))

            # Draw the player
            self.screen.blit(self.player_image,
                             (self.player.pos[0] * self.CELL_SIZE, self.player.pos[1] * self.CELL_SIZE))

            # Draw the cat
            self.screen.blit(self.cat_image, (self.cat_pos[0] * self.CELL_SIZE, self.cat_pos[1] * self.CELL_SIZE))

            # Draw the obstacles
            self.screen.blit(self.obstacle_image,
                             (self.obstacle1_pos[0] * self.CELL_SIZE, self.obstacle1_pos[1] * self.CELL_SIZE))
            self.screen.blit(self.obstacle_image,
                             (self.obstacle2_pos[0] * self.CELL_SIZE, self.obstacle2_pos[1] * self.CELL_SIZE))

            # Display score
            font = pygame.font.Font(None, 36)
            text = font.render(f"Your Score: {self.score} | Opponent Score: {self.opponent_score}", True, self.WHITE)
            self.screen.blit(text, (10, 10))

            # Check for win or loss
            if self.check_win():
                self.display_message("You won!", self.GREEN, self.GREEN)
                self.reset_game()

            elif self.check_loss():
                self.display_message("You lost!", self.RED, self.RED)
                self.reset_game()

            pygame.display.flip()
            pygame.time.Clock().tick(10)  # Adjust the speed of the game


# Run the game
game = Game1()
game.run()
