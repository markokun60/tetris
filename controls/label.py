from typing import Tuple,Final
import pygame

from   controls.controls import Control

class Label(Control):
    LEFT  :Final[int] = 0
    RIGHT :Final[int] = 1
    CENTER:Final[int] = 2

    def __init__(self, name: str,position: Tuple[float, float],text: str, font_size= None,align:int = LEFT):
        "A basic label."
        super().__init__(name,Control.LABEL,None,font_size,None,text)
        self.name = self.text if text == '' else name

        self.txt_surf_selected = self.font_selected.render(self.text, 1, self.CLR_SELECTED)
        w = max(self.txt_surf.get_width() ,self.txt_surf_selected.get_width())
        h = self.get_control_height(0)
        h = max(self.txt_surf.get_height(),self.txt_surf_selected.get_height(),h)
        
        self.rect = pygame.Rect(position[0], position[1], w, h)
        self.align   = align
        self.draw_box = False 
       
    def reset(self):
        super().reset()   
        self.txt_surf_selected = self.font_selected.render(self.text, 1, self.color_text)  

    def get_width(self):
        return self.rect.width

    def draw(self, surface: pygame.Surface):
        if self.active:
            t = self.txt_surf_selected
        else:
            t = self.txt_surf

        if self.align == Label.LEFT:
            x = self.rect.left
        elif self.align == Label.RIGHT:
            x = self.rect.right - t.get_width()
        else:
            x = self.rect.centerx - t.get_width() // 2
        y = self.rect.top + (self.rect.height - t.get_height())//2
        if self.draw_box:
            pygame.draw.rect(surface,Control.CLR_BORDER,self.rect,1)
        surface.blit(t,(x,y))


    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        if self.func != None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.position):
                    self.call_back()
                    return True
        return False            
    

        


