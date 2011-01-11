Dialogue(
    'Skwisgaar the Crazy Swede',
    'gui/portraits/crazy_swede.png',
    DialogueSection(
        'main_dialog',
        'Chop!  Chop!  Chopity Chop-chop?',
        responses=[
            DialogueResponse(
                'Chop-chop.  Chop-choppy, choppy chop.',
                'a1',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'You are the woodcutter?',
                'a2',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                "Sorry, I don't speak chop.",
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'skwisgaar'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'a1',
            'Ah, you speak the lingo!  How long have you been chopping the good chop?',
            responses=[
                DialogueResponse(
                    'Oh, me?  - These hands are not suited for manual labor.',
                    'a2',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I have been known to chop-chop the wood what needs choppin' -- if you know what I mean.",
                    'b1',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'a2',
            "You gots to Chop what to Chop when the Choppin' needs a Chop!!!",
            responses=[
                DialogueResponse(
                    'Yes, my man it is only us against the wood!',
                    'b1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Chop?  What the hell are you talking about!',
                    'b2',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Enough with the chop talk!  Do you have any yeast?',
                    'end',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'b1',
            'Ah, so you chop the chop... but do you Chop the Chop?',
            responses=[
                DialogueResponse(
                    "Well, that's how we did it back in Sweden!",
                    'c1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Well, that's how we did it back in Norway!",
                    'c2',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Well, that is how we Finns get it done!',
                    'c3',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'b2',
            'Chopity!!! Chop the Chop-chop!!!',
            responses=[
                DialogueResponse(
                    'Chop?  You betcha - chop, chop!',
                    'b1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Yeast.  Y-E-A-S-T.  For making booze.  Do you understand me?',
                    'end',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
                ),
                DialogueResponse(
                    'Screw this, you cannot argue with a Swede!',
                    'c1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You got a problem?  Hit in the head during the war?',
                    'permanent_failure',
                    actions=[
                        SetQuestVariableAction(
                            variable='yeast_available',
                            quest='beer',
                            value=0
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'c1',
            'Sweden!  Sweden?  Got no chops!!!',
            responses=[
                DialogueResponse(
                    'But they told me you were from there.',
                    'main_dialog',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Oh.. you aren't Swedish, are you?",
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Did I say Sweden?  I meant Norway.',
                    'c2',
                    actions=[],
                    condition="quest['beer'].getValue('yeast_available')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'c2',
            'N..n...Norway.  Norway...  NORWAY!  The FJORDS!!!! [sobs]',
            responses=[
                DialogueResponse(
                    'Did I say Norway?  I meant Sweden.',
                    'c1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Hey, Hey - there it's OK.  We have Fjords right here in Finland.",
                    'c3',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You are not pining, are you?',
                    'main_dialog',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Yeah, buddy.  You are a long way from home.  Be nice if we had a drink to toast to Norway.',
                    'd',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].getValue('yeast_available')"
                ),
                DialogueResponse(
                    'Yeah, buddy.  You are a long way from home.',
                    'dprime',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and not quest['beer'].getValue('yeast_available')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'c3',
            'FINLAND GOT NO FJORDS!!!!',
            responses=[
                DialogueResponse(
                    'Whoa... no need to get excited there... uh... Chop? Choppy-Chop-Chop?',
                    'b2',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'At least they know how to make booze!',
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You are totally insane.',
                    'permanent_failure',
                    actions=[
                        SetQuestVariableAction(
                            variable='yeast_available',
                            quest='beer',
                            value=0
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'd',
            'Ah, a toast to the King!  The King of Norway!  [looks around furtively]  But the Skol!  Need the bugs for the skol! ',
            responses=[
                DialogueResponse(
                    'Bugs?  You eat bugs?',
                    'e1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Bugs?  You mean for beer?  Little yeasties?',
                    'e2',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'dprime',
            'No bugs for you!',
            responses=[
                DialogueResponse(
                    'Nuts.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'e1',
            "HAHAA... uncultured baboon!  Baboon- bug eater!  Don't eat the bugs! Ferment with the bugs! ",
            responses=[
                DialogueResponse(
                    "That's what I need!  Fermentation bugs!",
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Ah, indeed!  A fermented beverage!  Fit for a King...',
                    'd',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'YES!  The bugs!  The yeast bugs!  For the Fermentation!',
                    'get_yeast',
                    actions=[
                        TakeStuffAction(
                            'Yeast'
                        ),
                        SetQuestVariableAction(
                            variable='yeast_available',
                            quest='beer',
                            value=0
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'e2',
            'Yeasties!  Belittle them not, foreign stranger!  The finest Norwegian yeast I have saved for 1,000 years!!',
            responses=[
                DialogueResponse(
                    "Oh you're one to talk about Foreigers, Swede!",
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Ah, Norwegian yeast.  Truly a permanent cultural artifact!',
                    'e1',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    '1000 years?',
                    'permanent_failure',
                    actions=[
                        SetQuestVariableAction(
                            variable='yeast_available',
                            quest='beer',
                            value=0
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'get_yeast',
            "My precious beasties... yeasty beasties for the fermentation!  Don't forget to save Culture and Civilization!",
            responses=[
                DialogueResponse(
                    'Thanks buddy!  Skol!',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'permanent_failure',
            '[ scowls ] Chop!  Chop!  Chopity Chop-chop.  Chop.',
            responses=[
                DialogueResponse(
                    'Go ahead and chop wood until the end of your days, nutball!',
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