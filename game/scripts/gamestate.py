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

from scripts.quest_engine import QuestEngine

class GameState(object):
    """This class holds the current state of the game."""
    def __init__(self, quests_dir = None):
        self.player_character = None
        self.quest_engine = QuestEngine(quests_dir)
        self.quest_engine.readQuests()
        self.objects = {}
        self.object_ids = {}
        self.current_map_name = None
        self.maps = {}
        
        
    def addObject(self, map_id, game_object):
        """Adds an object to the objects and object_ids
        dictionaries.
        @param map_id: ID of the map the object is on. 
        If the object is in a container this has to be None
        @param object: object to be added
        @type object: GameObject
        @type map_id: str or None
        """
        object_id = game_object.ID
        if not self.object_ids.has_key(object_id):
            if map_id:
                self.objects[map_id][object_id] = game_object
            self.object_ids[object_id] = map_id
    
    def deleteObject(self, object_id):
        """Removes an object from the dictionaries
        @param object_id: ID of the object
        @type object_id: str
        """
        if self.hasObject(object_id):
            map_id = self.getMapOfObject(object_id)
            if map_id:
                inst = self.maps[map_id].agent_layer.getInstance(object_id)
                self.maps[map_id].agent_layer.deleteInstance(inst)
                del self.objects[map_id][object_id]
            del self.object_ids[object_id]
            
            
    def getObjectsFromMap(self, map_id):
        """Gets all objects that are currently on the given map.
           @type map: String
           @param map: The map name.
           @returns: The list of objects on this map. Or an empty list"""
        if map_id in self.objects:
            return [i for i in self.objects[map_id].values() \
                                        if map_id in self.objects]
        
        return {}
    
    def hasObject(self, object_id):
        """Check if an object with the given id is present 
        @param object_id: ID of the object
        @type object_id: str
        @return: True if there is an object False if not
        """
        return self.object_ids.has_key(object_id)
    
    def getMapOfObject(self, object_id):
        """Returns the map the object is on.
        @param object_id: ID of the object
        @type object_id: str
        @return: Name of the map the object is on. 
        If there is no such object or the object is in a container None is returned
        """
        if self.object_ids.has_key(object_id):
            return self.object_ids[object_id]
        return None
    
    def getObjectById(self, obj_id, map_id = None):
        """Gets an object by its object id and map id
           @type obj_id: String
           @param obj_id: The id of the object.
           @type map_id: String
           @param map_id: It id of the map containing the object.
           @returns: The object or None."""
        if not map_id:
            map_id = self.getMapOfObject(obj_id)
        if not map_id in self.objects:
            self.objects[map_id] = {}
        if obj_id in self.objects[map_id]:
            return self.objects[map_id][obj_id]
    
    def clearObjects(self):
        """Delete all objects from the state
        """
        self.objects = {}
        self.object_ids = {}
        
    def getStateForSaving(self):
        """Prepares state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        ret_dict = {}
        ret_dict["CurrentMap"] = self.current_map_name
        ret_dict["Quests"] = self.quest_engine.getStateForSaving()
        return ret_dict

    def restoreFromState(self, state):
        """Restores the state"""
        self.current_map_name = state["CurrentMap"]
        self.quest_engine.readQuests()
        self.quest_engine.restoreFromState(state["Quests"])
        
