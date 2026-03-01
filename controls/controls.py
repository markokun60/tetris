import pygame
from typing import Tuple

class Control:
    #FONT = "Segoe Print"
    FONT = 'Arial'
    BK = (0,0,0)
    CLR_HINT = (0, 0, 255)

    def __init__(self,font_name = FONT,font_size=12,func = None,text = ''):
       # self.value: float = 0.0
        self.name = ''
        self.hide = False
        self.font_name= self.FONT if font_name == None else font_name
        self.font_size= font_size  
        self.func = func
        self.font = pygame.font.SysFont(self.font_name, self.font_size) 

        self.text = text 
        self.txt_surf = self.font.render(self.text, 1, (0,0,0))


    def move(self, position: Tuple[float, float]):
        pass  # controls can optionally overwrite this default move() method

    def update(self, mousedown: bool, position: Tuple[float, float]):
        return False  # controls can optionally overwrite this default update() method

    def draw(self, surface: pygame.Surface):
        raise Exception("All controls need to implement a draw() method")

    def call_back(self, *args):
        if self.func != None:
            if self.func:
                return self.func(*args)




