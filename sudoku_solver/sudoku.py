import os, pygame
pygame.font.init()
pygame.init()
import numpy as np
from dokusan import generators

WIDTH, HEIGHT = 640, 800
inc = WIDTH // 9

GREEN_BUTTON = pygame.image.load(os.path.join('Assets', 'green_button.png'))
ORANGE_BUTTON = pygame.image.load(os.path.join('Assets', 'orange_button.png'))

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        
        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        WIN.blit(self.image, (self.rect.x, self.rect.y))
        return action

# some global variables
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
main_font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 30)
x = 0
y = 0
inputValue = 0
strikes = 0

def randomize_grid():
    global grid
    grid = np.array(list(str(generators.random_sudoku(avg_rank=150))))
    grid = grid.reshape(9, 9)
    grid = [[int(x[0]), int(x[1]), int(x[2]), int(x[3]), int(x[4]), int(x[5]), int(x[6]), int(x[7]), int(x[8])] for x in grid]
    return grid
grid = randomize_grid()

def draw_window():
    WIN.fill((255, 255, 255))
    WIN.blit(small_font.render("Randomize", True, (0, 0, 0)), (100, 740))
    WIN.blit(small_font.render("Solve", True, (0, 0, 0)), (440, 740))

def draw_grid():
    for i in range(9):
        for j in range(9):
            if int(grid[i][j]) != 0:
                #fill the non zero cells
                pygame.draw.rect(WIN, (0, 128, 128), (i*inc, j*inc, inc+1, inc+1))
                text = main_font.render(str(grid[i][j]), True, (0, 0, 0))
                WIN.blit(text, (i*inc+20, j*inc+8))

    #lines that make the grid
    for i in range(10):
        pygame.draw.line(WIN, (0, 0, 0), (i*inc, 0), (i*inc, 640), 5) #vertical
        pygame.draw.line(WIN, (0, 0, 0), (0, i*inc), (700, i*inc), 5) #horizontal

def draw_selected_box():
    for i in range(2):
        pygame.draw.line(WIN, (0, 0, 255), (x*inc, (y+i)*inc), (x*inc+inc, (y + i)*inc), 5) #horizontal
        pygame.draw.line(WIN, (0, 0, 255), ((x+i)*inc, y*inc), ((x+i)*inc,y*inc+inc), 5) #vertical

def draw_strikes():
    if(strikes == 15):
        loseGame()
    for i in range(strikes):
        WIN.blit(main_font.render("x", True, (255, 0, 0)), (i * 25 + 15, 630))

def loseGame():
    WIN.fill((255, 255, 255))
    WIN.blit(main_font.render("YOU LOSE", True, (0, 0, 0)), (200, 300))

#draw screen while solving
def draw_init_solver():
    draw_window()
    draw_grid()
    # draw_strikes()
    b1.draw()
    b2.draw()
    pygame.display.update()

#draw screen if not solving
def draw_init():
    draw_window()
    draw_grid()
    draw_selected_box()
    drawSelectedValue()
    b1.draw()
    b2.draw()
    # draw_strikes()
    pygame.display.update()

def isValid(board, i, j, num):
    for f in range(9):
        if board[i][f] == num or board[f][j] == num:  #check cols and rows
            return False
    # checks the 3x3 block
    f = i // 3
    g = j // 3
    for i in range(f*3, f*3+3):
        for j in range(g*3, g*3+3):
            if board[i][j] == num:
                return False
    return True

# start at the (i, j) position which is usually (0, 0) and traverse the board
# and backtrack when necessary
def solve(board, i, j):
    while board[i][j] != 0:  # cell is not empty
        if i < 8:  
            i += 1
        elif i == 8 and j < 8:  # go back to the first column and next row
            i = 0
            j += 1
        elif i == 8 and j == 8:  # completed the board
            return True
    for num in range(1, 10):  # iterate 1 -> 9 inclusive
        if isValid(board, i, j, num):  # check if value is valid
            board[i][j] = num
            if solve(board, i, j):  # if the value is correct, keep it
                return True
            else:  # else keep the box empty
                board[i][j] = 0
        draw_init_solver()
    return False

#draw the user input value if valid and handle strikes
def drawInputValue():
    global inputValue, strikes
    if int(inputValue) > 0:
        if int(grid[int(x)][int(y)]) == 0:
            if isValid(grid, x, y, inputValue):
                grid[int(x)][int(y)] = inputValue
            else:
                strikes += 1
        inputValue = 0

#draw the number the user types in before entering it
def drawSelectedValue():
    if inputValue != 0 and grid[x][y] == 0:
        text = small_font.render(str(inputValue), True, (192, 192, 192))
        WIN.blit(text, (x * inc + 10, y * inc))

def main():
    global x, y, inputValue
    draw_init()
    run = True
    while run:     
        if b1.draw():
            randomize_grid()
        if b2.draw():
            solve(grid, 0, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if run == False:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if(x != 0):
                        x -= 1
                if event.key == pygame.K_RIGHT:
                    if(x != 8):
                        x += 1
                if event.key == pygame.K_UP:
                    if(y != 0):
                        y -= 1
                if event.key == pygame.K_DOWN:
                    if(y != 8):
                        y += 1
                if event.key == pygame.K_RETURN:
                    drawInputValue()
                if event.key == pygame.K_1:
                    inputValue = 1
                if event.key == pygame.K_2:
                    inputValue = 2
                if event.key == pygame.K_3:
                    inputValue = 3
                if event.key == pygame.K_4:
                    inputValue = 4
                if event.key == pygame.K_5:
                    inputValue = 5
                if event.key == pygame.K_6:
                    inputValue = 6
                if event.key == pygame.K_7:
                    inputValue = 7
                if event.key == pygame.K_8:
                    inputValue = 8
                if event.key == pygame.K_9:
                    inputValue = 9
            draw_init()
        pygame.display.update()

if __name__ == '__main__':
    b1 = Button(150, 710, GREEN_BUTTON, 2)
    b2 = Button(450, 710, ORANGE_BUTTON, 2)
    main()