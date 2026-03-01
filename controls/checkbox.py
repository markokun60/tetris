from typing import Tuple
import pygame

from   controls.controls import Control

class Checkbox(Control):
    CHECK_CLR = (0,0,0)
    CHECK_SIZE = 16 
    CHECK_MARK = [ (3,8),(6, 11),(12,4)]
    DX = 4
    def __init__(self, position: Tuple[float, float] = (0, 0),text: str='' ,
                checked: bool = False,name = ''):
        "A basic checkbox."
        super().__init__(None,16,None,text)

        self.checked: bool = checked
        self.rect = pygame.Rect(position[0], position[1], self.CHECK_SIZE, self.CHECK_SIZE)
        self.name = self.text if text == '' else name
        self.is_auto_check = True

    def update(self, mousedown: bool, position: Tuple[float, float]):
        if mousedown and self.rect.collidepoint(position):
            if self.is_auto_check:
                self.checked = not self.checked
            self.call_back(self)
            return True
        return False

    def get_width(self):
        return self.rect.width + self.DX + self.txt_surf.get_width()

    def draw(self, surface: pygame.Surface):
        checkmark = []
        #print(self.rect)

        for (x,y) in self.CHECK_MARK:
            x += self.rect.x
            y += self.rect.y
            checkmark.append((x,y))

        pygame.draw.rect(surface, self.CHECK_CLR, self.rect, 1)
        if self.checked:
            pygame.draw.lines(surface, self.CHECK_CLR, False, checkmark, 2)
        x = self.rect.right
        y = self.rect.top
        x += self.DX
        surface.blit(self.txt_surf ,(x,y))
        