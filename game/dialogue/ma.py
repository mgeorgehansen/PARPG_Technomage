Dialogue(
    'Ma Niitty',
    'gui/portraits/ma.png',
    DialogueSection(
        'main_dialog',
        "Why hello there... I don't recognize your face...",
        responses=[
            DialogueResponse(
                'I am trying to make beer, can you help me?',
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
                "I'm new here, I don't believe we've been introduced?",
                'introduce_ma',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Do you need a light?',
                'light_cigarette',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                "I am sorry to tell you... Pekko's dead",
                'dead_pekko',
                actions=[],
                condition="quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                "Sorry to bother you, I didn't realize you were awake",
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'ma'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'dead_pekko',
            "Oh, don't be silly.  I'm sure he is just off in the wilderness again",
            responses=[
                DialogueResponse(
                    'No, really, I found the body',
                    'found_body',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Oh, maybe you are right. I'll keep looking.  You take care now.",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'found_body',
            'Well, I am sure you are mistaken.',
            responses=[
                DialogueResponse(
                    "You must believe me, I'm quite sure.",
                    'dead_pekko',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I suppose I might be.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            "Beer?  Why don't you just get it at the supermarket?",
            responses=[
                DialogueResponse(
                    "I don't think... Oh, never mind.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'introduce_ma',
            "My name's Aino.  But everyone calls me 'Ma'.  Kimmo and Pekko are my boys. Good boys, both of 'em",
            responses=[
                DialogueResponse(
                    'Oh, tell me about your son, Kimmo.',
                    'talk_kimmo',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Oh, tell me about your son, Pekko.',
                    'talk_pekko',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You must be very proud.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'talk_kimmo',
            "Ah, Kimmo.  He is done such a good job here.  Everyone looks up to him, don't you think?  He's really a hero",
            responses=[
                DialogueResponse(
                    "He's a born leader.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'talk_pekko',
            'My Pekko.  Always the dreamer.  He spends so much time out in the woods, in his own head... He thinks we should move everyone!  ',
            responses=[
                DialogueResponse(
                    'Why does he want to leave?',
                    'explain_leaving',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_leaving',
            "He doesn't think it's going to be a very Nice Age.  It's just them crazy idea of the week.   Kimmo will keep us safe here.",
            responses=[
                DialogueResponse(
                    'Ah. [you nod understandingly]',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'light_cigarette',
            "For the cigarette?  No, they last longer this way.  I've had this one for about 4 years now...",
            responses=[
                DialogueResponse(
                    'Facinating.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'Ah, Pekko.  The apple of my eye.  Do you know where he is?',
            responses=[
                DialogueResponse(
                    'Well, actually... forget it.',
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