import random
import pygame
from pygame.locals import *


# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

direction = [0, 1]
angle = [0, 1, 2]


class Player:
    def __init__(self):
        self.score = 0


class Gadget:
    def __init__(self):
        self.active = 0
        self.number = 20

    def activation(self):
        self.active = 0
        self.number -= 1


class Ball:
    def __init__(self, screen_width, screen_height):
        self.radius = 15
        self.x = screen_width / 2 - self.radius
        self.y = screen_height / 2 - self.radius
        self.vel_x = 0.3
        self.vel_y = 0.3

        # Load an image as the background for the ball
        self.image = pygame.image.load("ball2.png")
        self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))

    def change_direction(self):
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                self.vel_y = -0.3
                self.vel_x = 0.6
            if ang == 1:
                self.vel_y = -0.6
                self.vel_x = 0.6
            if ang == 2:
                self.vel_y = -0.6
                self.vel_x = 0.3
        if dir == 1:
            if ang == 0:
                self.vel_y = 0.3
                self.vel_x = 0.6
            if ang == 1:
                self.vel_y = 0.6
                self.vel_x = 0.6
            if ang == 2:
                self.vel_y = 0.6
                self.vel_x = 0.3

    def serve_player_1(self, screen_width, screen_height, score):
        self.x = screen_width / 2 - self.radius
        self.y = screen_height / 2 - self.radius
        self.change_direction()
        self.vel_x *= -1
        score += 1
        return score

    def serve_player_2(self, screen_width, screen_height, score):
        self.x = screen_width / 2 - self.radius
        self.y = screen_height / 2 - self.radius
        self.change_direction()
        score += 1
        return score

    def add_velocity(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def check_edges(self, screen_height):
        if self.y <= 0 or self.y >= screen_height - self.radius:
            self.vel_y *= -1

    def draw(self, parent_screen):
        # Create a surface with an alpha channel for transparency
        ball_surface = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA)

        # Draw the image onto the ball_surface
        ball_surface.blit(self.image, (0, 0))
        parent_screen.blit(ball_surface, (self.x - self.radius, self.y - self.radius))


class Paddle:
    def __init__(self, x_position, screen_height):
        self.width = 20
        self.height = 120
        self.x = x_position
        self.y = screen_height / 2 - self.height / 2
        self.vel = 0

        # Load an image as the background for the paddle
        self.image = pygame.image.load("gate3.png")  # Replace with your image file
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, parent_screen):
        paddle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw the image onto the paddle_surface
        paddle_surface.blit(self.image, (0, 0))

        # Blit the paddle_surface onto the parent_screen
        parent_screen.blit(paddle_surface, (self.x, self.y))

    def draw_gadget(self, parent_screen):
        pygame.draw.circle(parent_screen, WHITE, (self.x + 10, self.y + 10), 4)

    def check_movement(self, screen_height):
        if self.y >= screen_height - self.height:
            self.y = screen_height - self.height
        if self.y <= 0:
            self.y = 0

    def add_velocity(self):
        self.y += self.vel


class StartPage:
    def __init__(self, width, height):
        title_font = pygame.font.SysFont('callibri', 70)
        self.title_text = title_font.render("Football Pong Game", True, WHITE)

        start_font = pygame.font.SysFont('callibri', 50)
        self.start_text = start_font.render("Press Space to Start", True, WHITE)

        self.title_rect = self.title_text.get_rect(center=(width // 2, height // 4 - 20))
        self.start_rect = self.start_text.get_rect(center=(width // 2, height // 2 - 100))

        # Load an image of a ball
        self.ball_image = pygame.image.load("ball2.png")
        self.ball_image = pygame.transform.scale(self.ball_image, (100, 100))

        self.ball_rect = self.ball_image.get_rect(topleft=(50, height // 2 + 50))
        self.ball_rect2 = self.ball_image.get_rect(topright=(width - 50, height // 2 - 150))

        # Load an image for the bottom left
        self.bottom_left_image = pygame.image.load("wasd.png")
        self.bottom_left_image = pygame.transform.scale(self.bottom_left_image, (200, 200))
        self.bottom_left_rect = self.bottom_left_image.get_rect(bottomleft=(200, height - 80))

        # Load an image for the bottom right
        self.bottom_right_image = pygame.image.load("buttons.png")
        self.bottom_right_image = pygame.transform.scale(self.bottom_right_image, (200, 200))
        self.bottom_right_rect = self.bottom_right_image.get_rect(bottomleft=(600, height - 80))

        self.player1 = start_font.render("Player 1", True, BLACK)
        self.player2 = start_font.render("Player 2", True, BLACK)
        self.player1_rect = self.player1.get_rect(topleft=(230, height - 80))
        self.player2_rect = self.player2.get_rect(topleft=(630, height - 80))

    def update_start_text_color(self):
        new_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        start_font = pygame.font.SysFont('callibri', 50)
        self.start_text = start_font.render("Press Space to Start", True, new_color)

    def draw_start(self, surface):
        surface.blit(self.title_text, self.title_rect)
        surface.blit(self.start_text, self.start_rect)
        surface.blit(self.ball_image, self.ball_rect)
        surface.blit(self.ball_image, self.ball_rect2)
        surface.blit(self.bottom_left_image, self.bottom_left_rect)
        surface.blit(self.bottom_right_image, self.bottom_right_rect)
        surface.blit(self.player1, self.player1_rect)
        surface.blit(self.player2, self.player2_rect)
        pygame.display.update()

    def draw_press(self, surface):
        self.update_start_text_color()
        surface.blit(self.start_text, self.start_rect)
        pygame.display.update()


class Game:
    def __init__(self):
        self.show_options_flag = None
        pygame.init()

        # initialization of the window
        self.width = 1000
        self.height = 600
        self.surface = pygame.display.set_mode((self.width, self.height))

        # initialization of the start page
        self.startPage = StartPage(self.width, self.height)
        pygame.display.set_caption("Football Pong Game")

        self.background_image = pygame.image.load("green4.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

        self.surface.blit(self.background_image, (0, 0))

        # initialization for the paddles and the ball
        self.left_paddle = Paddle(40, self.height)
        self.right_paddle = Paddle(960, self.height)
        self.ball = Ball(self.width, self.height)

        # initialization for the gadgets
        self.right_gadget = Gadget()
        self.left_gadget = Gadget()

        # initialization for the score
        self.player1 = Player()
        self.player2 = Player()

        self.retry_button_rect = pygame.Rect(350, 350, 300, 50)
        self.retry_button_color = WHITE
        font = pygame.font.SysFont('calibri', 32)
        self.retry_button_text = font.render("Retry", True, WHITE)

        self.menu_button_rect = pygame.Rect(350, 420, 300, 50)
        self.menu_button_color = WHITE
        self.menu_button_text = font.render("Go Back to Menu", True, WHITE)
        self.running = True

    def check_movement(self):
        # Ball's movement
        self.ball.check_edges(self.height)
        if self.ball.x >= self.width - self.ball.radius:
            self.player1.score = self.ball.serve_player_1(self.width, self.height, self.player1.score)
        if self.ball.x <= 0 + self.ball.radius:
            self.player2.score = self.ball.serve_player_2(self.width, self.height, self.player2.score)

        # Paddle's movement
        self.left_paddle.check_movement(self.height)
        self.right_paddle.check_movement(self.height)

    def draw_objects(self):
        self.ball.draw(self.surface)
        self.left_paddle.draw(self.surface)
        self.right_paddle.draw(self.surface)

        # Draw gadgets
        if self.left_gadget.active == 1:
            self.left_paddle.draw_gadget(self.surface)
        if self.right_gadget.active == 1:
            self.right_paddle.draw_gadget(self.surface)

    def collision_left(self, power, gadget):
        if self.left_paddle.x <= self.ball.x <= self.left_paddle.x + self.left_paddle.width:
            if self.left_paddle.y <= self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                self.ball.x = self.left_paddle.x + self.left_paddle.width
                self.ball.vel_x *= power
                if gadget == 1:
                    self.left_gadget.activation()

    def collision_right(self, power, gadget):
        if self.right_paddle.x <= self.ball.x <= self.right_paddle.x + self.right_paddle.width:
            if self.right_paddle.y <= self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                self.ball.x = self.right_paddle.x
                self.ball.vel_x *= power
                if gadget == 1:
                    self.right_gadget.activation()

    def scoreboard(self):
        font = pygame.font.SysFont('callibri', 32)
        score1 = font.render("Player 1: " + str(self.player1.score), True, WHITE)
        self.surface.blit(score1, (25, 25))

        gadgets_left = font.render("Gadgets left: " + str(self.left_gadget.number), True, WHITE)
        self.surface.blit(gadgets_left, (25, 65))

        score2 = font.render("Player 2: " + str(self.player2.score), True, WHITE)
        self.surface.blit(score2, (800, 25))

        gadgets_right = font.render("Gadgets right: " + str(self.right_gadget.number), True, WHITE)
        self.surface.blit(gadgets_right, (800, 65))

    def start_page(self):
        clock = pygame.time.Clock()

        self.startPage.draw_start(self.surface)

        waiting_for_start = True
        while waiting_for_start:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        waiting_for_start = False

            self.startPage.draw_press(self.surface)
            clock.tick(2)

    def retry(self):
        # Check for mouse clicks on the retry button
        mouse_pos = pygame.mouse.get_pos()
        if self.retry_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # Reset game state
                self.player1.score = 0
                self.player2.score = 0
                self.left_gadget.number = 20
                self.right_gadget.number = 20

    def back_to_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.show_options_flag = True
                from main import OptionsPage
                page = OptionsPage()
                page.run()

    def stop_screen(self):
        self.surface.fill(GREEN)
        winning_font = pygame.font.SysFont('callibri', 100)
        stop_screen = winning_font.render("Player1 won!" if self.player1.score >= 1 else "Player2 won!", True,
                                          WHITE)
        self.surface.blit(stop_screen, (290, 250))

        retry_button_background = pygame.image.load("retry2.png").convert_alpha()
        retry_button_background = pygame.transform.scale(retry_button_background, (300, 50))

        # Draw retry button
        pygame.draw.rect(self.surface, self.retry_button_color, self.retry_button_rect)
        self.surface.blit(retry_button_background, self.retry_button_rect.topleft)
        self.surface.blit(self.retry_button_text, self.retry_button_rect.topleft)

        pygame.draw.rect(self.surface, self.menu_button_color, self.menu_button_rect)
        self.surface.blit(retry_button_background, self.menu_button_rect.topleft)
        self.surface.blit(self.menu_button_text, self.menu_button_rect.topleft)

    def run(self):
        self.start_page()
        running = True
        self.show_options_flag = False
        while running:

            self.surface.blit(self.background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.right_paddle.vel = -0.5
                    if event.key == K_DOWN:
                        self.right_paddle.vel = 0.5
                    # activate the right gadgets
                    if event.key == K_RIGHT and self.right_gadget.number > 0:
                        self.right_gadget.active = 1
                    if event.key == K_LEFT and self.right_gadget.number > 0:
                        self.right_gadget.active = 2

                    if event.key == K_w:
                        self.left_paddle.vel = -0.5
                    if event.key == K_s:
                        self.left_paddle.vel = 0.5
                    # activate the left gadgets
                    if event.key == K_d and self.left_gadget.number > 0:
                        self.left_gadget.active = 1
                    if event.key == K_a and self.left_gadget.number > 0:
                        self.left_gadget.active = 2

                elif event.type == KEYUP:
                    self.right_paddle.vel = 0
                    self.left_paddle.vel = 0

            # check movement for the ball and the paddles
            self.check_movement()

            # paddle collisions
            self.collision_left(-1, 0)
            self.collision_right(-1, 0)

            # gadgets in action
            if self.left_gadget.active == 1:
                self.collision_left(-2, 1)
            elif self.left_gadget.active == 2:
                self.left_paddle.y = self.ball.y
                self.left_gadget.activation()

            if self.right_gadget.active == 1:
                self.collision_right(-2, 1)
            elif self.right_gadget.active == 2:
                self.right_paddle.y = self.ball.y
                self.right_gadget.activation()

            # add velocity to the ball movement
            self.ball.add_velocity()

            # add velocity to the paddle movement
            self.right_paddle.add_velocity()
            self.left_paddle.add_velocity()

            # display the score for both players
            self.scoreboard()

            # draw all the objects of the game
            self.draw_objects()

            # stop the game and choose if you want to replay
            if self.player1.score >= 10 or self.player2.score >= 10:
                self.stop_screen()
                self.retry()
                self.back_to_menu()

                if self.show_options_flag:
                    from main import MainPage
                    MainPage.show_options(self)
                    self.show_options_flag = False

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
