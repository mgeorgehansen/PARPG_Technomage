Dialogue(
    'Jacob',
    'gui/portraits/innkeeper.png',
    DialogueSection(
        'main_dialog',
        "Hi there, Stranger!  Welcome to Jacob's.  How can I help you?",
        responses=[
            DialogueResponse(
                "I'd like a drink.",
                'buy_drink',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                "Nice place you got here.  What's your story?",
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
                "I'm the bastard that's going to put you out of business!",
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
                "Pekko's dead.  I found his body.",
                'pekko_dead',
                actions=[],
                condition="quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                'Nothing for me, thanks.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'jacob'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'buy_drink',
            "Doesn't look like you got much to trade for any of my premium booze. Come back later when you can pay.",
            responses=[
                DialogueResponse(
                    "Alright, I'll scrounge something up.",
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Can't I run up a tab?",
                    'credit_check',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'credit_check',
            'Your credit is no good here.  Now, get out before I have Dig run you out.',
            responses=[
                DialogueResponse(
                    'OK, OK, I was just asking.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'inn_background',
            'Well... Dig, Enoch and I found this place some years back.  Kimmo and Pekko were here first, of course, but they obviously needed our help. The girls took a liking to it, and with the improvements we made, it seemed like a good place as any to set up shop. ',
            responses=[
                DialogueResponse(
                    "Who's Enoch?",
                    'explain_enoch',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Who's Dig?",
                    'explain_dig',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'What improvements do you mean?',
                    'explain_steam',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'What girls?',
                    'explain_girls',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Cool, this is probably the best bar in about 500 km.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_enoch',
            'Enoch was my engineer.  He worked for me before the war.  He outfitted this place with the steam heating system.',
            responses=[
                DialogueResponse(
                    'Oh wow, steam heat?  How does that work?',
                    'explain_steam',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Where is Enoch now?  Can I meet him?',
                    'enochs_demise',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'enochs_demise',
            "Alas, he's no longer with us.  He met with an unfortunate accident. Luckily, he taught me how to keep the system up and running.",
            responses=[
                DialogueResponse(
                    'Accident?',
                    'enochs_accident',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'So you are the only one who can maintain the steam system?',
                    'steam_maintainance',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'enochs_accident',
            'Oh, you know.  Just one of those things.  Dangerous world.',
            responses=[
                DialogueResponse(
                    'Uh, I see.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_steam',
            "Well it's pretty simple in principal.  We just have a big wood fire melting snow.  Some of it becomes drinking water, the rest gets vaporized and sent around in all these steam pipes.  The each have little radiator attachments.  As long as we have wood, the whole place stays quite cozy.  It's kind of a pain to keep up though.",
            responses=[
                DialogueResponse(
                    'Can anyone just go get water there?',
                    'help_water',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest.hasActiveQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'But you can keep it running indefinitely... and no one else knows how it works?',
                    'steam_maintainance',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Pretty nifty.',
                    'inn_background',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_water',
            "Sure, doesn't cost us a thing.  No shortage of snow.  But I'll warn you, the water's been tasting a little funny lately",
            responses=[
                DialogueResponse(
                    'Thanks for the tip.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'steam_maintainance',
            "Yeah, just me.  I call it job security.  Like I said, it's a dangerous world.",
            responses=[
                DialogueResponse(
                    'That must make you pretty popular around here.',
                    'popularity',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Interesting.',
                    'inn_background',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'popularity',
            "Ha, Ha, very funny.  Let's just say it's our own version of checks-and-balances with Fearless Leader Kimmo over there.",
            responses=[
                DialogueResponse(
                    'Well, we all do what we have to.',
                    'inn_background',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_girls',
            'My daughters: Camilla and Synnove.  They were just little girls when the whole world went to hell.  I hope they can still have some kind of life.',
            responses=[
                DialogueResponse(
                    'Can I talk to Camilla?',
                    'talk_camilla',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Can I talk to Synnove?',
                    'talk_synnove',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'At least you still have someone to call family.  Better than most of us.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'talk_camilla',
            "Can you talk to her?  Listen to her, more likely.  She's right over there and is usually handling the bar when I am busy.",
            responses=[
                DialogueResponse(
                    "Oh, that's her?",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'talk_synnove',
            "Synnove?  Maybe you can talk some sense into her.  I know, she's been through a lot - but haven't we all.  She's wandering around somewhere.",
            responses=[
                DialogueResponse(
                    'Alright, I will look around for her.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_dig',
            "Dig and I go way back.  We owe each other our lives more times than we can count.  He takes care of 'difficulties' for me.",
            responses=[
                DialogueResponse(
                    'Ah, I will stay out his way then.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'loose_women',
            "Candi and Kalli?  They're the hospitality squad.  Harmless fun, if you buy them a drink.",
            responses=[
                DialogueResponse(
                    'Ah, I see.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_dead',
            "Dead, huh.  That's a shame.  A damn shame.  He was a positive force around here.  How did he die?",
            responses=[
                DialogueResponse(
                    'I am not sure, I found his body in the cistern.',
                    'body_found',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Someone murdered him, and shoved his body in the cistern.',
                    'discuss_murder',
                    actions=[],
                    condition="quest['fedex'].getValue('accused_of_murder') != ''"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'body_found',
            "Well, if you ask me, that's a funny place to have an accident.  Enoch and I worked for a couple of weeks on that system.  There's really no way you could just fall in.  And Pekko's not the suicidal type.",
            responses=[
                DialogueResponse(
                    'So you think someone killed him?',
                    'discuss_murder',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'No, I am sure it was an accident.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_murder',
            "Damn if doesn't look like it.  I know some folks were mad at him for stirring up trouble, but I didn't they were the type to just snuff him like that.  It's a cold world, alright.",
            responses=[
                DialogueResponse(
                    'Who do you think killed him?',
                    'discuss_suspects',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I think Bart, the drunkard killed him.',
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
                    'I think that dim-witted Matti killed him.',
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
                    'Bart killed him, and Kimmo put him up to it.',
                    'accuse_kimmo',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_confesses')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_suspects',
            "I have my theories.  But I'll be keeping them to myself.  And if I were you, I would drop the subject.",
            responses=[
                DialogueResponse(
                    'Really?',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_bart',
            "Bart, huh?  Why? What's in it for him?",
            responses=[
                DialogueResponse(
                    'I guess I should look into it more.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Camilla said that she saw the two of them together out in the parking lot the night he disappeared.',
                    'back',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_evidence')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_matti',
            'You are barking up the wrong tree.',
            responses=[
                DialogueResponse(
                    "Is that what you think?  Why won't you talk about it?",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_kimmo',
            'So.  You figured it out, huh.  Big hero, proves the Fearless Leader himself had his own brother killed.  Did you ever stop to think that revealing this information could do even further damage?',
            responses=[
                DialogueResponse(
                    "So, this news doesn't shock you?",
                    'murder_fallout',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I never thought of it that way before...',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'murder_fallout',
            "Survival in this world is bigger than the life of any one man; even an innocent man.  Justice is not my - or anyone's - primary concern.",
            responses=[
                DialogueResponse(
                    'Without justice, is survival worth anything at all?',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            "Ah, adventure boy.  Nope, haven't seem him in a couple of days. Maybe check with one of the girls?",
            responses=[
                DialogueResponse(
                    'Girls?',
                    'explain_girls',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Hmmm... no one seems to have seen him.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'ungratitude',
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