import pygame
import requests

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def insert(win, position):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            #if event.type == pygame.KEYDOWN:
                #1. tries to edit original file
                #2. edit 
                #3. adding the digits
                
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    for i in range(0,10):
        pygame.draw.line(win, (0,0,0), (50+50*i, 50), (50+50*i, 500), 4 if (i%3==0) else 2)
        pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50+50*i), 4 if (i%3==0) else 2)
    pygame.display.update()
    
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (0 < grid[i][j] < 10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50+15, (i+1)*50))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()