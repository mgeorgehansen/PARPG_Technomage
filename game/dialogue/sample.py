Dialogue(
    'Friendly NPC',
    'gui/portraits/npc.png',
    DialogueSection(
        'main_dialog',
        'Things are tough around here, let me tell you our problems',
        responses=[
            DialogueResponse(
                'Sure, tell me all about it',
                'listen_more',
                actions=[],
                condition="not set(pc.finished_quests).intersection(['raiders','well','beer'])"
            ),
            DialogueResponse(
                'That sounds boring. Bye.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[]
    ),
    sections=[
        DialogueSection(
            'listen_more',
            'Raiders stole our cattle, our well was poisoned, and the beer is all gone!',
            responses=[
                DialogueResponse(
                    'Tell me about the raiders',
                    'elaborate_raiders',
                    actions=[],
                    condition="pc.canAcceptQuest('raiders')"
                ),
                DialogueResponse(
                    "I've taken care of the raiders",
                    'complete_raiders',
                    actions=[
                        CompleteQuestAction(
                            'raiders'
                        )
                    ],
                    condition="pc.hasSatisfiedQuest('raiders')"
                ),
                DialogueResponse(
                    'Tell me about the well',
                    'elaborate_well',
                    actions=[],
                    condition="pc.canAcceptQuest('well')"
                ),
                DialogueResponse(
                    'I have returned with the antidote',
                    'complete_well',
                    actions=[
                        CompleteQuestAction(
                            'well'
                        )
                    ],
                    condition="pc.hasSatisfiedQuest('well')"
                ),
                DialogueResponse(
                    'Tell me about the beer',
                    'elaborate_beer',
                    actions=[],
                    condition="pc.canAcceptQuest('beer')"
                ),
                DialogueResponse(
                    'Three cheers the beer is here!',
                    'complete_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="pc.hasSatisfiedQuest('beer')"
                ),
                DialogueResponse(
                    'Guard, I have solved all your problems',
                    'all_done',
                    actions=[],
                    condition="pc.finished_quests == set(['raiders','well','beer'])"
                ),
                DialogueResponse(
                    'Good luck with that',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'elaborate_raiders',
            'They mostly come at night... mostly.',
            responses=[
                DialogueResponse(
                    'I can help you, for a price',
                    'quest_raiders',
                    actions=[
                        StartQuestAction(
                            'raiders'
                        )
                    ],
                    condition="pc.canAcceptQuest('raiders')"
                ),
                DialogueResponse(
                    'What was that other stuff you were talking about again?',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'That sounds too dangerous for me, good luck!',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'quest_raiders',
            'Thank you so much, these raiders have terrified our village for too long!',
            responses=[
                DialogueResponse(
                    "Quit your yammering, those raiders won't be a problem anymore.",
                    'listen_more',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'complete_raiders',
            'Thank you for defeating those evil doers',
            responses=[
                DialogueResponse(
                    'Pffft, it was easy',
                    'listen_more',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'elaborate_well',
            'A foul and dreadful toxin has contaminated our water well. Rumors tell of an antidote. If only someone could find it.',
            responses=[
                DialogueResponse(
                    "Wait a second... I'm someone! I will fix your well.",
                    'quest_well',
                    actions=[
                        StartQuestAction(
                            'well'
                        )
                    ],
                    condition="pc.canAcceptQuest('well')"
                ),
                DialogueResponse(
                    'Tell me about that other stuff',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "You're scaring me, bye",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'quest_well',
            'You are a brave hero indeed, water bringer.',
            responses=[
                DialogueResponse(
                    'Fear not, gentle villager. I will return shortly with the antidote.',
                    'listen_more',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'complete_well',
            'Thank heavens now the orphans will have water to drink',
            responses=[],
            actions=[]
        ),
        DialogueSection(
            'elaborate_beer',
            'After this keg, and that keg, there is only one keg left! Something must be done.',
            responses=[
                DialogueResponse(
                    "Running out of beer is no laughing matter. I'll run to the brewery for more",
                    'quest_beer',
                    actions=[
                        StartQuestAction(
                            'beer'
                        )
                    ],
                    condition="pc.canAcceptQuest('beer')"
                ),
                DialogueResponse(
                    'Tell me about all that other stuff',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'quest_beer',
            'I do not know what we would have done without you.',
            responses=[
                DialogueResponse(
                    "It's my pleasure",
                    'listen_more',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'complete_beer',
            'Thank heavens now the orphans will have beer to drink',
            responses=[
                DialogueResponse(
                    "All in a day's work, now gimme some! *glug*",
                    'listen_more',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'all_done',
            'For saving our village, I will give you the prized McGuffin. Thank you, Player Character',
            responses=[
                DialogueResponse(
                    'I am so awesome',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        )
    ],
    greetings=[]
)