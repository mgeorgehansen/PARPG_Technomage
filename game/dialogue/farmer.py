Dialogue(
    'Farmer Manslow',
    'gui/portraits/farmer.png',
    DialogueSection(
        'main_dialog',
        'Who the hell are you??',
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with ",
                'convince_farmer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions') and not quest.hasFinishedQuest('beer') and not quest['beer'].isGoalValue('farmer_beer_convinced')"
            ),
            DialogueResponse(
                'You can help me with the beer, thing, right?',
                'help_beer',
                actions=[
                    SetQuestVariableAction(
                        variable='farmer_beer_convinced',
                        quest='beer',
                        value=1
                    )
                ],
                condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('farmer_beer_convinced')"
            ),
            DialogueResponse(
                'Hey, that wheat you gave me really made the brew work.',
                'gratitude',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') > 3"
            ),
            DialogueResponse(
                'Have you tried my beer?',
                'grumpitude',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') !=0 and quest['beer'].getValue('beer_quality') <= 3"
            ),
            DialogueResponse(
                "I'm looking for Pekko, you seen him?",
                'help_fedex',
                actions=[],
                condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex')"
            ),
            DialogueResponse(
                'This is quite a nice farm you have here, can you tell me about it?',
                'chat_farm',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Hey, relax there old timer!',
                'leave',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'manslow'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'convince_farmer',
            'Never touch the stuff.',
            responses=[
                DialogueResponse(
                    'Come on -- have a heart.  Man cannot live on bread alone!',
                    'leave',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Well to be honest... we are trying to undermine Jacob's stranglehold on the booze in this town.",
                    'inn_explain',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'inn_explain',
            "Really.  What makes you think I'll help you.",
            responses=[
                DialogueResponse(
                    "Well, you know, Bart, he's a good guy...",
                    'leave',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Because Jacob is the only guy here grumpier than you!',
                    'help_beer',
                    actions=[
                        SetQuestVariableAction(
                            variable='farmer_beer_convinced',
                            quest='beer',
                            value=1
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            'He is a right old bastard, that Jacob... What are you looking for?',
            responses=[
                DialogueResponse(
                    'First, I need some water.',
                    'help_water',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'What I really need is some kind of grain, or fruit or something.',
                    'help_grain',
                    actions=[
                        TakeStuffAction(
                            'Grain'
                        ),
                        SetQuestVariableAction(
                            variable='grain_available',
                            quest='beer',
                            value=0
                        )
                    ],
                    condition="not quest['beer'].isGoalValue('grain_available')"
                ),
                DialogueResponse(
                    "You wouldn't happen to know where I can find some yeast?",
                    'help_yeast',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Well, I need a big pot to cook the mash in.',
                    'help_pot',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'The final step is some thing to hold the final product in.',
                    'help_bottles',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You are the grumpiest old man ever.',
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_water',
            "What are you an idiot?  We're surrounded by SNOW.",
            responses=[
                DialogueResponse(
                    'Sorry, no need to be a jerk about it...',
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_grain',
            "Well, that is my department.  I'll give you a bushel if you promise to use your brew to cause Jacob trouble.",
            responses=[
                DialogueResponse(
                    'Deal.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_yeast',
            'Yeast.  You really think someone is keeping around some kind of starter culture?',
            responses=[
                DialogueResponse(
                    "Uh... yeah?  Hey, how do you know so much about brewing if you don't even drink!",
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_pot',
            'Is there anything that you HAVE to make beer with?',
            responses=[
                DialogueResponse(
                    'Well, I have these instructions...',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_bottles',
            'Junkyard.',
            responses=[
                DialogueResponse(
                    "Where's the junkyard?",
                    'explain_junkyard',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_junkyard',
            'Downstairs.  Near the woodpile and the garbage dump.',
            responses=[
                DialogueResponse(
                    "Wow, that was kind of helpful... maybe you aren't so bad after all! ",
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'Pekko... I thought he was out scouting?  Did you try the Inn?',
            responses=[
                DialogueResponse(
                    'OK, the Inn, thanks.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'gratitude',
            "I still think it's a waste of grain.  But anything that screws that bastard Jacob is OK by me.",
            responses=[
                DialogueResponse(
                    "Couldn't have done it without you.",
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'grumpitude',
            "At least you didn't waste any of my grain on it.  Awful stuff.",
            responses=[
                DialogueResponse(
                    'No thanks, to you old man.',
                    'leave',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'chat_farm',
            "I don't have time for chit chat.  Talk to my assistants.",
            responses=[
                DialogueResponse(
                    "OK, I'll do that.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'leave',
            'Get off mah land!',
            responses=[
                DialogueResponse(
                    'Bye!',
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