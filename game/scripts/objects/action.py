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

#exceptions

from scripts.gui import drag_drop_data as data_drag

class NoSuchQuestException(Exception):
    """NoQuestException is used when there is no active quest with the id"""
    pass

#classes

class Action(object):
    """Base Action class, to define the structure"""


    def __init__(self, controller, commands = None):
        """Basic action constructor
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        """
        self.commands = commands or ()
        self.controller = controller
        self.model = controller.model
    
    def execute(self):
        """To be overwritten"""        
        #Check if there are special commands and execute them
        for command_data in self.commands:
            command = command_data["Command"]
            if command == "SetQuestVariable":
                quest_id = command_data["ID"]
                variable = command_data["Variable"]
                value = command_data["Value"]
                quest_engine = self.model.game_state.quest_engine 
                if quest_engine.hasQuest(quest_id):
                    quest_engine[quest_id].setValue(variable, value)
                else:
                    raise NoSuchQuestException
            elif command == "ResetMouseCursor":
                self.controller.resetMouseCursor()
            elif command == "StopDragging":
                data_drag.dragging = False
                
class ChangeMapAction(Action):
    """A change map scheduled"""
    def __init__(self, controller, target_map_name, target_pos, commands = None):
        """Initiates a change of the position of the character
        possibly flagging a new map to be loaded.
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        @type target_map_name: String
        @param target_map_name: Target map id 
        @type target_pos: Tuple
        @param target_pos: (X, Y) coordinates on the target map.
        @return: None"""
        super(ChangeMapAction, self).__init__(controller, commands)
        self.view = controller.view
        self.target_pos = target_pos
        self.target_map_name = target_map_name

    def execute(self):
        """Executes the map change."""
        self.model.changeMap(self.target_map_name,
                              self.target_pos)
        super(ChangeMapAction, self).execute()

class OpenAction(Action):
    """Open a container"""
    def __init__(self, controller, container, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        @param container: A reference to the container
        """
        super(OpenAction, self).__init__(controller, commands)
        self.view = controller.view
        self.container = container
    def execute(self):
        """Open the box."""
        self.view.hud.createBoxGUI(self.container.name, \
                                              self.container)
        super(OpenAction, self).execute()
       
       
class OpenBoxAction(OpenAction):
    """Open a box. Needs to be more generic, but will do for now."""
    def __init__(self, controller, container, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        @param container: A reference to the container
        """
        super(OpenBoxAction, self).__init__(controller, commands)
        self.view = controller.view
        self.container = container
        
    def execute(self):
        """Open the box."""
        try:
            self.container.open()
            super(OpenBoxAction, self).execute()

        except ValueError:
            self.view.hud.createExamineBox(self.container.name, \
                                                  "The container is locked")
        
class UnlockBoxAction(Action):
    """Unlocks a box. Needs to be more generic, but will do for now."""
    def __init__(self, controller, container, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @param container: A reference to the container
        """
        super(UnlockBoxAction, self).__init__(controller, commands)
        self.container = container
    
    def execute(self):
        """Open the box."""
        self.container.unlock()
        super(UnlockBoxAction, self).execute()
        
class LockBoxAction(Action):
    """Locks a box. Needs to be more generic, but will do for now."""
    def __init__(self, controller, container, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @param container: A reference to the container
        """
        super(LockBoxAction, self).__init__(controller, commands)
        self.container = container
        
    def execute(self):
        """Lock the box."""
        self.container.lock()
        super(LockBoxAction, self).execute()


class ExamineAction(Action):
    """Examine an object."""
    def __init__(self, controller, examine_id, examine_name, examine_desc, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param examine_id: An object id
        @type examine_id: integer
        @param examine_name: An object name
        @type examine_name: string
        @param examine_desc: A description of the object that will be displayed.
        @type examine_desc: string
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        
        """
        super(ExamineAction, self).__init__(controller, commands)
        self.view = controller.view
        self.examine_id = examine_id
        self.examine_name = examine_name
        self.examine_desc = examine_desc
        
    def execute(self):
        """Display the text."""
        action_text = self.examine_desc
        self.view.hud.addAction(unicode(action_text))
        print action_text
        #this code will cut the line up into smaller lines that will be displayed
        place = 25
        while place <= len(action_text):
            if action_text[place] == ' ':
                action_text = action_text[:place] +'\n'+action_text[place:]
                place += 26 #plus 1 character to offset the new line
            else: place += 1
        self.view.displayObjectText(self.examine_id, unicode(action_text), time=3000)

class ExamineItemAction(Action):
    """Examine an item."""
    def __init__(self, controller, examine_name, examine_desc, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        @type examine_name: String
        @param examine_name: Name of the object to be examined.
        @type examine_name: String
        @param examine_name: Description of the object to be examined.
        """
        super(ExamineItemAction, self).__init__(controller, commands)
        self.view = controller.view
        self.examine_name = examine_name
        self.examine_desc = examine_desc
        
    def execute(self):
        """Display the text."""
        action_text = unicode(self.examine_desc)
        self.view.hud.addAction(action_text)
        print action_text

class ReadAction(Action):
    """Read a text."""
    def __init__(self, controller, text_name, text, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @param view: The view
        @type view: class derived from scripts.ViewBase
        @param text_name: Name of the object containing the text
        @type text_name: String
        @param text: Text to be displayied
        @type text: String
        """
        super(ReadAction, self).__init__(controller, commands)
        self.view = controller.view
        self.text_name = text_name
        self.text = text
        
    def execute(self):
        """Examine the box."""
        action_text = unicode('\n'.join(["You read " + self.text_name + ".", 
                                         self.text]))
        self.view.hud.addAction(action_text)
        print action_text
        super(ReadAction, self).execute()

class TalkAction(Action):
    """An action to represent starting a dialogue"""
    def __init__(self, controller, npc, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        @type view: class derived from scripts.ViewBase
        @param view: The view
        @type npc: NonPlayerCharacter
        @param npc: NPC to interact with.
        """
        super(TalkAction, self).__init__(controller, commands)
        self.view = controller.view
        self.npc = npc
        
    def execute(self):
        """Talk with the NPC when close enough, otherwise move closer.
           @return: None"""
        from scripts.dialoguecontroller import DialogueController
        
        player_char = self.model.game_state.player_character
        npc_coordinates = self.npc.getLocation().getLayerCoordinates()
        pc_coordinates = player_char.behaviour.agent.\
                            getLocation().getLayerCoordinates()
        
        distance_squared = (npc_coordinates.x - pc_coordinates.x) *\
                           (npc_coordinates.x - pc_coordinates.x) +\
                           (npc_coordinates.y - pc_coordinates.y) *\
                           (npc_coordinates.y - pc_coordinates.y)
        
        # If we are too far away, we approach the NPC again
        if distance_squared > 2:
            player_char.approach([self.npc.getLocation().
                         getLayerCoordinates().x,
                         self.npc.getLocation().
                         getLayerCoordinates().y], 
                        TalkAction(self.controller,
                                   self.npc, self.commands))        
        else:
            player_char.behaviour.agent.act('stand', self.npc.getLocation())
    
            if self.npc.dialogue is not None:
                dialogue_controller = DialogueController(self.controller.engine,
                                                         self.view,
                                                         self.model,
                                                         self.controller.application)
                self.controller.application.pushController(dialogue_controller)
                dialogue_controller.startTalk(self.npc)
            else:
                self.npc.behaviour.agent.say("Leave me alone!", 1000)
                
            self.model.game_state.player_character.behaviour.idle()
            self.model.game_state.player_character.nextAction = None
            super(TalkAction, self).execute()

class UseAction(Action):
    """Action for carryable items. It executes special commands that can be only
    used on carryable utens"""


    def __init__(self, controller, item, commands = None):
        """
        @param controller: A reference to the GameSceneController.
        @type controller: scripts.GameSceneController
        @param item: Item on which the action is called
        @type item: CarryableItem
        @param commands: Special commands that are executed
        @type commands: Dictionary 
        """
        super(UseAction, self).__init__(controller, commands)
        self.view = controller.view
        self.item = item
    
    def execute(self):
        #Check if there are special commands and execute them
        for command_data in self.commands:
            command = command_data["Command"]
            if command == "ReplaceItem":
                object_id = command_data["ID"]
                object_type = command_data["ObjectType"]
                container = self.item.in_container
                inst_dict = {}
                inst_dict["ID"] = object_id
                inst_dict["object_type"] = object_type
                new_item = self.model.createContainerObject(inst_dict)
                container.replaceItem(self.item, new_item)
                self.view.hud.inventory.updateInventoryButtons()
        super(UseAction, self).execute()

class PickUpAction(Action):
    """Action for picking up items from a map"""

    def __init__(self, controller, map_item, commands = None):
        super(PickUpAction, self).__init__(controller, commands)
        self.map_item = map_item
        self.view = controller.view
        
    def execute(self):
        real_item = self.map_item.item
        self.model.deleteObject(self.map_item.ID)
        self.model.game_state.player_character.\
                                inventory.placeItem(real_item)
        self.view.hud.inventory.updateInventoryButtons()
        super(PickUpAction, self).execute()

class DropItemAction(Action):
    """Action for dropping an items on a map"""
    def __init__(self, controller, item, commands = None):
        super(DropItemAction, self).__init__(controller, commands)
        self.item = item
        
    def execute(self):
        map_name = self.model.game_state.current_map_name
        map_item_values = {}
        map_item_values["ViewName"] = self.item.name
        map_item_values["ObjectType"] = "MapItem"
        map_item_values["ItemType"] = self.item.item_type
        map_item_values["Map"] = map_name
        coords = self.model.game_state.player_character.\
                                        getLocation().getExactLayerCoordinates()
        map_item_values["Position"] = (coords.x, coords.y)
        map_item_values["Rotation"] = 0
        map_item_values["item"] = self.item
        agent = {}
        agent[self.item.ID] = map_item_values
        self.model.addAgent("All", agent)
        self.model.placeAgents()
        super(DropItemAction, self).execute()
        
class DropItemFromContainerAction(DropItemAction):
    """Action for dropping an items from the Inventory to a map"""

    def __init__(self, controller, item, container_gui, commands = None):
        super(DropItemFromContainerAction, self).__init__(controller, item, commands)
        self.container_gui = container_gui

    def execute(self):
        super(DropItemFromContainerAction, self).execute()
        self.item.in_container.takeItem(self.item)
        self.container_gui.updateImages()
        
class BrewBeerAction(Action):
    """Action for brewing beer in a pot"""
    def __init__(self, controller, pot, commands = None):
        super(BrewBeerAction, self).__init__(controller, commands)
        self.pot = pot
        self.view = controller.view
        
    def execute(self):
        """Brew the beer"""
        has_water = False
        has_yeast = False
        has_fruit = False
        has_wood = False
        has_bottle = False
        player_character = self.model.game_state.player_character
        for item in self.pot.items.itervalues():
            if item.item_type == "Questionable water":
                if has_water:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 water in the pot"))
                    return
                has_water = True
                water_type = 1 
                water = item
            elif item.item_type == "Pure water":
                if has_water:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 water in the pot"))
                    return
                has_water = True
                water_type = 2
                water = item
            elif item.item_type == "Grain":
                if has_fruit:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 fruit in the pot"))
                    return
                has_fruit = True
                fruit_type = 3
                fruit = item
            elif item.item_type == "Wild potato":
                if has_fruit:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 fruit in the pot"))
                    return
                has_fruit = True
                fruit_type = 2
                fruit = item
            elif item.item_type == "Rotten yam":
                if has_fruit:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 fruit in the pot"))
                    return
                has_fruit = True
                fruit_type = 1
                fruit = item
            elif item.item_type == "Yeast":
                if has_yeast:
                    self.view.hud.addAction(unicode(\
                        "Please put only 1 yeast in the pot"))
                    return
                has_yeast = True
                yeast = item 
            else:
                self.view.hud.addAction(unicode("Item " + item.name + \
                                                " is not needed for brewing beer"))
                self.view.hud.addAction(unicode(\
                    "Please put only ingredients for the beer in the pot.\
                    Things like bottles and wood have to be in your inventory"))
                return
        wood = player_character.hasItem("Wood")
        if wood:
            has_wood = True        
        bottle = player_character.hasItem("Empty beer bottle")
        if bottle:
            has_bottle = True        
        if has_water and has_fruit and has_wood and has_bottle:
            self.pot.removeItem(water)
            self.pot.removeItem(fruit)
            if has_yeast:
                self.pot.removeItem(yeast)
            player_character.inventory.removeItem(wood)
            inst_dict = {}
            inst_dict["ID"] = "Beer"
            inst_dict["object_type"] = "Beer"
            new_item = self.model.createContainerObject(inst_dict)
            player_character.inventory.placeItem(new_item)
            self.view.hud.inventory.updateInventoryButtons()
            beer_quality = 0
            if water_type == 1:
                if fruit_type == 1:
                    beer_quality = -1
                elif fruit_type == 2:
                    beer_quality = 2
                elif fruit_type == 3:
                    beer_quality = 3
            if water_type == 2:
                if fruit_type == 1:
                    beer_quality = 1
                elif fruit_type == 2:
                    beer_quality = 3
                elif fruit_type == 3:
                    beer_quality = 4
            if beer_quality > 0 and has_yeast:
                beer_quality += 1
            self.model.game_state.quest_engine.quests["beer"].\
                    setValue("beer_quality", beer_quality)
        else:
            self.view.hud.addAction(unicode(
            """For brewing beer you need at least:
            In the pot:
                Fruit (like grain, potato, yam)
                Water
                Optionally:
                    Good quality yeast.
                    Wild yeast will be used if none present.
            In the inventory:
                Wood
                Empty bottle"""))
        super(BrewBeerAction, self).execute()

ACTIONS = {"ChangeMap":ChangeMapAction, 
           "Open":OpenAction,
           "OpenBox":OpenBoxAction, 
           "Unlock":UnlockBoxAction,
           "Lock":LockBoxAction,
           "ExamineItem":ExamineItemAction,
           "Examine":ExamineAction,
           "Look":ExamineItemAction,
           "Read":ReadAction,
           "Talk":TalkAction,
           "Use":UseAction,
           "PickUp":PickUpAction,
           "DropFromInventory":DropItemFromContainerAction,
           "BrewBeer":BrewBeerAction}
