#!/usr/bin/env python

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from fife import fife
from fife.extensions import pychan

from scripts.gui import drag_drop_data as data_drag
from scripts.objects.action import ACTIONS
from copy import deepcopy

class ContainerGUIBase(object):
    """
    Base class for windows that show the content of a container
    """


    def __init__(self, controller, gui_file):
        self.controller = controller
        self.gui = pychan.loadXML(gui_file)

    def dragDrop(self, obj):
        """Decide whether to drag or drop the image.
           @type obj: string
           @param obj: The name of the object within 
                       the dictionary 'self.buttons'
           @return: None"""
        if(data_drag.dragging == True):
            self.dropObject(obj)
        elif(data_drag.dragging == False):
            self.dragObject(obj)
                
    def dragObject(self, obj):
        """Drag the selected object.
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons'
           @return: None"""           
        pass
       
    def dropObject(self, obj):
        """Drops the object being dropped
           @type obj: string
           @param obj: The name of the object within
                       the dictionary 'self.buttons' 
           @return: None"""
        pass    
    

    def createMenuItems(self, item, actions):
        """Creates context menu items for all classes based on ContainerGUI"""
        menu_actions = []
        for action_name in actions:
            display_name = action_name
            if action_name in ACTIONS:
                param_dict = {}
                param_dict["controller"] = self.controller
                param_dict["commands"] = {}
                if action_name == "Look":
                    param_dict["examine_name"] = item.name
                    param_dict["examine_desc"] = actions[action_name].\
                                                                pop("text")
                if action_name == "Read":
                    param_dict["text_name"] = item.name
                    param_dict["text"] = ""
                if action_name == "Use":
                    param_dict["item"] = item
                    display_name = actions[action_name].pop("text")
                if action_name == "Open":
                    param_dict["container"] = item
                if action_name == "BrewBeer":
                    param_dict["pot"] = item
                    display_name = "Brew beer"
                if actions[action_name]:
                    param_dict.update(actions[action_name])
                menu_actions.append([action_name, 
                                     display_name, 
                                     self.executeMenuItem, 
                                     ACTIONS[action_name]\
                                                (**param_dict)])        
        return menu_actions

    def showContextMenu(self, event, widget):
        """Decide whether to drag or drop the image.
           @type obj: string
           @param obj: The name of the object within 
                       the dictionary 'self.buttons'
           @return: None"""
        if event.getButton() == event.RIGHT:
            item = widget.item
            if item and item.trueAttr("usable"):
                actions = deepcopy(item.actions)
                if not actions:
                    return
                x_pos, y_pos = widget.getAbsolutePos()
                x_pos += event.getX()
                y_pos += event.getY()
                menu_actions = self.createMenuItems(item, actions)
                self.controller.view.hud.hideContextMenu()
                self.controller.view.hud.showContextMenu(menu_actions,
                                                 (x_pos, 
                                                  y_pos)
                                                  )

    def executeMenuItem(self, action):
        """Executes the items action
        @param action: The action to run
        @type action: Class derived from scripts.objects.action.Action
        """
        action.execute()
    
    def updateImages(self):
        pass
