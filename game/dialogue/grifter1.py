Dialogue(
    'Cali',
    'gui/portraits/grifter_temp.png',
    DialogueSection(
        'main_dialog',
        'Hi there stranger.  Buy a gal a drink?',
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with. ",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                'My new beer is a great success...',
                'gratitude',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') >= 1"
            ),
            DialogueResponse(
                "I'm looking for Pekko, you seen him?",
                'help_fedex',
                actions=[],
                condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                "Sorry, I'm broke.",
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'cali'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'help_beer',
            "Trying to horn in on old Jacob here, huh?  I wouldn't if I were you.",
            responses=[
                DialogueResponse(
                    "Hey, we all do what we have to.  I'm sure you understand.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "[sigh] The cute one?.  He's in here all the time.  I guess it has been a couple days since I've seen him.",
            responses=[
                DialogueResponse(
                    'Yes, no one has seen him for a couple of days.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Was Camilla here all night the last time you saw Pekko here?',
                    'check_alibi',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_evidence')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'check_alibi',
            "Hmmmm... Yeah, I think so.  She's here almost every night.",
            responses=[
                DialogueResponse(
                    'OK, thanks.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'gratitude',
            "Huh.  Well, how about that.  You won't forget your friend Cali when you are famous, right?",
            responses=[
                DialogueResponse(
                    'No way, babe.',
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