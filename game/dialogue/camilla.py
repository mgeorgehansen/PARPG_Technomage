Dialogue(
    'Camilla Niitty',
    'gui/portraits/camilla.png',
    DialogueSection(
        'main_dialog',
        'Oh, another vagabond.  What do you want?',
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with ",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                "I'd like a drink.",
                'buy_drink',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'I like the bar.  Do you work here?',
                'inn_background',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Who are those two women over there?',
                'loose_women',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Your booze monopoly is over!!',
                'ungratitude',
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
                "Did you hear? Pekko's dead.  I found his body.",
                'pekko_dead',
                actions=[],
                condition="quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                'You are as cold as... well, everything.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'camilla'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'buy_drink',
            "I'm off duty right now.  Go talk to Jacob.",
            responses=[
                DialogueResponse(
                    'Oh, sorry to bother you.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'inn_background',
            "It's my Dad's place.  He's kind of a big shot around here, so watch yourself.  Dig is a personal friend of mine.",
            responses=[
                DialogueResponse(
                    "Who's Dig?",
                    'explain_dig',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Jacob is your father?',
                    'explain_jacob',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Can you tell me anything about your sister?',
                    'explain_synnove',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'OK, lady.. no need to get defensive.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_dig',
            'Dig is the badass at the end of the bar.  He eats fools and miscreants like you for breakfast.',
            responses=[
                DialogueResponse(
                    "Hmmm... I hope he's not hungry then",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_jacob',
            "Jacob is my father.  He runs this place.  He's basically the number two guy around here, after Kimmo.",
            responses=[
                DialogueResponse(
                    "Well, maybe I should talk to him if he's so important.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_synnove',
            "Ah, Synnove.  She's not really... you know.... with us.  I mean she is WITH us, with us, but not really all there.  But she's not crazy... just confused.  Oh, I probably said too much.",
            responses=[
                DialogueResponse(
                    'Sounds about par for the course.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            "Why don't you just buy... Oh.  OH.  Is that your little scheme?  If I were you I would just drop.  I don't think my dad will take kindly to competition.",
            responses=[
                DialogueResponse(
                    'Ooops.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'loose_women',
            "Those two?  Cande and Kalli.  They're trouble.  Watch your wallet around them.  I mean, if we still had wallets.  And money.",
            responses=[
                DialogueResponse(
                    'Ha, I can handle myself.  Thanks for the tip though.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'Pekko?  Yeah, he was here a couple of nights ago.  Talking to Bart.',
            responses=[
                DialogueResponse(
                    "Really?  You are the only person who's seen him lately.  Did he say anything about where he was going or what he was doing?",
                    'discuss_pekko',
                    actions=[
                        SetQuestVariableAction(
                            variable='drunkard_evidence',
                            quest='fedex',
                            value=True
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_pekko',
            "He didn't say anything directly... he mentioned getting ready to go out on one of his expeditions, but he wasn't going to leave until tomorrow.  He and Bart walked off together.  I saw them over by the cistern door, where that Matti guy puts all the snow.",
            responses=[
                DialogueResponse(
                    'Wow, I better check that out.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_dead',
            "Dead?  Gee, that's awful.  I enjoyed his stories of the wilderness... I guess I am the last person to see him alive.",
            responses=[
                DialogueResponse(
                    'Well, maybe the second-to-last.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Come to think of it... were you alone here that night you last saw Pekko?',
                    'discuss_alibi',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_alibi',
            "You think I had something to do with this?  Well... impossible... I was here all night.  Dig and the girls were here too.  Ask'em.",
            responses=[
                DialogueResponse(
                    "I suppose I'll do that.",
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'ungratitude',
            "You little rat!!! This is our business!!  Our livelyhood!!!  I'll KILL You!!!1",
            responses=[
                DialogueResponse(
                    'Hahaha... catch me if you can!!!',
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