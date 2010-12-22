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
"""This file contains the GameSceneController that handles 
input when the game is exploring a scene"""


from datetime import datetime
import random
import glob
import os

from fife import fife
from fife import extensions

from controllerbase import ControllerBase
from scripts.gui.hud import Hud
from scripts.gui import drag_drop_data as data_drag
from objects.action import ChangeMapAction, ExamineAction, OpenBoxAction, \
                           UnlockBoxAction, LockBoxAction, TalkAction, \
                           PickUpAction, DropItemAction

#For debugging/code analysis
if False:
    from gamesceneview import GameSceneView
    from gamemodel import GameModel
    from parpg import PARPGApplication

class GameSceneController(ControllerBase):
    '''
    This controller handles inputs when the game is in "scene" state.
    "Scene" state is when the player can move around and interact
    with objects. Like, talking to a npc or examining the contents of a box. 
    '''


    def __init__(self, engine, view, model, application):
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
        ControllerBase.__init__(self,
                                engine,
                                view,
                                model,
                                application)
        #this can be helpful for IDEs code analysis
        if False:
            assert(isinstance(self.engine, fife.Engine))
            assert(isinstance(self.view, GameSceneView))
            assert(isinstance(self.view, GameModel))
            assert(isinstance(self.application, PARPGApplication))
            assert(isinstance(self.event_manager, fife.EventManager))
        
        # Last saved mouse coords        
        self.action_number = 1

        self.has_mouse_focus = True
        self.last_mousecoords = None
        self.mouse_callback = None
        self.original_cursor_id = self.engine.getCursor().getId()        
        self.scroll_direction = [0, 0]
        self.scroll_timer = extensions.fife_timer.Timer(100,
                                          lambda: self.view.moveCamera \
                                                   (self.scroll_direction))    
        
        #this is temporary until we can set the native cursor
        self.resetMouseCursor()
        self.paused = False

        if model.settings.get("FIFE",  "PlaySounds"):
            if not self.view.sounds.music_init:
                music_file = random.choice(glob.glob(os.path.join(
                                                                  "music", 
                                                                  "*.ogg")))
                self.view.sounds.playMusic(music_file) 
        self.initHud()
                

    def initHud(self):
        """Initialize the hud member
        @return: None"""
        hud_callbacks = {
            'saveGame': self.saveGame,
            'loadGame': self.loadGame,
            'quitGame': self.quitGame,
        }
        self.view.hud = Hud(self, 
                            self.model.settings, 
                            hud_callbacks)

    def keyPressed(self, evt):
        """Whenever a key is pressed, fife calls this routine.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        key = evt.getKey()
        key_val = key.getValue()

        if(key_val == key.Q):
            # we need to quit the game
            self.view.hud.quitGame()
        if(key_val == key.T):
            self.model.active_map.toggleRenderer('GridRenderer')
        if(key_val == key.F1):
            # display the help screen and pause the game
            self.view.hud.displayHelp()
        if(key_val == key.F5):
            self.model.active_map.toggleRenderer('CoordinateRenderer')
        if(key_val == key.F7):
            # F7 saves a screenshot to fife/clients/parpg/screenshots
            
            screenshot_file = "screenshots/screen-%s.png" % \
                    (datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            print "PARPG: Saved:", screenshot_file
            self.engine.getRenderBackend().captureScreen(screenshot_file)
        if(key_val == key.F10):
            # F10 shows/hides the console
            self.engine.getGuiManager().getConsole().toggleShowHide()
        if(key_val == key.I):
            # I opens and closes the inventory
            self.view.hud.toggleInventory()
        if(key_val == key.A):
            # A adds a test action to the action box
            # The test actions will follow this format: Action 1,
            # Action 2, etc.
            self.view.hud.addAction("Action " + str(self.action_number))
            self.action_number += 1
        if(key_val == key.ESCAPE):
            # Escape brings up the main menu
            self.view.hud.displayMenu()
            # Hide the quit menu
            self.view.hud.quit_window.hide()
        if(key_val == key.M):
            self.view.sounds.toggleMusic()
        if(key_val == key.PAUSE):
            # Pause pause/unpause the game 
            self.model.togglePause()
            self.pause(False)
        if(key_val == key.SPACE):
            self.model.active_map.centerCameraOnPlayer() 
    
    def mouseReleased(self, evt):
        """If a mouse button is released, fife calls this routine.
           We want to wait until the button is released, because otherwise
           pychan captures the release if a menu is opened.
           @type evt: fife.event
           @param evt: The event that fife caught
           @return: None"""
        self.view.hud.hideContextMenu()
        scr_point = fife.ScreenPoint(evt.getX(), evt.getY())
        if(evt.getButton() == fife.MouseEvent.LEFT):
            if(data_drag.dragging):
                coord = self.model.getCoords(scr_point)\
                                    .getExactLayerCoordinates()
                commands = ({"Command": "ResetMouseCursor"}, 
                            {"Command": "StopDragging"})
                self.model.game_state.player_character.approach([coord.x, 
                                                                 coord.y],
                                    DropItemAction(self, 
                                                   data_drag.dragged_item, 
                                                   commands))
            else:
                self.model.movePlayer(self.model.getCoords(scr_point))
        elif(evt.getButton() == fife.MouseEvent.RIGHT):
            # is there an object here?
            tmp_active_map = self.model.active_map
            instances = tmp_active_map.cameras[tmp_active_map.my_cam_id].\
                            getMatchingInstances(scr_point,
                                                 tmp_active_map.agent_layer)
            info = None
            for inst in instances:
                # check to see if this is an active item
                if(self.model.objectActive(inst.getId())):
                    # yes, get the model
                    info = self.getItemActions(inst.getId())
                    break

            # take the menu items returned by the engine or show a
            # default menu if no items
            data = info or \
                [["Walk", "Walk here", self.view.onWalk, 
                  self.model.getCoords(scr_point)]]
            # show the menu
            self.view.hud.showContextMenu(data, (scr_point.x, scr_point.y))
    
        
    def updateMouse(self):
        """Updates the mouse values"""
        if self.paused:
            return
        cursor = self.engine.getCursor()
        #this can be helpful for IDEs code analysis
        if False:
            assert(isinstance(cursor, fife.Cursor))
        self.last_mousecoords = fife.ScreenPoint(cursor.getX(), 
                                                 cursor.getY())        
        self.view.highlightFrontObject(self.last_mousecoords)       
        
        #set the trigger area in pixles
        pixle_edge = 20
        
        mouse_x = self.last_mousecoords.x
        screen_width = self.model.engine.getSettings().getScreenWidth()
        mouse_y = self.last_mousecoords.y
        screen_height = self.model.engine.getSettings().getScreenHeight()
        
        image = None
        settings = self.model.settings
        
        
        #edge logic
        self.scroll_direction = [0, 0]
        if self.has_mouse_focus:
            direction = self.scroll_direction
            #up
            if mouse_y <= pixle_edge: 
                direction[0] += 1
                direction[1] -= 1
                image = settings.get("PARPG", "CursorUp")
                
            #right
            if mouse_x >= screen_width - pixle_edge:
                direction[0] += 1
                direction[1] += 1
                image = settings.get("PARPG", "CursorRight")
                
            #down
            if mouse_y >= screen_height - pixle_edge:
                direction[0] -= 1
                direction[1] += 1
                image = settings.get("PARPG", "CursorDown")
                
            #left
            if mouse_x <= pixle_edge:
                direction[0] -= 1
                direction[1] -= 1
                image = settings.get("PARPG", "CursorLeft")
            
            if image != None and not data_drag.dragging:
                self.setMouseCursor(image, image)
       

    def handleCommands(self):
        """Check if a command is to be executed
        """
        if self.model.map_change:
            self.pause(True)
            if self.model.active_map:
                player_char = self.model.game_state.player_character
                self.model.game_state.player_character = None
                pc_agent = self.model.agents[self.model.ALL_AGENTS_KEY]\
                                                ["PlayerCharacter"]
                pc_agent.update(player_char.getStateForSaving())
                pc_agent["Map"] = self.model.target_map_name 
                pc_agent["Position"] = self.model.target_position
                pc_agent["Inventory"] = \
                        player_char.inventory.serializeInventory()
                player_agent = self.model.active_map.\
                                    agent_layer.getInstance("PlayerCharacter")
                self.model.active_map.agent_layer.deleteInstance(player_agent)
            self.model.loadMap(self.model.target_map_name)
            self.model.setActiveMap(self.model.target_map_name)          
            self.model.readAgentsOfMap(self.model.target_map_name)
            self.model.placeAgents()
            self.model.placePC()
            self.model.map_change = False
            # The PlayerCharacter has an inventory, and also some 
            # filling of the ready slots in the HUD. 
            # At this point we sync the contents of the ready slots 
            # with the contents of the inventory.
            self.view.hud.inventory = None
            self.view.hud.initializeInventory()         
            self.pause(False)

    def nullFunc(self, userdata):
        """Sample callback for the context menus."""
        print userdata    

    def initTalk(self, npc_info):
        """ Starts the PlayerCharacter talking to an NPC. """
        # TODO: work more on this when we get NPCData and HeroData straightened
        # out
        npc = self.model.game_state.getObjectById(npc_info.ID,
                                            self.model.game_state.\
                                                current_map_name)
        self.model.game_state.player_character.approach([npc.getLocation().\
                                     getLayerCoordinates().x,
                                     npc.getLocation().\
                                     getLayerCoordinates().y],
                                    TalkAction(self, npc))

    def getItemActions(self, obj_id):
        """Given the objects ID, return the text strings and callbacks.
           @type obj_id: string
           @param obj_id: ID of object
           @rtype: list
           @return: List of text and callbacks"""
        actions = []
        # note: ALWAYS check NPC's first!
        obj = self.model.game_state.\
                        getObjectById(obj_id,
                                      self.model.game_state.current_map_name)
        
        if obj is not None:
            if obj.trueAttr("NPC"):
                # keep it simple for now, None to be replaced by callbacks
                actions.append(["Talk", "Talk", self.initTalk, obj])
                actions.append(["Attack", "Attack", self.nullFunc, obj])
            else:
                actions.append(["Examine", "Examine",
                                self.model.game_state.\
                                player_character.approach, 
                                [obj.X, obj.Y],
                                ExamineAction(self, 
                                              obj_id, obj.name, 
                                              obj.text)])
                # is it a Door?
                if obj.trueAttr("door"):
                    actions.append(["Change Map", "Change Map",
                       self.model.game_state.player_character.approach, 
                       [obj.X, obj.Y],
                       ChangeMapAction(self, obj.target_map_name,
                                       obj.target_pos)])
                # is it a container?
                if obj.trueAttr("container"):
                    actions.append(["Open", "Open", 
                                    self.model.game_state.\
                                        player_character.approach,
                                    [obj.X, obj.Y],
                                    OpenBoxAction(self, obj)])
                    actions.append(["Unlock", "Unlock", 
                                    self.model.game_state.\
                                        player_character.approach,
                                    [obj.X, obj.Y],
                                    UnlockBoxAction(self, obj)])
                    actions.append(["Lock", "Lock", 
                                    self.model.game_state.\
                                        player_character.approach,
                                    [obj.X, obj.Y],
                                    LockBoxAction(self, obj)])
                # can you pick it up?
                if obj.trueAttr("carryable"):
                    actions.append(["Pick Up", "Pick Up", 
                                    self.model.game_state.\
                                        player_character.approach,
                                    [obj.X, obj.Y],
                                    PickUpAction(self, obj)])

        return actions
    
    def saveGame(self, *args, **kwargs):
        """Saves the game state, delegates call to engine.Engine
           @return: None"""
        self.model.pause(False)
        self.pause(False)
        self.view.hud.enabled = True
        self.model.save(*args, **kwargs)

    def loadGame(self, *args, **kwargs):
        """Loads the game state, delegates call to engine.Engine
           @return: None"""
        # Remove all currently loaded maps so we can start fresh
        self.model.pause(False)
        self.pause(False)
        self.view.hud.enabled = True
        self.model.deleteMaps()
        self.view.hud.inventory = None

        self.model.load(*args, **kwargs)
        self.view.hud.initializeInventory()          

    def quitGame(self):
        """Quits the game
           @return: None"""
        self.application.listener.quitGame()
    
    def pause(self, paused):
        """Pauses the controller"""
        super(GameSceneController, self).pause(paused)
        self.paused = paused
        if paused:
            self.scroll_timer.stop()
            self.resetMouseCursor()
    
    def onCommand(self, command):
        if(command.getCommandType() == fife.CMD_MOUSE_FOCUS_GAINED):
            self.has_mouse_focus = True
        elif(command.getCommandType() == fife.CMD_MOUSE_FOCUS_LOST):
            self.has_mouse_focus = False
      
    def pump(self):
        """Routine called during each frame. Our main loop is in ./run.py"""
        # uncomment to instrument
        # t0 = time.time()
        if self.paused: 
            return
        self.updateMouse()
        if self.model.active_map:
            self.view.highlightFrontObject(self.last_mousecoords)
            self.view.refreshTopLayerTransparencies()
            if self.scroll_direction != [0, 0]:
                self.scroll_timer.start()
            else: 
                self.scroll_timer.stop()
                if not data_drag.dragging:
                    self.resetMouseCursor()
                
        self.handleCommands()
        # print "%05f" % (time.time()-t0,)
