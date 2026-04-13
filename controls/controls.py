import pygame
from typing  import Tuple,Final

def _find_defaut_font():
    fonts = pygame.font.get_fonts()
    #print (fonts)
    df = {}
    checkeds = ["verdana","arial","helvetica","segoeui","calibri","tahoma"]
    for f in fonts:
        #print(f)
        for t in checkeds:
            if t == f:
               df[t] = f
               return t

            elif not t in df and t in f:
                df[t] = f

    for t in checkeds:
        if t in df:
            return df[t]

    return fonts[0]

class Control:
    IS_DEBUG = True

    DAY_MODE   :Final[int] = 0
    NIGHT_MODE :Final[int] = 1 
    RED_MODE   :Final[int] = 2 
    GREEN_MODE :Final[int] = 3 
    GRAY_MODE  :Final[int] = 4
    DESERT_MODE:Final[int] = 5

    THEME_RED    :Final[str]= "Mars"
    THEME_FOREST :Final[str]= "Forest"
    THEME_GRAY   :Final[str]= "Gray"
    THEME_BLACK  :Final[str]= "Night"
    THEME_WHITE  :Final[str]= "Snow"
    THEME_DESERT :Final[str]= "Desert"

    THEMES_BY_NAME = {
      THEME_FOREST: GREEN_MODE, 
      THEME_GRAY  : GRAY_MODE,    
      THEME_RED   : RED_MODE,
      THEME_BLACK : NIGHT_MODE,
      THEME_WHITE : DAY_MODE,
      THEME_DESERT: DESERT_MODE
    }
    THEMES_BY_MODE = {
      GREEN_MODE : THEME_FOREST, 
      GRAY_MODE  : THEME_GRAY,    
      RED_MODE   : THEME_RED,
      NIGHT_MODE : THEME_BLACK,
      DAY_MODE   : THEME_WHITE,
      DESERT_MODE: THEME_DESERT
    }

    KEY_HINT            : Final[str]= "hint"
    KEY_TEXT            : Final[str]= "text"
    KEY_INACTIVE_TXT    : Final[str]= "inactive_txt"
    KEY_BK              : Final[str]= "bk"
    KEY_CHECK           : Final[str]= "check"
    KEY_SELECTED_ITEM   : Final[str]= "selected_item"
    KEY_SELECTED        : Final[str]= "selected"
    KEY_CBO_LINE        : Final[str]= "cbo_line"  # used to drow comboob
    KEY_AROW            : Final[str]= "arrow"
    KEY_ON              : Final[str]= "on"
    KEY_BORDER          : Final[str]= "border"

    KEY_BTN             : Final[str]= "button"
    KEY_BTN_CHNG        : Final[str]= "button_chng"
    KEY_BTN_HINT        : Final[str]= "button_hint"

    LABEL    :Final[int]= 0
    BUTTON   :Final[int]= 1
    CHECKBOX :Final[int]= 2
    TEXTBOX  :Final[int]= 3
    COMBOBOX :Final[int]= 4
    LISTBOX  :Final[int]= 5
    SLIDER   :Final[int]= 6

    MODES = {
        DAY_MODE:{
            KEY_HINT            :(0,0,255),
            KEY_TEXT            :(0,0, 0),
            KEY_SELECTED        :(0,0, 64),
            KEY_INACTIVE_TXT    :(64, 64, 205),
            KEY_BK              :(255,255,255),
            KEY_CHECK           :(0,0,0),
            KEY_SELECTED_ITEM   :(212,212,212),
            KEY_AROW            :(127,127,127),            
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 192, 192),
            KEY_ON              :( 0,127,0),
            KEY_BORDER          :( 0,  0,0)
        },
        NIGHT_MODE:{ 
            KEY_HINT            :(255,255,127),
            KEY_TEXT            :(255,255, 255),
            KEY_SELECTED        :(0,0, 0),
            KEY_INACTIVE_TXT    :(212, 212, 212),
            KEY_BK              :(0,0,0),
            KEY_CHECK           :(255,255,255),
            KEY_SELECTED_ITEM   :(255,0,0),
            KEY_AROW            :(127,127,127),  
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 0, 0),
            KEY_ON              :(  0,127,0),
            KEY_BORDER          :(255,255,255)
        },
        RED_MODE:{ 
            KEY_HINT            :(255,255,127),
            KEY_TEXT            :(255,255,255),
            KEY_SELECTED        :(0,0, 0),
            KEY_INACTIVE_TXT    :(255, 255, 0),
            KEY_BK              :(255,0,0),
            KEY_CHECK           :(255,255,255),
            KEY_SELECTED_ITEM   :(127,0,0),
            KEY_AROW            :(127,127,127),  
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 255, 0),
            KEY_ON              :(  0,127,0),
            KEY_BORDER          :(255,255,255)     
        },
        GREEN_MODE:{ 
            KEY_HINT            :(255,255,127),
            KEY_TEXT            :(255,255, 0),
            KEY_SELECTED        :(0,0, 0),
            KEY_INACTIVE_TXT    :(192, 192, 205),
            KEY_BK              :(0,127,0),
            KEY_CHECK           :(255,255,255),
            KEY_SELECTED_ITEM   :(0,64,0),
            KEY_AROW            :(127,127,127),  
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 0, 0),
            KEY_ON              :(  0,127,0),
            KEY_BORDER          :(255,255,255)    
        },
        GRAY_MODE:{ 
            KEY_HINT            :(255,255,127),
            KEY_TEXT            :(255,255, 255),
            KEY_SELECTED        :(0,0, 0),
            KEY_INACTIVE_TXT    :(141, 182, 205),
            KEY_BK              :(127,127,127),
            KEY_CHECK           :(255,255,255),
            KEY_SELECTED_ITEM   :(127,0,0),
            KEY_AROW            :(127,127,127),  
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 0, 0) ,
            KEY_ON              :(  0,127,0),
            KEY_BORDER          :(255,255,255)   
        },
        DESERT_MODE:{ 
            KEY_HINT            :(255,255,127),
            KEY_TEXT            :(255,255, 255),
            KEY_SELECTED        :(0,0, 0),
            KEY_INACTIVE_TXT    :(141, 182, 205),
            KEY_BK              :(255,127,0),
            KEY_CHECK           :(255,255,255),
            KEY_SELECTED_ITEM   :(127,0,0),
            KEY_AROW            :(127,127,127),  
            KEY_CBO_LINE        :(127,127,127),
            KEY_BTN             :(220, 220, 220),
            KEY_BTN_CHNG        :(255, 0, 0) ,
            KEY_ON              :(  0,127,0),
            KEY_BORDER          :(255,255,255)   
        }        
    }
    
    mode  = DAY_MODE

    BK                  = MODES[mode][KEY_BK]
    CLR_HINT            = MODES[mode][KEY_HINT]
    CLR_TEXT            = MODES[mode][KEY_TEXT]
    CLR_SELECTED        = MODES[mode][KEY_SELECTED]
    CLR_CHECK           = MODES[mode][KEY_CHECK]
    CLR_SELECTED_ITEM   = MODES[mode][KEY_SELECTED_ITEM]
    CLR_ARROW           = MODES[mode][KEY_AROW]
    CLR_CBO_LINE        = MODES[mode][KEY_CBO_LINE]
    CLR_INACTIVE_TXT    = MODES[mode][KEY_INACTIVE_TXT]
    CLR_BTN             = MODES[mode][KEY_BTN]
    CLR_BTN_CHNG        = MODES[mode][KEY_BTN_CHNG]
    CLR_ON              = MODES[mode][KEY_ON]
    CLR_BORDER          = MODES[mode][KEY_BORDER]
    #

    FONT_DEFAULT = _find_defaut_font()

    FONT         = FONT_DEFAULT
    FONT_BOLD   :Final[bool]=  False #True
    FONT_SIZE   :Final[int]= 18
    #print(FONT_DEFAULT)

    shared_font          = None
    shared_font_selected = None
    text_control_height  = 0
    BORDER_LIST_SIZE     = 1

    #
    controls    = []
    form        = None
    selected    = None

    def __init__(self,name,controlType,font_name = None,font_size= None,func = None,text = '',clr_text = None,hint_clr=None):
       # self.value: float = 0.0
        self.name = text if name == '' else name
        self.hide = False
        self.type = controlType
        self.func = func
        if font_name != None or font_size != None:
            self.shared_font = False
            self.font_name    = Control.FONT      if font_name == None else font_name
            self.font_size    = Control.FONT_SIZE if font_size == None else font_size
            self.font         = pygame.font.SysFont(self.font_name, self.font_size,Control.FONT_BOLD) 
            if text != None:
                self.font_selected = pygame.font.SysFont(self.font_name, self.font_size,Control.FONT_BOLD,italic=True) 
        else:
            self.shared_font = True
            self.font_name= Control.FONT 
            self.font_size= Control.FONT_SIZE 
            self.font     = Control.shared_font
            self.font_selected = Control.shared_font_selected 
        self.key  = None

        self.text = text    
        self.p_clr_txt = clr_text
        self.color_text = Control.CLR_TEXT if  self.p_clr_txt  == None else self.p_clr_txt 
        if self.text != None:
            self.txt_surf = self.font.render(self.text, 1, self.color_text)
        
        #hints
        self.show_hint = True
        self.hint      = ''
        self.hint_surf= None
        if hint_clr == None:
            self.hint_clr = self.CLR_HINT
        else:
            self.hint_clr = hint_clr

        self.active = False
        self.linked = []

        if self.name != None:
            if Control.form != None:
                Control.form.controls[self.name] = self
            Control.controls.append(self)
    
    def add_linked_controls(self,c):
        self.linked.append(c)
        c.linked.append(self)
        c.active    = False
        self.active = False

    def setActive(self,f):
        if f:
            if self.form != None:
                for c in self.form.controls.values():
                    if c.active:
                        c.active = False
            
        self.active = f
        for x in self.linked:
            x.active = f

    def is_has(self,pos):
        return self.rect.collidepoint(pos) 

    def set_hint(self,hint):
        self.hnt = hint
        if  self.hint_surf == None:
            font_size =  self.font_size - 2
            font_hint = pygame.font.SysFont(self.font_name,font_size)
            self.hint_surf = font_hint.render(self.hint, 1,  self.hint_clr)
        else:
            self.hint_surf = font_hint.render(self.hint, 1, self.hint_clr)

    def draw_hint(self,screen):
        if self.show_hint:
            if len(self.hint) > 0 :
                if self.hint_surf == None:
                    self.set_hint(self.hint)
                #print(f"hint:{self.rect}")
                screen.blit(self.hint_surf, (self.rect.left+ 10,self.rect.bottom))

    def reset(self):
        if self.shared_font:
            self.font_name= Control.FONT 
            self.font_size= Control.FONT_SIZE 
            self.font     = Control.shared_font
            self.font_selected = Control.shared_font_selected 
        self.color_text = Control.CLR_TEXT if  self.p_clr_txt  == None else self.p_clr_txt 
        if self.text != None:
            self.txt_surf = self.font.render(self.text, 1, self.color_text)

    def update(self):
        pass       

    def move(self, position: Tuple[float, float]):
        pass  # controls can optionally overwrite this default move() method

    def draw(self, surface: pygame.Surface):
        raise Exception("All controls need to implement a draw() method")

    def handle_event(self, event,is_left_mouse:bool, is_double_click:bool, position: Tuple[float, float]):
        return False

    def call_back(self, *args):
        Control.selected = self
        if self.func != None:
            if self.func:
                return self.func(*args)
            
    def get_control_height(self,height):
        if height == 0:
            return Control.text_control_height
        elif height > Control.text_control_height:
            return height        
        else:
            return Control.text_control_height

def set_contols_mode(mode):
    Control.mode = mode
    mode_values = Control.MODES[mode]
    Control.CLR_HINT            = mode_values[Control.KEY_HINT]
    Control.CLR_TEXT            = mode_values[Control.KEY_TEXT]
    Control.CLR_SELECTED        = mode_values[Control.KEY_SELECTED]
    Control.BK                  = mode_values[Control.KEY_BK]
    Control.CLR_CHECK           = mode_values[Control.KEY_CHECK]
    Control.CLR_SELECTED_ITEM   = mode_values[Control.KEY_SELECTED_ITEM]
    Control.CLR_ARROW           = mode_values[Control.KEY_AROW]
    Control.CLR_CBO_LINE        = mode_values[Control.KEY_CBO_LINE]
    Control.CLR_INACTIVE_TXT    = mode_values[Control.KEY_INACTIVE_TXT]
    Control.CLR_BTN             = mode_values[Control.KEY_BTN]
    Control.CLR_BTN_CHNG        = mode_values[Control.KEY_BTN_CHNG]
    Control.CLR_ON              = mode_values[Control.KEY_ON]
    Control.CLR_BORDER          = mode_values[Control.KEY_BORDER]

    #print("Theme",mode,Control.BK)

def reset_all_controls():
    for c in Control.controls:
        c.reset() 

def init_controls():
    if Control.shared_font == None:
        Control.shared_font           = pygame.font.SysFont(Control.FONT, Control.FONT_SIZE,bold = Control.FONT_BOLD) 
    if Control.shared_font_selected == None:
        Control.shared_font_selected = pygame.font.SysFont(Control.FONT, Control.FONT_SIZE,bold = Control.FONT_BOLD,italic=True) 
    temp_txt_surface = Control.shared_font.render("A",1,(0,0,0))   
    Control.text_control_height = temp_txt_surface.get_height()  

def update_controls_font(font_name):
    Control.FONT = font_name
    Control.shared_font          = pygame.font.SysFont(Control.FONT, Control.FONT_SIZE,bold = Control.FONT_BOLD) 
    Control.shared_font_selected = pygame.font.SysFont(Control.FONT, Control.FONT_SIZE,bold = Control.FONT_BOLD,italic=True) 
    reset_all_controls()

def save_controls_settings():
    values = {
        'mode' : Control.mode ,
        'font' : Control.FONT
    }
    return values

def default_contols_setings():
    Control.mode = Control.DAY_MODE
    update_controls_font(Control.FONT_DEFAULT)
   
def restore_controls_settings(values:list):
    Control.mode = values['mode']
    update_controls_font(values['font'])

def get_theme():
    return Control.THEMES_BY_MODE[Control.mode]


