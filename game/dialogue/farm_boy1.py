Dialogue(
    'Sami',
    'gui/portraits/farm_boy_temp.png',
    DialogueSection(
        'main_dialog',
        "Hi, I'm Sami.  How can I help you?",
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
                'Oh, I was looking for Rasmus.',
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
            'Oh, you better ask the boss about that.',
            responses=[
                DialogueResponse(
                    'OK, I will.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'No.. but we pretty much stay here on the farm.',
            responses=[
                DialogueResponse(
                    'I see.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'describe_farm',
            'Manslow figured out that the only way to keep things growing in the cold was to build a greenhouse. Luckily, someone managed to find all this clear plexiglass.',
            responses=[
                DialogueResponse(
                    'Wow, nice.',
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