Dialogue(
    'Synnove Niitty',
    'gui/portraits/synnove.png',
    DialogueSection(
        'main_dialog',
        "Hi there!  I don't recognize you.  Are you new here?",
        responses=[
            DialogueResponse(
                'Yes, I am new.  And who are you?',
                'meeting',
                actions=[],
                condition="not pc.met('synnove')"
            ),
            DialogueResponse(
                "You don't remember me?  We just talked!",
                'future_meetings',
                actions=[],
                condition="pc.met('synnove')"
            ),
            DialogueResponse(
                "I'm looking for stuff to make beer with ",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                "I'm got my beer made, finally!",
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
                'Never mind, thought you were someone else.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[]
    ),
    sections=[
        DialogueSection(
            'meeting',
            "My name's Synnove.  I live here.",
            responses=[
                DialogueResponse(
                    'Good to meet you.  What do you do around here.',
                    'synnove_job',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Ah.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[
                MeetAction(
                    'synnove'
                )
            ]
        ),
        DialogueSection(
            'synnove_job',
            'Do?',
            responses=[
                DialogueResponse(
                    'Oh, never mind.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'future_meetings',
            "Oh, I don't think so.  I would have definitely remembered you if we hadn't met.",
            responses=[
                DialogueResponse(
                    'You would have? But... how ... would... uh.  What?',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            "Hmmm... beer.  Doesn't it come in bottles?  Anyway, I am always happy to give intimate details of our home to strangers, what are you looking for?",
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
            'I would think that you could find water in a water tank.',
            responses=[
                DialogueResponse(
                    'Well, the water has to be pure to make good beer.  Where do you folks keep purified water?',
                    'expand_water',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Yes, you would think that...',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'expand_water',
            'In the purified water tank?',
            responses=[
                DialogueResponse(
                    'Never mind.',
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_grain',
            'You mean like stuff to cook with?  That goes in beer?',
            responses=[
                DialogueResponse(
                    'Yes, the yeast need to eat sugars to make alcohol.',
                    'expand_grain',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "You really aren't much help, are you?",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'expand_grain',
            "Oh, I don't think I've seen any sugar in years.",
            responses=[
                DialogueResponse(
                    "It doesn't have to be purified sugar...",
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_yeast',
            'Oh, Skwisgaar has some.  He talks about it all the time.',
            responses=[
                DialogueResponse(
                    'The wood cutter?  You have conversations with him?  Figures.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_pot',
            "Nope, don't know where you can find anything like that.  Don't you have one?",
            responses=[
                DialogueResponse(
                    "No, if I did, I wouldn't... forget it.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_bottles',
            "Oh yeah, like I said!  Bottles!  That's what beer comes in.  Or does it come only in cans now?",
            responses=[
                DialogueResponse(
                    'You are a strange lady',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "Who's Pekko?  I never heard of him.",
            responses=[
                DialogueResponse(
                    "Kimmo's brother.  You never heard of him?",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'gratitude',
            "Wow, that's great!  But where did you find it?",
            responses=[
                DialogueResponse(
                    'I made it!',
                    'make_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'make_beer',
            'Oh, you are so silly.  Make beer.  Indeed.  I suppose you think I was born yesterday.',
            responses=[
                DialogueResponse(
                    "Uh, yeah.  You got me.  'Just Kidding'.",
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