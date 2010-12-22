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

# there should be NO references to FIFE here!
import sys
import os.path
import logging
from copy import deepcopy

from fife import fife
from fife.extensions.serializers.xmlobject import XMLObjectLoader 

from gamestate import GameState
from objects import createObject
from objects.composed import CarryableItem, CarryableContainer
from gamemap import GameMap
from common.utils import locateFiles
from common.utils import parseBool
from inventory import Inventory
from scripts.dialogueparsers import YamlDialogueParser, DialogueFormatError

try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

import yaml

class GameModel(object):
    """GameModel holds the logic for the game.
       Since some data (object position and so forth) is held in the
       fife, and would be pointless to replicate, we hold a instance of
       the fife view here. This also prevents us from just having a
       function heavy controller."""
    ALL_AGENTS_KEY = "All"
    MAX_ID_NUMBER = 1000
    
    def __init__(self, engine, settings):
        """Initialize the instance.
        @param engine: A fife.Engine object
        @type emgome: fife.Engine 
        @param setting: The applications settigns
        @type setting: fife_settings.Setting 
        @return: None"""
        self.map_change = False
        self.load_saver = False
        self.savegame = None
        self.game_state = GameState(quests_dir = settings.get("PARPG",
                                                             "QuestsDirectory"))
        #self.game_state.quest_engine = 
        #self.game_state.quest_engine.readQuests()
        self.pc_run = 1
        self.target_position = None
        self.target_map_name = None
        self.object_db = {}
        self.active_map = None
        self.map_files = {}
        self.agents = {}
        self.agents[self.ALL_AGENTS_KEY] = {}
        self.engine = engine
        self.fife_model = engine.getModel()
        self.game_state.maps_file = "maps/maps.yaml"
        self.all_agents_file = "maps/all_agents.yaml"
        self.object_db_file = "objects/object_database.yaml"
        self.agents_directory = "objects/"
        self.dialogues_directory = "dialogue"
        self.dialogues = {}
        self.agent_import_files = {}
        self.settings = settings
        self.obj_loader = XMLObjectLoader(
                                          self.engine.getImagePool(), 
                                          self.engine.getAnimationPool(), 
                                          self.engine.getModel(),
                                          self.engine.getVFS() 
                                          )

    def checkAttributes(self, attributes):
        """Checks for attributes that where not given in the map file
        and fills them with values from the object database
        @param attributes: attributes to check
        @type attributes: Dictionary
        @return: The modified attributes""" 
        if attributes.has_key("object_type"):
            class_name = attributes.pop("object_type")
        else:
            class_name = attributes["type"]
        if not attributes.has_key("type"):
            attributes["type"] = class_name
        if self.object_db.has_key(class_name):
            db_attributes = deepcopy(self.object_db[class_name])
            for key in db_attributes.keys():
                if attributes.has_key(key):
                    attributes[key] = attributes[key] or db_attributes[key]
                else:
                    attributes[key] = db_attributes[key]
        return attributes
    
    def isIDUsed(self, ID):
        if self.game_state.hasObject(ID):
            return True
        for namespace in self.agents:
            if ID in self.agents[namespace]:
                return True
        return False
    
    def createUniqueID(self, ID):
        if self.isIDUsed(ID):
            id_number = 1
            while self.isIDUsed(ID + "_" + str(id_number)):
                id_number += 1
                if id_number > self.MAX_ID_NUMBER:
                    raise ValueError(
                        "Number exceeds MAX_ID_NUMBER:" + str(self.MAX_ID_NUMBER))
            
            ID = ID + "_" + str(id_number)
        return ID

    def createContainerItems(self, container_objs):
        """Create the items of a container from a dictionary
        @param container_objs: Dictionary containing the items
        @type container_objs: dict"""
        items = []
        for container_obj in container_objs:
            items.append(self.createContainerObject(container_obj))
        
        return items

    def createContainerObject(self, attributes):
        """Create an object that can be stored in 
        an container and return it
        @param attributes: Dictionary of all object attributes
        @type attributes: Dictionary
        @return: The created object """
        # create the extra data
        extra = {}
        extra['controller'] = self
        attributes = self.checkAttributes(attributes)
        
        info = {}
        info.update(attributes)
        info.update(extra)
        ID = info.pop("id") if info.has_key("id") else info.pop("ID")
        if not info.has_key("item_type"):
            info["item_type"] = info["type"]
        ID = self.createUniqueID(ID)
        if info.has_key("attributes"):
            attributes = info["attributes"]
            if "Container" in attributes:
                info["actions"]["Open"] = ""
                if info.has_key("Items"):
                    inventory_objs = info["Items"]
                    info["items"] = self.createContainerItems(inventory_objs)
                
                new_item = CarryableContainer(ID = ID, **info) 
            else:
                new_item = CarryableItem(ID = ID, **info) 
        else:
            new_item = CarryableItem(ID = ID, **info) 
        self.game_state.addObject(None, new_item)
        return new_item
      
    def createInventoryObject(self, container, attributes):
        """Create an inventory object and place it into a container
           @type container: base.Container
           @param container: Container where the item is on
           @type attributes: Dictionary
           @param attributes: Dictionary of all object attributes
           @return: None"""
        index = attributes.pop("index") if attributes.has_key("index") else None
        slot = attributes.pop("slot") if attributes.has_key("slot") else None
        obj = self.createContainerObject(attributes)        
        #obj = createObject(attributes, extra)
        if slot:
            container.moveItemToSlot(obj, slot)
        else:
            container.placeItem(obj, index)
    
    def deleteObject(self, object_id):
        """Removes an object from the game
        @param object_id: ID of the object
        @type object_id: str """
        del self.agents["All"][object_id]
        self.game_state.deleteObject(object_id)
        
    def save(self, path, filename):
        """Writes the saver to a file.
           @type filename: string
           @param filename: the name of the file to write to
           @return: None"""
        fname = '/'.join([path, filename])
        try:
            save_file = open(fname, 'w')
        except(IOError):
            sys.stderr.write("Error: Can't create save game: " + fname + "\n")
            return
        save_state = {}
        save_state["Agents"] = {}
        for map_name in self.agents:
            if map_name == self.ALL_AGENTS_KEY:
                continue
            agents_dict = {}
            for agent in self.agents[map_name]:
                agent_obj = self.game_state.getObjectById(agent, map_name)
                agent_inst = self.game_state.maps[map_name].\
                                    agent_layer.getInstance(agent)
                agent_dict = self.agents[map_name][agent]
                agent_dict.update(agent_obj.getStateForSaving())
                agent_dict["Rotation"] = agent_inst.getRotation()
                agents_dict[agent] = agent_dict
            save_state["Agents"][map_name] = agents_dict
        agents_dict = {}
        for agent in self.agents["All"]:
            map_name = self.agents["All"][agent]["Map"]
            agent_dict = self.agents["All"][agent]
            agent_obj = None
            if agent == "PlayerCharacter":
                agent_obj = self.game_state.player_character
            else:
                agent_obj = self.game_state.getObjectById(agent, map_name)
            if agent_obj:
                agent_inst = self.game_state.maps[map_name].\
                                    agent_layer.getInstance(agent)
                agent_dict.update(agent_obj.getStateForSaving())
                agent_dict["Rotation"] = agent_inst.getRotation()
                agent_dict["MapName"] = map_name
            agents_dict[agent] = agent_dict
        save_state["Agents"]["All"] = agents_dict
        save_state["GameState"] = self.game_state.getStateForSaving()
        yaml.dump(save_state, save_file)
        
        save_file.close()       

    def load(self, path, filename):
        """Loads a saver from a file.
           @type filename: string
           @param filename: the name of the file (including path) to load from
           @return: None"""
        fname = '/'.join([path, filename])

        try:
            load_file = open(fname, 'r')
        except(IOError):
            sys.stderr.write("Error: Can't find save game file\n")
            return        
        self.deleteMaps()
        self.clearAgents()
        
        save_state = yaml.load(load_file)
        self.game_state.restoreFromState(save_state["GameState"])
        maps = save_state["Agents"]
        for map_name in maps:
            for agent_name in maps[map_name]:
                agent = {agent_name:maps[map_name][agent_name]}
                self.addAgent(map_name, agent)
                
        # Load the current map
        if self.game_state.current_map_name:
            self.loadMap(self.game_state.current_map_name)         
        load_file.close()
        

        # Recreate all the behaviours. These can't be saved because FIFE
        # objects cannot be pickled
        
        self.placeAgents()
        self.placePC()
      
        # In most maps we'll create the PlayerCharacter Instance internally. 
        # In these cases we need a target position
         
    def teleport(self, agent, position):
        """Called when a an agent is moved instantly to a new position. 
        The setting of position may wan to be created as its own method down the road.
        @type position: String Tuple
        @param position: X,Y coordinates passed from engine.changeMap
        @return: fife.Location"""
        print position
        coord = fife.DoublePoint3D(float(position[0]), float(position[1]), 0)
        location = fife.Location(self.active_map.agent_layer)
        location.setMapCoordinates(coord)
        agent.teleport(location)         
               
    def getObjectAtCoords(self, coords):
        """Get the object which is at the given coords
        @type coords: fife.Screenpoint
        @param coords: Coordinates where to check for an object
        @rtype: fife.Object
        @return: An object or None"""
        instances = self.active_map.cameras[
                                            self.active_map.my_cam_id].\
            getMatchingInstances(coords, self.active_map.agent_layer)
        # no object returns an empty tuple
        if(instances != ()):
            front_y = 0
            

            for obj in instances:
                # check to see if this in our list at all
                if(self.objectActive(obj.getId())):
                    # check if the object is on the foreground
                    obj_map_coords = \
                                      obj.getLocation().getMapCoordinates()
                    obj_screen_coords = self.active_map.\
                        cameras[self.active_map.my_cam_id]\
                        .toScreenCoordinates(obj_map_coords)

                    if obj_screen_coords.y > front_y:
                        #Object on the foreground
                        front_y = obj_screen_coords.y
                        return obj
                    else:
                        return None
        else:
            return None

    def getCoords(self, click):
        """Get the map location x, y coordinates from the screen coordinates
           @type click: fife.ScreenPoint
           @param click: Screen coordinates
           @rtype: fife.Location
           @return: The map coordinates"""
        coord = self.active_map.cameras[self.active_map.my_cam_id].\
                    toMapCoordinates(click, False)
        coord.z = 0
        location = fife.Location(self.active_map.agent_layer)
        location.setMapCoordinates(coord)
        return location

    def pause(self, paused):
        """ Pause/Unpause the game
        @return: nothing"""
        if self.active_map:
            self.active_map.pause(paused)
    
    def togglePause(self):
        """ Toggle paused state.
        @return: nothing"""
        self.active_map.togglePause()
        
    def isPaused(self):
        """Returns wheter the game is paused or not"""
        return self.active_map.isPaused()
    
    def readMapFiles(self):
        """Read all a available map-files and store them"""
        maps_data = file(self.game_state.maps_file)
        self.map_files = yaml.load(maps_data)["Maps"]
    
    def addAgent(self, namespace, agent):
        """Adds an agent to the agents dictionary
        @param namespace: the namespace where the agent is to be added to
        @type namespace: str
        @param agent: The agent to be added
        @type agent: dict """
        from fife.extensions.serializers.xml_loader_tools import loadImportFile
        if not self.agents.has_key(namespace):
            self.agents[namespace] = {}
            
        agent_values = agent.values()[0]
        unique_agent_id = self.createUniqueID(agent.keys()[0])
        del agent[agent.keys()[0]]
        agent[unique_agent_id] = agent_values
        self.agents[namespace].update(agent)
        object_model = ""
        if agent_values.has_key("ObjectModel"): 
            object_model =  agent_values["ObjectModel"]
        elif agent_values["ObjectType"] == "MapItem":
            object_data = self.object_db[agent_values["ItemType"]]
            object_model = object_data["gfx"] if object_data.has_key("gfx") \
                        else "generic_item"
        else:
            object_model = self.object_db[agent_values["ObjectType"]]["gfx"]
        import_file = self.agent_import_files[object_model]
        loadImportFile(self.obj_loader, import_file, self.engine)
        
    def readAgentsOfMap(self, map_name):
        """Read the agents of the map
        @param map_name: Name of the map
        @type map_name: str """
        #Get the agents of the map        
        map_agents_file = self.map_files[map_name].\
                            replace(".xml", "_agents.yaml")   
        agents_data = file(map_agents_file)
        agents = yaml.load_all(agents_data)
        for agent in agents:
            if not agent == None:
                self.addAgent(map_name, agent)  
    
    def readAllAgents(self):
        """Read the agents of the all_agents_file and store them"""
        agents_data = file(self.all_agents_file)
        agents = yaml.load_all(agents_data)
        for agent in agents:
            if not agent == None:
                self.addAgent(self.ALL_AGENTS_KEY, agent)  
                
    def getAgentsOfMap(self, map_name):
        """Returns the agents that are on the given map
        @param map_name: Name of the map
        @type map_name: str
        @return: A dictionary with the agents of the map"""
        if not self.agents.has_key(map_name):
            return {}
        ret_dict = self.agents[map_name].copy()
        for agent_name, agent_value in self.agents[self.ALL_AGENTS_KEY]\
                                                .iteritems():
            if agent_value["Map"] == map_name:
                ret_dict[agent_name] = agent_value
        return ret_dict
                
    def getAgentsOfActiveMap(self):
        """Returns the agents that are on active map
        @return: A dictionary with the agents of the map """
        return self.getAgentsOfMap(self.active_map.map.getId())

    def clearAgents(self):
        """Resets the agents dictionary"""
        self.agents = {}
        self.agents[self.ALL_AGENTS_KEY] = {}
    
    def loadMap(self, map_name):
        """Load a new map.
           @type map_name: string
           @param map_name: Name of the map to load
           @return: None"""
        if not map_name in self.game_state.maps:  
            map_file = self.map_files[map_name]
            new_map = GameMap(self.engine, self)
            self.game_state.maps[map_name] = new_map
            new_map.load(map_file)    

    def createAgent(self, agent, inst_id):
        object_type = agent["ObjectType"]
        object_id = agent["ObjectModel"] \
                                if agent.has_key("ObjectModel") \
                                else None
        if object_id == None:
            if object_type == "MapItem":
                object_data = self.object_db[agent["ItemType"]]
                object_id = object_data["gfx"] if object_data.has_key("gfx") \
                            else "generic_item"
            else:
                object_id = self.object_db[object_type]["gfx"]
        map_obj = self.fife_model.getObject(str(object_id), "PARPG")
        if not map_obj:
            print ''.join(['Object with inst_id=', str(object_id), 
                           ' ns=PARPG', \
                           ' could not be found. Omitting...'])

        x_pos = agent["Position"][0]
        y_pos = agent["Position"][1]
        z_pos = agent["Position"][2] if len(agent["Position"]) == 3 \
                                        else -0.1 if object_type == "MapItem" \
                                        else 0.0  
        stack_pos = agent["Stackposition"] if \
                        agent.has_key("StackPosition") \
                        else None
        inst = self.active_map.agent_layer.\
                        createInstance(map_obj,
                                       fife.ExactModelCoordinate(x_pos, 
                                                                 y_pos, 
                                                                 z_pos),
                                       inst_id)
        inst.setId(inst_id)

        rotation = agent["Rotation"]
        inst.setRotation(rotation)

        fife.InstanceVisual.create(inst)
        if (stack_pos):
            inst.get2dGfxVisual().setStackPosition(int(stack_pos))

        if (map_obj.getAction('default')):
            target = fife.Location(self.active_map.agent_layer)
            inst.act('default', target, True)
            
        inst_dict = {}
        inst_dict["id"] = inst_id
        inst_dict["type"] = object_type
        inst_dict["xpos"] = x_pos
        inst_dict["ypos"] = y_pos
        inst_dict["gfx"] = object_id
        inst_dict["is_open"] = parseBool(agent["Open"]) \
                                if agent.has_key("Open") \
                                else False
        inst_dict["locked"] = parseBool(agent["Locked"]) \
                                if agent.has_key("Locked") \
                                else False
        inst_dict["name"] = agent["ViewName"]
        inst_dict["real_name"] = agent["RealName"] \
                                    if agent.has_key("RealName") \
                                    else agent["ViewName"]
        inst_dict["text"] = agent["Text"] \
                                    if agent.has_key("Text") \
                                    else None
        if self.dialogues.has_key(inst_id):
            inst_dict["dialogue"] = self.dialogues[inst_id]
        inst_dict["target_map_name"] = agent["TargetMap"] \
                                        if agent.\
                                            has_key("TargetMap") \
                                        else None
        inst_dict["target_x"] = agent["TargetPosition"][0] \
                                    if agent.\
                                        has_key("TargetPosition") \
                                    else None
        inst_dict["target_y"] = agent["TargetPosition"][1] \
                                    if agent.\
                                        has_key("TargetPosition") \
                                    else None
        if agent.has_key("Inventory"):
            inventory = Inventory()
            inventory_objs = agent["Inventory"]
            for inventory_obj in inventory_objs:
                self.createInventoryObject(inventory,
                                           inventory_obj 
                                           )
            inst_dict["inventory"] = inventory

        if agent.has_key("Items"):
            container_objs = agent["Items"]
            items = self.createContainerItems(container_objs)
            inst_dict["items"] = items
            
        if agent.has_key("ItemType"):
            if not agent.has_key("item"):
                item_data = {}
                item_data["type"] = agent["ItemType"]
                item_data["ID"] = inst_id 
                item_data = self.createContainerObject(item_data)
            else:
                item_data = agent["item"]
            inst_dict["item"] = item_data
            inst_dict["item_type"] = agent["ItemType"]

        self.createMapObject(self.active_map.agent_layer, inst_dict)
    
    def placeAgents(self):
        """Places the current maps agents """
        if not self.active_map:
            return
        agents = self.getAgentsOfMap(self.game_state.current_map_name)
        for agent in agents:
            if agent == "PlayerCharacter":
                continue
            if self.active_map.agent_layer.getInstances(agent):
                continue
            self.createAgent(agents[agent], agent)

    def placePC(self):
        """Places the PlayerCharacter on the map"""
        agent = self.agents[self.ALL_AGENTS_KEY]["PlayerCharacter"]
        inst_id = "PlayerCharacter"
        self.createAgent(agent, inst_id)
        
        # create the PlayerCharacter agent
        self.active_map.addPC()
        self.game_state.player_character.start()
        if agent.has_key("PeopleKnown"):
            self.game_state.player_character.people_i_know = agent["PeopleKnown"]
                      
    def changeMap(self, map_name, target_position = None):
        """Registers for a map change on the next pump().
           @type map_name: String
           @param map_name: Id of the map to teleport to
           @type map_file: String
           @param map_file: Filename of the map to teleport to
           @type target_position: Tuple
           @param target_position: Position of PlayerCharacter on target map.
           @return None"""
        # set the parameters for the map change if moving to a new map
        if map_name != self.game_state.current_map_name:
            self.target_map_name = map_name
            self.target_position = target_position
            # issue the map change
            self.map_change = True

    def deleteMaps(self):
        """Clear all currently loaded maps from FIFE as well as clear our
            local map cache
            @return: nothing"""
        self.engine.getModel().deleteMaps()
        self.engine.getModel().deleteObjects()
        self.game_state.clearObjects()
        self.game_state.maps = {}
        
    def setActiveMap(self, map_name):
        """Sets the active map that is to be rendered.
           @type map_name: String
           @param map_name: The name of the map to load
           @return: None"""
        # Turn off the camera on the old map before we turn on the camera
        # on the new map.
        self.active_map.cameras[self.active_map.my_cam_id].setEnabled(False)
        # Make the new map active.
        self.active_map = self.game_state.maps[map_name]
        self.active_map.makeActive()
        self.game_state.current_map_name = map_name

    def createMapObject (self, layer, attributes):
        """Create an object and add it to the current map.
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type attributes: Dictionary
           @param attributes: Dictionary of all object attributes
           @type instance: fife.Instance
           @param instance: FIFE instance corresponding to the object
           @return: None"""
        # create the extra data
        extra = {}
        if layer is not None:
            extra['agent_layer'] = layer
        attributes = self.checkAttributes(attributes)
        
        obj = createObject(attributes, extra)
        
        if obj.trueAttr("PC"):
            self.addPC(layer, obj)
        else:
            self.addObject(layer, obj) 

    def addPC(self, layer, player_char):
        """Add the PlayerCharacter to the map
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type player_char: PlayerCharacter
           @param player_char: PlayerCharacter object
           @type instance: fife.Instance
           @param instance: FIFE instance of PlayerCharacter
           @return: None"""
        # For now we copy the PlayerCharacter, 
        # in the future we will need to copy
        # PlayerCharacter specifics between the different PlayerCharacter's
        self.game_state.player_character = player_char
        self.game_state.player_character.setup()        

    def addObject(self, layer, obj):
        """Adds an object to the map.
           @type layer: fife.Layer
           @param layer: FIFE layer object exists in
           @type obj: GameObject
           @param obj: corresponding object class
           @type instance: fife.Instance
           @param instance: FIFE instance of object
           @return: None"""
        ref = self.game_state.getObjectById(obj.ID, \
                                            self.game_state.current_map_name) 
        if ref is None:
            # no, add it to the game state
            self.game_state.addObject(self.game_state.current_map_name, obj)
        else:
            # yes, use the current game state data
            obj.X = ref.X
            obj.Y = ref.Y
            obj.gfx = ref.gfx  
             
        if obj.trueAttr("NPC"):
            # create the agent
            obj.setup()
            # create the PlayerCharacter agent
            obj.start()
        if obj.trueAttr("AnimatedContainer"):
            # create the agent
            obj.setup()

    def objectActive(self, ident):
        """Given the objects ID, pass back the object if it is active,
           False if it doesn't exist or not displayed
           @type ident: string
           @param ident: ID of object
           @rtype: boolean
           @return: Status of result (True/False)"""
        for game_object in \
           self.game_state.getObjectsFromMap(self.game_state.current_map_name):
            if (game_object.ID == ident):
                # we found a match
                return game_object
        # no match
        return False    

    def movePlayer(self, position):
        """Code called when the player should move to another location
           @type position: fife.ScreenPoint
           @param position: Screen position to move to
           @return: None"""
        if(self.pc_run == 1):
            self.game_state.player_character.run(position)
        else:
            self.game_state.player_character.walk(position)
        
    def teleportAgent(self, agent, position):
        """Code called when an agent should teleport to another location
           @type position: fife.ScreenPoint
           @param position: Screen position to teleport to
           @return: None"""
        agent.teleport(position)
        self.agents[agent.ID]["Position"] = position

    def readObjectDB(self):
        """Reads the Object Information Database from a file. """
        database_file = file(self.object_db_file, "r")
        database = yaml.load_all(database_file)
        for object_info in database:
            self.object_db.update(object_info)

    def getAgentImportFiles(self):
        """Searches the agents directory for import files """
        files = locateFiles("*.xml", self.agents_directory)
        for xml_file in files:
            xml_file = os.path.relpath(xml_file).replace("\\", "/")
            try:
                root = ElementTree.parse(xml_file).getroot()
                if root.tag == "object":
                    self.agent_import_files[root.attrib["id"]] = xml_file
            except SyntaxError as error:
                assert(isinstance(error, SyntaxError))
                print "Error parsing file " + xml_file + ": " + error.msg
                #TODO: We may want to make this an fatal error later.
    
    def getDialogues(self):
        """Searches the dialogue directory for dialogues """
        files = locateFiles("*.yaml", self.dialogues_directory)
        dialogue_parser = YamlDialogueParser()
        for dialogue_filepath in files:
            dialogue_filepath = os.path.relpath(dialogue_filepath) \
                                .replace("\\", "/")
            # Note Technomage 2010-11-13: the new DialogueEngine uses its own
            #     parser now, YamlDialogueParser.
#            dialogues = yaml.load_all(file(dialogue_file, "r"))
            with file(dialogue_filepath, 'r') as dialogue_file:
                try:
                    dialogue = dialogue_parser.load(dialogue_file)
                except (DialogueFormatError,) as error:
                    logging.error('unable to load dialogue file {0}: {1}'
                                  .format(dialogue_filepath, error))
                else:
                    self.dialogues[dialogue.npc_name] = dialogue
            # Note Technomage 2010-11-13: the below code is used to load
            #     multiple dialogues from a single file. Is this functionality
            #     used/necessary?
#            for dialogue in dialogues:
#                self.dialogues[dialogue["NPC"]] = dialogue
