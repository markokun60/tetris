from typing import Tuple
import pygame

from   controls.controls import Control

class Label(Control):
    LEFT   = 0,
    RIGHT  = 1,
    CENTER = 2
    def __init__(self, name: str,position: Tuple[float, float],text: str, align:int = LEFT):

        "A basic label."
        super().__init__(name,None,Control.FONT_SIZE,None,text)
        self.name = self.text if text == '' else name
        self.rect = pygame.Rect(position[0], position[1], self.txt_surf.get_width(), self.txt_surf.get_height())
        self.align = align
   
    def get_width(self):
        return self.txt_surf.get_width()

    def draw(self, surface: pygame.Surface):
        if self.align == Label.LEFT:
            x = self.rect.left
        elif self.align == Label.RIGHT:
            x = self.rect.right - self.get_width()
        else:
            x = self.rect.centerx - self.get_width() / 2
        y = self.rect.top
        surface.blit(self.txt_surf ,(x,y))
        


