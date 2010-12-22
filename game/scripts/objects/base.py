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

"""Containes classes defining the base properties of all interactable in-game 
   objects (such as Carryable, Openable, etc. These are generally independent 
   classes, which can be combined in almost any way and order. 

   Some rules that should be followed when CREATING base property classes:
   
   1. If you want to support some custom initialization arguments, 
      always define them as keyword ones. Only GameObject would use 
      positional arguments.
   2. In __init__() **ALWAYS** call the parent's __init__(**kwargs), preferably 
      *at the end* of your __init__() (makes it easier to follow)
   3. There should always be an attributes.append(x) call on __init__ 
      (where X is the name of the class)

   EXAMPLE:

   class Openable(object):
       def __init__ (self, is_open = True, **kwargs):
           self.attribbutes.append("openable")
           self.is_open = is_open
           super(Openable,self).__init__ (**kwargs)
        

   Some rules are to be followed when USING the base classes to make composed 
   ones:

   1. The first parent should always be the base GameObject class
   2. Base classes other than GameObject can be inherited in any order
   3. The __init__ functoin of the composed class should always invoke the
      parent's __init__() *before* it starts customizing any variables.

   EXAMPLE:

   class TinCan (GameObject, Container, Scriptable, Destructable, Carryable):
       def __init__ (self, *args, **kwargs):
           super(TinCan,self).__init__ (*args, **kwargs)
           self.name = 'Tin Can'"""
         
class BaseObject(object):
    """A base class that supports dynamic attributes functionality"""
    def __init__ (self):
        if not self.__dict__.has_key("attributes"):
            self.attributes = []
    
    def trueAttr(self, attr):
        """Method that checks if the instance has an attribute"""
        return attr in self.attributes

    def getStateForSaving(self):
        """Returns state for saving
        """
        state = {}
        state["attributes"] = self.attributes
        return state

class DynamicObject (BaseObject):
    """Class with basic attributes"""
    def __init__ (self, name="Dynamic object", real_name=None, image=None, **kwargs):
        """Initialise minimalistic set of data
           @type name: String
           @param name: Object display name
           @type image: String or None
           @param name: Filename of image to use in inventory"""
        BaseObject.__init__(self)
        self.name = name
        self.real_name = real_name or name
        self.image = image

    def prepareStateForSaving(self, state):
        """Prepares state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        pass
    
    def restoreState(self, state):
        """Restores a state from a saved state
        @type state: dictionary
        @param state: Saved state  
        """
        self.__dict__.update(state)

    def __getstate__(self):
        odict = self.__dict__.copy()
        self.prepareStateForSaving(odict)
        return odict
    
    def __setstate__(self, state):
        self.restoreState(state)
    
    def getStateForSaving(self):
        """Returns state for saving
        """
        state = BaseObject.getStateForSaving(self)
        state["Name"] = self.name
        state["RealName"] = self.real_name
        state["Image"] = self.image
        return state

class GameObject (DynamicObject):
    """A base class to be inherited by all game objects. This must be the
       first class (left to right) inherited by any game object."""
    def __init__ (self, ID, gfx = None, xpos = 0.0, ypos = 0.0, map_id = None, 
                  blocking=True, name="Generic object", real_name="Generic object", text="Item description",
                  desc="Detailed description", **kwargs):
        """Set the basic values that are shared by all game objects.
           @type ID: String
           @param ID: Unique object identifier. Must be present.
           @type gfx: Dictionary
           @param gfx: Dictionary with graphics for the different contexts       
           @type coords 2-item tuple
           @param coords: Initial coordinates of the object.
           @type map_id: String
           @param map_id: Identifier of the map where the object is located
           @type blocking: Boolean
           @param blocking: Whether the object blocks character movement
           @type name: String
           @param name: The display name of this object (e.g. 'Dirty crate')
           @type text: String
           @param text: A longer description of the item
           @type desc: String
           @param desc: A long description of the item that is displayed when it is examined
           """
        DynamicObject.__init__(self, name, real_name, **kwargs)
        self.ID = ID
        self.gfx = gfx or {}
        self.X = xpos
        self.Y = ypos
        self.map_id = map_id
        self.blocking = True
        self.text = text
        self.desc = desc
        
    def _getCoords(self):
        """Get-er property function"""
        return (self.X, self.Y)
    
    def _setCoords(self, coords):
        """Set-er property function"""
        self.X, self.Y = float(coords[0]), float (coords[1])
        
    coords = property (_getCoords, _setCoords, 
        doc = "Property allowing you to get and set the object's \
                coordinates via tuples")
    
    def __repr__(self):
        """A debugging string representation of the object"""
        return "<%s:%s>" % (self.name, self.ID)

    def getStateForSaving(self):
        """Returns state for saving
        """
        state = super(GameObject, self).getStateForSaving()
        state["ObjectModel"] = self.gfx
        state["Text"] = self.text
        state["Desc"] = self.desc
        state["Position"] = list(self.coords)
        return state


class Scriptable (BaseObject):
    """Allows objects to have predefined scripts executed on certain events"""
    def __init__ (self, scripts = None, **kwargs):
        """Init operation for scriptable objects
           @type scripts: Dictionary
           @param scripts: Dictionary where the event strings are keys. The 
           values are 3-item tuples (function, positional_args, keyword_args)"""
        BaseObject.__init__(self)
        self.attributes.append("scriptable")
        self.scripts = scripts or {}
        
    def runScript (self, event):
        """Runs the script for the given event"""
        if event in self.scripts and self.scripts[event]:
            func, args, kwargs = self.scripts[event]
            func (*args, **kwargs)
            
    def setScript (self, event, func, args = None , kwargs = None):
        """Sets a script to be executed for the given event."""
        args = args or {}
        kwargs = kwargs or {}
        self.scripts[event] = (func, args, kwargs)

class Openable(DynamicObject, Scriptable):
    """Adds open() and .close() capabilities to game objects
       The current state is tracked by the .is_open variable"""
    def __init__(self, is_open = True, **kwargs):
        """Init operation for openable objects
           @type is_open: Boolean
           @param is_open: Keyword boolean argument sets the initial state."""
        DynamicObject.__init__(self, **kwargs)
        Scriptable.__init__(self, **kwargs)
        self.attributes.append("openable")
        self.is_open = is_open
    
    def open(self):
        """Opens the object, and runs an 'onOpen' script, if present"""
        self.is_open = True
        try:
            if self.trueAttr ('scriptable'):
                self.runScript('onOpen')
        except AttributeError :
            pass
            
    def close(self):
        """Opens the object, and runs an 'onClose' script, if present"""
        self.is_open = False
        try:
            if self.trueAttr ('scriptable'):
                self.runScript('onClose')
        except AttributeError :
            pass
        
class Lockable (Openable):
    """Allows objects to be locked"""
    def __init__ (self, locked = False, is_open = True, **kwargs):
        """Init operation for lockable objects
           @type locked: Boolean
           @param locked: Keyword boolen argument sets the initial locked state.
           @type is_open: Boolean
           @param is_open: Keyword boolean argument sets the initial open state.
                           It is ignored if locked is True -- locked objects
                           are always closed."""
        self.attributes.append("lockable")
        self.locked = locked
        if locked :
            is_open = False
        Openable.__init__( self, is_open, **kwargs )
        
    def unlock (self):
        """Handles unlocking functionality"""
        self.locked = False      
        
    def lock (self):
        """Handles  locking functionality"""
        self.close()
        self.locked = True
        
    def open (self, *args, **kwargs):
        """Adds a check to see if the object is unlocked before running the
           .open() function of the parent class"""
        if self.locked:
            raise ValueError ("Open failed: object locked")
        super (Lockable, self).open(*args, **kwargs)
        
class Carryable (DynamicObject):
    """Allows objects to be stored in containers"""
    def __init__ (self, weight=0.0, bulk=0.0, **kwargs):
        DynamicObject.__init__(self, **kwargs)
        self.attributes.append("carryable")
        self.in_container = None
        self.on_map = None
        self.agent = None
        self.weight = weight
        self.bulk = bulk

    def getInventoryThumbnail(self):
        """Returns the inventory thumbnail of the object"""
        # TODO: Implement properly after the objects database is in place
        if self.image == None:
            return "gui/inv_images/inv_litem.png"
        else:
            return self.image
    
class Container (DynamicObject, Scriptable):
    """Gives objects the capability to hold other objects"""
    class TooBig(Exception):
        """Exception to be raised when the object is too big
        to fit into container"""
        pass
    
    class SlotBusy(Exception):
        """Exception to be raised when the requested slot is occupied"""
        pass
    
    class ItemSelf(Exception):
        """Exception to be raised when trying to add the container as an item"""
        pass
  
    def __init__ (self, capacity = 0, items = None, **kwargs):
        DynamicObject.__init__(self, **kwargs)
        Scriptable.__init__(self, **kwargs)
        self.attributes.append("container")
        self.items = {}
        self.capacity = capacity
        if items:
            for item in items:
                self.placeItem(item)
        
    def placeItem (self, item, index=None):
        """Adds the provided carryable item to the inventory. 
           Runs an 'onStoreItem' script, if present""" 
        if item is self:
            raise self.ItemSelf("Paradox: Can't contain myself")    
        if not item.trueAttr ('carryable'):
            raise TypeError ('%s is not carryable!' % item)
        if self.capacity and self.getContentsBulk()+item.bulk > self.capacity:
            raise self.TooBig ('%s is too big to fit into %s' % (item, self))
        item.in_container = self
        if index == None:
            self._placeAtVacant(item)
        else:
            if index in self.items :
                raise self.SlotBusy('Slot %d is busy in %s' % (index, 
                                                               self.name))
            self.items[index] = item

        # Run any scripts associated with storing an item in the container
        try:
            if self.trueAttr ('scriptable'):
                self.runScript('onPlaceItem')
        except AttributeError :
            pass

    def _placeAtVacant(self, item):
        """Places an item at a vacant slot"""
        vacant = None
        for i in range(len(self.items)):
            if i not in self.items :
                vacant = i
        if vacant == None :
            vacant = len(self.items)
        self.items[vacant] = item
    
    def takeItem (self, item):
        """Takes the listed item out of the inventory. 
           Runs an 'onTakeItem' script"""        
        if not item in self.items.values():
            raise ValueError ('I do not contain this item: %s' % item)
        del self.items[self.items.keys()[self.items.values().index(item)]]

        # Run any scripts associated with popping an item out of the container
        try:
            if self.trueAttr ('scriptable'):
                self.runScript('onTakeItem')
        except AttributeError :
            pass
    
    def replaceItem(self, old_item, new_item):
        """Replaces the old item with the new one
        @param old_item: Old item which is removed
        @type old_item: Carryable
        @param new_item: New item which is added
        @type new_item: Carryable
        """
        old_index = self.indexOf(old_item.ID)
        self.removeItem(old_item)
        self.placeItem(new_item, old_index)
        
    def removeItem(self, item):
        """Removes an item from the container, basically the same as 'takeItem'
        but does run a different script. This should be used when an item is
        destroyed rather than moved out.
        Runs 'onRemoveItem' script
        """
        if not item in self.items.values():
            raise ValueError ('I do not contain this item: %s' % item)
        del self.items[self.items.keys()[self.items.values().index(item)]]

        # Run any scripts associated with popping an item out of the container
        try:
            if self.trueAttr ('scriptable'):
                self.runScript('onRemoveItem')
        except AttributeError :
            pass

    def count (self, item_type = ""):
        """Returns the number of items"""
        if item_type:
            ret_count = 0
            for index in self.items :
                if self.items[index].item_type == item_type:
                    ret_count += 1
            return ret_count
        return len(self.items)   
    
    def getContentsBulk(self):
        """Bulk of the container contents"""
        return sum((item.bulk for item in self.items.values()))

    def getItemAt(self, index):
        return self.items[index]
    
    def indexOf(self, ID):
        """Returns the index of the item with the passed ID"""
        for index in self.items :
            if self.items[index].ID == ID:
                return index
        return None

    def findItemByID(self, ID):
        """Returns the item with the passed ID"""
        for i in self.items :
            if self.items[i].ID == ID:
                return self.items[i]
        return None

    def findItemByItemType(self, item_type):
        """Returns the item with the passed item_type"""
        for index in self.items :
            if self.items[index].item_type == item_type:
                return self.items[index]
        return None

    def findItem(self, **kwargs):
        """Find an item in container by attributes. All params are optional.
           @type name: String
           @param name: If the name is non-unique, return first matching object
           @type kind: String
           @param kind: One of the possible object types
           @return: The item matching criteria or None if none was found"""
        for index in self.items :
            if "name" in kwargs and self.items[index].name != kwargs["name"]:
                continue
            if "ID" in kwargs and self.items[index].ID != kwargs["ID"]:
                continue
            if "kind" in kwargs and not self.items[index].trueAttr(kwargs["kind"]):
                continue
            if "item_type" in kwargs and self.items[index].item_type != kwargs["item_type"]:
                continue
            return self.items[index]
        return None    
    
    def serializeItems(self):
        """Returns the items as a list"""
        items = []
        for index, item in self.items.iteritems():
            item_dict = item.getStateForSaving()
            item_dict["index"] = index
            item_dict["type"] = item.item_type
            items.append(item_dict)
        return items
    
    def getStateForSaving(self):
        """Returns state for saving
        """
        ret_state = DynamicObject.getStateForSaving(self)
        ret_state["Items"] = self.serializeItems()
        return ret_state
        
class Living (BaseObject):
    """Objects that 'live'"""
    def __init__ (self, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("living")
        self.lives = True

    def die(self):
        """Kills the object"""
        self.lives = False   

class CharStats (BaseObject):
    """Provides the object with character statistics"""
    def __init__ (self, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("charstats")
        
class Wearable (BaseObject):
    """Objects than can be weared"""
    def __init__ (self, slots, **kwargs):
        """Allows the object to be worn somewhere on the body (e.g. pants)"""
        BaseObject.__init__(self)
        self.attributes.append("wearable")
        if isinstance(slots, tuple) :
            self.slots = slots
        else :
            self.slots = (slots,)
    
class Usable (BaseObject):
    """Allows the object to be used in some way (e.g. a Zippo lighter 
       to make a fire)"""
    def __init__ (self, actions = None, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("usable")
        self.actions = actions or {}   
        
class Weapon (BaseObject):
    """Allows the object to be used as a weapon"""
    def __init__ (self, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("weapon")
        
class Destructable (BaseObject):
    """Allows the object to be destroyed"""
    def __init__ (self, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("destructable")
        
class Trapable (BaseObject):
    """Provides trap slots to the object"""
    def __init__ (self, **kwargs):
        BaseObject.__init__(self)
        self.attributes.append("trapable")
