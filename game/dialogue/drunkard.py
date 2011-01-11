Dialogue(
    'Bart The Drunkard',
    'gui/portraits/drunkard.png',
    DialogueSection(
        'main_dialog',
        'Hey there, back up... no need to gang up on a poor guy!',
        responses=[
            DialogueResponse(
                "Gang up?  There's only one of me!",
                'first_impression',
                actions=[],
                condition="not pc.met('bart')"
            ),
            DialogueResponse(
                "Glad to see you're feeling better.",
                'gratitude',
                actions=[],
                condition="pc.met('bart') and quest.hasFinishedQuest('beer')"
            ),
            DialogueResponse(
                'Same old Bart,  I see.',
                'old_pals',
                actions=[],
                condition="pc.met('bart') and not quest['fedex'].isGoalValue('accused_of_murder')"
            ),
            DialogueResponse(
                'See you later, Killer.',
                'end',
                actions=[],
                condition="pc.met('bart') and quest['fedex'].isGoalValue('accused_of_murder')"
            ),
            DialogueResponse(
                'Ha, you better sleep it off, buddy.',
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
            "Oh... yeah... sorry.  My vision goes a little funny sometimes. Name's Bart.",
            responses=[
                DialogueResponse(
                    'Are you drunk?',
                    'elaborate_beer',
                    actions=[],
                    condition="not quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer')"
                ),
                DialogueResponse(
                    "Wow, you're really hammered.  I'll come back when you're sober.",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[
                MeetAction(
                    'bart'
                )
            ]
        ),
        DialogueSection(
            'elaborate_beer',
            'Well, not for much longer, unfortunately.  My stash is just about run dry.  That bastard, Jacob has a still, but who can afford his prices! He basically has a monopoly.  No one else around here knows how to brew us up some more booze!',
            responses=[
                DialogueResponse(
                    "Wow, what a jerk.  Well, I'll be glad to lend a hand to such a noble task. Assuming you guys will supply the raw materials.",
                    'quest_beer',
                    actions=[
                        StartQuestAction(
                            'beer'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    "Hey, the man is entitled to run his business.  I'm not going to mess up his meal ticket.",
                    'old_pals',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Alcohol is work of the Devil!!',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'quest_beer',
            'You sir, are a gentleman and a scholar.  I am sure folks around here will help you find what you need.',
            responses=[
                DialogueResponse(
                    "You aren't even going to offer me a reward?",
                    'reward_query',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Well, I'll get right on it.  Finally, a worthwhile test of my scrounging skills.",
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
                    'Hey, Bart - here is my shopping list I need to brew us up something tasty.  Can you help?',
                    'help_beer',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions') and not quest.hasFinishedQuest('beer')"
                ),
                DialogueResponse(
                    "By the way, Bart, I am looking for a chap named 'Pekko', you know were I can find him?",
                    'help_fedex',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    'Hm.  You got a good buzz on, today?',
                    'elaborate_beer',
                    actions=[],
                    condition="not quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer')"
                ),
                DialogueResponse(
                    'Hey, try my fantastic brew!',
                    'beer_tasting',
                    actions=[],
                    condition="quest['beer'].getValue('beer_quality') != 0"
                ),
                DialogueResponse(
                    'Well, I am off to make some beer, wish me luck!',
                    'end',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and not quest.hasFinishedQuest('beer') and quest['beer'].getValue('beer_quality') == 0"
                ),
                DialogueResponse(
                    'Adios, Bart',
                    'end',
                    actions=[],
                    condition="not quest.hasActiveQuest('beer') or quest.hasFinishedQuest('beer')"
                ),
                DialogueResponse(
                    'Did you hear about Pekko?',
                    'dead_pekko',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].isGoalValue('accused_of_murder')"
                ),
                DialogueResponse(
                    "Pekko was murdered.  And someone's responsible.",
                    'murder_accuse',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].isGoalValue('accused_of_murder')"
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
                    condition="not quest['fedex'].isGoalValue('drunkard_water_asked')"
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
            'Water!  I dunno.  I never trust the stuff.  Guess you could melt snow or something.',
            responses=[
                DialogueResponse(
                    'Yeah, I suppose I could at that.  What does everyone drink when the snow melts?',
                    'snow_melting',
                    actions=[
                        SetQuestVariableAction(
                            variable='drunkard_water_asked',
                            quest='fedex',
                            value=1
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_grain',
            'You mean like wheat, hops, barley?  I dunno about that, but if you poke around you should be able to find something with enough starch to ferment.',
            responses=[
                DialogueResponse(
                    'Yeah, but where?',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_yeast',
            'Good luck finding that!',
            responses=[
                DialogueResponse(
                    'This is going to be harder than I thought',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_pot',
            "I'm pretty sure the quartermaster has one, back in the store room. She can be hard to get stuff out of, though.  It's kind of her job to be stingy",
            responses=[
                DialogueResponse(
                    "Fantastic, I'll give the quartermaster a try.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_bottles',
            "I don't know, myself.  One of the scavenging teams must have brought in something.",
            responses=[
                DialogueResponse(
                    'Scavenging teams?',
                    'explain_scavenging',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "OK, I'll poke around some more.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_scavenging',
            'Yeah, when the weather is good, we send out teams to dig around in the ruins and forests.  This place takes quite a bit of upkeep you know.',
            responses=[
                DialogueResponse(
                    'Ah, makes sense.',
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'snow_melting',
            'Like I said, I never drink the stuff.',
            responses=[
                DialogueResponse(
                    'Well, alrighty then.',
                    'help_beer',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'reward_query',
            'I would think that getting your own booze ration would be reward enough!',
            responses=[
                DialogueResponse(
                    "I am fond of a bender now and again, it's true.",
                    'old_pals',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Personally, I stay away from alcohol.  Dulls the senses.  But I suppose I'll help you out of the goodness of my heart.",
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'dead_pekko',
            "Dead, huh.  That's a shame.",
            responses=[
                DialogueResponse(
                    'You seem really broken up about it.',
                    'dead_discuss',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "You don't seem very surprised to hear.",
                    'dead_discuss_ii',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'dead_discuss',
            "The kid was a problem.  It's no surprise to me that someone had it in for him.",
            responses=[
                DialogueResponse(
                    'So you are saying that a lot of people wanted him dead?',
                    'dead_discuss_ii',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Had it in for him... I didn't say he was murdered!",
                    'murder_accuse',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'dead_discuss_ii',
            "Well, I'm sure it was just an accident.  It's a dangerous world today.",
            responses=[
                DialogueResponse(
                    'Accident, huh.  Interesting theory',
                    'old_pals',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Oh, I don't think it was an accident at all.  I think he was murdered.",
                    'murder_accuse',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'help_fedex',
            'No idea.',
            responses=[
                DialogueResponse(
                    'Thanks...',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'murder_accuse',
            'Wait... so .. you are the junior detective now?  How do you know he was murdered?',
            responses=[
                DialogueResponse(
                    'His head was caved in, and his arm was broken from being forced into the snow hopper at the top of the cistern.',
                    'discuss_murder',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I know he was murdered, and I know you did it.  But I don't know why.",
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
                    'I think we both know how he was killed, Bart.  The question remains, who do I tell.',
                    'blackmail_bart',
                    actions=[],
                    condition="not quest['fedex'].getValue('report_murder_to_janie') and not quest['fedex'].getValue('report_murder_to_kimmo')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'discuss_murder',
            "Maybe he just fuckin' fell.",
            responses=[
                DialogueResponse(
                    "Maybe.  But I'll get to the bottom of this.",
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I don't think so, I think it was you.  The question is, why?",
                    'accuse_bart',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value='bart'
                        )
                    ],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_bart',
            "Look, stranger...  I don't know who you think you are but this isn't your place.  The fact is, Pekko didn't have many friends, and even his friends didn't even really like him.",
            responses=[
                DialogueResponse(
                    'What about Janie?',
                    'janie_pekko_connection',
                    actions=[],
                    condition="quest.hasFinishedQuest('fedex')"
                ),
                DialogueResponse(
                    "Whatever, murderer.  I'll see you hang.",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'blackmail_bart',
            "Oh, so that's how it's going to be.  And what is the cost of your silence?",
            responses=[
                DialogueResponse(
                    "That's right, scumbag.  I'm going to squeeze you until you're dry.",
                    'greedy_blackmail',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "That's a pretty nice coat you go there, I'll take that...",
                    'light_blackmail',
                    actions=[
                        SetQuestVariableAction(
                            variable='got_drunkards_coat',
                            quest='fedex',
                            value=1
                        ),
                        TakeStuffAction(
                            'coat'
                        )
                    ],
                    condition="not quest['fedex'].isGoalValue('got_drunkards_coat')"
                ),
                DialogueResponse(
                    "Hey, I'm not a greedy bastard.  How about you just owe me?",
                    'delayed_blackmail',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Ha, just joshing with ya.  Near as I can tell the guy deserved it.',
                    'feint_blackmail',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'greedy_blackmail',
            "You haven't got the guts.  My friends are powerful, and you ain't got nuthin' on me.  I'm calling your bluff.",
            responses=[
                DialogueResponse(
                    "Guess we'll find out HOW powerful, now, won't we!",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'light_blackmail',
            "My coat, huh.  That's it?  I guess life is pretty cheap these days. Here ya go.",
            responses=[
                DialogueResponse(
                    'Hey, pretty nice.  Fits too!  Catch ya later, Bart.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'delayed_blackmail',
            'OK, so I owe you one.  You never know when you might need a favor.',
            responses=[
                DialogueResponse(
                    "That's what I was thinking.",
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'feint_blackmail',
            "Deserve got nothin' to do with it.  You're OK by me, though.",
            responses=[
                DialogueResponse(
                    'Likewise, Bart.  This could be the result of a bee-you-ti-ful friendship',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'janie_pekko_connection',
            'Janie... what does she have anything to this?  What have you told her?',
            responses=[
                DialogueResponse(
                    "I don't see what difference it makes.",
                    'janie_pekko_continued',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'janie_pekko_continued',
            "It.. it.. has everything.  Look.  You can't tell her, OK.  You just can't.",
            responses=[
                DialogueResponse(
                    "It's too late.  She already knows you killed him.",
                    'janie_knows',
                    actions=[],
                    condition="quest['fedex'].getValue('report_murder_to_janie') and quest['fedex'].getValue('accused_of_murder') = 'bart'"
                ),
                DialogueResponse(
                    "Oh, I can't?  Why shouldn't I?",
                    'force_bart',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'janie_knows',
            'Aw, hell.  You gotta... I dunno.  Take it back... I ... I .. Aw, hell.',
            responses=[
                DialogueResponse(
                    'Will you tell me the whole story if I convince her it was someone else?  Or an accident?',
                    'recant_testimony',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "How did you think you could keep it from her?  Idiot.  You deserve what's coming to you.",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'recant_testimony',
            "Anything man, I'll do anything.",
            responses=[
                DialogueResponse(
                    "I don't know if it will work, but I'll try",
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'force_bart',
            "Because... because... [sobs].  I love her.  Look.  Promise me you won't tell her and I'll spill.",
            responses=[
                DialogueResponse(
                    "I can't promise that.",
                    'no_promise',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Alright.. What she doesn't know can't hurt her.",
                    'bart_confess',
                    actions=[
                        SetQuestVariableAction(
                            variable='drunkard_confesses',
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
            'no_promise',
            'Fuck you.',
            responses=[
                DialogueResponse(
                    'Fuck _you_.',
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Hmmmm.  Your arguments have swayed me.  I won't tell her if you tell what really happened.",
                    'bart_confess',
                    actions=[
                        SetQuestVariableAction(
                            variable='drunkard_confesses',
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
            'bart_confess',
            "So. It went down like this.  It was Kimmo.  He had enough of his brother stirring up trouble; causing a panic about the weather.  IF we leave here, his Ma will die, and Kimmo will lose his power over us.  He knows this.  Pekko just wouldn't shut up about that ice age nonsense. People were getting scared.",
            responses=[
                DialogueResponse(
                    'So what does that have to do with you.',
                    'barts_price',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'barts_price',
            "Tha fuckin' booze, man.  I had to have it.  That bastard Jacob priced me out, I was starting to get the shakes.  Kimmo had a whole case of the real stuff - pre war stuff.  That was the deal.  Disappear his brother, get the hooch.",
            responses=[
                DialogueResponse(
                    'What were you going to do when the booze ran out?',
                    'consequences',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'consequences',
            'Whatever it takes.  Whatever it takes.  Maybe if you had shown up a few days earlier, things would have been different.',
            responses=[
                DialogueResponse(
                    'This is a cold blooded town.  I am not sure what to do now.',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'beer_tasting',
            'You are a genius, sir, a genius. [Bart holds bottle up to the light] Looks great. How did it come out?',
            responses=[
                DialogueResponse(
                    "I think it's just about perfect",
                    'best_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') >= 5"
                ),
                DialogueResponse(
                    'It took some doing, but I think I got it down.',
                    'good_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') == 4"
                ),
                DialogueResponse(
                    'I am pretty happy about it, given the circumstances.',
                    'decent_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') == 3"
                ),
                DialogueResponse(
                    "It's not my best work, but it will get you hammered.",
                    'ok_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') == 2"
                ),
                DialogueResponse(
                    'I hope it turned out OK.',
                    'bad_beer',
                    actions=[
                        CompleteQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') == 1"
                ),
                DialogueResponse(
                    'No promises on the the taste...',
                    'poisonous_beer',
                    actions=[
                        RestartQuestAction(
                            'beer'
                        )
                    ],
                    condition="quest['beer'].getValue('beer_quality') < 0"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'best_beer',
            '[ Bart drinks the beer] Let the church bells ring!  This stuff is awesome!',
            responses=[
                DialogueResponse(
                    'Glad you like it!',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'good_beer',
            '[ Bart drinks the beer] Nice job, Stranger.  You may fit in around here after all.',
            responses=[
                DialogueResponse(
                    'Everyone likes a good brew.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'decent_beer',
            "[ Bart drinks the beer] It's got a decent bite, that's for sure. Drinkable, anyway.",
            responses=[
                DialogueResponse(
                    'A couple more batches and I can hopefully work the kinks out.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'ok_beer',
            "[ Bart drinks the beer] Well, it's beer-like.  Odd aftertaste, though.",
            responses=[
                DialogueResponse(
                    'Yeah, it could use some malt and hops, but it was the best I could do considering.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'bad_beer',
            '[ Bart drinks the beer, makes a face] You promise that this.. this... stuff will get me drunk???',
            responses=[
                DialogueResponse(
                    'It ought to, if you drink enough of it.',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'poisonous_beer',
            '[ Bart drinks the beer, then sits down fast.] Oh... I uh... hmmm... are.. uh, you sure you did this right? [vomits]',
            responses=[
                DialogueResponse(
                    "Whoa... that's those old yams... yeah, gotta be the yams. My bad.  I'll try again.",
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'gratitude',
            'Ah, Mysterious Stranger, Braumeister of the Frozen North.   Now, if we can only get that still up and running my good chap!',
            responses=[
                DialogueResponse(
                    'I got some ideas on that, Bart... ',
                    'old_pals',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        )
    ],
    greetings=[]
)