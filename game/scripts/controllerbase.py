#!/usr/bin/env python

#   This file is part of PARPG.

#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.
from fife import fife

from scripts.common.listeners.key_listener import KeyListener
from scripts.common.listeners.mouse_listener import MouseListener
from scripts.common.listeners.command_listener import CommandListener

class ControllerBase(KeyListener, MouseListener, CommandListener):
    """Base of Controllers"""
    def __init__(self, 
                 engine, 
                 view, 
                 model, 
                 application):
        '''
        Constructor
        @param engine: Instance of the active fife engine
        @type engine: fife.Engine
        @param view: Instance of a GameSceneView
        @param type: scripts.GameSceneView
        @param model: The model that has the current gamestate
        @type model: scripts.GameModel
        @param application: The application that created this controller
        @type application: scripts.PARPGApplication
        @param settings: The current settings of the application
        @type settings: fife.extensions.fife_settings.Setting
        '''
        KeyListener.__init__(self, application.event_listener)        
        MouseListener.__init__(self, application.event_listener)
        CommandListener.__init__(self, application.event_listener)
        self.engine = engine
        self.event_manager = engine.getEventManager()
        self.view = view
        self.model = model
        self.application = application
        
    def pause(self, paused):
        """Stops receiving events"""
        if paused:
            KeyListener.detach(self)
            MouseListener.detach(self)
        else:
            KeyListener.attach(self, self.application.event_listener)
            MouseListener.attach(self, self.application.event_listener)
    
    def setMouseCursor(self, image, dummy_image, mc_type="native"): 
        """Set the mouse cursor to an image.
           @type image: string
           @param image: The image you want to set the cursor to
           @type dummy_image: string
           @param dummy_image: ???
           @type type: string
           @param type: ???
           @return: None"""
        cursor = self.engine.getCursor()
        cursor_type = fife.CURSOR_IMAGE
        img_pool = self.engine.getImagePool()
        if(mc_type == "target"):
            target_cursor_id = img_pool.addResourceFromFile(image)  
            dummy_cursor_id = img_pool.addResourceFromFile(dummy_image)
            cursor.set(cursor_type, dummy_cursor_id)
            cursor.setDrag(cursor_type, target_cursor_id, -16, -16)
        else:
            cursor_type = fife.CURSOR_IMAGE
            zero_cursor_id = img_pool.addResourceFromFile(image)
            cursor.set(cursor_type, zero_cursor_id)
            cursor.setDrag(cursor_type, zero_cursor_id)

    def resetMouseCursor(self):
        """Reset cursor to default image.
           @return: None"""
        image = self.model.settings.get("PARPG", "CursorDefault")
        self.setMouseCursor(image, image)
        
    def onStop(self):
        """Called when the controller is removed from the list"""
        pass 
                
    def pump(self):
        """This method gets called every frame"""
        pass
    
