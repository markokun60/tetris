#https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
import pygame as pg
import string
import time
from typing import Tuple,Final
from controls.controls import Control

class InputBox(Control):
    #COLOR_INACTIVE = pg.Color('lightskyblue3')
    DX : Final[int] = 3
    DY : Final[int] = 2

    def __init__(self, name:str,  position: Tuple(float,float), text:str,width:int,height:int = 0, func = None):
        
        super().__init__(name,Control.TEXTBOX,None,None,func,None)
        x = position[0]
        y = position[1]      
        self.width = width+ 2 * InputBox.DX
        self.height=self.get_control_height(height)

        self.rect  = pg.Rect(x, y, self.width, self.height)
        self.text  = text
        self.width_large = self.width + 10
  
        self.border = 2
        self.create_text_surf()
        self.phase = 0
        self.cur_index = len(self.text)
        self.is_alpha   = True
        self.is_numeric = True
        self.is_punctuation = False
        self.phase_time = time.time()

    def check_char(self,ch):
        if not self.is_numeric:
            if ch in string.digits:
                return False
        if not self.is_alpha:
            if ch in string.ascii_letters:
                return False
        if not self.is_punctuation:
            if ch in string.punctuation:
                return False    
        return True
        
    def create_text_surf(self):
         # Change the current color of the input box.
        self.color = self.color_text if self.active else InputBox.CLR_INACTIVE_TXT
        self.txt_surf = self.font.render(self.text, True, self.color)

    def at_end(self):
        return self.cur_index == len(self.text)

    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        if self.hide:
            return False
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.setActive (not self.active)
            elif self.active:
                if Control.IS_DEBUG:
                    print(self.text)
                self.call_back(self.text)
                self.setActive(False)
           
            self.create_text_surf()
            #print(f'text conrotol is {self.active}')
        elif event.type == pg.MOUSEBUTTONUP:
           if is_left_mouse and is_double_click:
            if self.rect.width == self.width:
                self.rect.width = self.width_large
            else:
                self.rect.width = self.width    
        elif event.type == pg.KEYDOWN:
            self.hint = ""
            if self.active:
                if event.key == pg.K_RETURN:
                    if Control.IS_DEBUG:
                        print(self.text)
                    #self.text = ''

                    self.call_back(self.text)
                elif event.key == pg.K_HOME:
                    self.cur_index = 0
                elif event.key == pg.K_BACKSPACE:
                    if self.at_end():
                        self.text = self.text[:-1]
                    elif self.cur_index > 0:
                        self.text = self.text[:self.cur_index - 1] + self.text[self.cur_index:]
                    if self.cur_index > 0:
                        self.cur_index -= 1
                elif event.key == pg.K_LEFT:
                    if self.cur_index > 0:
                        self.cur_index -= 1
                elif event.key == pg.K_RIGHT:
                    if not self.at_end():
                        self.cur_index += 1
                elif not self.check_char(event.unicode):
                    self.hint = f"Invalid character {event.unicode}"    
                elif self.at_end():
                    self.text += event.unicode
                    self.cur_index += 1
                elif self.cur_index == 0:
                    self.text = event.unicode + self.text
                    self.cur_index += 1
                else:
                    self.text = self.text[:self.cur_index] +  event.unicode + self.text[self.cur_index:]
                    self.cur_index += 1
                # Re-render the text.
                self.txt_surf = self.font.render(self.text, True, self.color)
                return True
        return False           

    def update(self):
        dt = time.time() - self.phase_time 
        if dt  >= 0.5:
            self.phase_time = time.time()
            if self.phase == 0:
                self.phase = 1
            else:
                self.phase = 0
            
    def draw(self, screen: pg.Surface):
        # Blit the text.
        x = self.rect.x + InputBox.DX
        y = self.rect.y +(self.height - self.txt_surf.get_height())/2
        screen.blit(self.txt_surf, (x, y))
        if self.active:
            if self.phase == 0:
                if self.at_end():
                    x +=  self.txt_surf.get_width()
                elif self.cur_index > 0:
                    s = self.font.render(self.text[:self.cur_index],1,self.color)
                    x +=  s.get_width()
                pg.draw.line(screen,Control.CLR_TEXT,(x,self.rect.top),(x,self.rect.bottom),1)

        elif self.show_hint:      
            pos = pg.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.draw_hint(screen)
   
        # Blit the rect.
        pg.draw.rect(screen, self.color_text, self.rect, self.border)
       
