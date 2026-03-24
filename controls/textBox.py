#https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
import pygame as pg
from typing import Tuple
from controls.controls import Control

class InputBox(Control):
    COLOR_INACTIVE = pg.Color('lightskyblue3')
    #COLOR_ACTIVE   = pg.Color('dodgerblue2')
    COLOR_ACTIVE =  Control.CLR_TEXT
    DX = 3
    DY = 2

    def __init__(self, name:str, x, y, w, h, text):
        super().__init__(name,None,Control.FONT_SIZE,None,text)
        w += 2 * InputBox.DX
        h += 2 * InputBox.DY
        self.rect  = pg.Rect(x-InputBox.DX, y-InputBox.DY, w, h)
        self.color = Control.CLR_TEXT
        self.text  = text
        self.width = w
        self.width_large = self.width + 10
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.border = 2

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            elif self.active:
                if self.func != None:
                    self.func(self.text)
                self.active = False
            # Change the current color of the input box.
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
            #print(f'text conrotol is {self.active}')
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    #print(self.text)
                    #self.text = ''
                    if self.func != None:
                        self.func(self.text)
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self, mousedown: bool, is_left_mouse:bool, is_double_click:bool,position: Tuple[float, float]):
        # Resize the box if the text is too long.
        if is_left_mouse and is_double_click:
            if self.rect.width == self.width:
                self.rect.width = self.width_large
            else:
                self.rect.width = self.width
        return False

    def draw(self, screen: pg.Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+InputBox.DX, self.rect.y+InputBox.DY))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, self.border)

  
