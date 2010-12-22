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

"""Composite game object classes are kept here"""

from base import GameObject, Container, Lockable, \
                Scriptable, Trapable, Destructable, Carryable, \
                Usable

class ImmovableContainer(GameObject, Container, Lockable, Scriptable, 
                         Trapable, Destructable):
    """Composite class that can be used for crates, chests, etc."""
    def __init__ (self, **kwargs):
        GameObject   .__init__(self, **kwargs)
        Container    .__init__(self, **kwargs)
        Lockable     .__init__(self, **kwargs)
        Scriptable   .__init__(self, **kwargs)
        Trapable    .__init__(self, **kwargs)
        Destructable .__init__(self, **kwargs)
        self.blocking = True

class SingleItemContainer (Container) :
    """Container that can only store a single item.
       This class can represent single-item inventory slots"""
    def __init__ (self, **kwargs):
        Container.__init__(self, **kwargs)

    def placeItem(self,item, index=None):
        if len(self.items) > 0 :
            raise self.SlotBusy ('%s is already busy' % self)
        Container.placeItem(self, item)
    
class CarryableItem (GameObject, Carryable, Usable):
    """Composite class that will be used for all carryable items"""
    def __init__(self, item_type, **kwargs):
        GameObject.__init__(self, **kwargs)
        Carryable.__init__(self, **kwargs)
        Usable.__init__(self, **kwargs)
        self.item_type = item_type

    def prepareStateForSaving(self, state):
        """Prepares state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        super(CarryableItem, self).prepareStateForSaving(state)
        if state.has_key("in_container"):
            del state["in_container"]
        if state.has_key("on_map"):
            del state["on_map"]
        if state.has_key("agent"):
            del state["agent"]

    def getStateForSaving(self):
        """Returns state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        ret_dict = self.__dict__.copy()
        self.prepareStateForSaving(ret_dict)
        return ret_dict

class CarryableContainer(Container, CarryableItem):
    """Composite class that will be used for backpack, pouches, etc."""
    def __init__ (self, item_type, **kwargs):
        Container.__init__(self, **kwargs)
        CarryableItem.__init__(self, item_type, **kwargs)
        self.own_bulk = 0
        self.own_weight = 0

    def getWeight(self):
        """Resulting weight of a container"""
        return sum((item.weight for item in self.items.values()), 
                   self.own_weight)

    def setWeight(self, weight):
        """Set container's own weight. 
        For compatibility with inherited methods"""
        self.own_weight = weight

    weight = property(getWeight, setWeight, "Total weight of container")

    def getBulk(self):
        """Resulting bulk of container"""
        return self.getContentsBulk()+self.own_bulk

    def setBulk(self, bulk):
        """Set container's own bulk. For compatibility with inherited methods"""
        self.own_bulk = bulk

    bulk = property(getBulk, setBulk, "Total bulk of container")
    
    def __repr__(self):
        return "[%s" % self.name + str(reduce((lambda a, b: a + ', ' + \
                                    str(self.items[b])), self.items, "")) + " ]"

    def getStateForSaving(self):
        """Returns state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        state = Container.getStateForSaving(self)
        if not state.has_key("attributes"):
            state["attributes"] = []
        state["attributes"].append("Container")
        state.update(CarryableItem.getStateForSaving(self))
        return state

class CarryableSingleItemContainer (SingleItemContainer, CarryableContainer) :
    """Container that can only store a single item.
       This class can represent single-item inventory slots"""
    def __init__ (self, item_type, **kwargs):
        SingleItemContainer.__init__(self, **kwargs)
        CarryableContainer.__init__(self, item_type, **kwargs)
        
class Door(GameObject, Lockable, Scriptable, Trapable):
    """Composite class that can be used to create doors on a map."""
    def __init__ (self, target_map_name = 'my-map',
                  target_x = 0.0, target_y = 0.0, **kwargs):
        GameObject.__init__(self, **kwargs)
        Lockable.__init__(self, **kwargs)
        Scriptable.__init__(self, **kwargs)
        Trapable.__init__(self, **kwargs)
        self.attributes.append("door")
        self.target_map_name = target_map_name
        self.target_pos = (target_x, target_y)
        self.blocking = True

    def getStateForSaving(self):
        """Returns state for saving
        """
        ret_dict = super(Door, self).getStateForSaving()
        return ret_dict
