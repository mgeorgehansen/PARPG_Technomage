Dialogue(
    'Dig',
    'gui/portraits/bouncer.png',
    DialogueSection(
        'main_dialog',
        "What do you want?  Can't you see I'm drinking here?",
        responses=[
            DialogueResponse(
                "I'm looking for stuff to make beer with.",
                'help_beer',
                actions=[],
                condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].isGoalValue('beer_instructions')"
            ),
            DialogueResponse(
                'Do you know Jacob?',
                'explain_jacob',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Do you work here?',
                'inn_background',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Are you going to kick my ass?',
                'ass_kicking',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Was Camillia with you in the bar here two nights ago?',
                'check_alibi',
                actions=[],
                condition="quest['fedex'].isGoalValue('drunkard_evidence')"
            ),
            DialogueResponse(
                'Who are those two women over there?',
                'loose_women',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Why is Camilla such a bitch?',
                'explain_camilla',
                actions=[],
                condition="pc.met('camilla')"
            ),
            DialogueResponse(
                'What is up with Synnove?',
                'explain_synnove',
                actions=[],
                condition="pc.met('synnove')"
            ),
            DialogueResponse(
                "Your boss's booze monopoly is over!!",
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
                'Hey, back off.  Just making small talk.',
                'parting_shot',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'dig'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'explain_camilla',
            "Well, it's probably because she gets hit on by greasy layabouts all hours of the day.  Maybe you should cut her some slack.",
            responses=[
                DialogueResponse(
                    'Hmmm... Can you confirm that she was here all night with you two days ago?',
                    'check_alibi',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_evidence')"
                ),
                DialogueResponse(
                    "I suppose that's not unreasonable.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'check_alibi',
            "Huh?  You're not her boyfriend.  And I'm not her babysitter.  Why do you care?",
            responses=[
                DialogueResponse(
                    "I'm investigating a murder",
                    'investigate',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'No reason.  No reason at all.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'investigate',
            'Oh, in that case officer, she was with me the whole time. [rolls eyes]',
            responses=[
                DialogueResponse(
                    'I get the sense that you are not taking this very seriously.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'ass_kicking',
            "Not today.  I'm off duty.  But watch yourself all the same.",
            responses=[
                DialogueResponse(
                    "I'll do that.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_jacob',
            "I'm Jacob's guy.  You got a problem with him - or his family - you got a problem with me.  So do you have a problem?",
            responses=[
                DialogueResponse(
                    'Nope.  No problem at all.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_synnove',
            "OK, she's a little weird.  She was 5 when she saw what those Russians bastards did to her mother.  She'd have been next if Jacob and I hadn't shown up in time.",
            responses=[
                DialogueResponse(
                    'Oh, I had no idea.  Gruesome.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'inn_background',
            "If you call sittin' here and bullshitting `working`.  But I do solve problems for Jacob.  You're not a problem, are ya?",
            responses=[
                DialogueResponse(
                    'No sir, no problem here.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_beer',
            'Now you are just trying to be funny.  And failing.   Get out of here before I decide to throw you out.',
            responses=[
                DialogueResponse(
                    "Yeah, well maybe I'll find my own bouncer, too!",
                    'parting_shot',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'loose_women',
            "Buy 'em a drink and find out.",
            responses=[
                DialogueResponse(
                    'I would do that if I could afford the booze in this place.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "I dunno.  Dude's in here all the time.",
            responses=[
                DialogueResponse(
                    'Was he here talking to Bart a couple nights ago?',
                    'pekko_check',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_evidence')"
                ),
                DialogueResponse(
                    'Lot of help you are.',
                    'parting_shot',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_check',
            "Buy 'em a drink and find out.",
            responses=[
                DialogueResponse(
                    'I would do that if I could afford the booze in this place.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'parting_shot',
            "Watch yourself, Bub.  I don't want to get out this chair.",
            responses=[
                DialogueResponse(
                    'Ulp.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'ungratitude',
            'Oh, a wise guy huh??? [gets out of chair]',
            responses=[
                DialogueResponse(
                    "I'm out of here!",
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