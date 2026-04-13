from typing import Tuple,Final
import pygame

from controls.controls import Control
from controls.listbox  import ListBox

class Combobox(Control):
    DY      :Final[int] = 2 
    SIZE_TR :Final[int] = 16
    H_TR    :Final[float]= 0.7 * SIZE_TR
    D_TR    :Final[int] = 2

    def __init__(self, name: str,position: Tuple(float,float),values:list,index:int, width:int,height:int=0,func=None,visible_size = 0):
        "A basic combobox."
        super().__init__(name,Control.COMBOBOX,func=func,text=values[index])
        self.pwidth  = width
        self.pheight = height
    
        self.height     = self.get_control_height(self.pheight )
        self.active     = False
        self.index_top    = 0
        self.visible_size = visible_size

        self.index        = index
        self.values       = values
        self.size         = len(values)
        x = position[0]
        y = position[1]     

        self.list = ListBox(name=None,position=(x,y+self.height), values=values,index=self.index,visible_size=self.visible_size)
        self.list.hide = True
        self.list.parentCombo = self
  
        self.border       = self.list.border
        self.text_surfs = self.list.text_surfs

        self.height = self.get_control_height(height)
        self._calculate_width()
        self.rect  = pygame.Rect(self.list.rect.x, y-Combobox.DY, self.width , self.height)
        self.list.rect.width = self.rect.width
    
    def _calculate_width(self):
        self.width = self.list.rect.width 
        if self.visible_size == 0:
            self.width += (Combobox.SIZE_TR + 2 * Combobox.D_TR)
        if self.width < self.pwidth:
            self.width = self.pwidth
  
    def is_has(self,pos):
        if super().is_has(pos):
            return True
        if self.is_expanded():
            return self.list.is_has(pos)
        return False

    def reset(self):    
        super().reset() 
        self.list.reset()
        self.height= self.get_control_height(self.pheight)
        self._calculate_width()
        self.list.rect.width = self.rect.width    

    def setValue(self,value):
        try:
            i = self.values.index(value)
            self.setIndex(i)
        except:
            pass

    def setIndex(self,index):
        if index != self.index:
            self.index = index
            self.text  = self.values[self.index]
            self.txt_surf = self.font.render(self.text, 1, self.color_text)
            self.call_back(self.text,self.index)

    def is_expanded(self):
        return not self.list.hide

    def expand(self):
        self.list.hide = False
        self.list.adjust_top_index()
        self.list.active = True

    def draw_tr(self,screen):
        x = self.rect.right - Combobox.SIZE_TR - Combobox.D_TR
        y = self.rect.top + (self.rect.height - Combobox.H_TR) // 2
        h = Combobox.H_TR
        size = Combobox.SIZE_TR
        if self.is_expanded():
            triangle_points = [(x, y+h), (x + size, y+h), (x+size//2, y)]
        else:     
            triangle_points = [(x, y), (x + size ,y), (x+size//2, y+h)]   
        pygame.draw.polygon(screen, Combobox.CLR_ARROW, triangle_points)
    
    def update_value(self):
        self.text = self.values[self.index]
        self.txt_surf = self.font.render(self.text, 1, self.color_text) 
        self.call_back(self.text,self.index)

    def collapse(self):
        self.update_value()

    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        if self.is_expanded():
            #print('expnaded')
            if self.list.handle_event(event,is_left_mouse,is_double_click,position):
                return True 
         
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_UP:
                    self.update_index(-1)
                    return True
                elif event.key == pygame.K_DOWN:
                    self.update_index(1)
                    return True
                else:
                    i = 0
                    for v in self.values:
                        ch = v[0].casefold()
                        if ch == event.unicode.casefold():
                            self.index = i
                            self.update_value()
                            break
                        i += 1
        elif event.type == pygame.MOUSEWHEEL:
            if self.active and not self.is_expanded():
                if event.y > 0:
                    self.update_index(1)
                elif event.y < 0:
                    self.update_index(-1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(position):
                if not self.active:
                    self.setActive(True)
                if self.is_expanded():
                    self.list.hide = True
                else:
                    self.expand()
                return True
            else:
                self.setActive(False)
                self.list.hide = True     
        return False         
     
    def update_index(self,d):
        index = self.index + d 
        if index >= 0 and index < self.size:
            self.setIndex(index)
            if self.index < self.index_top:
                self.index_top = self.index
            elif self.index >= self.index_top + self.visible_size:
                self.index_top = self.index - self.visible_size+2
            if not self.is_expanded():
                self.update_value()    
            #print('Combo:',self.index_top,self.index,self.values[self.index])       

    def draw(self, screen: pygame.Surface): 
        # Blit the text.
        y = self.rect.top + (self.rect.height - self.txt_surf.get_height())//2
        screen.blit(self.txt_surf, (self.rect.x+ListBox.DX, y))
        self.draw_tr(screen)
        # Blit the rect.
        pygame.draw.rect(screen, self.CLR_BORDER, self.rect, self.border)
        if self.is_expanded() and self.active:
            self.list.draw(screen)
   
