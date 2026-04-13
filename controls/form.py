import pygame
import time
from controls.controls import Control

class Form:
    DOUBLE_CLICK_TIME = 0.5
    IS_DEBUG = False

    def __init__(self):
        self.left_click_time  = 0
        self.right_click_time = 0
        self.controls = {}
        self.groups  = []

    def last_control(self):
        return next(reversed(self.controls.values()))

    def next_down(self,dy:int = 0,c = None):
        if c == None:
            c = self.last_control()
        x = c.rect.left
        y = c.rect.bottom + dy
        return (x,y)

    def next_right(self,dx:int,c=None):
        if c == None:
            c = self.last_control()
        x = c.rect.right + dx
        y = c.rect.top
        return(x,y)

    def get_control_rect(self):
        x0 = 100000
        y0 = 100000
        x1 = 0
        y1 = 0
        for c in self.controls.values():
            if c.rect.left < x0:
                x0 = c.rect.left    
            if c.rect.right > x1:
                x1 = c.rect.right
            if c.rect.top < y0:
                y0 = c.rect.top
            if c.rect.bottom > y1:
                y1 = c.rect.bottom
        return pygame.Rect(x0,y0,x1-x0,y1-y0)         

    def check_cbo(self):
        f = True
        for c in self.controls.values():
            if not c.hide and c.type == Control.COMBOBOX:
                if c.expanded:
                    f = False
                    break

        for c in self.controls.values():
            if not c.hide and c.type == Control.COMBOBOX:
                if not c.expanded:
                    c.clickable = f

    def activate_prev(self):
        l = list(self.controls.values())
        l = list(reversed(l))  
        self._activate_from_list(l) 

    def activate_next(self):
        l = list(self.controls.values())
        self._activate_from_list(l)

    def _activate_from_list(self,list):
        b = 0
        cFirst = None
        for c in list:
            if not c.hide and c.type != Control.LABEL: 
                if cFirst == None:
                    cFirst = c
                if c.active:
                    b = 1
                    c.setActive(False)
                elif b == 1:
                    c.setActive(True)
                    b = 2
                    #print ('Active:',c.name)
                    break
        if cFirst != None:            
            if b != 2:
                cFirst.setActive(True)
                #print ('First: Active:',cFirst.name)

    def handle_controls_events(self,event):
        #self.check_cbo()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT]:
                    self.activate_prev()
                else:
                    self.activate_next()
                return True                       
            else:    
                for c in self.controls.values():
                    if not c.hide and c.type == Control.BUTTON: 
                        if c.key != None:
                            if event.key == c.key:
                                c.call_back()
                                return True
                        if c.active and event.key == pygame.K_RETURN:
                            c.call_back()
                            return True
                        
        pos = pygame.mouse.get_pos()   
        is_left_mouse = False
        is_double     = False   
        is_mouse      = False  

        if event.type == pygame.MOUSEBUTTONDOWN:
            is_left_mouse = True if event.button == 1 else False
            is_mouse = True
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouse = True
            if event.button == 1: #left click
                is_left_mouse = True
                if time.time() - self.left_click_time < Form.DOUBLE_CLICK_TIME:
                    if Form.IS_DEBUG:
                        print("Left double click detected")
                    is_double = True
                self.left_click_time  = time.time()
                self.right_click_time = 0             
            else: #right click
                if time.time() - self.right_click_time < Form.DOUBLE_CLICK_TIME:
                    if Form.IS_DEBUG:
                        print("Right double click detected") 
                    is_double = True
                self.right_click_time = time.time()
                self.left_click_time = 0
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEWHEEL:
            pass
        else:
            return False

        for c in self.controls.values():
            if not c.hide:
                if c.is_has(pos):   
                    c.setActive(True)
                    if c.handle_event(event,is_left_mouse,is_double,pos):
                        return True
                elif c.active and is_mouse:
                    c.setActive(False)
        return False

    def reset(self):
        for c in self.controls.values():
            c.reset()
        for p in self.groups:
            g.reset()

    def show_hint(self,f):
        for c in self.controls.values(): 
            c.show_hint = f   

    def update_controls(self):
        for c in self.controls.values(): 
            c.update()  

    def hide_show(self):
        for c in self.controls.values(): 
            c.hide = not c.hide
            c.reset()
            #print(f"{c.name}-{c.hide}")

    def draw(self, surface: pygame.Surface):
        for p in self.groups:
            p.draw(surface)

        for c in self.controls.values():
            if not c.hide:
                if c.type != Control.COMBOBOX:
                    c.draw(surface)  
                elif not c.is_expanded():
                    c.draw(surface)

        for c in self.controls.values():
            if not c.hide and c.type == Control.COMBOBOX:
                if c.is_expanded():
                    c.draw(surface)  
                    break
        
