Dialogue(
    'Anyone',
    'gui/portraits/npc.png',
    DialogueSection(
        'main_dialog',
        'Hello.  How can I help you?',
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with ",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                "I'm the beer savior, remember?",
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
                'Whoa!  It talks!  Never mind',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[]
    ),
    sections=[
        DialogueSection(
            'help_beer',
            'I am always happy to give intimate details of our home to strangers, shoot!',
            responses=[
                DialogueResponse(
                    'Where do you folks get water from.  The more pure, the better.',
                    'help_water',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Some kind of grain, or fruit or something.',
                    'help_grain',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I'm really looking for some brewer's yeast.",
                    'help_yeast',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I need a pot to cook the mash in.',
                    'help_pot',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'It would be great if I had some bottles to put the brew in!',
                    'help_bottles',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I think I can handle it from here.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_water',
            "Oh, that is the one thing we have plenty of.  We have an old tanker trunk that we shovel the snow in and melt it.  You can see it from up here, but you have to go downstairs to tap it.  But the water's been tasting a little funny lately.",
            responses=[
                DialogueResponse(
                    "Great, that's a huge help.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_grain',
            'You could try the farm, and there should be some food in the storerooms',
            responses=[
                DialogueResponse(
                    "Thanks, I'll try that.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_yeast',
            'You got me.  I wonder if there is even any left at all.',
            responses=[
                DialogueResponse(
                    'Someone must have some!',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_pot',
            'Did you try the kitchen?  Or the storerooms?',
            responses=[
                DialogueResponse(
                    'Uh, yeah.  I guess that was obvious.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_bottles',
            'All the random junk is downstairs in old parking lot.  We have our own little junkyard.',
            responses=[
                DialogueResponse(
                    'Oooh... there is probably lots of good stuff down there.',
                    'back',
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
            "Well aren't you just a thick slice of awesome.",
            responses=[
                DialogueResponse(
                    'I try, I try.',
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