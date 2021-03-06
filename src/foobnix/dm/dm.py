'''
Created on Oct 26, 2010

@author: ivan
'''
import gtk
import threading
from foobnix.regui.treeview.dm_tree import DownloadManagerTreeControl
from foobnix.util.const import DOWNLOAD_STATUS_INACTIVE, DOWNLOAD_STATUS_ACTIVE, \
    DOWNLOAD_STATUS_COMPLETED, DOWNLOAD_STATUS_DOWNLOADING, DOWNLOAD_STATUS_ALL, \
    DOWNLOAD_STATUS_STOP, DOWNLOAD_STATUS_ERROR
from foobnix.regui.treeview.dm_nav_tree import DMNavigationTreeControl
import thread
import time
from foobnix.regui.model import FDModel, FModel
from foobnix.dm.dm_dowloader import Dowloader
from foobnix.helpers.window import ChildTopWindow
from foobnix.helpers.toolbar import MyToolbar
import logging
from foobnix.preferences.configs import CONFIG_OTHER

class DMControls(MyToolbar):
    def __init__(self, controls, dm_tree): 
        MyToolbar.__init__(self)   
        
        self.add_button(_("Preferences"), gtk.STOCK_PREFERENCES, controls.preferences.show, CONFIG_OTHER)
        self.add_separator()   
        self.add_button(_("Start Downloading"), gtk.STOCK_MEDIA_PLAY, dm_tree.update_status_for_selected, DOWNLOAD_STATUS_ACTIVE)
        self.add_button(_("Stop Downloading"), gtk.STOCK_MEDIA_PAUSE, dm_tree.update_status_for_selected, DOWNLOAD_STATUS_STOP)
        self.add_separator()   
        #self.add_button("Start All", gtk.STOCK_MEDIA_FORWARD, dm_tree.update_status_for_all, DOWNLOAD_STATUS_ACTIVE)
        #self.add_button("Stop All", gtk.STOCK_STOP, dm_tree.update_status_for_all, DOWNLOAD_STATUS_STOP)
        #self.add_separator()   
        self.add_button("Delete", gtk.STOCK_DELETE, dm_tree.delete_all_selected, None)
        #self.add_button("Delete All", gtk.STOCK_CLEAR, dm_tree.delete_all, None)
        #self.add_separator()
        
    def on_load(self): pass
    def on_save(self): pass

class DM(ChildTopWindow):
    def __init__(self, controls):
        self.controls = controls        
        ChildTopWindow.__init__(self, _("Download Manager"))
        self.set_resizable(True)
        self.set_default_size(900, 700)
        
        vbox = gtk.VBox(False, 0)
        #paned = gtk.HPaned()
        #paned.set_position(200)
        
        self.navigation = DMNavigationTreeControl()
            
        self.navigation.append(FDModel("All").add_artist("All").add_status(DOWNLOAD_STATUS_ALL))
        self.navigation.append(FDModel("Downloading").add_artist("Downloading").add_status(DOWNLOAD_STATUS_DOWNLOADING))
        self.navigation.append(FDModel("Completed").add_artist("Completed").add_status(DOWNLOAD_STATUS_COMPLETED))
        self.navigation.append(FDModel("Active").add_artist("Active").add_status(DOWNLOAD_STATUS_ACTIVE))
        self.navigation.append(FDModel("Inactive").add_artist("Inactive").add_status(DOWNLOAD_STATUS_INACTIVE))
        
        self.dm_list = DownloadManagerTreeControl(self.navigation)
        self.navigation.dm_list = self.dm_list
        #paned.pack1(self.navigation.scroll)
        #paned.pack2(self.dm_list.scroll)
        playback = DMControls(self.controls, self.dm_list)
        
        vbox.pack_start(playback, False, True)
        #vbox.pack_start(paned, True, True)
        vbox.pack_start(self.dm_list.scroll, True, True)
                       
        self.add(vbox)
        thread.start_new_thread(self.dowloader, (self.dm_list,))
        
           
    def demo_tasks(self):
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        self.append_task(FModel("Madonna - Sorry"))
        self.append_task(FModel("Madonna - Frozen"))
        
        
    def show(self):
        self.show_all()
    
    def append_task(self, bean):
        bean.status = DOWNLOAD_STATUS_ACTIVE
        self.dm_list.append(bean)
    
    def append_tasks(self, beans):
        self.show()
        for bean in beans:
            self.append_task(bean)
    
    def dowloader(self, dm_list):
        semaphore = threading.Semaphore(5)
        while True:
            time.sleep(2)
            #self.navigation.use_filter()
            
            
            semaphore.acquire()
            bean = dm_list.get_next_bean_to_dowload()            
            if bean:
                if not bean.path:                 
                    vk = self.controls.vk.find_one_track(bean.get_display_name())
                    if not vk:
                        bean.status = DOWNLOAD_STATUS_ERROR
                        dm_list.update_bean_info(bean)
                        logging.debug("Source for song not found" + bean.text)
                        semaphore.release()
                        continue
                        
                    bean.path = vk.path
                         
                def notify_finish():
                    self.navigation.update_statistics()                    
                    semaphore.release()
                    
                thread = Dowloader(dm_list.update_bean_info, bean, notify_finish)                
                thread.start()
            else:
                time.sleep(1)
                semaphore.release()
if __name__ == '__main__':
    class FakePref():
            def show(self):
                pass
    class Fake():        
        def __init__(self):
            self.preferences = FakePref()
        def show(self):
            pass
        
    controls = Fake()
    dm = DM(controls)
    dm.show()            
    gtk.main()
