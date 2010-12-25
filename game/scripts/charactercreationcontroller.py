#   This file is part of PARPG.
#
#   PARPG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   PARPG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with PARPG.  If not, see <http://www.gnu.org/licenses/>.
"""Provides the controller that defines the behavior of the character creation
   screen."""
from controllerbase import ControllerBase
from gamescenecontroller import GameSceneController
from gamesceneview import GameSceneView

class CharacterCreationController(ControllerBase):
    """Controller defining the behavior of the character creation screen."""
    def __init__(self, engine, view, model, application):
        """Construct a new L{CharacterCreationController} instance.
           @param engine: Rendering engine used to display the associated view.
           @type engine: L{fife.Engine}
           @param view: View used to display the character creation screen.
           @type view: L{ViewBase}
           @param model: Model of the game state.
           @type model: L{GameModel}
           @param application: Application used to glue the various MVC
               components together.
           @type application: 
               L{fife.extensions.basicapplication.ApplicationBase}"""
        ControllerBase.__init__(self, engine, view, model, application)
        self.view.start_new_game_callback = self.startNewGame
        self.view.cancel_new_game_callback = self.cancelNewGame
        self.view.show()
    
    def startNewGame(self):
        """Create the new character and start a new game.
           @return: None"""
        view = GameSceneView(self.engine, self.model)
        controller = GameSceneController(self.engine, view, self.model,
                                         self.application)
        self.application.view = view
        self.application.switchController(controller)
        start_map = self.model.settings.get("PARPG", "Map")
        self.model.changeMap(start_map)
    
    def cancelNewGame(self):
        """Exit the character creation view and return the to main menu.
           @return: None"""
        # KLUDGE Technomage 2010-12-24: This is to prevent a circular import
        #     but a better fix needs to be thought up.
        from mainmenucontroller import MainMenuController
        from mainmenuview import MainMenuView
        view = MainMenuView(self.engine, self.model)
        controller = MainMenuController(self.engine, view, self.model,
                                        self.application)
        self.application.view = view
        self.application.switchController(controller)
    
    def onStop(self):
        """Called when the controller is removed from the list.
           @return: None"""
        self.view.hide()
