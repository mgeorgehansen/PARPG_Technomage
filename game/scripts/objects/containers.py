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

"""Containes classes defining concrete container game objects like crates,
   barrels, chests, etc."""

__all__ = ["WoodenCrate", "Footlocker"]

_AGENT_STATE_NONE, _AGENT_STATE_OPENED, _AGENT_STATE_CLOSED, \
_AGENT_STATE_OPENING, _AGENT_STATE_CLOSING = xrange(5)

from composed import ImmovableContainer
from fife import fife

class WoodenCrate (ImmovableContainer):
    def __init__(self, object_id, name = 'Wooden Crate',
                 text = 'A battered crate', gfx = 'crate', **kwargs):
        ImmovableContainer.__init__(self, ID = object_id, name = name, 
                                    gfx = gfx, text = text, **kwargs)
        
class ContainerBehaviour(fife.InstanceActionListener):
    def __init__(self, parent = None, agent_layer = None):
        fife.InstanceActionListener.__init__(self)
        self.parent = parent
        self.layer = agent_layer
        self.state = _AGENT_STATE_CLOSED
        self.agent = None

    def attachToLayer(self, agent_id):
        """ Attaches to a certain layer
            @type agent_id: String
            @param agent_id: ID of the layer to attach to.
            @return: None"""
        self.agent = self.layer.getInstance(agent_id)
        self.agent.addActionListener(self)
        self.state = _AGENT_STATE_CLOSED
        self.agent.act('closed', self.agent.getLocation())
        
    def onInstanceActionFinished(self, instance, action):
        """What the Actor does when it has finished an action.
           Called by the engine and required for InstanceActionListeners.
           @type instance: fife.Instance
           @param instance: self.agent (the Actor listener is listening for this
            instance)
           @type action: ???
           @param action: ???
           @return: None"""
        if self.state == _AGENT_STATE_OPENING:
            self.agent.act('opened', self.agent.getFacingLocation(), True)
            self.state = _AGENT_STATE_OPENED
        if self.state == _AGENT_STATE_CLOSING:
            self.agent.act('closed', self.agent.getFacingLocation(), True)
            self.state = _AGENT_STATE_CLOSED
        
    def open (self):
        if self.state != _AGENT_STATE_OPENED and self.state != \
                                                _AGENT_STATE_OPENING:
            self.agent.act('open', self.agent.getLocation())
            self.state = _AGENT_STATE_OPENING

    def close(self):
        if self.state != _AGENT_STATE_CLOSED and self.state != \
                                                _AGENT_STATE_CLOSING:
            self.agent.act('close', self.agent.getLocation())
            self.state = _AGENT_STATE_CLOSING  
    
class Footlocker(ImmovableContainer):
    def __init__ (self, object_id, agent_layer=None, name = 'Footlocker',
                  text = 'A Footlocker', gfx = 'lock_box_metal01', **kwargs):
        ImmovableContainer.__init__(self, ID = object_id, name = name, 
                                    gfx = gfx, text = text, **kwargs)
        self.behaviour = None

        self.attributes.append("AnimatedContainer")
        self.createBehaviour(agent_layer)        
        
    def prepareStateForSaving(self, state):
        """Prepares state for saving
        @type state: dictionary
        @param state: State of the object  
        """
        ImmovableContainer.prepareStateForSaving(self, state)
        del state["behaviour"]
    
    def createBehaviour(self, layer):
        self.behaviour = ContainerBehaviour(self, layer)

    def setup(self):
        """@return: None"""
        self.behaviour.attachToLayer(self.ID)

    def open (self):
        super (Footlocker, self).open()
        self.behaviour.open()

    def close(self):
        super (Footlocker, self).close()
        self.behaviour.close()
