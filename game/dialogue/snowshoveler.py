Dialogue(
    'Matti',
    'gui/portraits/snowshoveler.png',
    DialogueSection(
        'opening_dialog',
        'Good to talk to someone, Matti could use a break',
        responses=[
            DialogueResponse(
                "You are some kind of psycho-killer, aren't you?",
                'end',
                actions=[],
                condition="quest['fedex'].getValue('accused_of_murder') == 'matti'"
            ),
            DialogueResponse(
                "Matti, I was wrong about Pekko's killer - I think it was someone else.",
                'unaccuse_matti',
                actions=[
                    SetQuestVariableAction(
                        variable='accused_of_murder',
                        quest='fedex',
                        value=''
                    )
                ],
                condition="quest['fedex'].getValue('accused_of_murder') == 'matti'"
            ),
            DialogueResponse(
                'I found a body in your cistern there.  What do you know about it?',
                'discuss_body',
                actions=[],
                condition="not quest['fedex'].getValue('accused_of_murder') and quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                "Hey, what's going on here?",
                'main_dialog',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'matti'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'main_dialog',
            'Matti shovels the snow.',
            responses=[
                DialogueResponse(
                    'Matti?  Oh, you must be Matti.  Where does all the snow... you know... go?',
                    'explain_shoveling',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I'm looking for stuff to make beer with",
                    'help_beer',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
                ),
                DialogueResponse(
                    "I'm looking for Pekko, you seen him?",
                    'help_fedex',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    "Oh, were you working?  I'll let you get back to it",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            'Whoa.  Whoa.  WHOA.  You can make beer?  Astounding.',
            responses=[
                DialogueResponse(
                    'Never mind',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "Uhhh... Pekko.. Um... Matti saw him.. some time... but Matti don't remember",
            responses=[
                DialogueResponse(
                    "Really?  You don't remember?  Weird.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_shoveling',
            'Yeah, uh, Matti basically justs shovel all the snow into this here tank.',
            responses=[
                DialogueResponse(
                    'And then what happens?',
                    'snow_tank',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'snow_tank',
            'Well, uh, it gets melted.. and magically turned into STEAM!!',
            responses=[
                DialogueResponse(
                    'Magically?  What?  Oh, that tanker must be a boiler or something',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_body',
            'A body?  You mean a Dead body?  How did that get there?',
            responses=[
                DialogueResponse(
                    "That's what I'm trying to figure out, Matti.  You are the guy who shovels stuff in there?",
                    'body_continued',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'body_continued',
            "But Matti only puts the snow into the tank!  Matti don't think dead things are allowed!",
            responses=[
                DialogueResponse(
                    "I don't really see how it could be anyone else...",
                    'accuse_matti',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value='matti'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'Who else has access?',
                    'drop_matti',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_matti',
            'You think Matti killed Pekko?  No way!  Matti was framed!',
            responses=[
                DialogueResponse(
                    "Sure, that's what they all say.",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'drop_matti',
            "Matti doesn't know, but Matti has to sleep sometime",
            responses=[
                DialogueResponse(
                    "I guess that's true.  Still, are the closest person to it.",
                    'opening_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'unaccuse_matti',
            'Matti knew you would see the light!  Matti innocent.',
            responses=[
                DialogueResponse(
                    "I'm sorry for my mistake, Matti.  I hope we can be friends again",
                    'opening_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        )
    ],
    greetings=[]
)