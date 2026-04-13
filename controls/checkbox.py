from typing import Tuple,Final
import pygame

from   controls.controls import Control

class Checkbox(Control):
    CHECK_SIZE :Final[int] = 16 
    CHECK_BAR  :Final[int] = CHECK_SIZE * 4
    CHECK_MARK :Final      = [(3,8),(6, 11),(12,4)]
    DX         :Final[int] = 4
    BORDER     :Final[int] = 1
    #
    STYLE_BOX   :Final[int]= 0
    STYLE_RADIO :Final[int]= 1
    STYLE_BAR   :Final[int]= 2

    def __init__(self, name,position: Tuple[float, float] = (0, 0),text: str='' ,checked: bool = False,func=None,style= STYLE_BOX):
        "A basic checkbox."
        super().__init__(name,Control.CHECKBOX,text=text,func=func)
        self.style = style
        self.checked: bool = checked
        self.is_auto_check = True
        self.txt_surf_selected = self.font_selected.render(self.text, 1, Control.CLR_SELECTED)   

        w = Checkbox.CHECK_SIZE
        h = Checkbox.CHECK_SIZE
        
        if self.style == Checkbox.STYLE_BAR:
            self.on  = self.font.render("on" ,1,self.color_text)
            self.off = self.font.render("off",1,self.color_text)
            h = self.font_size + 2
            if h < self.CHECK_SIZE:
                h = self.CHECK_SIZE
            w = self.CHECK_BAR
        
        self.rect_check =pygame.Rect(position[0], position[1], w, h)   
        w += self.txt_surf.get_width()+Checkbox.DX
        h = self.get_control_height(h) 
        self.rect  = pygame.Rect(position[0], position[1], w, h) 
        hy = (self.rect.height - self.rect_check.height)// 2
        self.rect_check.y += hy
        

    def reset(self):
        super().reset()   
        self.txt_surf_selected = self.font_selected.render(self.text, 1, Control.CLR_SELECTED)  

        w = Checkbox.CHECK_BAR if self.style == Checkbox.STYLE_BAR else self.CHECK_SIZE
        w += self.txt_surf.get_width()+Checkbox.DX
        self.rect.width  = w
        self.rect.height = self.get_control_height(Checkbox.CHECK_SIZE)

    def handle_event(self, event, is_left_mouse:bool, is_double_click:bool,position: Tuple[float, float]):  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_auto_check:
                self.checked = not self.checked
            self.call_back(self.checked)
            return True
        return False

    def get_width(self):
        return self.rect.width

    def draw(self, surface: pygame.Surface):
        if self.style == Checkbox.STYLE_BAR:
            if self.checked:
                pygame.draw.rect(surface,Control.CLR_ON,
                                 (self.rect_check.left,self.rect_check.top,self.rect.width - Checkbox.CHECK_SIZE,self.rect.height))
                pygame.draw.rect(surface,Control.CLR_CHECK,self.rect_check,1)
                
                y = (self.rect_check.height - self.off.get_height())// 2 + self.rect.top 
                surface.blit(self.on,(self.rect_check.left,y))
            else:    
                pygame.draw.rect(surface,Control.CLR_INACTIVE_TXT,
                                (self.rect_check.left + Checkbox.CHECK_SIZE ,self.rect_check.top,self.rect_check.width - Checkbox.CHECK_SIZE,self.rect_check.height))
                pygame.draw.rect(surface,Control.CLR_CHECK,self.rect_check,1)
                y = (self.rect_check.height - self.off.get_height())// 2 + self.rect_check.top 
                x = self.rect_check.left + self.rect.width   - self.off.get_width() - 4
                surface.blit(self.off,(x,y)) 

        elif self.style == Checkbox.STYLE_RADIO:
            r = Checkbox.CHECK_SIZE / 2
            x = self.rect_check.centerx
            y = self.rect_check.centery
            pygame.draw.circle(surface,Control.CLR_CHECK,(x,y),r,Checkbox.BORDER)
            if self.checked:
                r -= 4
                pygame.draw.circle(surface,Control.CLR_CHECK,(x,y),r)
        else:    
            checkmark = []
            #print(self.rect)

            for (x,y) in self.CHECK_MARK:
                x += self.rect_check.x
                y += self.rect_check.y 
                checkmark.append((x,y))

            pygame.draw.rect(surface, Control.CLR_CHECK, self.rect_check, 1)
            if self.checked:
                pygame.draw.lines(surface, Control.CLR_CHECK, False, checkmark, Checkbox.BORDER)
        x = self.rect_check.right + Checkbox.DX
        y = self.rect.top + (self.rect.height - self.txt_surf.get_height())//2
        
        if self.active:
            surface.blit(self.txt_surf_selected ,(x,y))
        else:    
            surface.blit(self.txt_surf ,(x,y))
        #pygame.draw.rect(surface,Control.CLR_BORDER,self.rect,1)    
        