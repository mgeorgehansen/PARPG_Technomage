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

import PyCEGUI as pycegui
from PyCEGUI import UVector2, UDim
from PyCEGUIOpenGLRenderer import OpenGLRenderer as CeguiOpenGlRenderer

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

class ApplicationListener(KeyListener, MouseListener, ConsoleExecuter,
                          CommandListener, WidgetListener):
    """Basic listener for PARPG"""
        
    def __init__(self, application):
        """Initialize the instance.
           @type engine: fife.engine
           @param engine: ???
           @type view: viewbase.ViewBase
           @param view: View that draws the current state
           @type model: GameModel
           @param model: The game model"""
        event_listener = application.event_listener
        KeyListener.__init__(self, event_listener)
        MouseListener.__init__(self, event_listener)
        ConsoleExecuter.__init__(self, event_listener)
        CommandListener.__init__(self, event_listener)
        WidgetListener.__init__(self, event_listener)
        self.application = application
        self.view = application.view
        self.model = application.model
        self.engine = application.engine
        keyfilter = KeyFilter([fife.Key.ESCAPE])
        keyfilter.__disown__()
        
        event_manager = self.engine.getEventManager()
        event_manager.setKeyFilter(keyfilter)
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


class CeguiListener(KeyListener, MouseListener):
    mouse_button_map = {
        fife.MouseEvent.LEFT: pycegui.MouseButton.LeftButton,
        fife.MouseEvent.MIDDLE: pycegui.MouseButton.MiddleButton,
        fife.MouseEvent.RIGHT: pycegui.MouseButton.RightButton,
        fife.MouseEvent.EMPTY: pycegui.MouseButton.NoButton,
        fife.MouseEvent.UNKNOWN_BUTTON: pycegui.MouseButton.NoButton,
    }
    key_code_map = {
        fife.Key.BACKSPACE:     pycegui.Key.Backspace,
        fife.Key.TAB:           pycegui.Key.Tab,
#        fife.Key.CLEAR:         pycegui.Key.Clear,
        fife.Key.ENTER:         pycegui.Key.Return,
        fife.Key.PAUSE:         pycegui.Key.Pause,
        fife.Key.ESCAPE:        pycegui.Key.Escape,
        fife.Key.SPACE:         pycegui.Key.Space,
#        fife.Key.EXCLAIM:       pycegui.Key.Exclaim,
#        fife.Key.QUOTEDBL:      pycegui.Key.QuoteDbl,
#        fife.Key.HASH:          pycegui.Key.Hash,
#        fife.Key.DOLLAR:        pycegui.Key.Dollar,
#        fife.Key.AMPERSAND:     pycegui.Key.Ampersand,
#        fife.Key.QUOTE:         pycegui.Key.Quote,
#        fife.Key.LEFTPAREN:     pycegui.Key.LeftParen,
#        fife.Key.RIGHTPAREN:    pycegui.Key.RrightParen,
#        fife.Key.ASTERISK:      pycegui.Key.ASTERISK,
#        fife.Key.PLUS:          pycegui.Key.PLUS,
        fife.Key.COMMA:         pycegui.Key.Comma,
        fife.Key.MINUS:         pycegui.Key.Minus,
        fife.Key.PERIOD:        pycegui.Key.Period,
        fife.Key.SLASH:         pycegui.Key.Slash,
        fife.Key.NUM_0:         pycegui.Key.Zero,
        fife.Key.NUM_1:         pycegui.Key.One,
        fife.Key.NUM_2:         pycegui.Key.Two,
        fife.Key.NUM_3:         pycegui.Key.Three,
        fife.Key.NUM_4:         pycegui.Key.Four,
        fife.Key.NUM_5:         pycegui.Key.Five,
        fife.Key.NUM_6:         pycegui.Key.Six,
        fife.Key.NUM_7:         pycegui.Key.Seven,
        fife.Key.NUM_8:         pycegui.Key.Eight,
        fife.Key.NUM_9:         pycegui.Key.Nine,
        fife.Key.COLON:         pycegui.Key.Colon,
        fife.Key.SEMICOLON:     pycegui.Key.Semicolon,
#        fife.Key.LESS:          pycegui.Key.LESS,
        fife.Key.EQUALS:        pycegui.Key.Equals,
#        fife.Key.GREATER:       pycegui.Key.GREATER,
#        fife.Key.QUESTION:      pycegui.Key.QUESTION,
#        fife.Key.AT:            pycegui.Key.AT,
        fife.Key.LEFTBRACKET:   pycegui.Key.LeftBracket,
        fife.Key.BACKSLASH:     pycegui.Key.Backslash,
        fife.Key.RIGHTBRACKET:  pycegui.Key.RightBracket,
#        fife.Key.CARET:         pycegui.Key.CARET,
#        fife.Key.UNDERSCORE:    pycegui.Key.UNDERSCORE,
#        fife.Key.BACKQUOTE:     pycegui.Key.BACKQUOTE,
        fife.Key.A:             pycegui.Key.A,
        fife.Key.B:             pycegui.Key.B,
        fife.Key.C:             pycegui.Key.C,
        fife.Key.D:             pycegui.Key.D,
        fife.Key.E:             pycegui.Key.E,
        fife.Key.F:             pycegui.Key.F,
        fife.Key.G:             pycegui.Key.G,
        fife.Key.H:             pycegui.Key.H,
        fife.Key.I:             pycegui.Key.I,
        fife.Key.J:             pycegui.Key.J,
        fife.Key.K:             pycegui.Key.K,
        fife.Key.L:             pycegui.Key.L,
        fife.Key.M:             pycegui.Key.M,
        fife.Key.N:             pycegui.Key.N,
        fife.Key.O:             pycegui.Key.O,
        fife.Key.P:             pycegui.Key.P,
        fife.Key.Q:             pycegui.Key.Q,
        fife.Key.R:             pycegui.Key.R,
        fife.Key.S:             pycegui.Key.S,
        fife.Key.T:             pycegui.Key.T,
        fife.Key.U:             pycegui.Key.U,
        fife.Key.V:             pycegui.Key.V,
        fife.Key.W:             pycegui.Key.W,
        fife.Key.X:             pycegui.Key.X,
        fife.Key.Y:             pycegui.Key.Y,
        fife.Key.Z:             pycegui.Key.Z,
        fife.Key.DELETE:        pycegui.Key.Delete,
#        fife.Key.WORLD_0:       pycegui.Key.WORLD_0,
#        fife.Key.WORLD_1:       pycegui.Key.WORLD_1,
#        fife.Key.WORLD_2:       pycegui.Key.WORLD_2,
#        fife.Key.WORLD_3:       pycegui.Key.WORLD_3,
#        fife.Key.WORLD_4:       pycegui.Key.WORLD_4,
#        fife.Key.WORLD_5:       pycegui.Key.WORLD_5,
#        fife.Key.WORLD_6:       pycegui.Key.WORLD_6,
#        fife.Key.WORLD_7:       pycegui.Key.WORLD_7,
#        fife.Key.WORLD_8:       pycegui.Key.WORLD_8,
#        fife.Key.WORLD_9:       pycegui.Key.WORLD_9,
#        fife.Key.WORLD_10:      pycegui.Key.WORLD_10,
#        fife.Key.WORLD_11:      pycegui.Key.WORLD_11,
#        fife.Key.WORLD_12:      pycegui.Key.WORLD_12,
#        fife.Key.WORLD_13:      pycegui.Key.WORLD_13,
#        fife.Key.WORLD_14:      pycegui.Key.WORLD_14,
#        fife.Key.WORLD_15:      pycegui.Key.WORLD_15,
#        fife.Key.WORLD_16:      pycegui.Key.WORLD_16,
#        fife.Key.WORLD_17:      pycegui.Key.WORLD_17,
#        fife.Key.WORLD_18:      pycegui.Key.WORLD_18,
#        fife.Key.WORLD_19:      pycegui.Key.WORLD_19,
#        fife.Key.WORLD_20:      pycegui.Key.WORLD_20,
#        fife.Key.WORLD_21:      pycegui.Key.WORLD_21,
#        fife.Key.WORLD_22:      pycegui.Key.WORLD_22,
#        fife.Key.WORLD_23:      pycegui.Key.WORLD_23,
#        fife.Key.WORLD_24:      pycegui.Key.WORLD_24,
#        fife.Key.WORLD_25:      pycegui.Key.WORLD_25,
#        fife.Key.WORLD_26:      pycegui.Key.WORLD_26,
#        fife.Key.WORLD_27:      pycegui.Key.WORLD_27,
#        fife.Key.WORLD_28:      pycegui.Key.WORLD_28,
#        fife.Key.WORLD_29:      pycegui.Key.WORLD_29,
#        fife.Key.WORLD_30:      pycegui.Key.WORLD_30,
#        fife.Key.WORLD_31:      pycegui.Key.WORLD_31,
#        fife.Key.WORLD_32:      pycegui.Key.WORLD_32,
#        fife.Key.WORLD_33:      pycegui.Key.WORLD_33,
#        fife.Key.WORLD_34:      pycegui.Key.WORLD_34,
#        fife.Key.WORLD_35:      pycegui.Key.WORLD_35,
#        fife.Key.WORLD_36:      pycegui.Key.WORLD_36,
#        fife.Key.WORLD_37:      pycegui.Key.WORLD_37,
#        fife.Key.WORLD_38:      pycegui.Key.WORLD_38,
#        fife.Key.WORLD_39:      pycegui.Key.WORLD_39,
#        fife.Key.WORLD_40:      pycegui.Key.WORLD_40,
#        fife.Key.WORLD_41:      pycegui.Key.WORLD_41,
#        fife.Key.WORLD_42:      pycegui.Key.WORLD_42,
#        fife.Key.WORLD_43:      pycegui.Key.WORLD_43,
#        fife.Key.WORLD_44:      pycegui.Key.WORLD_44,
#        fife.Key.WORLD_45:      pycegui.Key.WORLD_45,
#        fife.Key.WORLD_46:      pycegui.Key.WORLD_46,
#        fife.Key.WORLD_47:      pycegui.Key.WORLD_47,
#        fife.Key.WORLD_48:      pycegui.Key.WORLD_48,
#        fife.Key.WORLD_49:      pycegui.Key.WORLD_49,
#        fife.Key.WORLD_50:      pycegui.Key.WORLD_50,
#        fife.Key.WORLD_51:      pycegui.Key.WORLD_51,
#        fife.Key.WORLD_52:      pycegui.Key.WORLD_52,
#        fife.Key.WORLD_53:      pycegui.Key.WORLD_53,
#        fife.Key.WORLD_54:      pycegui.Key.WORLD_54,
#        fife.Key.WORLD_55:      pycegui.Key.WORLD_55,
#        fife.Key.WORLD_56:      pycegui.Key.WORLD_56,
#        fife.Key.WORLD_57:      pycegui.Key.WORLD_57,
#        fife.Key.WORLD_58:      pycegui.Key.WORLD_58,
#        fife.Key.WORLD_59:      pycegui.Key.WORLD_59,
#        fife.Key.WORLD_60:      pycegui.Key.WORLD_60,
#        fife.Key.WORLD_61:      pycegui.Key.WORLD_61,
#        fife.Key.WORLD_62:      pycegui.Key.WORLD_62,
#        fife.Key.WORLD_63:      pycegui.Key.WORLD_63,
#        fife.Key.WORLD_64:      pycegui.Key.WORLD_64,
#        fife.Key.WORLD_65:      pycegui.Key.WORLD_65,
#        fife.Key.WORLD_66:      pycegui.Key.WORLD_66,
#        fife.Key.WORLD_67:      pycegui.Key.WORLD_67,
#        fife.Key.WORLD_68:      pycegui.Key.WORLD_68,
#        fife.Key.WORLD_69:      pycegui.Key.WORLD_69,
#        fife.Key.WORLD_70:      pycegui.Key.WORLD_70,
#        fife.Key.WORLD_71:      pycegui.Key.WORLD_71,
#        fife.Key.WORLD_72:      pycegui.Key.WORLD_72,
#        fife.Key.WORLD_73:      pycegui.Key.WORLD_73,
#        fife.Key.WORLD_74:      pycegui.Key.WORLD_74,
#        fife.Key.WORLD_75:      pycegui.Key.WORLD_75,
#        fife.Key.WORLD_76:      pycegui.Key.WORLD_76,
#        fife.Key.WORLD_77:      pycegui.Key.WORLD_77,
#        fife.Key.WORLD_78:      pycegui.Key.WORLD_78,
#        fife.Key.WORLD_79:      pycegui.Key.WORLD_79,
#        fife.Key.WORLD_80:      pycegui.Key.WORLD_80,
#        fife.Key.WORLD_81:      pycegui.Key.WORLD_81,
#        fife.Key.WORLD_82:      pycegui.Key.WORLD_82,
#        fife.Key.WORLD_83:      pycegui.Key.WORLD_83,
#        fife.Key.WORLD_84:      pycegui.Key.WORLD_84,
#        fife.Key.WORLD_85:      pycegui.Key.WORLD_85,
#        fife.Key.WORLD_86:      pycegui.Key.WORLD_86,
#        fife.Key.WORLD_87:      pycegui.Key.WORLD_87,
#        fife.Key.WORLD_88:      pycegui.Key.WORLD_88,
#        fife.Key.WORLD_89:      pycegui.Key.WORLD_89,
#        fife.Key.WORLD_90:      pycegui.Key.WORLD_90,
#        fife.Key.WORLD_91:      pycegui.Key.WORLD_91,
#        fife.Key.WORLD_92:      pycegui.Key.WORLD_92,
#        fife.Key.WORLD_93:      pycegui.Key.WORLD_93,
#        fife.Key.WORLD_94:      pycegui.Key.WORLD_94,
#        fife.Key.WORLD_95:      pycegui.Key.WORLD_95,
        fife.Key.KP0:           pycegui.Key.Numpad0,
        fife.Key.KP1:           pycegui.Key.Numpad1,
        fife.Key.KP2:           pycegui.Key.Numpad2,
        fife.Key.KP3:           pycegui.Key.Numpad3,
        fife.Key.KP4:           pycegui.Key.Numpad4,
        fife.Key.KP5:           pycegui.Key.Numpad5,
        fife.Key.KP6:           pycegui.Key.Numpad6,
        fife.Key.KP7:           pycegui.Key.Numpad7,
        fife.Key.KP8:           pycegui.Key.Numpad8,
        fife.Key.KP9:           pycegui.Key.Numpad9,
        fife.Key.KP_PERIOD:     pycegui.Key.Decimal,
        fife.Key.KP_DIVIDE:     pycegui.Key.Divide,
        fife.Key.KP_MULTIPLY:   pycegui.Key.Multiply,
        fife.Key.KP_MINUS:      pycegui.Key.Subtract,
        fife.Key.KP_PLUS:       pycegui.Key.Add,
        fife.Key.KP_ENTER:      pycegui.Key.NumpadEnter,
        fife.Key.KP_EQUALS:     pycegui.Key.NumpadEquals,
        fife.Key.UP:            pycegui.Key.ArrowUp,
        fife.Key.DOWN:          pycegui.Key.ArrowDown,
        fife.Key.RIGHT:         pycegui.Key.ArrowRight,
        fife.Key.LEFT:          pycegui.Key.ArrowLeft,
        fife.Key.INSERT:        pycegui.Key.Insert,
        fife.Key.HOME:          pycegui.Key.Home,
        fife.Key.END:           pycegui.Key.End,
        fife.Key.PAGE_UP:       pycegui.Key.PageUp,
        fife.Key.PAGE_DOWN:     pycegui.Key.PageDown,
        fife.Key.F1:            pycegui.Key.F1,
        fife.Key.F2:            pycegui.Key.F2,
        fife.Key.F3:            pycegui.Key.F3,
        fife.Key.F4:            pycegui.Key.F4,
        fife.Key.F5:            pycegui.Key.F5,
        fife.Key.F6:            pycegui.Key.F6,
        fife.Key.F7:            pycegui.Key.F7,
        fife.Key.F8:            pycegui.Key.F8,
        fife.Key.F9:            pycegui.Key.F9,
        fife.Key.F10:           pycegui.Key.F10,
        fife.Key.F11:           pycegui.Key.F11,
        fife.Key.F12:           pycegui.Key.F12,
        fife.Key.F13:           pycegui.Key.F13,
        fife.Key.F14:           pycegui.Key.F14,
        fife.Key.F15:           pycegui.Key.F15,
        fife.Key.NUM_LOCK:      pycegui.Key.NumLock,
        fife.Key.CAPS_LOCK:     pycegui.Key.Capital,
        fife.Key.SCROLL_LOCK:   pycegui.Key.ScrollLock,
        fife.Key.RIGHT_SHIFT:   pycegui.Key.RightShift,
        fife.Key.LEFT_SHIFT:    pycegui.Key.LeftShift,
        fife.Key.RIGHT_CONTROL: pycegui.Key.RightControl,
        fife.Key.LEFT_CONTROL:  pycegui.Key.LeftControl,
        fife.Key.RIGHT_ALT:     pycegui.Key.RightAlt,
        fife.Key.LEFT_ALT:      pycegui.Key.LeftAlt,
#        fife.Key.RIGHT_META:    pycegui.Key.RMETA,
#        fife.Key.LEFT_META:     pycegui.Key.LMETA,
        fife.Key.RIGHT_SUPER:   pycegui.Key.RightWindows,
        fife.Key.LEFT_SUPER:    pycegui.Key.LeftWindows,
#        fife.Key.ALT_GR:        pycegui.Key.MODE,
#        fife.Key.COMPOSE:       pycegui.Key.COMPOSE,
#        fife.Key.HELP:          pycegui.Key.HELP,
#        fife.Key.PRINT_SCREEN:  pycegui.Key.PRINT,
#        fife.Key.SYSREQ:        pycegui.Key.SYSREQ,
#        fife.Key.BREAK:         pycegui.Key.BREAK,
#        fife.Key.MENU:          pycegui.Key.MENU,
#        fife.Key.POWER:         pycegui.Key.POWER,
#        fife.Key.EURO:          pycegui.Key.EURO,
#        fife.Key.UNDO:          pycegui.Key.UNDO
    }
    wheel_speed = 1.0
    
    def __init__(self, event_listener):
        KeyListener.__init__(self, event_listener)
        MouseListener.__init__(self, event_listener)
    
    def keyPressed(self, event):
        key_code = event.getKey()
        key_value = event.getValue()
        cegui_key_code = self.key_code_map.get(key_code)
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectKeyDown(cegui_key_code)
        # TODO: check for non-print characters.
        cegui_system.injectChar(key_value)
    
    def keyReleased(self, event):
        key_code = event.getKey()
        cegui_key_code = self.key_code_map.get(key_code)
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectKeyUp(cegui_key_code)
    
    def mouseMoved(self, event):
        delta_x, delta_y = event.getX(), event.getY()
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectMousePosition(delta_x, delta_y)
    
    def mousePressed(self, event):
        button = event.getButton()
        cegui_button = self.mouse_button_map.get(button,
                                                 pycegui.MouseButton.NoButton)
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectMouseButtonDown(cegui_button)
    
    def mouseReleased(self, event):
        button = event.getButton()
        cegui_button = self.mouse_button_map.get(button,
                                                 pycegui.MouseButton.NoButton)
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectMouseButtonUp(cegui_button)
    
    def mouseWheelMovedUp(self, event):
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectMouseWheelChange(self.wheel_speed)
    
    def mouseWheelMovedDown(self, event):
        cegui_system = pycegui.System.getSingleton()
        cegui_system.injectMouseWheelChange(-self.wheel_speed)
    
    def mouseDragged(self, event):
        self.mouseMoved(event)
    
    def mouseClicked(self, event):
        self.mousePressed(event)
        self.mouseReleased(event)


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
        self.listener = ApplicationListener(self)
        self.cegui_listener = CeguiListener(self.event_listener)
        #start_map = self._setting.get("PARPG", "Map")
        #self.model.changeMap(start_map)
        self.cegui_renderer = CeguiOpenGlRenderer.bootstrapSystem()
        cegui_system = pycegui.System.getSingleton()
        self.engine.registerPostRenderCallback(cegui_system.renderGUI)
        cegui_resource_provider = cegui_system.getResourceProvider()
        cegui_resource_provider.setResourceGroupDirectory(
            "schemes",
            "/home/george/Workspace/parpg/parpg/game/cegui/schemes"
        )
        cegui_resource_provider.setResourceGroupDirectory(
            "imagesets",
            "/home/george/Workspace/parpg/parpg/game/cegui/imagesets"
        )
        cegui_resource_provider.setResourceGroupDirectory(
            "fonts",
            "/home/george/Workspace/parpg/parpg/game/cegui/fonts"
        )
        cegui_resource_provider.setResourceGroupDirectory(
            "layouts",
            "/home/george/Workspace/parpg/parpg/game/cegui/layouts"
        )
        cegui_resource_provider.setResourceGroupDirectory(
            "looknfeels",
            "/home/george/Workspace/parpg/parpg/game/cegui/looknfeels"
        )
        cegui_resource_provider.setResourceGroupDirectory(
            "scripts",
            "/home/george/Workspace/parpg/parpg/game/cegui/scripts"
        )
        pycegui.Imageset.setDefaultResourceGroup("imagesets")
        pycegui.Font.setDefaultResourceGroup("fonts")
        pycegui.Scheme.setDefaultResourceGroup("schemes")
        pycegui.WidgetLookManager.setDefaultResourceGroup("looknfeels")
        pycegui.WindowManager.setDefaultResourceGroup("layouts")
        pycegui.ScriptModule.setDefaultResourceGroup("scripts");
        
        pycegui.SchemeManager.getSingleton().create("TaharezLook.scheme")
        pycegui.FontManager.getSingleton().create("DejaVuSans-10.font")
        cegui_system.setDefaultMouseCursor("TaharezLook", "MouseArrow")
        
        cegui_window_manager = pycegui.WindowManager.getSingleton()
        root_window = cegui_window_manager.createWindow("DefaultWindow",
                                                        "root")
        cegui_system.setGUISheet(root_window)
        frame_window = cegui_window_manager.createWindow(
            "TaharezLook/FrameWindow",
            "testWindow"
        )
        root_window.addChildWindow(frame_window)
        frame_window.setPosition(UVector2(UDim(0.25, 0), UDim(0.25, 0)))
        frame_window.setSize(UVector2(UDim(0.75, 0), UDim(0.75, 0)))

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
