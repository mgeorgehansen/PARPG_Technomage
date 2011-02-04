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
try:
    # Python 2.6
    import unittest2 as unittest
except:
    # Python 2.7
    import unittest

from scripts.common.utils import dedent_chomp
from scripts.dialogueprocessor import DialogueProcessor
# NOTE Technomage 2010-12-08: Using the dialogue data structures might be a
#    violation of unit test isolation, but ultimately they are just simple
#    data structures that don't require much testing of their own so I feel
#    that it isn't a mistake to use them.
from scripts.dialogue import (Dialogue, DialogueSection, DialogueResponse,
    DialogueGreeting)

class MockDialogueAction(object):
    keyword = 'mock_action'
    
    def __init__(self, *args, **kwargs):
        self.arguments = (args, kwargs)
        self.was_called = False
        self.call_arguments = []
    
    def __call__(self, game_state):
        self.was_called = True
        self.call_arguments = ((game_state,), {})


class TestDialogueProcessor(unittest.TestCase):
    """Base class for tests of the L{DialogueProcessor} class."""
    def assertStateEqual(self, object_, **state):
        """
        Assert that an object's attributes match an expected state.
        
        @param 
        """
        object_dict = {}
        for key in state.keys():
            if (hasattr(object_, key)):
                actual_value = getattr(object_, key)
                object_dict[key] = actual_value
        self.assertDictContainsSubset(state, object_dict)
    
    def setUp(self):
        self.npc_id = 'mr_npc'
        self.dialogue = Dialogue(
            npc_name='Mr. NPC',
            avatar_path='/some/path',
            default_greeting=DialogueSection(
                id_='greeting',
                text='This is the root dialogue section.',
                actions=[
                    MockDialogueAction('foo'),
                ],
                responses=[
                    DialogueResponse(
                        text='A response.',
                        next_section_id='another_section',
                    ),
                    DialogueResponse(
                        text='A conditional response evaluated to True.',
                        condition='True',
                        actions=[
                            MockDialogueAction('foo'),
                        ],
                        next_section_id='another_section',
                    ),
                    DialogueResponse(
                        text='A conditional response evaluated to False.',
                        condition='False',
                        next_section_id='another_section',
                    ),
                    DialogueResponse(
                        text='A response that ends the dialogue.',
                        next_section_id='end',
                    ),
                ],
            ),
            greetings=[
                DialogueGreeting(
                    id_='alternative_greeting',
                    condition='use_alternative_root is True',
                    text='This is an alternate root section.',
                    responses=[
                        DialogueResponse(
                            text='End dialogue.',
                            next_section_id='end',
                        ),
                    ],
                ),
            ],
            sections=[
                DialogueSection(
                    id_='another_section',
                    text='This is another dialogue section.',
                    responses=[
                        DialogueResponse(
                            text='End dialogue.',
                            next_section_id='end',
                        ),
                    ],
                ),
            ]
        )
        self.game_state = {'use_alternative_root': False}


class TestInitiateDialogue(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.initiateDialogue} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue = Dialogue(
            npc_name='Mr. NPC',
            avatar_path='/some/path',
            default_greeting=DialogueSection(
                id_='greeting',
                text='This is the one (and only) dialogue section.',
                responses=[
                    DialogueResponse(
                        text=dedent_chomp('''
                            A response that moves the dialogue to
                            another_section.
                        '''),
                        next_section_id='another_section'
                    ),
                    DialogueResponse(
                        text='A response that ends the dialogue.',
                        next_section_id='end',
                    ),
                ],
            ),
            sections=[
                DialogueSection(
                    id_='another_section',
                    text='This is another section.',
                    responses=[
                        DialogueResponse(
                            text='A response that ends the dialogue',
                            next_section_id='end',
                        )
                    ],
                ),
            ]
        )
        self.dialogue_processor = DialogueProcessor(self.dialogue, {})
    
    def testSetsState(self):
        """initiateDialogue correctly sets DialogueProcessor state"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.initiateDialogue()
        
        # Default root dialogue section should have been pushed onto the stack.
        default_greeting = self.dialogue.default_greeting
        self.assertStateEqual(dialogue_processor, in_dialogue=True,
                              dialogue=self.dialogue,
                              dialogue_section_stack=[default_greeting])
    
    def testEndsExistingDialogue(self):
        """initiateDialogue ends a previously initiated dialogue"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.initiateDialogue()
        valid_responses = dialogue_processor.continueDialogue()
        dialogue_processor.reply(valid_responses[0])
        
        # Sanity check.
        assert dialogue_processor.in_dialogue
        dialogue_processor.initiateDialogue()
        default_greeting = self.dialogue.default_greeting
        self.assertStateEqual(dialogue_processor, in_dialogue=True,
                              dialogue=self.dialogue,
                              dialogue_section_stack=[default_greeting])

class TestEndDialogue(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.endDialogue} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
    
    def testResetsState(self):
        """endDialogue correctly resets DialogueProcessor state"""
        dialogue_processor = self.dialogue_processor
        # Case: No dialogue initiated.
        assert not dialogue_processor.in_dialogue, \
            'assumption that dialogue_processor has not initiated a dialogue '\
            'violated'
        self.assertStateEqual(dialogue_processor, in_dialogue=False,
                              dialogue=self.dialogue,
                              dialogue_section_stack=[])
        # Case: Dialogue previously initiated.
        dialogue_processor.initiateDialogue()
        assert dialogue_processor.in_dialogue, \
            'assumption that dialogue_processor initiated a dialogue violated'
        dialogue_processor.endDialogue()
        self.assertStateEqual(dialogue_processor, in_dialogue=False,
                              dialogue=self.dialogue,
                              dialogue_section_stack=[])


class TestContinueDialogue(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.continueDialogue} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
        self.dialogue_processor.initiateDialogue()
        self.dialogue_action = \
            self.dialogue.default_greeting.actions[0]
    
    def testRunsDialogueActions(self):
        """continueDialogue executes all DialogueActions"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.continueDialogue()
        self.assertTrue(self.dialogue_action.was_called)
        expected_tuple = ((self.game_state,), {})
        self.assertTupleEqual(expected_tuple,
                              self.dialogue_action.call_arguments)
    
    def testReturnsValidResponses(self):
        """continueDialogue returns list of valid DialogueResponses"""
        dialogue_processor = self.dialogue_processor
        valid_responses = \
            dialogue_processor.dialogue_section_stack[0].responses
        valid_responses.pop(2)
        # Sanity check, all "valid" responses should have a condition that
        # evaluates to True.
        for response in valid_responses:
            if (response.condition is not None):
                result = eval(response.condition, self.game_state, {})
                self.assertTrue(result)
        responses = dialogue_processor.continueDialogue()
        self.assertItemsEqual(responses, valid_responses)


class TestGetRootDialogueSection(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.getDialogueGreeting} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(
            self.dialogue,
            {'use_alternative_root': True}
        )
        self.dialogue_processor.initiateDialogue()
    
    def testReturnsCorrectDialogueSection(self):
        """getDialogueGreeting returns first section with true condition"""
        dialogue_processor = self.dialogue_processor
        dialogue = self.dialogue
        root_dialogue_section = dialogue_processor.getDialogueGreeting()
        expected_dialogue_section = dialogue.greetings[0]
        self.assertEqual(root_dialogue_section, expected_dialogue_section)


class TestGetCurrentDialogueSection(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.getCurrentDialogueSection} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
        self.dialogue_processor.initiateDialogue()
    
    def testReturnsCorrectDialogueSection(self):
        """getCurrentDialogueSection returns section at top of stack"""
        dialogue_processor = self.dialogue_processor
        expected_dialogue_section = self.dialogue.default_greeting
        actual_dialogue_section = \
            dialogue_processor.getCurrentDialogueSection()
        self.assertEqual(expected_dialogue_section, actual_dialogue_section)


class TestRunDialogueActions(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.runDialogueActions} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
        self.dialogue_processor.initiateDialogue()
        self.dialogue_section = DialogueSection(
            id_='some_section',
            text='Test dialogue section.',
            actions=[
                MockDialogueAction('foo'),
            ],
        )
        self.dialogue_response = DialogueResponse(
            text='A response.',
            actions=[
                MockDialogueAction('foo'),
            ],
            next_section_id='end',
        )
    
    def testExecutesDialogueActions(self):
        """runDialogueActions correctly executes DialogueActions"""
        dialogue_processor = self.dialogue_processor
        # Case: DialogueSection
        dialogue_processor.runDialogueActions(self.dialogue_section)
        dialogue_section_action = self.dialogue_section.actions[0]
        self.assertTrue(dialogue_section_action.was_called)
        expected_call_args = ((self.game_state,), {})
        self.assertTupleEqual(expected_call_args,
                              dialogue_section_action.call_arguments)
        # Case: DialogueResponse
        dialogue_processor.runDialogueActions(self.dialogue_response)
        dialogue_response_action = self.dialogue_response.actions[0]
        self.assertTrue(dialogue_response_action.was_called)
        self.assertTupleEqual(expected_call_args,
                              dialogue_response_action.call_arguments)


class TestGetValidResponses(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.getValidResponses} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
        self.dialogue_processor.initiateDialogue()
    
    def testReturnsValidResponses(self):
        """getValidResponses returns list of valid DialogueResponses"""
        dialogue_processor = self.dialogue_processor
        valid_responses = \
            dialogue_processor.dialogue_section_stack[0].responses
        valid_responses.pop(2)
        # Sanity check, all "valid" responses should have a condition that
        # evaluates to True.
        for response in valid_responses:
            if (response.condition is not None):
                result = eval(response.condition, {}, {})
                self.assertTrue(result)
        responses = dialogue_processor.continueDialogue()
        self.assertItemsEqual(responses, valid_responses)


class TestReply(TestDialogueProcessor):
    """Tests of the L{DialogueProcessor.reply} method."""
    def setUp(self):
        TestDialogueProcessor.setUp(self)
        self.dialogue_processor = DialogueProcessor(self.dialogue,
                                                    self.game_state)
        self.response = self.dialogue.default_greeting.responses[1]
        self.ending_response = \
            self.dialogue.default_greeting.responses[3]
    
    def testRaisesExceptionWhenNotInitiated(self):
        """reply raises exception when called before initiateDialogue"""
        dialogue_processor = self.dialogue_processor
        # Sanity check: A dialogue must not have been initiated beforehand.
        self.assertFalse(dialogue_processor.in_dialogue)
        with self.assertRaisesRegexp(RuntimeError, r'initiateDialogue'):
            dialogue_processor.reply(self.response)
    
    def testExecutesDialogueActions(self):
        """reply correctly executes DialogueActions in a DialogueResponse"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.initiateDialogue()
        dialogue_processor.reply(self.response)
        dialogue_action = self.response.actions[0]
        self.assertTrue(dialogue_action.was_called)
        expected_call_args = ((self.game_state,), {})
        self.assertTupleEqual(expected_call_args,
                              dialogue_action.call_arguments)
    
    def testJumpsToCorrectSection(self):
        """reply pushes section specified by response onto stack"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.initiateDialogue()
        # Sanity check: Test response's next_section_id attribute must be refer
        # to a valid DialogueSection in the test Dialogue.
        self.assertIn(self.response.next_section_id,
                      self.dialogue.sections.keys())
        dialogue_processor.reply(self.response)
        greeting = self.dialogue.default_greeting
        next_section = self.dialogue.sections[self.response.next_section_id]
        self.assertStateEqual(
            dialogue_processor,
            in_dialogue=True,
            dialogue=self.dialogue,
            dialogue_section_stack=[greeting, next_section],
        )
    
    def testCorrectlyEndsDialogue(self):
        """reply ends dialogue when DialogueResponse specifies 'end'"""
        dialogue_processor = self.dialogue_processor
        dialogue_processor.initiateDialogue()
        # Sanity check: Test response must have a next_section_id of 'end'.
        self.assertEqual(self.ending_response.next_section_id, 'end')
        dialogue_processor.reply(self.ending_response)
        self.assertStateEqual(dialogue_processor, in_dialogue=False,
                              dialogue=self.dialogue,
                              dialogue_section_stack=[])


if __name__ == "__main__":
    unittest.main()
