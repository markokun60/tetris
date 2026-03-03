import pygame
from typing import Final

from settings import *

class Block:
    def __init__(self,cells,id,cell_size,row = 0,col = 3):
        self.id = id
        self.cell_size = cell_size
        self.all_cells = cells
        self.row   = row
        self.col   = col
        self.color = COLORS[self.id-1]
        self.rotation_state = 0
        self.active = True

        self.images = {}
        for i in self.all_cells.keys():
            image = self.createImage(self.all_cells[i],self.cell_size)
            self.images[i] = image

        self._current_values()
     
    def _current_values(self):
        self.cells = self.all_cells[self.rotation_state]
        self.image = self.images[self.rotation_state]
        self.max_row,self.max_col,self.min_row,self.min_col = self.get_max_edges(self.cells)
        
    def get_max_edges(self,cells):
        min_col = 100
        min_row = 100
        max_col = 0
        max_row = 0
        for (r,c) in cells:
            if r > max_row:
                max_row = r

            if r < min_row:
                min_row = r

            if c > max_col:
                max_col = c

            if c < min_col:
                min_col = c

        return max_row,max_col,min_row,min_col            
     
   
    def turn(self):
        if len(self.all_cells) == 1:
            return

        self.rotation_state += 1
        if self.rotation_state == len(self.all_cells):
            self.rotation_state = 0
        
        self._current_values()

    def turn_back(self):
        if len(self.all_cells) == 1:
            return

        self.rotation_state -= 1
        if self.rotation_state < 0:
            self.rotation_state = len(self.all_cells)-1
        
        self._current_values()


    def createImage(self,cells,cell_size): 
        max_row,max_col,min_row,min_col = self.get_max_edges(cells)
        #print(cells,max_row,max_col)

        size_x = (max_col + 1) * cell_size
        size_y = (max_row + 1) * cell_size

        image = pygame.Surface((size_x,size_y), pygame.SRCALPHA, 32)
        image = image.convert_alpha()

        for (r,c) in cells:           
            y = r * cell_size
            x = c * cell_size

            pygame.draw.rect(image,self.color  ,(x,y,cell_size,cell_size),0)
            pygame.draw.rect(image,BLOCK_BORDER,(x,y,cell_size,cell_size),1)
        return image

    def is_collided(self,field,dr,dc):
        for (r,c) in self.cells:           
            rf = self.row + r + dr 
            cf = self.col + c + dc
            if field.grid[rf][cf] != 0:
                return True
        return False

    def get_path(self,field):
        cells = []
        row = self.row
        f = True
        while row < field.rows:
           
            for (r,c) in self.cells:           
                rf = row + r + 1 
                cf = self.col + c
                if rf >= field.rows: 
                    f = False
                    break
                if field.grid[rf][cf] != 0:
                    f = False
                    break
            if not f:
                break
            row += 1
    
        for (r,c) in self.cells:
            cells.append((r+ row,c+self.col))
        return cells

    def attach_to_field(self,field):
        #print(self.id)
        for (r,c) in self.cells:           
            rf = self.row + r
            cf = self.col + c
         
            field.grid[rf][cf] = self.id
        self.active = False

    def draw(self,screen,field):
        self.y = self.row * self.cell_size + field.yTop
        self.x = self.col * self.cell_size + field.xLeft
        screen.blit(self.image,(self.x,self.y))

    def move_horizontal(self,field,c):             
        if (self.min_col + self.col + c) < 0:
            return False

        if (self.max_col + self.col + c) >= field.cols:
            return False

        if self.is_collided(field,0,c):
            return False

        self.col += c
        return True

    def move(self,field):
        #return True     
        if self.max_row + 1 + self.row == field.rows:
            self.attach_to_field(field)
            return False
          
        elif self.is_collided(field,1,0) :      
            self.attach_to_field(field) 
            return False
        
        self.row +=1     
        return True

class BlockI(Block):
    #  
    # XXXXX
    #
    CELLS:Final = {
        0:[(1,0),(1,1),(1,2),(1,3)],
        1:[(0,2),(1,2),(2,2),(3,2)],
        2:[(2,0),(2,1),(2,2),(2,3)],
        3:[(0,1),(1,1),(2,1),(3,1)],
    }

    def __init__(self,cell_size):
        super().__init__(self.CELLS,1,cell_size,-1)
        
class BlockO(Block):
    #
    #  XX
    #  XX
    #
    CELLS = {
        0: [(0,0),(0,1),(1,0),(1,1)]
    }

    def __init__(self,cell_size):
        super().__init__(self.CELLS,2,cell_size)


class BlockT(Block):
    #
    #  .X. 
    #  XXX 
    #
    CELLS = {
        0:[(0,1),(1,0),(1,1),(1,2)],
        1:[(0,1),(1,1),(1,2),(2,1)],
        2:[(1,0),(1,1),(1,2),(2,1)],
        3:[(0,1),(1,0),(1,1),(2,1)],
    }

    def __init__(self,cell_size):
        super().__init__(self.CELLS,3,cell_size)

class BlockJ(Block):
    #  .X
    #  .X 
    #  .X 
    #  XX

    CELLS = {
        0:[(0,0),(1,0),(1,1),(1,2)],
        1:[(0,1),(0,2),(1,1),(2,1)],
        2:[(1,0),(1,1),(1,2),(2,2)],
        3:[(0,1),(1,1),(2,0),(2,1)],
    }

    def __init__(self,cell_size):
        super().__init__(self.CELLS,4,cell_size)

class BlockL(Block):

    #  X
    #  X 
    #  X 
    #  XX

    CELLS = {
        0:[(0,2),(1,0),(1,1),(1,2)],
        1:[(0,1),(1,1),(2,1),(2,2)],
        2:[(1,0),(1,1),(1,2),(2,0)],
        3:[(0,0),(0,1),(1,1),(2,1)],
    }
    def __init__(self,cell_size):
        super().__init__(self.CELLS,5,cell_size)

class BlockS(Block):

    #  
    #  .XX 
    #  XX. 
    #  

    CELLS = {
        0:[(0,1),(0,2),(1,0),(1,1)],
        1:[(0,1),(1,1),(1,2),(2,2)],
        2:[(1,1),(1,2),(2,0),(2,1)],
        3:[(0,0),(1,0),(1,1),(2,1)],
    }
    def __init__(self,cell_size):
        super().__init__(self.CELLS,6,cell_size)


class BlockZ(Block):

    #  
    #  .XX 
    #  XX. 
    #  
    CELLS = {
        0:[(0,0),(0,1),(1,1),(1,2)],
        1:[(0,2),(1,1),(1,2),(2,1)],
        2:[(1,0),(1,1),(2,1),(2,2)],
        3:[(0,1),(1,0),(1,1),(2,0)],
    }
    def __init__(self,cell_size):
        super().__init__(self.CELLS,7,cell_size)



   