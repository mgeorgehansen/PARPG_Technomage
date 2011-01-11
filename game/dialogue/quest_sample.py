Dialogue(
    'NPC',
    'gui/portraits/npc.png',
    DialogueSection(
        'main_dialog',
        'Things are tough around here, let me tell you our problems',
        responses=[
            DialogueResponse(
                "Here's your beer",
                'finish_quest',
                actions=[
                    CompleteQuestAction(
                        'beer'
                    )
                ],
                condition='quest[\'beer\'].isGoalValue("beer_gathered") and not quest.hasFinishedQuest(\'beer\')'
            ),
            DialogueResponse(
                'No problem (finished quest)',
                'main_dialog',
                actions=[],
                condition="quest.hasFinishedQuest('beer')"
            ),
            DialogueResponse(
                'Give me a beer! (Cheater!)',
                'give_beer',
                actions=[
                    IncreaseQuestVariableAction(
                        variable='beer_gathered',
                        quest='beer',
                        value=1
                    )
                ],
                condition='quest.hasActiveQuest(\'beer\') and not quest.hasFinishedQuest(\'beer\') and not quest[\'beer\'].isGoalValue("beer_gathered")'
            ),
            DialogueResponse(
                "I'm on it",
                'main_dialog',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer')"
            ),
            DialogueResponse(
                'Sure, tell me all about it',
                'listen_more',
                actions=[],
                condition="not quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer')"
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
                    'I help you',
                    'quest_accept',
                    actions=[
                        StartQuestAction(
                            'beer'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'Good luck with that',
                    'end',
                    actions=[],
                    condition=None
                ),
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
            'quest_accept',
            'All your beer are belong to us!',
            responses=[
                DialogueResponse(
                    'Right...',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'give_beer',
            "Here's your beer...",
            responses=[
                DialogueResponse(
                    'Thanks.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'finish_quest',
            'This is the good stuff! *hik*',
            responses=[
                DialogueResponse(
                    'Sigh',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'stop_quest',
            'Jerk.',
            responses=[
                DialogueResponse(
                    "That's how they call me!",
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        )
    ],
    greetings=[]
)