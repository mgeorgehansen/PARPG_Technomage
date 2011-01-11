Dialogue(
    'Janie',
    'gui/portraits/fguard.png',
    DialogueSection(
        'main_dialog',
        'Halt, identify yourself!',
        responses=[
            DialogueResponse(
                'Whoa, easy with that weapon, sister',
                'first_impression',
                actions=[],
                condition="not pc.met('janie')"
            ),
            DialogueResponse(
                "I'm the beer savior, baby!",
                'gratitude',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') >= 1"
            ),
            DialogueResponse(
                "It's me - don't you remember?",
                'old_pals',
                actions=[],
                condition="pc.met('janie')"
            ),
            DialogueResponse(
                "Sorry, didn't mean to startle you. I'll just be moving along now.",
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[]
    ),
    sections=[
        DialogueSection(
            'first_impression',
            "Hey Stranger.  You're new around here, I don't recognize your face...",
            responses=[
                DialogueResponse(
                    'Yeah, just blew in with the last storm.',
                    'elaborate_fedex',
                    actions=[],
                    condition="not quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex')"
                ),
                DialogueResponse(
                    "But one night with me, babe, and you'll never forget it",
                    'rude_comeon',
                    actions=[],
                    condition=None
                )
            ],
            actions=[
                MeetAction(
                    'janie'
                )
            ]
        ),
        DialogueSection(
            'elaborate_fedex',
            'Well, maybe you can do me a favor.   I have this package I need delivered to Pekko.  But you gotta be casual about it.  No one can know you why you are looking for him.',
            responses=[
                DialogueResponse(
                    'Me?  Why Me?',
                    'why_me',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Why the secrecy?',
                    'why_secret',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "What's in it for me?",
                    'what_do_i_get',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Whatever, I need an excuse to wander around anyway.',
                    'quest_fedex',
                    actions=[
                        StartQuestAction(
                            'fedex'
                        ),
                        TakeStuffAction(
                            'Box'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'Find another errand boy.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'why_me',
            "No one knows you.  You're new here.  You can be expected to be wandering around being nosy.",
            responses=[
                DialogueResponse(
                    "I'm still not convinced.",
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Beats watching nuthin' on TV.",
                    'quest_fedex',
                    actions=[
                        StartQuestAction(
                            'fedex'
                        ),
                        TakeStuffAction(
                            'Box'
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'why_secret',
            "Look buddy, it's no questions asked.  You think you are the only frozen bum to come wandering in here?",
            responses=[
                DialogueResponse(
                    "Bum?  You don't even know who I am.",
                    'why_me',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Really.  I remain unswayed by your logic, but you are pleasing to the eye so keep talking.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "No need to get testy, I'll do it.",
                    'quest_fedex',
                    actions=[
                        StartQuestAction(
                            'fedex'
                        ),
                        TakeStuffAction(
                            'Box'
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'what_do_i_get',
            "Everybody wants something, huh.  I suppose my undying gratitude won't cut it?  How about a beaver pelt?  They make great hats...",
            responses=[
                DialogueResponse(
                    "Naw, it's OK, your gratitude's enough for me.",
                    'quest_fedex',
                    actions=[
                        StartQuestAction(
                            'fedex'
                        ),
                        TakeStuffAction(
                            'Box'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'A beaver pelt it is, then!',
                    'quest_fedex',
                    actions=[
                        StartQuestAction(
                            'fedex'
                        ),
                        TakeStuffAction(
                            'Box'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'I already gotta hat.  Deliver your own package.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'quest_fedex',
            "You should be able to find Pekko in the main compound area.  If anyone asks you why you are looking for him, 'say that he promised you something'.  Pekko's always making promises.  Oh, and don't open the box. [ Janie hands you the package ]",
            responses=[
                DialogueResponse(
                    "Why can't I open the box?",
                    'why_no_open',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'You got it, boss.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'why_no_open',
            "You are the nosiest little mailman anywhere, ain'tcha?  How about 'it's private.'?  If I wanted you to know what it was, I wouldn't have wasted a perfectly good box it, now would I?",
            responses=[
                DialogueResponse(
                    'I guess not.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'old_pals',
            'So what can I do for you?',
            responses=[
                DialogueResponse(
                    "I'm trying to make beer, can you help me find some stuff?",
                    'help_beer',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions') and not quest.hasFinishedQuest('beer') and quest['beer'].getValue('beer_quality') < 1"
                ),
                DialogueResponse(
                    "I guess I'll see if I can't find this Pekko character for you.",
                    'end',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and not quest.hasFinishedQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'So long, Janie.  Catch you later.',
                    'end',
                    actions=[],
                    condition="not quest.hasActiveQuest('fedex') or quest.hasFinishedQuest('fedex')"
                ),
                DialogueResponse(
                    'Uh, I opened the box.',
                    'open_box',
                    actions=[],
                    condition="quest['fedex'].getValue('open_box')"
                ),
                DialogueResponse(
                    'Hey, some folks seem to think Pekko left the compound.  Would you have seen him?',
                    'pekko_left',
                    actions=[
                        SetQuestVariableAction(
                            variable='check_pekko_left',
                            quest='fedex',
                            value=True
                        )
                    ],
                    condition="quest['fedex'].getValue('check_pekko_left') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'I have some bad news.  I found your friend, Pekko.  In the water tank.  Dead.',
                    'dead_pekko',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].getValue('accused_of_murder')"
                ),
                DialogueResponse(
                    "What are we going to do about Pekko's murder?",
                    'discuss_murder',
                    actions=[
                        SetQuestVariableAction(
                            variable='report_murder_to_janie',
                            quest='fedex',
                            value=True
                        )
                    ],
                    condition="quest.hasActiveQuest('fedex') and quest['fedex'].getValue('accused_of_murder')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            'Well, what do you need?',
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
            'open_box',
            'What!  You little worm!  Why did you do that!',
            responses=[
                DialogueResponse(
                    'Well, I figured since Pekko was dead and all...',
                    'dead_pekko',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    "I'm sorry, I was just curious.",
                    'give_back_boots',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'boot_gift',
            "That's what was in the package. [Janie takes boots out of the package, and gives them to you]",
            responses=[
                DialogueResponse(
                    'Oh.  I must be missing something...',
                    'explain_boots',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_left',
            "Left?  No, he's here.  I didn't see him leave, and there's no entry in the log.  He's definitly here.  I'd know.",
            responses=[
                DialogueResponse(
                    "Boy, that's strange.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_murder',
            "Look.  Just stay out of it.  It's not really your business anyway, Stranger.  Just forget we ever talked.",
            responses=[
                DialogueResponse(
                    "Alright, Alright.  But I don't like it.",
                    'give_up_quest',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'It was Bart.',
                    'accuse_bart',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value='bart'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'It was Matti, the Snow Shoveler!',
                    'accuse_matti',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value='matti'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'I think it was an accident.',
                    'report_accident',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value=''
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    "Well, I'm going to talk to the boss about it.",
                    'report_to_boss',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'give_up_quest',
            'You are making the right decision.',
            responses=[
                DialogueResponse(
                    "If you want me to drop it, I'll drop it.",
                    'drop_quest',
                    actions=[
                        FailQuestAction(
                            'fedex'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    "No, I can't drop it.  I have to talk to the authorities",
                    'report_to_boss',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'drop_quest',
            "Drop it.  It's bigger than than both of us.",
            responses=[
                DialogueResponse(
                    'Consider it dropped.  How about a date?',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_bart',
            "The town drunk???  ...really?  Anyway... I don't want to know.  He's dead.  I knew his big mouth and goofy ideas were going to get him in trouble.  Just drop it, please.",
            responses=[
                DialogueResponse(
                    "You can't just allow folks to murder people! It's wrong! Someone must be informed!",
                    'report_to_boss',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "If you want me to, I'll forget about the whole thing...",
                    'give_up_quest',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_matti',
            "Matti?  He looks mean, but I don't think he would hurt a fly. Anyway...  I don't want to know.  He's dead. He saved me you, know.  I guess he needed to pay more attention to himself.  Just drop it, please.",
            responses=[
                DialogueResponse(
                    "You can't just allow folks to murder people! It's wrong! Someone must be informed!",
                    'report_to_boss',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "If you want me to, I'll forget about the whole thing...",
                    'give_up_quest',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'report_accident',
            "An accident?  That's... convenient.  For someone.",
            responses=[
                DialogueResponse(
                    "Well, uh, you know.  It's a dangerous world.  I guess he slipped and fell in the cistern.",
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'report_to_boss',
            "You can talk to Kimmo, but I don't think you'll find the justice you are looking for.",
            responses=[
                DialogueResponse(
                    'Maybe.  But I have to try, right?  Otherwise, we are no better than wild animals.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_boots',
            "The boots were a signal that he should leave town... that he'd gone too far this time.",
            responses=[
                DialogueResponse(
                    'You knew about this?  Who do you think killed him?',
                    'discuss_murder',
                    actions=[
                        SetQuestVariableAction(
                            variable='report_murder_to_janie',
                            quest='fedex',
                            value=True
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'I think I know who killed him.',
                    'discuss_murder',
                    actions=[
                        SetQuestVariableAction(
                            variable='report_murder_to_janie',
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
            'dead_pekko',
            "He's dead?  Well, I'm too late then. I guess you can keep the boots, then.",
            responses=[
                DialogueResponse(
                    'What boots?',
                    'boot_gift',
                    actions=[
                        TakeStuffAction(
                            'boots'
                        )
                    ],
                    condition="not quest['fedex'].getValue('open_box')"
                ),
                DialogueResponse(
                    "Yeah, I figured he wouldn't need them.  Why did you send him boots, anyway?",
                    'explain_boots',
                    actions=[],
                    condition="quest['fedex'].getValue('open_box')"
                ),
                DialogueResponse(
                    'Does this mean no beaver pelt?',
                    'no_beaver_pelt',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'no_beaver_pelt',
            'No pelt.',
            responses=[
                DialogueResponse(
                    'Awwwwww...',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'give_back_boots',
            'Give me that back!',
            responses=[
                DialogueResponse(
                    'Here',
                    'rewrap_box',
                    actions=[
                        RestartQuestAction(
                            'fedex'
                        )
                    ],
                    condition='pc.hasItem("Boots")'
                ),
                DialogueResponse(
                    'I seem to have... misplaced them...',
                    'lost_boots',
                    actions=[],
                    condition='not pc.hasItem("Boots")'
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'lost_boots',
            'WHAT!?',
            responses=[
                DialogueResponse(
                    'I, uh, go search them',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'rewrap_box',
            "[Janie takes boots from PC and rewraps them].  Now, here.  And don't open it again.",
            responses=[
                DialogueResponse(
                    'OK, It will never happen again.',
                    'old_pals',
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
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'rude_comeon',
            '[fondles weapon] I hope you can take it as well as you give it...',
            responses=[
                DialogueResponse(
                    "Any way you want it, that's the way you need it!",
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