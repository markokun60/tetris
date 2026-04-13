from typing import Tuple,Final
import pygame

from   controls.controls import Control

class Slider(Control):
    HOR     :Final[int] = 0
    VER     :Final[int] = 1
    #
    H       :Final[int] = 16  
    SIZE_TR :Final[int] = 16
    H_TR    :Final[float]= 0.7 * SIZE_TR
    D_TR    :Final[int] = 2

    def __init__(self, name: str,position: Tuple[float, float],size:int,min_value:int,max_value:int,value:int,is_arrow:bool, is_marker:bool,align:int = VER):
        "A basic slider"
        super().__init__(name=name,controlType=Control.SLIDER)
        self.align = align
        self.min_value = min_value
        self.max_value = max_value
        self.value     = value
        self.is_arrow  = is_arrow
        self.is_marker = is_marker
        x = position[0]
        y = position[1]
        
        if align == Slider.VER:
            self.rect = pygame.Rect(x,y,  Slider.H, size)
            self.e = (self.max_value - self.min_value) / self.rect.height

        else: # Not done
            self.rect = pygame.Rect(x,y,  size, Slider.H)
            self.e = (self.max_value - self.min_value) / self.rect.width
    

    def draw_tr_v(self,screen,up):
        x = self.rect.right - Slider.SIZE_TR
        h = Slider.H_TR
        size = Slider.SIZE_TR
        if up:
            y = self.rect.top
            triangle_points = [(x, y+h), (x + size, y+h), (x+size//2, y)]
        else:    
            y = self.rect.bottom - Slider.SIZE_TR  
            triangle_points = [(x, y), (x + size ,y), (x+size//2, y+h)]   

        pygame.draw.polygon(screen, Slider.CLR_ARROW, triangle_points)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface,Control.CLR_BTN,self.rect)
        if self.is_arrow:
            if self.align == Slider.VER:
                self.draw_tr_v(surface,True)
                self.draw_tr_v(surface,False)
         
        if self.is_marker:
            if self.align == Slider.VER:
                y = self.value * self.e + self.rect.top + self.H_TR
                x = self.rect.left
                pygame.draw.rect(surface,Control.CLR_ARROW,(x,y,self.rect.width,2),1)
            else:
                x = self.value * self.e + self.rect.left
                y = self.rect.top
                pygame.draw.rect(surface,Control.CLR_ARROW,(x,y,16,16))

     
    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]): 
        if self.hide:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(position):
                if self.align == Slider.VER:
                    d = position[1] - self.rect.top
                else:
                    d = position[0] - self.rect.left
                self.value = d * self.e  + self.min_value    
                #self.value = round(v) 
                print(f"slider:{self.value},{self.max_value}")                
                return True
       
        return False


                
                    

        


