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
"""This module contains the main Application class 
and the basic Listener for PARPG """


from fife import fife
from fife.extensions import pychan
from fife.extensions.basicapplication import ApplicationBase

from scripts.gamemodel import GameModel
from scripts.mainmenuview import MainMenuView
from scripts import console
from scripts.mainmenucontroller import MainMenuController
from scripts.common.listeners.event_listener import EventListener
from scripts.common.listeners.key_listener import KeyListener
from scripts.common.listeners.mouse_listener import MouseListener
from scripts.common.listeners.command_listener import CommandListener
from scripts.common.listeners.console_executor import ConsoleExecuter
from scripts.common.listeners.widget_listener import WidgetListener

class KeyFilter(fife.IKeyFilter):
    """
    This is the implementation of the fife.IKeyFilter class.
    
    Prevents any filtered keys from being consumed by guichan.
    """
    def __init__(self, keys):
        fife.IKeyFilter.__init__(self)
        self._keys = keys

    def isFiltered(self, event):
        """Checks if an key is filtered"""
        return event.getKey().getValue() in self._keys

class ApplicationListener(KeyListener,
                        MouseListener,
                        ConsoleExecuter,
                        CommandListener,
                        WidgetListener):    
    """Basic listener for PARPG"""
        
    def __init__(self, event_listener, engine, view, model):
        """Initialize the instance.
           @type engine: fife.engine
           @param engine: ???
           @type view: viewbase.ViewBase
           @param view: View that draws the current state
           @type model: GameModel
           @param model: The game model"""
        KeyListener.__init__(self, event_listener)
        MouseListener.__init__(self, event_listener)
        ConsoleExecuter.__init__(self, event_listener)
        CommandListener.__init__(self, event_listener)
        WidgetListener.__init__(self, event_listener)        
        self.engine = engine
        self.view = view
        self.model = model
        keyfilter = KeyFilter([fife.Key.ESCAPE])
        keyfilter.__disown__()        
        
        engine.getEventManager().setKeyFilter(keyfilter)
        self.quit = False
        self.about_window = None
        self.console = console.Console(self)

    def quitGame(self):
        """Forces a quit game on next cycle.
           @return: None"""
        self.quit = True

    def onConsoleCommand(self, command):
        """
        Called on every console comand, delegates calls  to the a console
        object, implementing the callbacks
        @type command: string
        @param command: the command to run
        @return: result
        """
        return self.console.handleConsoleCommand(command)

    def onCommand(self, command):
        """Enables the game to be closed via the 'X' button on the window frame
           @type command: fife.Command
           @param command: The command to read.
           @return: None"""
        if(command.getCommandType() == fife.CMD_QUIT_GAME):
            self.quit = True
            command.consume()

class PARPGApplication(ApplicationBase):
    """Main Application class
       We use an MVC model model
       self.gamesceneview is our view,self.model is our model
       self.controller is the controller"""
       
    def __init__(self, setting):
        """Initialise the instance.
           @return: None"""
        super(PARPGApplication, self).__init__(setting)
        pychan.init(self.engine, debug = True)
        #self.engine.getModel(self)
        self.model = GameModel(self.engine, setting)
        self.model.maps_file = self._setting.get("PARPG", "MapsFile")
        self.model.readMapFiles()
        self.model.object_db_file = self._setting.get("PARPG", 
                                                      "ObjectDatabaseFile") 
        self.model.readObjectDB()
        self.model.agents_directory = self._setting.get("PARPG",
                                                        "AgentsDirectory") 
        self.model.getAgentImportFiles()
        self.model.all_agents_file = self._setting.get("PARPG", "AllAgentsFile")
        self.model.readAllAgents()
        self.model.dialogues_directory = self._setting.get("PARPG", 
                                                           "DialoguesDirectory")
        self.model.getDialogues()
        self.view = MainMenuView(self.engine, self.model)
        self.event_listener = EventListener(self.engine)
        self.controllers = []
        controller = MainMenuController(self.engine, 
                                                        self.view, 
                                                        self.model,
                                                        self)
        #controller.initHud()
        self.controllers.append(controller)
        self.listener = ApplicationListener(self.event_listener,
                                            self.engine, 
                                            self.view, 
                                            self.model)
        #start_map = self._setting.get("PARPG", "Map")
        #self.model.changeMap(start_map)

    def createListener(self):
        """@return: None"""
        # already created in constructor
        # but if we don't put one here, Fife gets all fussy :-)
        pass
    
    def pushController(self, controller):
        """Adds a controller to the list to be the current active one."""
        self.controllers[-1].pause(True)
        self.controllers.append(controller)
    
    def popController(self):
        """Removes and returns the current active controller, unless its the last one"""
        ret_controller = None
        if self.controllers.count > 1:
            ret_controller = self.controllers.pop()
            self.controllers[-1].pause(False)
        ret_controller.onStop()
        return ret_controller
    
    def switchController(self, controller):
        """Clears the controller list and adds a controller to be the current active one"""
        for old_controller in self.controllers:
            old_controller.onStop()
        self.controllers = []
        self.controllers.append(controller)
    
    def _pump(self):
        """Main game loop.
           There are in fact 2 main loops, this one and the one in GameSceneView.
           @return: None"""
        if self.listener.quit:
            self.breakRequested = True #pylint: disable-msg=C0103
        else:
            for controller in self.controllers:
                controller.pump()