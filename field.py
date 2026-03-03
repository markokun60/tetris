import pygame 
from math import ceil
from settings import * 
from lib      import scale_image_keep_ratio

class Field():
    def __init__(self):
        self.cell_size = CELL_SIZE
        self.backgroundImage = None
        self.imgBK = None


    def set_sizes(self,rows,cols):
        self.rows   = rows
        self.cols   = cols

        if self.rows == ROWS:
            self.cell_size = 16
        elif self.rows == M_ROWS:
             self.cell_size = 18
        elif self.rows == S_ROWS:
             self.cell_size = 24
        
        self.width  = self.cols * self.cell_size
        self.height = self.rows * self.cell_size
        
        self.xLeft = (INFO_X  - self.width)  // 2
        self.yTop  = (WINDOW_HEIGHT - self.height) // 2

        if self.backgroundImage != None:
            #self.imgBK = scale_image_keep_ratio(self.backgroundImage,self.width,self.height)
            self.imgBK = pygame.transform.smoothscale(self.backgroundImage,(self.width,self.height))
        else:
            self.imgBK = None
            
        self.image  = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.rect   = pygame.Rect(self .xLeft,self.yTop,self.width,self.height)
        self.grid   = [[0 for c in range(self.cols)] for r in range(self.rows)]

        self.reset()
        self.draw_background()
   

    def print(self):
        for r in range(self.rows):          
            for c in range(self.cols):  
               print(self.grid[r][c],end=' ')
            print('')

    def reset(self):
        for r in range(self.rows):
            for c in range(self.cols):  
                self.grid[r][c] = 0
        
    def is_row_full(self,row):
        for c in range(self.cols):
            if self.grid[row][c] == 0:
                return False
        return True

    def clear_row(self, row):
	    for column in range(self.cols):
		    self.grid[row][column] = 0

    def move_row_down(self,row,num_rows):
        for c in range(self.cols):
            self.grid[row+num_rows][c] = self.grid[row][c]
            self.grid[row][c] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.rows-1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1 
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed


    def draw_cells_border(self,screen,cells,color):
        for (r,c) in cells:
            x = self.xLeft + c * self.cell_size
            y = self.yTop  + r * self.cell_size
            pygame.draw.rect(screen,color,(x,y,self.cell_size,self.cell_size),1)


    def draw_background(self):
       
        if self.imgBK != None:
            x = (self.width -  self.imgBK.get_width()) //2
            y = (self.height - self.imgBK.get_height())/2
            self.image.fill(BLACK)
            self.image.blit(self.imgBK,(x,y))
            return

        MIN_CLR = 64
        MAX_CLR = 127
        h = (MAX_CLR-MIN_CLR) / self.height
        for i in range(self.height):
            k = int(h * i) + MIN_CLR 
            pygame.draw.line(self.image, (20, 20, k), (0, i), (self.width, i))
        
        y = 0
        h = (MAX_CLR-MIN_CLR) / self.rows
        for r in range(self.rows):
            k = int(h * r) + MIN_CLR + 64 
            clr = (0,0,k)
            x = 0
            for c in range(self.cols):  
                pygame.draw.rect(self.image,clr,(x,y,self.cell_size,self.cell_size),1)
                x += self.cell_size
            y += self.cell_size

    
    def draw(self,screen):
        border_size = 2
        pygame.draw.rect(screen,ORANGE,(self.xLeft - border_size/2,self.yTop - border_size/2,self.width + border_size,self.height + border_size),border_size)
        
        screen.blit(self.image,(self.xLeft,self.yTop))
        y = self.yTop
        for r in range(self.rows):
            x = self.xLeft
            for c in range(self.cols):  
                val = self.grid[r][c] 
                if val != 0:
                    color = COLORS[val-1]
                    pygame.draw.rect(screen,color       ,(x,y,self.cell_size,self.cell_size))
                    pygame.draw.rect(screen,BLOCK_BORDER,(x,y,self.cell_size,self.cell_size),1)
                x += self.cell_size
            y += self.cell_size




