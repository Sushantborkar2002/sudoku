import pygame
import requests


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return i, j  # row, col

    return None


def enter_dif():
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("enter difficulty")
    win.fill((255, 255, 255))
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
        pygame.draw.rect(win, (0, 255, 100), (100, 50, 300, 100))
        pygame.draw.rect(win, (0, 150, 200), (100, 200, 300, 100))
        pygame.draw.rect(win, (255, 0, 0), (100, 350, 300, 100))
        myfont = pygame.font.SysFont('Comic Sans MS', 35)
        value = myfont.render("EASY", True, (0, 0, 0))
        win.blit(value, (200, 75))
        value = myfont.render("MEDIUM", True, (0, 0, 0))
        win.blit(value, (170, 225))
        value = myfont.render("HARD", True, (0, 0, 0))
        win.blit(value, (200, 375))
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 100 < x < 400 and 50 < y < 150:
                response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
                grid = response.json()['board']
                pygame.quit()
                return grid
            if 100 < x < 400 and 200 < y < 300:
                response = requests.get("https://sugoku.herokuapp.com/board?difficulty=medium")
                grid = response.json()['board']
                pygame.quit()
                return grid
            if 100 < x < 400 and 350 < y < 450:
                response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard")
                grid = response.json()['board']
                pygame.quit()
                return grid
        pygame.display.update()


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                grid[i - 1][j - 1] = event.key - 48
                pygame.draw.rect(win, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                pygame.display.update()
                if 0 < event.key - 48 < 10:
                    pygame.draw.rect(win, background_color, (position[0] * 50 + buffer, position[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    value = myfont.render(str(event.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0] * 50 + 15, position[1] * 50))
                    grid[i - 1][j - 1] = event.key - 48
                    pygame.display.update()
                    return
                x, y = pygame.mouse.get_pos()
                return


grid = enter_dif()
WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
pygame.init()
win = pygame.display.set_mode((WIDTH + 550, WIDTH))
pygame.display.set_caption("Sudoku")
win.fill(background_color)
myfont = pygame.font.SysFont('Comic Sans MS', 35)
pygame.draw.rect(win, (200, 200, 200), (700, 250, 250, 50))
value = myfont.render("Auto Solve", True, (0, 0, 0))
win.blit(value, (730, 250))
for i in range(0, 10):
    if i % 3 == 0:
        pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 4)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 4)

    pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
    pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)

pygame.display.update()

for i in range(0, len(grid[0])):
    for j in range(0, len(grid[0])):
        if 0 < grid[i][j] < 10:
            value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
            win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
pygame.display.update()

while True:
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            pos = pygame.mouse.get_pos()
            insert(win, (x // 50, y // 50))
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 700 < x < 950 and 250 < y < 300:
                pygame.draw.rect(win, (255, 255, 255), (550, 0, 550, 550))
                for i in range(0, 10):
                    if i % 3 == 0:
                        pygame.draw.line(win, (0, 0, 0), (600 + 50 * i, 50), (600 + 50 * i, 500), 4)
                        pygame.draw.line(win, (0, 0, 0), (600, 50 + 50 * i), (1050, 50 + 50 * i), 4)
                    pygame.draw.line(win, (0, 0, 0), (600 + 50 * i, 50), (600 + 50 * i, 500), 2)
                    pygame.draw.line(win, (0, 0, 0), (600, 50 + 50 * i), (1050, 50 + 50 * i), 2)
                solve(grid_original)
                for i in range(0, len(grid_original[0])):
                    for j in range(0, len(grid_original[0])):
                        if 0 < grid_original[i][j] < 10:
                            value = myfont.render(str(grid_original[i][j]), True, original_grid_element_color)
                            win.blit(value, ((j + 1) * 50 + 15 + 550, (i + 1) * 50))
                if grid_original == grid:
                    win.fill((255, 255, 255))
                    image = pygame.image.load(r'C:\Users\sushant\Downloads\check-mark.png')
                    win.blit(image, (0, 0))
                else:
                    value = myfont.render("try again", True, (0, 0, 0))
                    win.blit(value, (500, 500))

        pygame.display.update()
