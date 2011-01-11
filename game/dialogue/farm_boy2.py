Dialogue(
    'Rasmus',
    'gui/portraits/farm_boy_temp.png',
    DialogueSection(
        'main_dialog',
        "Hi, I'm Rasmus.  What can I do for you?",
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with ",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                'Tell me about the farm',
                'describe_farm',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                "I'm looking for Pekko, you seen him?",
                'help_fedex',
                actions=[],
                condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                'Oh, I was looking for Sami.',
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
            'Not my place to hand out any stuff.  I just work here.  Talk to Manslow.',
            responses=[
                DialogueResponse(
                    'Alright.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "Kimmo's brother?  Nope, he never comes down here, and we basically live here.",
            responses=[
                DialogueResponse(
                    "At least it's warm.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'describe_farm',
            "It was just an empty lot before.  I don't envy the folks who had to break up all this ground.",
            responses=[
                DialogueResponse(
                    'That must have been some effort.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        )
    ],
    greetings=[]
)