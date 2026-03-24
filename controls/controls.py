import pygame
import time
from typing import Tuple
from settings import * 

class Control:
    #FONT = "Segoe Print"
    FONT = 'Arial'
    BK = (0,0,0)
    CLR_HINT = (0, 0, 255)
    CLR_TEXT = (0, 0, 0)
    CLR_INACTIVE = (64,64,64)
    FONT_SIZE   = 16
    
    controls = {}

    def __init__(self,name,font_name = FONT,font_size= FONT_SIZE,func = None,text = ''):
       # self.value: float = 0.0
        self.name = text if name == '' else name
        self.hide = False
        self.font_name= Control.FONT if font_name == None else font_name
        self.font_size= font_size  
        self.func = func
        self.font = pygame.font.SysFont(self.font_name, self.font_size) 

        self.text = text 
        self.txt_surf = self.font.render(self.text, 1, Control.CLR_TEXT)
        Control.controls[self.name] = self


    def move(self, position: Tuple[float, float]):
        pass  # controls can optionally overwrite this default move() method

    def update(self, mousedown: bool, is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        return False  # controls can optionally overwrite this default update() method

    def draw(self, surface: pygame.Surface):
        raise Exception("All controls need to implement a draw() method")

    def handle_event(self, event):
        return False

    def call_back(self, *args):
        if self.func != None:
            if self.func:
                return self.func(*args)

def handle_controls_events(event,left_click_time,right_click_time):
    DOUBLE_CLICK_TIME = 0.5
    if event.type == pygame.MOUSEBUTTONDOWN:
        is_left_mouse = True if event.button == 1 else False
        pos = pygame.mouse.get_pos()   
        for c in Control.controls.values():
            if not c.hide:
                if c.update(True,is_left_mouse,False,pos):
                    break
                        
    elif event.type == pygame.MOUSEBUTTONUP:
        is_left_mouse = False
        is_double     = False
        if event.button == 1: #left click
            is_left_mouse = True
            if time.time() - left_click_time < DOUBLE_CLICK_TIME:
                if IS_DEBUG:
                    print("Left double click detected")
                is_double = True
            left_click_time  = time.time()
            right_click_time = 0             
        else: #right click
            if time.time() - right_click_time < DOUBLE_CLICK_TIME:
                if IS_DEBUG:
                    print("Right double click detected")
                is_double = True
            right_click_time = time.time()
            left_click_time = 0
         
        pos = pygame.mouse.get_pos()
        for c in Control.controls.values():
            if not c.hide:
                if c.update(False,is_left_mouse,is_double,pos):
                    break
               
    for c in Control.controls.values():
        if not c.hide:
            c.handle_event(event)

    return (left_click_time,right_click_time)




