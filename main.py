import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GAME_SCREEN_HEIGHT = 800
GAME_SCREEN_WIDTH = 1000
ROWS = 7
COLS = 6
BLOCK_HEIGHT = int(GAME_SCREEN_HEIGHT / ROWS)
BLOCK_WIDTH = int(GAME_SCREEN_WIDTH / COLS)
CURRENT_PLAYER = 0
GRID = [
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
    ['', '', '', '', '', ''],
]
WAIT_TIME = 500
MENU_HEIGHT = 100
FULL_SCREEN_HEIGHT = GAME_SCREEN_HEIGHT + MENU_HEIGHT
GAME_OVER = False
WINNER = ''


def game_loop():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((GAME_SCREEN_WIDTH, FULL_SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    draw_grid()
    start_time = 0
    render_text_menu("Current Turn: Player 1 - Press Space to place")
    while True:
        if not GAME_OVER:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                end_time = pygame.time.get_ticks()
                current_wait_time = end_time - start_time
                if current_wait_time > WAIT_TIME:
                    player_played()
                    check_win()
                    start_time = pygame.time.get_ticks()
        else:
            render_text_menu("Winner: " + WINNER + " Press ENTER to restart the game")
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                reset_game()
                print('enter')
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


def get_col():
    pos = pygame.mouse.get_pos()
    pixel_width = pos[0]
    col = 0
    while pixel_width > BLOCK_WIDTH:
        col = col + 1
        pixel_width = pixel_width - BLOCK_WIDTH
    return col


def get_col_pixels(col):
    col_pixels = (col * BLOCK_WIDTH) + (BLOCK_WIDTH / 2)
    return col_pixels


def get_row(col):
    row = 0
    if GRID[6][col] == '':
        row = 6
    elif GRID[5][col] == '':
        row = 5
    elif GRID[4][col] == '':
        row = 4
    elif GRID[3][col] == '':
        row = 3
    elif GRID[2][col] == '':
        row = 2
    elif GRID[1][col] == '':
        row = 1
    elif GRID[0][col] == '':
        row = 0
    else:
        return 'FULL'
    return row


def get_row_pixels(row):
    row_pixels = (row * BLOCK_HEIGHT) + (BLOCK_HEIGHT / 2) + MENU_HEIGHT
    return row_pixels


def player_played():
    global CURRENT_PLAYER
    col = get_col()
    col_pixels = get_col_pixels(col)
    row = get_row(col)
    if row == 'FULL':
        return 0
    row_pixels = get_row_pixels(row)

    if CURRENT_PLAYER == 0:
        add_to_grid_array(col, row, "P1")
        draw_circle(0, col_pixels, row_pixels)
        CURRENT_PLAYER = 1
        render_text_menu("Current Turn: Player 2 - Press Space to place")
    elif CURRENT_PLAYER == 1:
        add_to_grid_array(col, row, "P2")
        draw_circle(1, col_pixels, row_pixels)
        CURRENT_PLAYER = 0
        render_text_menu("Current Turn: Player 1 - Press Space to place")


def check_win():
    global WINNER
    for r in range(ROWS):
        for c in range(COLS):
            if not GRID[r][c] == '':
                if check_player_win('P1', r, c):
                    WINNER = 'Player 1'
                if check_player_win('P2', r, c):
                    WINNER = 'Player 2'


def check_player_win(player, r, c):
    global GAME_OVER

    if GRID[r][c] == player:
        # SAME ROW
        if c + 4 <= COLS:
            if GRID[r][c + 1] == player:
                if GRID[r][c + 2] == player:
                    if GRID[r][c + 3] == player:
                        GAME_OVER = True
                        return True
        elif c - 4 > 0:
            if GRID[r][c - 1] == player:
                if GRID[r][c - 2] == player:
                    if GRID[r][c - 3] == player:
                        GAME_OVER = True
                        return True
        # SAME COLUMN
        if r + 4 <= ROWS:
            if GRID[r + 1][c] == player:
                if GRID[r + 2][c] == player:
                    if GRID[r + 3][c] == player:
                        GAME_OVER = True
                        return True
        elif r - 4 > 0:
            if GRID[r - 1][c] == player:
                if GRID[r - 2][c] == player:
                    if GRID[r - 3][c] == player:
                        GAME_OVER = True
                        return True
        # DIAGONAL
        if c + 4 <= COLS & r + 4 <= ROWS:
            if GRID[r + 1][c + 1] == player:
                if GRID[r + 2][c + 2] == player:
                    if GRID[r + 3][c + 3] == player: #works
                        GAME_OVER = True
                        return True
        if r + 4 <=ROWS & c - 4 > 0:
            if GRID[r + 1][c - 1] == player:
                if GRID[r + 2][c - 2] == player:
                    if GRID[r + 3][c - 3] == player:
                        GAME_OVER = True
                        return True
        # LEFT DOWN TO RIGHT UP
        # LEFT UP TO RIGHT DOWN

    return False


def draw_circle(player, x, y):
    if player == 0:
        circle = pygame.draw.circle(SCREEN, RED, (x, y), 50)
    elif player == 1:
        circle = pygame.draw.circle(SCREEN, GREEN, (x, y), 50)


def render_text_menu(text):
    rect = pygame.Rect(0, 0, GAME_SCREEN_WIDTH, MENU_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, rect, 0)

    pygame.font.init()
    Font = pygame.font.SysFont('timesnewroman', 30)
    ftext = Font.render(text, True, WHITE)
    SCREEN.blit(ftext, (GAME_SCREEN_WIDTH / 10, MENU_HEIGHT / 2))


def draw_grid():
    for x in range(0, GAME_SCREEN_WIDTH, BLOCK_WIDTH):
        for y in range(MENU_HEIGHT, FULL_SCREEN_HEIGHT, BLOCK_HEIGHT):
            rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def add_to_grid_array(col, row, player):
    global GRID
    GRID[row][col] = player


def reset_game():
    global GAME_OVER, WINNER, CURRENT_PLAYER, SCREEN, CLOCK, GRID
    print('RESET')
    GAME_OVER = False
    WINNER = ''
    CURRENT_PLAYER = 0
    pygame.init()
    SCREEN = pygame.display.set_mode((GAME_SCREEN_WIDTH, FULL_SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    render_text_menu("Current Turn: Player 1 - Press Space to place")
    draw_grid()
    pygame.display.update()
    GRID = [
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
    ]


if __name__ == '__main__':
    game_loop()
