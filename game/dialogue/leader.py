Dialogue(
    'Kimmo Niitty',
    'gui/portraits/leader.png',
    DialogueSection(
        'main_dialog',
        'What do you want?',
        responses=[
            DialogueResponse(
                'Nice office you have here.',
                'feedback_office',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Tell me about this place.',
                'feedback_community',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'You are the one running things around here?',
                'feedback_leader',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Where can I get some booze around here?',
                'help_alcohol',
                actions=[],
                condition=None
            ),
            DialogueResponse(
                'Have you seen Pekko around?',
                'pekko_missing',
                actions=[],
                condition="quest.hasActiveQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
            ),
            DialogueResponse(
                'Your brother is dead.  I think he was murdered.',
                'pekko_dead',
                actions=[],
                condition="quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].getValue('accused_of_murder')"
            ),
            DialogueResponse(
                "I want to talk to about about your brother's murder.",
                'pekko_murdered',
                actions=[
                    SetQuestVariableAction(
                        variable='murder_report_to_kimmo',
                        quest='fedex',
                        value=True
                    )
                ],
                condition="quest['fedex'].getValue('accused_of_murder')"
            ),
            DialogueResponse(
                'Why did you have your brother killed?',
                'confront_kimmo',
                actions=[],
                condition="quest['fedex'].isGoalValue('bart_confesses')"
            ),
            DialogueResponse(
                'I managed to create some palatable beer...',
                'gratitude',
                actions=[],
                condition="quest['beer'].getValue('beer_quality') >= 1"
            ),
            DialogueResponse(
                'See you later.',
                'end',
                actions=[],
                condition=None
            )
        ],
        actions=[
            MeetAction(
                'kimmo'
            )
        ]
    ),
    sections=[
        DialogueSection(
            'help_alcohol',
            "Well, if you've got enough to pay him, Jacob can set you up, over at the Inn.",
            responses=[
                DialogueResponse(
                    'That Jacob must be an important guy around here!',
                    'feedback_jacob',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'No competition, huh?  Must be nice for him.',
                    'booze_business',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'feedback_jacob',
            "Pshaw!  He's a shopkeeper.  It's me who runs thing around here!",
            responses=[
                DialogueResponse(
                    "Oh, so you're the big cheese!",
                    'feedback_leader',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I seem to have touched a nerve... change of subject, Kimmo...',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'booze_business',
            "Yes.  A nice little monopoly he's set up.",
            responses=[
                DialogueResponse(
                    'Sounds like you would not be opposed to ... alternate sources of alcohol?',
                    'beer_competition',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Huh, interesting.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'beer_competition',
            '[Narrows eyes] I think I see where you are going with this.  I cannot challenge Jacob directly on this... but I can look the other way, too',
            responses=[
                DialogueResponse(
                    'Duly noted.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'feedback_leader',
            "I prefer to think of myself as providing `gentle guidance`. Someone has to keep the community in shape.  \nWe have to work together to survive.  \nAnd you know... without proper leadership the community would decay to 'every man for himself'.",
            responses=[
                DialogueResponse(
                    'Well, as long as the Leader is well, taken care of, eh?',
                    'criticize_lifestyle',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Someone has to be foundation; to help hold everything together',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'criticize_lifestyle',
            'I only take what I need to be most... efficient.',
            responses=[
                DialogueResponse(
                    'Efficient, gotcha.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'feedback_office',
            "You like it, huh?  I figure it's my reward for all the hard years. Things have quieted down recently, and they should stay that way.",
            responses=[
                DialogueResponse(
                    'Quiet, huh. I wonder how long it will last.',
                    'talk_moving',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'It suits you.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Well, it sure is fancy.  Good to be the man at the top, huh?',
                    'criticize_lifestyle',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'feedback_community',
            'Ok ... where should I start.',
            responses=[
                DialogueResponse(
                    "Begin at the beginning, I guess - What's the story behind this place?",
                    'explain_origins',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Tell me about your brother, Pekko.',
                    'explain_pekko',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex')"
                ),
                DialogueResponse(
                    'Tell me about Jacob.',
                    'explain_jacob',
                    actions=[],
                    condition="pc.met('jacob')"
                ),
                DialogueResponse(
                    'Tell me about Janie.',
                    'explain_janie',
                    actions=[],
                    condition="pc.met('janie')"
                ),
                DialogueResponse(
                    'Tell me about Bart.',
                    'explain_bart',
                    actions=[],
                    condition="pc.met('bart')"
                ),
                DialogueResponse(
                    'Tell me about your mother,  Aino.',
                    'explain_ma',
                    actions=[],
                    condition="pc.met('ma')"
                ),
                DialogueResponse(
                    'Tell me about Helja.',
                    'explain_helja',
                    actions=[],
                    condition="pc.met('helja')"
                ),
                DialogueResponse(
                    'Tell me about Matti.',
                    'explain_matti',
                    actions=[],
                    condition="pc.met('matti')"
                ),
                DialogueResponse(
                    'Tell me about Skwisgaar.',
                    'explain_skwisgaar',
                    actions=[],
                    condition="pc.met('skwisgaar')"
                ),
                DialogueResponse(
                    'Anyone else I should know about?',
                    'explain_others',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I think I got what I came for.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_others',
            "Well, we have the usual mixed bag of folks.  Everyone works together to keep this place running.  I don't like to talk about folks that aren't mutual aquainances, though.",
            responses=[
                DialogueResponse(
                    "Oh, OK, I'll meet the locals and get back to you.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_skwisgaar',
            "Skwisgaar was Norwegian special forces.  He was sent here during the war to help the Finnish resistance in occupied territories.  After what he's seen and done - he's lucky to be in as good shape as he is.  For some reason everyone here thinks he's Swedish.",
            responses=[
                DialogueResponse(
                    'Yeah, that dude has more than a few screws loose.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_matti',
            "Matti was just a kid when the bombs went off.  He's just not the brightest fellow.  Strong like and ox, too, and innocent as a lamb. Someone's got to shovel all this snow.",
            responses=[
                DialogueResponse(
                    'He seemed nice enough.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I think he may have been involved in your brother's murder",
                    'accuse_matti',
                    actions=[
                        SetQuestVariableAction(
                            variable='accused_of_murder',
                            quest='fedex',
                            value='matti'
                        )
                    ],
                    condition="quest['fedex'].isGoalValue('found_pekko') and quest['fedex'].getValue('murder_reported_to_kimmmo')"
                ),
                DialogueResponse(
                    "I think he may have been involved in your brother's murder",
                    'pekko_dead',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].getValue('murder_reported_to_kimmmo')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_helja',
            "Helja is a rock.  She's been here since the beginning.  Frankly, I don't know what I would do without her keeping track of stuff.  I am more of a motivator than an organizer.",
            responses=[
                DialogueResponse(
                    'She seems very good at her job.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Do you think you can tell her to release some supplies for my beer project',
                    'beer_request',
                    actions=[],
                    condition="quest.hasActiveQuest('beer') and quest['beer'].isGoalValue('beer_instructions') and quest['beer'].getValue('beer_quality') > 0"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'beer_request',
            'Well, that project has no official backing [wink].  But if you have anything to trade her, she always has something extra.',
            responses=[
                DialogueResponse(
                    'Oh, I gotcha.',
                    'feedback_community',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_ma',
            "I don't think I could have made all that you see here without Ma. She is like the spiritual center of our community, the one people go to when they have problems.  I don't know what we would do without her.",
            responses=[
                DialogueResponse(
                    'What is going to happen to her if you migrate south?',
                    'go_south',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "She's clearly a very important part of your society.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'go_south',
            "You've been talking to my brother, haven't you!?!?  Him and his fool ideas.  It's just a harsh winter.  Not even as bad as the first couple after the war. We are staying put, and that's that!",
            responses=[
                DialogueResponse(
                    'But Aino is not going to live forever, and it is getting cold... maybe Pekko is right...',
                    'argue_migration',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Well, I guess that's settled.  Where is your brother, anyway, I wonder...",
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Actually, I am trying to find your Brother, have you seen him?',
                    'pekko_missing',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'argue_migration',
            "It's ridiculous.  We aren't moving.  How can we pack up after all we've invested in this place?",
            responses=[
                DialogueResponse(
                    'I suppose it depends how long you can stay fed.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_janie',
            "Janie's a tough kid - and a good fighter.  Quick with a knife and an acid tongue.  I remember when Pekko brought her in.  She was really just a kid then, couldn't have been more than 5 or 6.  Probably the first act of kindness she ever saw.  She turned out alright, even if she is a little bossy.",
            responses=[
                DialogueResponse(
                    'Bossy is one way to put it.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_bart',
            'Bart is something of a slacker.  But, hell, he was here before the rest of us.  When we found this place, he was trying to drink himself to death on the liquor store.  We probably ended up saving his life by rationing the alcohol.  Still, he can be ... useful.',
            responses=[
                DialogueResponse(
                    'I would have thought alcholism would have been eradicated by now...',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Drunk or not, I think he may have been involved in your brother's murder",
                    'accuse_bart',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko') and quest['fedex'].getValue('murder_reported_to_kimmmo')"
                ),
                DialogueResponse(
                    "Drunk or not, I think he may have been involved in your brother's murder",
                    'pekko_dead',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('found_pekko') and not quest['fedex'].getValue('murder_reported_to_kimmmo')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_jacob',
            'At the time, he seemed like a great addition.  I let him in some years back; we was a traveling salesman and fix-it type.  I thought it would work out for both us.  But he is not happy with his little shop. A very political character.',
            responses=[
                DialogueResponse(
                    'Wow, the steam heating was his idea, huh?  You really must need him.',
                    'continue_jacob',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'continue_jacob',
            "I'll say this for Jacob.  Without him, we'd never have the steam heating system.  Still the guy doesn't know his place, and some of his `loyal cronies` are a bad element.",
            responses=[
                DialogueResponse(
                    'Wow, the steam heating was his idea, huh?  You really must need him.',
                    'feedback_jacob',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'He certainly is pretty arrogant.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_pekko',
            "Ah, my brother the dreamer.  [sighs] He has no idea how the world works.  It was the same before the war, and it's still the same.  I'll miss him.  Always has a theory for everything.  And will talk your ear off if you let him.",
            responses=[
                DialogueResponse(
                    'What do you mean, `miss him`?  Where is he going?',
                    'kimmo_slip',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "You do know he's missing, right?",
                    'pekko_missing',
                    actions=[],
                    condition="quest.hasActiveQuest('fedex') and not quest['fedex'].isGoalValue('found_pekko')"
                ),
                DialogueResponse(
                    "What if he's right about the weather?  That's it's getting worse?  You can't stay here.",
                    'argue_migration',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'It does seem pretty crazy, I agree.  How could it actually get colder?',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'kimmo_slip',
            "Did I say that?  Weird.  I just meant that he's reckless... and one of these days he's might not make it back from one his little jaunts in the woods.",
            responses=[
                DialogueResponse(
                    "Yeah, it is weird.  I'm sure you would miss your brother if he was gone for good...",
                    'feedback_community',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_missing',
            'What do you mean, `missing`?',
            responses=[
                DialogueResponse(
                    'I mean, no one seems to know where I can find him.',
                    'pekko_continue',
                    actions=[
                        SetQuestVariableAction(
                            variable='check_bart_left',
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
            'pekko_continue',
            "Oh, that Pekko.  I'm sure he's just out collecting samples, or measuring snowbanks or something.  You'd think he'd bring something useful back sometimes.",
            responses=[
                DialogueResponse(
                    "So you are pretty sure he's out of town at the moment.",
                    'feedback_community',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'explain_origins',
            "Well, of course Finland was overrun very early in the war.  My battalion fought on for a while, but due to reprisals against the civilians, we were forced to disband.  I grew up not too far from here, and by the time I made it home, there wasn't any Finland, or Russia, or NATO, or Warsaw pact or even any war left.  I hear the war was starting to spread into Africa, South America.  The whole world.  Almost everyone was dead by the time I started to fortify this place.  It has some tactical advantages - can shut out people, plus there was still a good supply of food and clothes and stuff.  We ate almost all the food in the first couple of 'dark' years.  Those were the hardest.  I didn't think we'd ever see the sun again.  I would have given up - my wife and kids killed by some nasty war virus, but Ma convinced me to fight on. That we might be the only people left in the world.  After a while, when the epidemics and fallout had mostly subsided, we began to get some travelers.  This place was quite the trading post for central Finland.  None of the bandit gangs would dare attack it.  We put in the green house when the winters started getting long and the supermarket stuff started to run low.   Jacob and his guys put the steam heating system in, and we'd have never survived the last few years without it.",
            responses=[
                DialogueResponse(
                    'I guess we all have our stories.',
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_matti',
            'Matti? The dim kid?  You think he killed my brother?',
            responses=[
                DialogueResponse(
                    "I can't be sure, but he certainly had access to the cistern. And he seems... unstable.  I could try to find proof it you like.",
                    'investigate',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'accuse_bart',
            'Bart, huh.  Do you have any proof?',
            responses=[
                DialogueResponse(
                    "No proof, yet.  But something about his story isn't right.",
                    'investigate',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Yes, in fact he told me the whole story.  Including your involvement',
                    'confront_kimmo',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_confessed')"
                ),
                DialogueResponse(
                    'Camille.  She saw them together, right before he disappeared. And according to Janie, he never left the compound.',
                    'bart_evidence',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_evidence') and quest['fedex'].isGoalValue('check_pekko_left')"
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'bart_evidence',
            "Uh-huh.  And that's it.  He was the last guy seen with him.  You going to hang your hat on that?",
            responses=[
                DialogueResponse(
                    'Yes.  I am sure that Bart killed your brother.',
                    'bart_convicted',
                    actions=[
                        SetQuestVariableAction(
                            variable='bart_in_trouble',
                            quest='fedex',
                            value=True
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    'I guess it does sound a little flimsy at that.  I can look around a bit more.',
                    'investigate',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'bart_convicted',
            'I guess I will have a little talk with the old boy then.',
            responses=[
                DialogueResponse(
                    'Yes, you do that.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'pekko_dead',
            'Dead?  Murdered... what are you talking about?',
            responses=[
                DialogueResponse(
                    'I found his body in the cistern.',
                    'pekko_murdered',
                    actions=[
                        SetQuestVariableAction(
                            variable='murder_report_to_kimmo',
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
            'pekko_murdered',
            'What makes you think he was murdered?',
            responses=[
                DialogueResponse(
                    "Well, I suppose it was the way his head was smashed in.  That and the fact someone had to dislocate both shoulders to fit him in hatch.  Other than that, it's just a guess.",
                    'murder_continued',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "It might have been an accident.  He could have just fallen in, I suppose.  I'll have to look into it further.",
                    'investigate',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'murder_continued',
            "So you have no proof... [steadies himself]  But this is terrible!  My brother dead. Ah, our poor mother!  Please don't tell her.  Let me.",
            responses=[
                DialogueResponse(
                    'Actually, Kimmo.  Bart confessed to me.',
                    'confront_kimmo',
                    actions=[],
                    condition="quest['fedex'].isGoalValue('drunkard_confessed')"
                ),
                DialogueResponse(
                    'No proof, but if I keep investigating, I am sure something more will turn up.',
                    'investigate',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'I think it must be Matti, the snow shoveler.',
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
                    'I am pretty sure Bart is involved.',
                    'accuse_bart',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'investigate',
            'You know, uh... stranger.  I think it might be best if you let me handle it from here.',
            responses=[
                DialogueResponse(
                    'You want me to drop it?  Well, you are the big cheese around here.',
                    'drop_quest',
                    actions=[
                        CompleteQuestAction(
                            'fedex'
                        )
                    ],
                    condition=None
                ),
                DialogueResponse(
                    "No... no.  I don't think so.  It's going to keep me up not knowing.  I'll continue to poke around on my own.",
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'drop_quest',
            "I think you are doing the right thing... whomever did this might start looking for you, too. [ahem] Assuming it wasn't just an accident.",
            responses=[
                DialogueResponse(
                    'Yeah, good point.',
                    'main_dialog',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'confront_kimmo',
            "WHAT?!  You come into MY office, tell me that my brother's been killed.  And you have to the nerve to accuse me of doing it?",
            responses=[
                DialogueResponse(
                    'Yes, you sick fuck.  How could such a monster come to power here?  I hope the good people of this... this... place have enough nerve to hang you for it.',
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Yes.  Bart told me you put him up to it, for the booze.  But he didn't tell me why.",
                    'why_murder',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    'Well.  Now we find out what you are going to do for me to keep this quiet.',
                    'hush_money',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'why_murder',
            "To be honest, I had to do it.  It was him or me.. him, or all of us. Well, Ma for certain.  He says we can't stay this far north.  But if we pack it up and move, I know a bunch of us will not make it.  And I don't think he's right about the weather, anyway.  You know he never graduated?",
            responses=[
                DialogueResponse(
                    "You better hope you are right, or you're all dead anyway.",
                    'back',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'hush_money',
            "You gonna blackmail me, kid?  Don't count on it.  How about this: You keep your fool mouth shut, or you die next.",
            responses=[
                DialogueResponse(
                    'Is that a threat?  You think I am that easy to disappear? Well, you just try.',
                    'end',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "Hey, now...  I'd say we both have each other pretty good. Truce, then?",
                    'truce',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'truce',
            "Funny way to put it.  But OK...  Don't think that bastard Jacob can protect you, though.   I need him.  I sure as shit don't need you.",
            responses=[
                DialogueResponse(
                    'I guess it will have to do',
                    'end',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'talk_moving',
            "What do you mean, 'you wonder'?  There is no reason why we can't stay here indefinitly.  As long as no outsiders stir up trouble.",
            responses=[
                DialogueResponse(
                    'Oh, no doubt... this place is about as about as ideal as you can get in these times.',
                    'back',
                    actions=[],
                    condition=None
                ),
                DialogueResponse(
                    "I don't know.  I am not sure that any place is permanent in this world.  It doesn't seem that stable to me.",
                    'go_south',
                    actions=[],
                    condition=None
                )
            ],
            actions=[]
        ),
        DialogueSection(
            'gratitude',
            "Heh.  That's put the screws on old Jacob.  I owe you one for that. Let me know if you need a favor - or if his thugs give you any trouble.",
            responses=[
                DialogueResponse(
                    "Thanks, I'll keep that in mind.",
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