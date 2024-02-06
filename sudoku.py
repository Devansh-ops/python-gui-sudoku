import pygame
import requests

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)

response = requests.get("https://sudoku-api.vercel.app/api/dosuku?query={newboard(limit:1){grids{value}}}")
grid = response.json()['newboard']['grids'][0]['value']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
buffer = 5

def isEmpty(num):
    if num == 0:
        return True
    return False

def isValid(position, num):
     #Check for Column, row and sub-grid
    
    #Checking row
    for i in range(0, len(grid[0])):
        if(grid[position[0]][i] == num):
            return False
    
    #Checking column
    for i in range(0, len(grid[0])):
        if(grid[i][position[1]] == num):
            return False
    
    #Check sub-grid  
    x = position[0]//3*3
    y = position[1]//3*3
    #Gives us the box number
    
    for i in range(0,3):
        for j in range(0,3):
            if(grid[x+i][y+j]== num):
                return False
    return True


def insert(win, position):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    i, j = position[1], position[0]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                #1. tries to edit original file
                #2. edit 
                #3. adding the digits
                if grid_original[i-1][j-1] != 0:
                    return
                if event.key == ord('0'): # ASCII 48
                    grid[i-1][j-1] = 0
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    pygame.display.update()
                    
                if 0 < event.key - ord('0') < 10: 
                    col = (0,0,0) if isValid((i-1,j-1), event.key - ord('0')) else (255, 0, 0)
                    grid[i-1][j-1] = event.key - ord('0')
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                    value = myfont.render(str(event.key-ord('0')), True, col)
                    win.blit(value, (position[0]*50 +15, position[1]*50))
                    pygame.display.update()
                
                return

solved = 0
def sudoku_solver(win):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    for i in range(0,len(grid[0])):
        for j in range(0, len(grid[0])):
            if(isEmpty(grid[i][j])):
                for k in range(1,10):
                    if isValid((i,j), k):                   
                        grid[i][j] = k
                        pygame.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        value = myfont.render(str(k), True, (0,0,0))
                        win.blit(value, ((j+1)*50 +15,(i+1)*50))
                        pygame.display.update()
                        pygame.time.delay(25)
                        
                        sudoku_solver(win)
                        
                        #Exit condition
                        global solved
                        if(solved == 1):
                            return
                        
                        #if sudoku_solver returns, there's a mismatch
                        grid[i][j] = 0
                        pygame.draw.rect(win, background_color, ((j+1)*50 + buffer, (i+1)*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                        pygame.display.update()
                        #pygame.time.delay(50)
                return               
    solved = 1
    
def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    icon_img = pygame.image.load('sudoku_icon.png')
    pygame.display.set_icon(icon_img)
    
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

    solve_button = pygame.Rect(225, 10, 100, 30)
    pygame.draw.rect(win, (0,200,100), solve_button)
    solve_text = pygame.font.SysFont('Comic Sans MS', 25).render("Solve", True, (0,0,0))
    win.blit(solve_text, (245, 5))
    pygame.display.update()
    
    #solve_sudoku(win)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if solve_button.collidepoint(pos):
                    sudoku_solver(win)
                else:
                    insert(win, (pos[0]//50, pos[1]//50))
            
            if event.type == pygame.MOUSEMOTION:
                if solve_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (200,100,100), solve_button)
                    win.blit(solve_text, (245, 5))
                else:
                    pygame.draw.rect(win, (0,200,100), solve_button)
                    win.blit(solve_text, (245, 5))
                pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()