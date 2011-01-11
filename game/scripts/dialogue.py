#!/usr/bin/env python
#
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
"""
Provides classes used to contain and organize dialogue data for use within
in-game dialogues between the player character and NPCs.
"""
try:
    from collections import OrderedDict
except ImportError:
    # Python version 2.4-2.6 doesn't have the OrderedDict
    from scripts.common.ordereddict import OrderedDict

from scripts.common.pythonserializable import PythonSerializable

class Dialogue(PythonSerializable):
    """
    Represents a complete dialogue and acts as a container for the dialogue
    data belonging to a particular NPC.
    """
    __slots__ = ['npc_name', 'avatar_path', 'default_greeting',
                 'greetings', 'sections']
    
    def __init__(self, npc_name, avatar_path, default_greeting, greetings=None,
                 sections=None):
        """
        Initialize a new L{Dialogue} instance.
        
        @param npc_name: name displayed for the NPC in the dialogue.
        @type npc_name: basestring
        @param avatar_path: path to the image that should be displayed as the
            NPC's avatar.
        @type avatar_path: basestring
        @param default_greeting: section of dialogue that should be
            displayed when the dialogue is first initiated and no other start
            sections are available.
        @type default_greeting: L{DialogueSection}
        @param greetings: sections of dialogue defining the conditions
            under which each should be displayed when the dialogue is first
            initiated.
        @type greetings: list of 
            L{RootDialogueSections<DialogueGreeting>}
        @param sections: sections of dialogue that make up this
            L{Dialogue} instance.
        @type sections: list of L{DialogueSections<DialogueSection>}
        """
        PythonSerializable.__init__(self, npc_name, avatar_path,
                                    default_greeting, greetings=greetings,
                                    sections=sections)
        self.npc_name = npc_name
        self.avatar_path = avatar_path
        self.default_greeting = default_greeting
        self.greetings = greetings
        self.sections = OrderedDict()
        all_sections = sections + [default_greeting] + greetings
        if (__debug__):
            section_ids = [section.id for section in all_sections]
        for section in all_sections:
            # Sanity check: All DialogueResponses should have next_section_id
            # attributes that refer to valid DialogueSections in the Dialogue.
            if (__debug__):
                for response in section.responses:
                    assert response.next_section_id in section_ids + \
                        ['end', 'back'], ('"{0}" does not refer to a ' 
                                          'DialogueSection in this Dialogue')\
                        .format(response.next_section_id)
            self.sections[section.id] = section
    
    def __str__(self):
        """Return the string representation of the L{Dialogue} instance."""
        string_representation = 'Dialogue(npc_id={0.npc_name})'.format(self)
        return string_representation


class DialogueNode(object):
    """
    Abstract base class that represents a node or related group of attributes
    within a Dialogue.
    """
    def __init__(self, text, actions=None):
        """
        Initialize a new L{DialogueNode} instance.
        
        @param text: textual content of the L{DialogueNode}.
        @type text: basestring
        @param actions: dialogue actions associated with the L{DialogueNode}.
        @type actions: list of L{DialogueActions<DialogueAction>}
        """
        self.text = text
        self.actions = actions or []


class DialogueSection(DialogueNode, PythonSerializable):
    """DialogueNode that represents a distinct section of the dialogue."""
    __slots__ = ['id', 'text', 'responses', 'actions']
    
    def __init__(self, id_, text, responses=None, actions=None):
        """
        Initialize a new L{DialogueSection} instance.
        
        @param id_: named used to uniquely identify the L{DialogueSection}
            within a L{Dialogue}.
        @type id_: basestring
        @param text: text displayed as the NPC's part of the L{Dialogue}.
        @type text: basestring
        @param responses: possible responses that the player can choose from.
        @type responses: list of L{DialogueResponses<DialogueResponse>}
        @param actions: dialogue actions that should be executed when the
            L{DialogueSection} is reached.
        @type actions: list of L{DialogueActions<DialogueAction>}
        """
        DialogueNode.__init__(self, text=text, actions=actions)
        PythonSerializable.__init__(self, id_, text, responses=responses,
                                    actions=actions)
        self.id = id_
        if (responses is not None):
            self.responses = list(responses)


class DialogueGreeting(DialogueNode, PythonSerializable):
    """
    Represents a root section of dialogue in a L{Dialogue} along with the
    conditional statement used to determine the whether this section should be
    displayed first upon dialogue initiation.
    
    @ivar id: Name used to uniquely identify the L{DialogueSection} to which
        the L{DialogueRootSectionReference} points.
    @type id: basestring
    @ivar condition: Boolean Python expression used to determine if the
        L{DialogueSection} referenced is a valid starting section.
    @type condition: basestring
    """
    __slots__ = ['id', 'text',  'condition', 'actions', 'responses']
    
    def __init__(self, id_, condition, text, responses=None, actions=None):
        """
        Initialize a new L{DialogueGreeting} instance.
        
        @param id_: named used to uniquely identify the L{DialogueSection}
            within a L{Dialogue}.
        @type id_: basestring
        @param condition: Boolean Python expression used to determine if this
            root dialogue section should be displayed.
        @type condition: basestring
        @param text: text displayed as the NPC's part of the L{Dialogue}.
        @type text: basestring
        @param responses: possible responses that the player can choose from.
        @type responses: list of L{DialogueResponses<DialogueResponse>}
        @param actions: dialogue actions that should be executed when the
            L{DialogueSection} is reached.
        @type actions: list of L{DialogueActions<DialogueAction>}
        """
        DialogueNode.__init__(self, text=text, actions=actions)
        PythonSerializable.__init__(self, id_, text, condition=condition,
                                    responses=responses, actions=actions)
        self.id = id_
        self.condition = condition
        self.responses = responses


class DialogueResponse(DialogueNode, PythonSerializable):
    """
    L{DialogueNode} that represents one possible player response to a
    particular L{DialogueSection}.
    """
    __slots__ = ['text', 'condition', 'actions', 'next_section_id']
    
    def __init__(self, text, next_section_id, actions=None, condition=None):
        """
        Initialize a new L{DialogueResponse} instance.
        
        @param text: text displayed as the content of the player's response.
        @type text: basestring
        @param next_section_id: ID of the L{DialogueSection} that should be
            jumped to if this response is chosen by the player.
        @type next_section_id: basestring
        @param actions: dialogue actions that should be executed if this
            response is chosen by the player.
        @type actions: list of L{DialogueActions<DialogueAction>}
        @param condition: Python expression that when evaluated determines
            whether the L{DialogueResponse} should be displayed to the player
            as a valid response.
        @type condition: basestring
        """
        DialogueNode.__init__(self, text=text, actions=actions)
        PythonSerializable.__init__(self, text, next_section_id,
                                    condition=condition, actions=actions)
        self.condition = condition
        self.next_section_id = next_section_id
