from typing import Tuple,Final
import pygame

from controls.controls import Control
from controls.slider   import Slider

class ListBox(Control):
    DX:Final[int] = 3
    DY:Final[int] = 2

    def __init__(self, name: str,position: Tuple(float,float), values:list,index:int,visible_size=0, func=None,width = 0):
        "A basic listbox."
        super().__init__(name,Control.LISTBOX,font_name=None,font_size=None,func=func,text=values[index])

        self.index_top    = 0
        self.border       = Control.BORDER_LIST_SIZE
        self.index        = index
        self.visible_size = visible_size
        self.values       = values
        self.size         = len(self.values)
        self.item_height  = self.font_size + self.border 
        
        self.text_surfs = [] 
        x = position[0]
        y = position[1]     

        self.p_width = width
        self.set_values()

        self.slider = None
        if self.visible_size == 0:
            h = self.item_height * self.size  + self.border + 2 * ListBox.DY   
            self.rect = pygame.Rect(x,y,self.width,h)
        else:
            h = self.item_height * self.visible_size + self.border +  2 * ListBox.DY 
            self.rect = pygame.Rect(x,y,self.width,h)
      
            if self.index >=  self.visible_size:
                self.index_top = self.index - self.visible_size+1       
            dl = 1
            x = self.rect.right - Slider.H-dl           
            self.slider = Slider(name=None,position=(x,self.rect.top+dl),size=self.rect.height-2*dl,
                                 min_value=0,max_value=1,value=self.index,is_arrow=True,is_marker=False)
            #print(self.index_top,self.index)
        self.parentCombo = None
      
    def set_values(self):
        w = 0
        self.text_surfs.clear()
        for v in self.values:
            t = self.font.render(v,1,self.color_text)
            self.text_surfs.append(t)
            witem = t.get_width()
            if witem > w:
                w = witem
        #   
        w += 2 * ListBox.DX 
        if w < self.p_width:
            w = self.p_width
        self.width = w 

    def reset(self):
        super().reset()
        self.text_surfs.clear()
        self.set_values()
        self.rect.width = self.width

    def is_has(self,pos):
        if super().is_has(pos):
            return True
        if self.slider != None:
            if self.slider.is_has(pos):
                return True
        return False

    def find_selected(self,y):
        y -= self.rect.top
        i = y // self.item_height   
        return i + self.index_top        

    def adjust_top_index(self):
        if self.visible_size != 0:
            if self.index < self.index_top:
                self.index_top = self.index
            elif self.index >= self.index_top + self.visible_size:
                self.index_top = self.index - self.visible_size+1
            #print(f"list {self.name},index={self.index},top={self.index_top} ,size={self.visible_size}")

    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        if self.hide:
            return False
        
        if self.slider != None:
            if self.slider.handle_event(event,is_left_mouse,is_double_click,position):
                v = self.slider.value
                index = self.index
                if v < 0.5:
                    index -= 1
                else:
                    index += 1
                if index >= 0 and index < self.size:
                    self.index = index       
                    self.adjust_top_index()
                    if self.parentCombo != None:
                        self.parentCombo.setIndex(self.index)
                    else:
                        self.call_back(self.values[self.index],self.index)

                return True 
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                mods = pygame.key.get_mods()
                if event.key == pygame.K_UP:
                    if mods & pygame.KMOD_META:
                        self.index = 0
                        self.adjust_top_index()    
                    else:     
                        self.update_index(-1)
                    return True
                elif event.key == pygame.K_DOWN:
                    if mods & pygame.KMOD_META:
                        self.index = self.size -1 
                        self.adjust_top_index()
                    else:
                        self.update_index(1)
                    return True
                else:
                    i = 0
                    for v in self.values:
                        ch = v[0].casefold()
                        if ch == event.unicode.casefold():
                            self.index = i
                            self.adjust_top_index()
                            break
                        i += 1            
                
        elif event.type == pygame.MOUSEWHEEL:
            if self.active:
                if event.y > 0:
                    self.update_index(1)
                elif event.y < 0:
                    self.update_index(-1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('List-mouse down',self.rect,position)
            if self.rect.collidepoint(position):
                #print('list = mouse down')
                self.index = self.find_selected(position[1])
                if self.parentCombo == None:
                    self.setActive(True)
                    self.call_back(self.values[self.index],self.index)
                else:
                    self.parentCombo.setIndex(self.index) 
                    self.hide = True
                return True                
            elif self.active:
                if self.slider != None:
                    if not self.slider.rect.collidepoint(position):
                        self.setActive(False)
                else:
                    self.setActive(False)
        return False

    def update_index(self,d):
        index = self.index + d
        if index >= 0 and index < self.size:
            #print(f"list:{self.name},changes {d},old index={self.index}, new index {index}")
            self.index = index
            self.adjust_top_index()
            if self.parentCombo != None:
                self.parentCombo.setIndex(self.index)
            else:
                self.call_back(self.values[self.index],self.index)
            
    def draw(self, screen: pygame.Surface):     
        x = self.rect.left+ListBox.DX
        y = self.rect.top +ListBox.DY
        pygame.draw.rect(screen,Control.BK,self.rect) 
        pygame.draw.rect(screen,Control.CLR_BORDER,self.rect,self.border) 
        i = 0
        j = 0
    
        for t in self.text_surfs:
            if i >= self.index_top:
                if i == self.index:
                    pygame.draw.rect(screen,Control.CLR_SELECTED_ITEM,(x,y,self.rect.width - 2 * ListBox.DX,self.item_height))
                if i != 0:
                    pygame.draw.line(screen,Control.CLR_CBO_LINE,(x,y),(self.rect.right-ListBox.DX,y),1)
                dy = (self.item_height - t.get_height()) / 2     
                screen.blit(t,(x,y+dy))
                y += self.item_height
                j += 1
                if j == self.visible_size and self.visible_size != 0:
                    break    
            i += 1

        if self.slider != None:
            self.slider.draw(screen)      
    