
import pygame
import os
from   typing import Final

from controls.form       import Form
from controls.button     import Button
from controls.controls   import Control,init_controls
from controls.label      import Label 
from controls.textBox    import InputBox
from controls.label      import Label 
from controls.checkbox   import Checkbox
from controls.combobox   import Combobox
from controls.checkGroup import CheckGroup,reset_all_groups
from settings   import *


class MainForm(Form):
    def __init__(self,field,game):
        super().__init__()
        Control.FONT_SIZE = 16
        CheckGroup.DY     = 6

        init_controls()
        Control.mode = Control.DAY_MODE
        Control.form = self
        self.rect  = game.info_rect
        self.field = field
        self.game  = game
        
        self._create_controls()
        self.show_hint(False)
    
    def _create_controls(self):
        W_BUTTON = 116
        H_BUTTON = 48
        D_H = 18

        resource_folder = self.game.resource_folder
        x_button = self.rect.left + (self.rect.width -  W_BUTTON)//2 + W_BUTTON/2
        y_button = self.field.yTop + H_BUTTON // 2

        imgBack = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER, 'cancel.png')).convert_alpha()
        self.btnBack = Button('btnBack',position=(x_button, y_button),  size=(W_BUTTON, H_BUTTON),  func=self._back, text='Back',image=imgBack)
        self.btnBack.hide  = True
        self.btnBack.hint  = "Back to main menu" 
        self.btnBack.key   = pygame.K_ESCAPE

        imgStart = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER,'start.png')).convert_alpha()
        btnStart = Button('btnStart',position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func= self.game.start, text='Start',image = imgStart)
        btnStart.hint  = "Start play the game"
        btnStart.key   = pygame.K_SPACE
   
        y_button += H_BUTTON
        y_button += D_H
        imgAbout = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER, self.game.ABOUT_IMAGE)).convert_alpha()
        btnAbout = Button('btnAbout',position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.about, text='About',image=imgAbout)
        btnAbout.hint  = "Show about information"
          
        y_button += H_BUTTON
        y_button += D_H
        imgHelp  = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER,"help.png")).convert_alpha()
        btnHelp  = Button('btnHelp',position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.help, text='Help',image=imgHelp)
        btnHelp.hint  = "Show help information"

        y_button += H_BUTTON
        y_button += D_H
        imgOptions  = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER,"options.png")).convert_alpha()
        btnOptions  = Button('btnOptions',position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.change_settings, text='Settings',image=imgOptions)
        btnOptions.hint  = "Change settings"
     
        y_button += H_BUTTON
        y_button += D_H
        imgExit  = pygame.image.load(os.path.join(resource_folder,IMAGE_FOLDER,'exit.png')).convert_alpha()
        btnExit  = Button('btnExit',position=(x_button, y_button), size=(W_BUTTON, H_BUTTON), func=self.exit_game, text='Exit',image=imgExit)
        btnExit.hint  = "Exit the game"      

    def _back(self):
        self.game.mode = MODE_INFO
        self.hide_show()        

    def about(self):
        self.game.mode = MODE_ABOUT
        self.hide_show()

    def help(self):
        self.game.mode = MODE_HELP
        self.hide_show()    

    def exit_game(self):
        self.game.running = False    
   
    def change_settings(self):
        self.game.mode = MODE_SETTINGS
        self.hide_show()    

    def y_info(self):
        return self.btnBack.rect.bottom     

class FormOptions(Form):
    def __init__(self,game):
        super().__init__()
        #
        self.main_form = Control.form  
        Control.form = self
        #
        self.game = game 
        self.rect = game.info_rect
        self._create_controls()

    def _create_controls(self):
        DY = 4
        #x = self.rect.left + CELL_SIZE * 4 
        x = self.rect.left + CELL_SIZE * 2 
        y = self.main_form.btnBack.rect.bottom + CELL_SIZE 

        self.chk_sound = Checkbox('chkSound',(x,y),"Sound",self.game.is_sound,func= self.sound_from_settings)
      
        (x,y) = self.next_down(DY)
        self.chk_mk_music = Checkbox('chkMusic',(x,y),"Backround music",self.game.is_background_music,func= self.bk_music_from_settings)
      
        (x,y) = self.next_down(DY)
        self.chk_hold = Checkbox('chkHold',(x,y),"Use hold",self.game.is_hold,func= self.set_hold)

        (x,y )= self.next_down(DY)
        lblPreview = Label('lblPreview',(x,y),"Preview:")
        preview_list = ['None',"1 item","2 items"]
        cboPreview = Combobox('cboPreview',position=(x + lblPreview.get_width() + 10,y),values=preview_list,index=self.game.next_block_size,width = 0,func=self.set_preview)
        
        (xv,y )= self.next_down(DY)
        lblGarbage = Label('lblGarbage',(x,y),"Garbage rows:")
        garbage_list = []
        for i in range(8):
            garbage_list.append(str(i))            
        cboGarbage= Combobox('cboGarbage',position=(x + lblGarbage.get_width() + 10,y),values=garbage_list,index=self.game.garbage_rows,width = 0,func=self.set_garage)
       
      
        (xv,y) = self.next_down(DY)
        y += CELL_SIZE * 2
        sizes = []
        for key in SIZES.keys():
            sizes.append(SIZES[key])
            
        self.sizeGroup = CheckGroup(sizes,self.game.size_index,x,y,caption= "Sizes",name="grpSize",
                                    multi_sellect = False,func=self.set_size)

        y = self.sizeGroup.rect.bottom
        y += 16
        self.bkGroup = CheckGroup(self.game.background,self.game.bk_index,x,y,caption="Background",name="grpBK",
                                  multi_sellect=False,func=self.set_background)

        y = self.bkGroup.rect.bottom
        y += 16
        self.label = Label('lblName',(x,y),"Your name:")
        self.txtName = InputBox('txtName', position=( x + self.label.get_width() + 10,y),text=self.game.user_name,width=80,height=24)
        self.txtName.func = self.set_user_name               

    def sound_from_settings(self,source):
        self.game.is_sound = self.chk_sound.checked   

    def bk_music_from_settings(self,source):
        self.game.is_background_music = self.chk_mk_music.checked

    def set_user_name(self,un):
        self.game.user_name = un       

    def set_background(self,index,checked):
        self.game.bk_index = index
        self.game.set_field_size() 
            
    def set_size(self,index,checked): 
        self.game.size_index = index
        self.game.set_field_size() 

    def set_preview(self,value,index):
        self.game.next_block_size = index

    def set_garage (self,value,index):
        self.game.garbage_rows = index      
        
    def set_hold(self,value):
        self.game.is_hold = value     
  
