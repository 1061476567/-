import pygame
import sys

# 初始化游戏
pygame.init()

# 常量定义集中化
WIDTH = 960
HEIGHT = 720
SIZE = 23
MARGIN = 30
BOARD_SIZE = SIZE * MARGIN + MARGIN
WINDOW_SIZE = (WIDTH, HEIGHT)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 202)

# 创建游戏窗口
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("五子棋")

# 创建棋盘
board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]


# 绘制棋盘和棋子的通用函数
def draw_board():
    screen.fill(WHITE)
    for row in range(SIZE):
        for col in range(SIZE):
            pygame.draw.rect(screen, BLACK, (MARGIN + col * MARGIN, MARGIN + row * MARGIN, MARGIN, MARGIN), 1)
            draw_piece(row, col)


# 绘制棋子和圆形的通用函数
def draw_piece(row, col):
    if board[row][col] == 1:
        draw_circle(BLACK, row, col)
    elif board[row][col] == 2:
        draw_circle(PINK, row, col)


def draw_circle(color, row, col):
    pygame.draw.circle(screen, color, (MARGIN + col * MARGIN, MARGIN + row * MARGIN), MARGIN // 2)


# 判断胜利条件
def check_win(row, col, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = count_consecutive_pieces(row, col, dr, dc, player)
        count += count_consecutive_pieces(row, col, -dr, -dc, player) - 1
        if count >= 5:
            return True
    return False


# 计算连续相同子的数量
def count_consecutive_pieces(row, col, dr, dc, player):
    count = 0
    while 0 <= row < SIZE and 0 <= col < SIZE and board[row][col] == player:
        count += 1
        row += dr
        col += dc
    return count


# 游戏主循环
def main():
    player = 1  # 玩家1为黑子，玩家2为粉子
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    x, y = event.pos
                    col = round((x - MARGIN) / MARGIN)  # 调整鼠标位置到棋盘交叉点
                    row = round((y - MARGIN) / MARGIN)
                    if 0 <= row < SIZE and 0 <= col < SIZE and board[row][col] == 0:
                        board[row][col] = player
                        draw_board()
                        pygame.display.update()
                        if check_win(row, col, player):
                            msg = f"player {player} wins!"
                            font = pygame.font.Font(None, 60)  # 调整字体大小
                            text = font.render(msg, True, BLACK)
                            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 设置文字位置居中
                            screen.blit(text, text_rect)
                            pygame.display.update()
                            game_over = True
                        else:
                            player = 2 if player == 1 else 1

        if not game_over:
            draw_board()
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()