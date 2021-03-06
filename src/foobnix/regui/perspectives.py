#-*- coding: utf-8 -*-
'''
Created on 22 сент. 2010

@author: ivan
'''
import gtk
from foobnix.helpers.toggled import OneActiveToggledButton
from foobnix.regui.model.signal import FControl
from foobnix.util.fc import FC
from foobnix.util.const import LEFT_PERSPECTIVE_INFO, LEFT_PERSPECTIVE_VIRTUAL, \
    LEFT_PERSPECTIVE_NAVIGATION, LEFT_PERSPECTIVE_RADIO
from foobnix.helpers.my_widgets import PespectiveToogledButton, ButtonStockText
from foobnix.regui.state import LoadSave
class PerspectiveControls(FControl, gtk.VBox, LoadSave):
    def __init__(self, controls):
        FControl.__init__(self, controls)
        gtk.VBox.__init__(self, False, 0)
        
        self.perspectivs = {
                     LEFT_PERSPECTIVE_NAVIGATION:controls.tabhelper,
                     LEFT_PERSPECTIVE_RADIO:controls.radio.scroll,
                     LEFT_PERSPECTIVE_VIRTUAL:controls.virtual.scroll,
                     LEFT_PERSPECTIVE_INFO:controls.info_panel
                     }
        
        self.buttons = PerspectiveButtonControlls(self.activate_perspective, controls)
        self.buttons.show_all()
        
        self.add_button = ButtonStockText(_("Add Folder(s) in tree"), gtk.STOCK_ADD)
        self.add_button.connect("clicked", lambda * a :controls.tree.add_folder())
        
        self.pack_start(self.add_button, False, False)
        
        for widget in self.perspectivs.values():
            self.pack_start(widget, True, True)
                
        self.pack_start(controls.filter, False, False)
        self.pack_start(self.buttons, False, False)
    
    def show_add_button(self):
        self.add_button.show()
    
    def hide_add_button(self):
        self.add_button.hide()
    
    def activate_perspective(self, name):
        for widget in self.perspectivs.values():
            widget.hide()
        FC().left_perspective = name
        self.perspectivs[name].show()
        
        if name == LEFT_PERSPECTIVE_INFO:
            self.controls.filter.hide()
            self.controls.info_panel.update_info_panel()
        else:
            self.controls.filter.show()
   
    def activate_perspective_key(self, name):
        self.buttons.activate_button(name)
    
    def on_load(self):  
        self.activate_perspective(LEFT_PERSPECTIVE_NAVIGATION)
        
    def on_save(self):
        pass

class PerspectiveButtonControlls(gtk.HBox):
    def __init__(self, activate_perspective, controls):
        
        gtk.HBox.__init__(self, False, 0)
        
        self.active = None
               
        musics = PespectiveToogledButton(_("Music"), gtk.STOCK_HARDDISK, _("Music Navigation (Alt+1)"))
        musics.connect("clicked", lambda * a: activate_perspective(LEFT_PERSPECTIVE_NAVIGATION))        
        musics.set_active(True)
        
                
        radios = PespectiveToogledButton(_("Radio"), gtk.STOCK_NETWORK, _("Radio Stantions (Alt+2)"))
        radios.connect("clicked", lambda * a:controls.radio.lazy_load())
        radios.connect("clicked", lambda * a:activate_perspective(LEFT_PERSPECTIVE_RADIO))
        
        
        
        virtuals = PespectiveToogledButton(_("Play Lists"), gtk.STOCK_INDEX, _("Virtual Play Lists (Alt+3)"))
        virtuals.connect("clicked", lambda * a:activate_perspective(LEFT_PERSPECTIVE_VIRTUAL))
        
        
        info = PespectiveToogledButton(_("Info"), gtk.STOCK_INFO, _("Info Panel (Alt+4)"))
        info.connect("clicked", lambda * a: activate_perspective(LEFT_PERSPECTIVE_INFO))
                
        self.button_list = {
                     LEFT_PERSPECTIVE_NAVIGATION:musics,
                     LEFT_PERSPECTIVE_RADIO:radios,
                     LEFT_PERSPECTIVE_VIRTUAL:virtuals,
                     LEFT_PERSPECTIVE_INFO:info
                     }
        
        OneActiveToggledButton(self.button_list.values())
        
        self.pack_start(musics, False, False, 0)
        self.pack_start(radios, False, False, 0)
        self.pack_start(virtuals, False, False, 0)
        self.pack_start(info, False, False, 0)
    
    def activate_button(self, name):
        self.button_list[name].set_active(True)
