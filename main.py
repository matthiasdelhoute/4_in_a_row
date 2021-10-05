import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0,255)
GAME_SCREEN_HEIGHT = 800
GAME_SCREEN_WIDTH = 1000
MENU_HEIGHT = 100
HOVER_HEIGHT = 100
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
WINNING_SPOTS = []
FULL_SCREEN_HEIGHT = GAME_SCREEN_HEIGHT + MENU_HEIGHT + HOVER_HEIGHT
GAME_OVER = False
WINNER = ''
SCORE_P1 = 0
SCORE_P2 = 0
FONT_STYLE = 'timesnewroman'


def game_loop():
    global SCREEN, CLOCK
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((GAME_SCREEN_WIDTH, FULL_SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    draw_grid()
    start_time = 0
    while True:
        draw_game_screen()
        if not GAME_OVER:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                end_time = pygame.time.get_ticks()
                current_wait_time = end_time - start_time
                if current_wait_time > WAIT_TIME:
                    player_played()
                    check_win()
                    start_time = pygame.time.get_ticks()
        else:
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                reset_game()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()


def draw_game_screen():
    # Reset screen
    reset_screen()
    # draw grid
    draw_grid()
    # draw played locations
    for row in range(ROWS):
        for column in range(COLS):
            if GRID[row][column] == 'P1':
                x = get_col_pixels(column)
                y = get_row_pixels(row)
                draw_circle('P1', x, y)
            elif GRID[row][column] == 'P2':
                x = get_col_pixels(column)
                y = get_row_pixels(row)
                draw_circle('P2', x, y)
    # draw static text
    draw_static_score_text()
    # draw current score
    draw_score()

    if CURRENT_PLAYER != 2:
        # draw current player
        draw_current_player()
        draw_static_currentplayer_text()
        draw_mouse_hover_place()
    else:
        # Draw winner text
        draw_winner_text()
        show_winning_spots()


def reset_screen():
    rect = pygame.Rect(0, 0, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)
    pygame.draw.rect(SCREEN, BLACK, rect, 0)


def draw_grid():
    for x in range(0, GAME_SCREEN_WIDTH, BLOCK_WIDTH):
        for y in range(MENU_HEIGHT + HOVER_HEIGHT, FULL_SCREEN_HEIGHT, BLOCK_HEIGHT):
            rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)


def draw_circle(player, x, y):
    if player == 'P1':
        pygame.draw.circle(SCREEN, RED, (x, y), 50)
    elif player == 'P2':
        pygame.draw.circle(SCREEN, GREEN, (x, y), 50)


def draw_score():
    Font = pygame.font.SysFont(FONT_STYLE, 30)
    ftext = Font.render("Player 1 = " + str(SCORE_P1) + " ------- Player 2 = " + str(SCORE_P2), True, WHITE)
    SCREEN.blit(ftext, (10, MENU_HEIGHT / 2))


def draw_winner_text():
    Font = pygame.font.SysFont(FONT_STYLE, 30)
    ftext = Font.render('Winner: ' + WINNER + ' Press ENTER to restart the game', True, WHITE)
    SCREEN.blit(ftext, (GAME_SCREEN_WIDTH / 2, MENU_HEIGHT / 3))


def draw_current_player():
    Font = pygame.font.SysFont(FONT_STYLE, 30)
    if CURRENT_PLAYER == 0:
        ftext = Font.render('Player 1 - Press Space to place', True, WHITE)
    elif CURRENT_PLAYER == 1:
        ftext = Font.render('Player 2 - Press Space to place', True, WHITE)

    SCREEN.blit(ftext, (GAME_SCREEN_WIDTH / 2, MENU_HEIGHT / 2))


def draw_static_score_text():
    Font = pygame.font.SysFont(FONT_STYLE, 30)
    ftext = Font.render('Score:', True, WHITE)
    SCREEN.blit(ftext, (10, 10))


def draw_static_currentplayer_text():
    Font = pygame.font.SysFont(FONT_STYLE, 30)
    ftext = Font.render('Current Player:', True, WHITE)
    SCREEN.blit(ftext, (GAME_SCREEN_WIDTH / 2, 10))


def draw_mouse_hover_place():
    x = get_col_pixels(get_col())
    y = MENU_HEIGHT + (HOVER_HEIGHT / 2)
    if CURRENT_PLAYER == 0:
        draw_circle('P1', x, y)
    if CURRENT_PLAYER == 1:
        draw_circle('P2', x, y)


def show_winning_spots():
    print('winning spots')
    for spot in range(0, 4):
        print(WINNING_SPOTS[spot])
        location=WINNING_SPOTS[spot]
        row=location[0]
        col=location[1]
        x=get_col_pixels(col)
        y=get_row_pixels(row)
        pygame.draw.circle(SCREEN, BLUE, (x, y), 50)

    print('end')


def add_score(player):
    global SCORE_P1, SCORE_P2

    if player == 'P1':
        SCORE_P1 = SCORE_P1 + 1
    elif player == 'P2':
        SCORE_P2 = SCORE_P2 + 1


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
    row_pixels = (row * BLOCK_HEIGHT) + (BLOCK_HEIGHT / 2) + MENU_HEIGHT + HOVER_HEIGHT
    return row_pixels


def player_played():
    global CURRENT_PLAYER
    col = get_col()
    row = get_row(col)
    if row == 'FULL':
        return 0

    if CURRENT_PLAYER == 0:
        add_to_grid_array(col, row, "P1")
        CURRENT_PLAYER = 1
    elif CURRENT_PLAYER == 1:
        add_to_grid_array(col, row, "P2")
        CURRENT_PLAYER = 0


def check_win():
    global WINNER, CURRENT_PLAYER
    for r in range(ROWS):
        for c in range(COLS):
            if not GRID[r][c] == '':
                if check_player_win('P1', r, c):
                    WINNER = 'Player 1'
                    add_score('P1')
                    CURRENT_PLAYER = 2
                if check_player_win('P2', r, c):
                    WINNER = 'Player 2'
                    add_score('P2')
                    CURRENT_PLAYER = 2


def check_player_win(player, r, c):
    global GAME_OVER, WINNING_SPOTS

    if GRID[r][c] == player:
        # SAME ROW
        if c + 4 <= COLS:
            if GRID[r][c + 1] == player:
                if GRID[r][c + 2] == player:
                    if GRID[r][c + 3] == player:
                        WINNING_SPOTS = [[r, c], [r, c + 1], [r, c + 2], [r, c + 3]]
                        GAME_OVER = True
                        return True
        elif c - 4 > 0:
            if GRID[r][c - 1] == player:
                if GRID[r][c - 2] == player:
                    if GRID[r][c - 3] == player:
                        WINNING_SPOTS = [[r, c], [r, c - 1], [r, c - 2], [r, c - 3]]
                        GAME_OVER = True
                        return True
        # SAME COLUMN
        if r + 4 <= ROWS:
            if GRID[r + 1][c] == player:
                if GRID[r + 2][c] == player:
                    if GRID[r + 3][c] == player:
                        WINNING_SPOTS = [[r, c], [r + 1, c], [r + 2, c], [r + 3, c]]
                        GAME_OVER = True
                        return True
        elif r - 4 > 0:
            if GRID[r - 1][c] == player:
                if GRID[r - 2][c] == player:
                    if GRID[r - 3][c] == player:
                        WINNING_SPOTS = [[r, c], [r - 1, c], [r - 2, c], [r - 3, c]]
                        GAME_OVER = True
                        return True
        # DIAGONAL
        if c + 4 <= COLS & r + 4 <= ROWS:
            if GRID[r + 1][c + 1] == player:
                if GRID[r + 2][c + 2] == player:
                    if GRID[r + 3][c + 3] == player:  # works
                        WINNING_SPOTS = [[r, c], [r + 1, c + 1], [r + 2, c + 2], [r + 3, c + 3]]
                        GAME_OVER = True
                        return True
        if r + 4 <= ROWS & c - 4 > 0:
            if GRID[r + 1][c - 1] == player:
                if GRID[r + 2][c - 2] == player:
                    if GRID[r + 3][c - 3] == player:
                        WINNING_SPOTS = [[r, c], [r + 1, c - 1], [r + 2, c - 2], [r + 3, c - 3]]
                        GAME_OVER = True
                        return True
    return False


def add_to_grid_array(col, row, player):
    global GRID
    GRID[row][col] = player


def reset_game():
    global GAME_OVER, WINNER, CURRENT_PLAYER, SCREEN, CLOCK, GRID, WINNING_SPOTS
    GAME_OVER = False
    WINNER = ''
    CURRENT_PLAYER = 0
    pygame.init()
    SCREEN = pygame.display.set_mode((GAME_SCREEN_WIDTH, FULL_SCREEN_HEIGHT))
    CLOCK = pygame.time.Clock()
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
    WINNING_SPOTS = []


if __name__ == '__main__':
    game_loop()
