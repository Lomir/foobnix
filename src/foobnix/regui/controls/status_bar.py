#-*- coding: utf-8 -*-
'''
Created on 28 сент. 2010

@author: ivan
'''
from foobnix.regui.model.signal import FControl
import gtk
class StatusbarControls(gtk.Statusbar, FControl):
    def __init__(self, controls):
        gtk.Statusbar.__init__(self)
        FControl.__init__(self, controls)
        self.show()

    def set_text(self, text):
        if text:
            self.push(0, text)
        else:
            self.push(0, "")
    
