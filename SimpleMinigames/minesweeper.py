import pygame
import random

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 20
CELL_SIZE = 30
MINE_COUNT = 60
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FLAG_MODE_RECT = (WIDTH - 270, 150, 130, 50)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minesweeper')

# Load images
font = pygame.font.Font(None, 36)


class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0


class Board:
    def __init__(self, size, mine_count):
        self.size = size
        self.mine_count = mine_count
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]
        self._plant_mines()
        self._calculate_adjacent_mines()

    def _plant_mines(self):
        planted = 0
        while planted < self.mine_count:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            cell = self.grid[y][x]
            if not cell.is_mine:
                cell.is_mine = True
                planted += 1

    def _calculate_adjacent_mines(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x].is_mine:
                    continue
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx].is_mine:
                            self.grid[y][x].adjacent_mines += 1

    def reveal_cell(self, x, y):
        cell = self.grid[y][x]
        if cell.is_mine:
            return True
        if cell.is_revealed or cell.is_flagged:
            return False
        cell.is_revealed = True
        if cell.adjacent_mines == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        self.reveal_cell(nx, ny)
        return False

    def flag_cell(self, x, y):
        cell = self.grid[y][x]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def draw(self, surface):
        for y in range(self.size):
            for x in range(self.size):
                rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surface, GRAY, rect)
                pygame.draw.rect(surface, LINE_COLOR, rect, 1)  # Draw cell borders
                cell = self.grid[y][x]
                if cell.is_revealed:
                    pygame.draw.rect(surface, WHITE, rect)
                    if cell.is_mine:
                        pygame.draw.circle(surface, BLACK,
                                           (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                           CELL_SIZE // 2 - 5)
                    elif cell.adjacent_mines > 0:
                        text = font.render(str(cell.adjacent_mines), True, BLACK)
                        text_rect = text.get_rect(
                            center=(x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2))
                        surface.blit(text, text_rect)
                elif cell.is_flagged:
                    pygame.draw.rect(surface, RED, rect)  # Red color for flagged cells


def run_game():
    pygame.init()
    board = Board(GRID_SIZE, MINE_COUNT)
    running = True
    game_over = False
    win = None
    flag_mode = False  # Flagging mode
    show_end_game_menu = False
    play_again_button = back_to_menu_button = None

    # Buttons for Restart and Menu
    restart_button = pygame.Rect(FLAG_MODE_RECT[0], FLAG_MODE_RECT[1] + 170, 130, 40)
    menu_button = pygame.Rect(FLAG_MODE_RECT[0], FLAG_MODE_RECT[1] + 220, 130, 40)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag_mode = not flag_mode
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if FLAG_MODE_RECT[0] <= x <= FLAG_MODE_RECT[0] + FLAG_MODE_RECT[2] and FLAG_MODE_RECT[1] <= y <= \
                            FLAG_MODE_RECT[1] + FLAG_MODE_RECT[3]:
                        flag_mode = not flag_mode
                    elif x < GRID_SIZE * CELL_SIZE and y < GRID_SIZE * CELL_SIZE:
                        x //= CELL_SIZE
                        y //= CELL_SIZE
                        if flag_mode and event.button == 1:
                            board.flag_cell(x, y)
                        elif event.button == 1:
                            game_over = board.reveal_cell(x, y)
                            if game_over:
                                show_end_game_menu = True
                    elif restart_button.collidepoint(x, y):
                        board = Board(GRID_SIZE, MINE_COUNT)
                        game_over = False
                        win = None
                    elif menu_button.collidepoint(x, y):
                        from main import OptionsPage
                        menu = OptionsPage()
                        menu.run()
            elif game_over and show_end_game_menu:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        board = Board(GRID_SIZE, MINE_COUNT)
                        game_over = False
                        win = None
                        show_end_game_menu = False
                    elif back_to_menu_button.collidepoint(event.pos):
                        from main import OptionsPage
                        menu = OptionsPage()
                        menu.run()

        screen.fill(BLACK)
        board.draw(screen)

        # Draw flag mode toggle button and instruction
        pygame.draw.rect(screen, GRAY, FLAG_MODE_RECT)
        flag_text = font.render("Click to Flag", True, WHITE)
        flag_text_rect = flag_text.get_rect(center=(FLAG_MODE_RECT[0] + 65, FLAG_MODE_RECT[1] + 75))
        screen.blit(flag_text, flag_text_rect)
        if flag_mode:
            pygame.draw.circle(screen, RED, (FLAG_MODE_RECT[0] + 65, FLAG_MODE_RECT[1] + 25), 20)

        # Draw restart and menu buttons
        pygame.draw.rect(screen, GRAY, restart_button)
        pygame.draw.rect(screen, GRAY, menu_button)
        restart_text = font.render("Restart", True, WHITE)
        menu_text = font.render("Menu", True, WHITE)
        screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
        screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))

        # Check for win condition
        if not win and not game_over:
            if all(cell.is_revealed or (cell.is_mine and cell.is_flagged) for row in board.grid for cell in row):
                win = True
                game_over = True
                show_end_game_menu = True

        if game_over and show_end_game_menu:
            play_again_button, back_to_menu_button = draw_end_game_menu(screen, win)

        pygame.display.flip()

    pygame.quit()


def draw_end_game_menu(screen, win):
    font = pygame.font.Font(None, 36)
    play_again_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    back_to_menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)

    # Drawing the background for the end game menu
    screen.fill(GRAY)

    # Displaying the end game message
    message = "You Won!" if win else "You Lost!"
    message_color = GREEN if win else RED
    message_surface = font.render(message, True, message_color)
    message_rect = message_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(message_surface, message_rect)

    # Drawing buttons
    pygame.draw.rect(screen, WHITE, play_again_button)
    pygame.draw.rect(screen, WHITE, back_to_menu_button)

    # Button text
    play_text = font.render("Play Again", True, BLACK)
    back_text = font.render("Back to Menu", True, BLACK)
    screen.blit(play_text, play_text.get_rect(center=play_again_button.center))
    screen.blit(back_text, back_text.get_rect(center=back_to_menu_button.center))

    return play_again_button, back_to_menu_button


if __name__ == '__main__':
    run_game()
