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

from random import randrange


from fife import fife

from base import GameObject, Living, Scriptable, CharStats
from composed import CarryableItem
from scripts.inventory import Inventory
from scripts.common.utils import loadSettings

"""All actors go here. Concrete classes only."""

__all__ = ["PlayerCharacter", "NonPlayerCharacter",]

Settings = loadSettings()

_AGENT_STATE_NONE, _AGENT_STATE_IDLE, _AGENT_STATE_APPROACH, _AGENT_STATE_RUN, _AGENT_STATE_WANDER, _AGENT_STATE_TALK = xrange(6)

class ActorBehaviour (fife.InstanceActionListener):
    """Fife agent listener"""
    def __init__(self, layer):
        fife.InstanceActionListener.__init__(self)
        self.layer = layer
        self.agent = None
        self.state = None
        self.speed = 0
        self.idle_counter = 1
    
    def attachToLayer(self, agent_ID):
        """Attaches to a certain layer
           @type agent_ID: String
           @param agent_ID: ID of the layer to attach to.
           @return: None"""
        self.agent = self.layer.getInstance(agent_ID)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_NONE
        # TODO: rework/improve
        self.speed = Settings.get("PARPG", "PCSpeed")-1
        
    def getX(self):
        """Get the NPC's x position on the map.
           @rtype: integer"
           @return: the x coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().x

    def getY(self):
        """Get the NPC's y position on the map.
           @rtype: integer
           @return: the y coordinate of the NPC's location"""
        return self.agent.getLocation().getLayerCoordinates().y
        
    def onNewMap(self, layer):
        """Sets the agent onto the new layer."""
        if self.agent is not None:
            self.agent.removeActionListener(self)
            
        self.agent = layer.getInstance(self.parent.ID)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_NONE
        self.idle_counter = 1
    
    def idle(self):
        """@return: None"""
        self.state = _AGENT_STATE_IDLE
        self.agent.act('stand', self.agent.getFacingLocation())

    def onInstanceActionFinished(self, instance, action):
        pass

class PCBehaviour (ActorBehaviour):
    def __init__(self, parent = None, layer = None):
        super(PCBehaviour, self).__init__(layer)        
        self.parent = parent
        self.idle_counter = 1
        # TODO: rework/improve
        self.speed = Settings.get("PARPG", "PCSpeed")
        self.nextAction = None
        self.agent = None
        
    def onInstanceActionFinished(self, instance, action):
        """@type instance: ???
           @param instance: ???
           @type action: ???
           @param action: ???
           @return: None"""
        # First we reset the next behavior 
        act = self.nextAction
        self.nextAction = None 
        self.idle()
        
        if act:
            act.execute()
            
        if(action.getId() != 'stand'):
            self.idle_counter = 1
        else:
            self.idle_counter += 1            


class NPCBehaviour(ActorBehaviour):
    def __init__(self, Parent = None, Layer = None):
        super(NPCBehaviour, self).__init__(Layer)
        
        self.parent = Parent
        self.state = _AGENT_STATE_NONE
        self.pc = None
        self.target_loc = None
        self.nextAction = None
        
        # hard code these for now
        self.distRange = (2, 4)
        # these are parameters to lower the rate of wandering
        # wander rate is the number of "IDLEs" before a wander step
        # this could be set for individual NPCs at load time
        # or thrown out altogether.
        self.wanderCounter = 0
        self.wanderRate = 9
        
    def getTargetLocation(self):
        """@rtype: fife.Location
           @return: NPC's position"""
        x = self.getX()
        y = self.getY()
        if self.state == _AGENT_STATE_WANDER:
            """ Random Target Location """
            l = [0, 0]
            for i in range(len(l)):
                sign = randrange(0, 2)
                dist = randrange(self.distRange[0], self.distRange[1])
                if sign == 0:
                    dist *= -1
                l[i] = dist
            x += l[0]
            y += l[1]
            # Random walk is
            # rl = randint(-1, 1);ud = randint(-1, 1);x += rl;y += ud
        l = fife.Location(self.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(x, y))
        return l

    def onInstanceActionFinished(self, instance, action):
        """What the NPC does when it has finished an action.
           Called by the engine and required for InstanceActionListeners.
           @type instance: fife.Instance
           @param instance: self.agent (the NPC listener is listening for this
                                        instance)
           @type action: ???
           @param action: ???
           @return: None"""
        if self.state == _AGENT_STATE_WANDER:
            self.target_loc = self.getTargetLocation()
        self.idle()
        
    
    def idle(self):
        """Controls the NPC when it is idling. Different actions
           based on the NPC's state.
           @return: None"""
        if self.state == _AGENT_STATE_NONE:
            self.state = _AGENT_STATE_IDLE
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_IDLE:
            if self.wanderCounter > self.wanderRate:
                self.wanderCounter = 0
                self.state = _AGENT_STATE_WANDER
            else:
                self.wanderCounter += 1
                self.state = _AGENT_STATE_NONE
            
            self.target_loc = self.getTargetLocation()
            self.agent.act('stand', self.agent.getFacingLocation())
        elif self.state == _AGENT_STATE_WANDER:
            self.parent.wander(self.target_loc)
            self.state = _AGENT_STATE_NONE
        elif self.state == _AGENT_STATE_TALK:
            self.agent.act('stand', self.pc.getLocation())
            
class CharacterBase(GameObject, Living, CharStats):
    """Base class for Characters"""
    def __init__(self, ID, agent_layer = None, inventory = None, 
                 text = "", **kwargs):
        GameObject.__init__( self, ID, text = text, **kwargs )
        Living.__init__( self, **kwargs )
        CharStats.__init__( self, **kwargs )
        
        self.behaviour = None
        
        if inventory == None:
            self.inventory = Inventory()
        else:
            self.inventory = inventory

        self.state = _AGENT_STATE_NONE
        self.layer_id = agent_layer.getId()
        self.createBehaviour(agent_layer)
    
    def createBehaviour(self, layer):
        """Creates the behaviour for this actor.
           @return: None"""
        pass
    
    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.ID)

    def start(self):
        """@return: None"""
        self.behaviour.idle()

    def teleport(self, location):
        """Teleports a Character instantly to the given location.
           @type location: fife.Location
           @param location: Target coordinates for Character.
           @return: None"""
        self.state = _AGENT_STATE_IDLE
        self.behaviour.nextAction = None 
        self.behaviour.agent.setLocation(location)

    def give (self, item, actor):
        """Gives the specified item to the different actor. Raises an exception if the item was invalid or not found
           @type item: Carryable
           @param item: The item object to give
           @param actor: Person to give item to"""
        if item == None: 
            raise ValueError("I don't have %s" % item.name)
        self.inventory.takeItem(item)
        actor.inventory.placeItem(item)           
        
    def hasItem(self, item_type):
        """Returns wether an item is present in the players inventory or not
        @param item_type: ID of the item
        @type item_type: str
        @return: True when the item is present, False when not"""
        return self.inventory.findItem(item_type = item_type)

    def itemCount(self, item_type = ""):
        """Returns number of all items or items specified by item_type 
        the player has.
        @param item_type: ID of the item, can be empty
        @type item_type: str
        @return: Number of items"""
        return self.inventory.count(item_type)

    def getLocation(self):
        """Get the NPC's position as a fife.Location object. Basically a
           wrapper.
           @rtype: fife.Location
           @return: the location of the NPC"""
        return self.behaviour.agent.getLocation()
    
    def run(self, location):
        """Makes the PC run to a certain location
           @type location: fife.ScreenPoint
           @param location: Screen position to run to.
           @return: None"""
        self.state = _AGENT_STATE_RUN
        self.behaviour.nextAction = None
        self.behaviour.agent.move('run', location, self.behaviour.speed+1)

    def walk(self, location):
        """Makes the PC walk to a certain location.
           @type location: fife.ScreenPoint
           @param location: Screen position to walk to.
           @return: None"""
        self.state = _AGENT_STATE_RUN
        self.behaviour.nextAction = None 
        self.behaviour.agent.move('walk', location, self.behaviour.speed-1)

    def getStateForSaving(self):
        """Returns state for saving
        """
        ret_dict = GameObject.getStateForSaving(self)
        ret_dict["Inventory"] = self.inventory.serializeInventory()
        return ret_dict

    def _getCoords(self):
        """Get-er property function"""
        return (self.getLocation().getMapCoordinates().x, 
                self.getLocation().getMapCoordinates().y)
    
    def _setCoords(self, coords):
        """Set-er property function"""
        map_coords = self.getLocation().getMapCoordinates()
        map_coords.X, map_coords.Y = float(coords[0]), float (coords[1])
        self.teleport(map_coords)
    
    coords = property (_getCoords, _setCoords, 
        doc = "Property allowing you to get and set the object's \
                coordinates via tuples")
           
class PlayerCharacter (CharacterBase):
    """PC class"""
    def __init__ (self, ID, agent_layer = None, inventory = None, 
                  text = "Its you. Who would've thought that?", **kwargs):
        if inventory == None:
            inventory = Inventory()
            inventory.placeItem(CarryableItem(ID=456, name="Dagger123"))
            inventory.placeItem(CarryableItem(ID=555, name="Beer"))
            inventory.placeItem(CarryableItem(ID = 616,
                                    name = "Pamphlet",
                                    image = "/gui/inv_images/inv_pamphlet.png"))
        CharacterBase.__init__(self, ID, agent_layer, inventory, text, **kwargs)
        self.people_i_know = set()
        self.attributes.append("PC")
  
    def getStateForSaving(self):
        """Returns state for saving
        """
        ret_dict = super(PlayerCharacter, self).getStateForSaving()
        ret_dict["PeopleKnown"] = self.people_i_know
        return ret_dict
    
    def meet(self, npc):
        """Record that the PC has met a certain NPC
           @type npc: str
           @param npc: The NPC's name or id"""
        if npc in self.people_i_know:
            # we could raise an error here, but should probably be a warn
            # raise RuntimeError("I already know %s" % npc)
            return
        self.people_i_know.add(npc)

    def met(self, npc):
        """Indicate whether the PC has met this npc before
           @type npc: str
           @param npc: The NPC's name or id
           @return: None"""
        return npc in self.people_i_know

    def createBehaviour(self, layer):
        """Creates the behaviour for this actor.
           @return: None"""
        self.behaviour = PCBehaviour(self, layer)
 
    def approach(self, location, action = None):
        """Approaches a location and then perform an action (if set).
           @type loc: fife.Location
           @param loc: the location to approach
           @type action: Action
           @param action: The action to schedule for execution after the approach.
           @return: None"""
        self.state = _AGENT_STATE_APPROACH
        self.behaviour.nextAction = action
        boxLocation = tuple([int(float(i)) for i in location])
        l = fife.Location(self.behaviour.agent.getLocation())
        l.setLayerCoordinates(fife.ModelCoordinate(*boxLocation))
        self.behaviour.agent.move('run', l, self.behaviour.speed+1)
    
class NonPlayerCharacter(CharacterBase, Scriptable):
    """NPC class"""
    def __init__(self, ID, agent_layer=None, name='NPC', \
                 text = 'A nonplayer character', inventory = None, 
                 real_name = 'NPC', dialogue = None, **kwargs):
        # init game object
        CharacterBase.__init__(self, ID, agent_layer = agent_layer, 
                               inventory = inventory, name=name, 
                               real_name=real_name, text = text, **kwargs)
        Scriptable.__init__(self, **kwargs)

        self.attributes.append("NPC")
        self.dialogue = dialogue

    def prepareStateForSaving(self, state):
        """Prepares state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        CharacterBase.prepareStateForSaving(self, state)
        del state["behaviour"]

    def getStateForSaving(self):
        """Returns state for saving
        """
        ret_dict = CharacterBase.getStateForSaving(self)
        ret_dict["Lives"] = self.lives
        ret_dict["State"] = self.behaviour.state
        return ret_dict

    def createBehaviour(self, layer):
        """Creates the behaviour for this actor.
           @return None """
        self.behaviour = NPCBehaviour(self, layer)

    def wander(self, location):
        """Nice slow movement for random walking.
           @type location: fife.Location
           @param location: Where the NPC will walk to.
           @return: None"""
        self.behaviour.agent.move('walk', location, self.behaviour.speed-1)

    def talk(self, pc):
        """Makes the NPC ready to talk to the PC
           @return: None"""
        self.behaviour.state = _AGENT_STATE_TALK
        self.behaviour.pc = pc.behaviour.agent
        self.behaviour.idle()