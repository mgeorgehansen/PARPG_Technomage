Dialogue(
    'Helja',
    'gui/portraits/quartermaster.jpg',
    DialogueSection(
        'main_dialog',
        'Hello, there!  A new addition to the labor pool, I see.',
        responses=[
            DialogueResponse(
                'What do you do around here?',
                'expound_quartermaster',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                "You're the Quartermaster?  I bet you can help me with some requisitions?",
                'pre_help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                'You going to help me distribute this new beer?',
                'beer_network',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') >= 1"
            ),
            DialogueResponse(
                "You haven't seen Pekko around lately, have you?",
                'help_fedex',
                actions=[
                    SetQuestVariableAction(
                        variable='check_bart_left',
                        quest='fedex',
                        value=True
                    )
                ],
                condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                'Labor pool?  I forgot my suit.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'helja'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'expound_quartermaster',
            'I am the like the supply sergeant.  I am in charge of all the communal goods - particularly food.',
            responses=[
                DialogueResponse(
                    'Sounds like an important job.  Are you bribe-able?',
                    'bribe_comment',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Really?  Because I am looking for some items to brew some beer...',
                    'pre_help_beer',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'bribe_comment',
            'Oh, funny. [narrows eyes] But I do like to help people who help themselves.  Like God.',
            responses=[
                DialogueResponse(
                    'So you accept burnt offerings?',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pre_help_beer',
            "Hey, I don't just give stuff away.  You have to have a requisition note from Kimmo, or at least trade something. ",
            responses=[
                DialogueResponse(
                    "Who's Kimmo?",
                    'describe_kimmo',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Well, I don't have a requisition... I am going to make some beer.",
                    'elaborate_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'describe_kimmo',
            "Kimmo is the leader of our merry band.  He's my boss -- the boss of all of us, currently.",
            responses=[
                DialogueResponse(
                    'What do you mean, currently?',
                    'describe_rivalry',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'So do you think Kimmo would let me have some stuff to make beer?',
                    'elaborate_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'elaborate_beer',
            "Beer, huh.  That might undermine Jacob's inn a bit.  Kimmo would probably approve of that.",
            responses=[
                DialogueResponse(
                    'So you will help me?',
                    'help_beer',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Why would Kimmo want to undermine Jacob?',
                    'describe_rivalry',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'describe_rivalry',
            "Well, Jacob -- I guess you would call him Kimmmo's primary rival for leadership.",
            responses=[
                DialogueResponse(
                    "Do you think he'll try to take over?",
                    'elaborate_rivalry',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Interesting.  And whom do you support?',
                    'which_side',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'So, Kimmo would want me to give the place another source of beer, right?',
                    'help_beer',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Ugh, small town politics.  Say no more.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'which_side',
            "Well, most of us owe Kimmo our lives.  But I'm no fighter.  I've survived this long without getting involved in petty power struggles. I am good at what I do.",
            responses=[
                DialogueResponse(
                    'But you are not against a little underhanded move against Jacob...',
                    'help_beer',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'So, playing both sides against the middle.  What if Jacob makes a move?',
                    'elaborate_rivalry',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'elaborate_rivalry',
            "I don't think he'll make a move... as long as we stay here.",
            responses=[
                DialogueResponse(
                    'Why would you move?  This place is awesome!',
                    'why_move',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'why_move',
            "Pekko's got this idea that the winters are going to get worse.  He says Lapland up north is already glaciated, and it's only a matter of time before this place is totally frozen out.",
            responses=[
                DialogueResponse(
                    'So you will help me make some beer?',
                    'help_beer',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "And away from the Paatalo, Kimmo's power base is weak.  Who do you support?",
                    'which_side',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            'Well, what do you need exactly?',
            responses=[
                DialogueResponse(
                    'I need some pure water.',
                    'help_water_clean',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'I need some pure water.',
                    'help_water_dirty',
                    actions=[],
                    condition="not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'The basis of the the brew is some source of sugar, like grain or potatoes.',
                    'help_grain',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'A yeast culture would really make the thing less dicey',
                    'help_yeast',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Of course, I'll need something to cook the mash in...",
                    'help_pot',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "When it's all done, I'll need to put the beer in something",
                    'help_bottles',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'That should about do it, thanks.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_water_dirty',
            'You can have all the water you want... but people have been complaining about the taste lately.  It should probably be checked out.',
            responses=[
                DialogueResponse(
                    "Oh, that's interesting.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_water_clean',
            "Water is unrestricted.  Go downstairs and draw a bucket from the cistern, it's filtered.",
            responses=[
                DialogueResponse(
                    'Water, check.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_grain',
            "Well, food.  Now that is not easy to get.  I can't authorize you any grain.  But maybe there are some old potatoes around...",
            responses=[
                DialogueResponse(
                    "Potatoes? I guess that's not too bad. Where would I find some?",
                    'help_potatoes',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Grain would really be the best... where do you get it?',
                    'help_farm',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "OK, I'll see what I can scrounge up",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_yeast',
            'You know... Skwisgaar is always babbling about yeast and stuff.  Good luck getting a straight answer out of him though.',
            responses=[
                DialogueResponse(
                    'Skwisgaar... is that the wood chopper?',
                    'wood_chopper',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_pot',
            "Well, I got a pot.  But I can't just give it up.  What will you give me for it?",
            responses=[
                DialogueResponse(
                    'Well, I got this pocket knife... would that do?',
                    'trade_knife',
                    actions=[
                        GiveStuffAction(
                            'pocket_knife'
                        ),
                        TakeStuffAction(
                            'brew_pot'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    "No deal.  I'll find my own.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_bottles',
            'Junkyard.  Also unrestricted.  Help yourself.',
            responses=[
                DialogueResponse(
                    'Thanks.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'trade_knife',
            'Let me see it. [You hand over the knife].  Humh.  A little used. But OK, I like you.',
            responses=[
                DialogueResponse(
                    "It's a deal then.",
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'wood_chopper',
            "Yeah, the wood chopper.  Came over to help us against the Russkies. From Sweden or something.  I don't think he's quite right in the head.",
            responses=[
                DialogueResponse(
                    "I'll keep that in mind",
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_potatoes',
            "There should be some old ones in that storeroom back there.  Probably won't be missed.",
            responses=[
                DialogueResponse(
                    "Wow, thanks.  You won't regret this.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_farm',
            "I'm sorry.  I can't really disclose that information.  That farm is our life.",
            responses=[
                DialogueResponse(
                    "Hey, it's cool.  I am not looking for trouble.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'He was here a couple of days ago, getting provisioned for one of his excursions.  He should be back by now though.',
            responses=[
                DialogueResponse(
                    'So the you last saw him, he was leaving the compound.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'beer_network',
            "I'll think about it.  Let's see if things quiet down.",
            responses=[
                DialogueResponse(
                    'Alright, Helja.',
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