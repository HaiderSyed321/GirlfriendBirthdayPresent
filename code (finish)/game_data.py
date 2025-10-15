TRAINER_DATA = {
	'o1': {
		'monsters': {0: ('Jacana', 14), 1: ('Cleaf', 15)},
		'dialog': {
			'before_quest': ['Hey Eman! Happy Birthday!', 'Shouldn\'t you check your house first?', 'I think someone left you something...'],
			'default': ['Hey, how are you?', 'Oh, so you want to fight?', 'FIGHT!'], 
			'defeated': ['You are very strong!', 'Let\'s fight again sometime?']},
		'directions': ['down'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest'
		},
	'o2': {
		'monsters': {0: ('Jacana', 18), 1: ('Pluma', 20)},  # Birthday NPC: Shop Owner (2 battles!)
		'dialog': {
			'default': [
				"Eman! Happy Birthday!",
				"I have the perfect GIFT for Haider's party!",
				"But first... let me see if you're worthy!",
				"",
				"Prepare for battle!"
			],
			'pre_quiz': [
				"Ah shucks! You beat all my monsters!",
				"You're really strong, Eman!",
				"",
				"But if you want the GIFT...",
				"You must answer my quiz question correctly!",
				"",
				"Get it wrong and you'll have to battle me again!",
				"Ready?"
			],
			'correct': [
				"Excellent! You really know Haider!",
				"Here's the GIFT for the party!",
				"",
				"Now head to the ice area (top-left)",
				"once you have all 3 items!",
				"",
				"*** GIFT COLLECTED! ***"
			],
			'wrong': [
				"Oops! That's not quite right...",
				"You'll need to try again!",
				"",
				"Battle me again and I'll give you",
				"another chance at the quiz!",
				"",
				"(+20 minutes time penalty)"
			],
			'defeated': [
				"You already got the GIFT from me!",
				"Keep collecting the other items!",
				"",
				"Don't forget - you need all 3 items",
				"to enter the ice area!"
			]
		},
		'directions': ['left', 'down'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest',
		'question': "What's Haider's favorite food?",
		'options': ['A) Sushi', 'B) Pad Thai with Beef', 'C) Pizza', 'D) Burgers'],
		'quiz_answer': 'B',
		'item_reward': 'gift',
		'time_cost': 45,
		'wrong_penalty': 20
		},
	'o3': {
		'monsters': {0: ('Atrox', 22), 1: ('Finsta', 24)},  # Birthday NPC: Gardener (2 battles!)
		'dialog': {
			'default': [
				"Ah, Eman! Looking for FLOWERS?",
				"These are special birthday flowers for Haider!",
				"But I need to make sure you're the right person...",
				"",
				"Let's battle!"
			],
			'pre_quiz': [
				"Wow! You defeated all my monsters!",
				"Impressive skills, Eman!",
				"",
				"But before I give you the FLOWERS...",
				"Answer my relationship quiz correctly!",
				"",
				"Get it wrong? You'll battle me again!",
				"Here's your question..."
			],
			'correct': [
				"Beautiful! The Woodsworth water fountain!",
				"That's where your love story began...",
				"These FLOWERS are perfect for the party!",
				"",
				"Collect all 3 items, then head to",
				"the ice area to find Haider!",
				"",
				"*** FLOWERS COLLECTED! ***"
			],
			'wrong': [
				"Hmm, that's not right!",
				"It was at Woodsworth College water fountain!",
				"",
				"Come back and battle me again",
				"for another shot at the quiz!",
				"",
				"(+20 minutes time penalty)"
			],
			'defeated': [
				"You already have the FLOWERS!",
				"Keep going, Eman!",
				"",
				"Collect all 3 items to unlock",
				"the ice area party!"
			]
		},
		'directions': ['left', 'right', 'up', 'down'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest',
		'question': "Where did you and Haider first meet?",
		'options': ['A) At a coffee shop', 'B) At Woodsworth College water fountain', 'C) At the library', 'D) At a party'],
		'quiz_answer': 'B',
		# Flowers are now a progressive count; this NPC grants 5 flowers
		'flowers_reward': 5,
		'time_cost': 45,
		'wrong_penalty': 20
		},
	'o4': {
		'monsters': {0: ('Charmadillo', 26), 1: ('Friolera', 28)},  # Birthday NPC: Baker (2 battles!)
		'dialog': {
			'default': [
				"Eman! Perfect timing!",
				"I have a birthday CAKE ready for Haider!",
				"But first, let me test if you deserve it...",
				"",
				"Show me what you've got!"
			],
			'pre_quiz': [
				"Oh no! You beat all my monsters!",
				"You're too strong, Eman!",
				"",
				"But wait! To get the CAKE...",
				"You must prove your love with a quiz!",
				"",
				"Wrong answer = battle me again!",
				"Let's see what you know..."
			],
			'correct': [
				"December 2019! Almost 6 years together!",
				"What a beautiful journey you two have had!",
				"Here's the birthday CAKE!",
				"",
				"Once you have all 3 items,",
				"head to the ice area for the party!",
				"",
				"*** CAKE COLLECTED! ***"
			],
			'wrong': [
				"Oops! Not quite right!",
				"The correct answer is December 2019!",
				"",
				"You'll need to battle me again",
				"to try the quiz once more!",
				"",
				"(+20 minutes time penalty)"
			],
			'defeated': [
				"You already got the CAKE!",
				"How's your collection going?",
				"",
				"Remember - all 3 items needed",
				"to access the ice area!"
			]
		},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand',
		'question': "When did you two start dating?",
		'options': ['A) November 2019', 'B) December 2019', 'C) January 2020', 'D) December 2018'],
		'quiz_answer': 'B',
		'item_reward': 'cake',
		'time_cost': 45,
		'wrong_penalty': 20
		},
	'o5': {
		'monsters': {},  # Birthday NPC: Haider at Party - NO BATTLE
		'dialog': {
			'default': [
				"Eman! You're here at the ice area!",
				"Do you have everything for the party?"
			],
			'perfect': [
				"Eman! You made it with time to spare!",
				"And you brought the Gift, Flowers, AND Cake!",
				"",
				"Welcome to your birthday party!",
				"",
				"Happy Birthday my love.",
				"Congrats on beating all the challenges today.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day",
				"and wonderful time.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** PERFECT ENDING ***",
				"Now let's celebrate in the ice!"
			],
			'good': [
				"Eman! You made it just in time!",
				"That was close! But you got all 3 items!",
				"",
				"Welcome to the party!",
				"",
				"Happy Birthday my love.",
				"You did it! I knew you could!",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** GOOD ENDING ***",
				"The party is just beginning!"
			],
			'late': [
				"Eman! You're here!",
				"A bit late, but you got all 3 items!",
				"Fashionably late, as always!",
				"",
				"Welcome to the party!",
				"",
				"Happy Birthday my love.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** LATE ENDING ***",
				"Better late than never! Let's party!"
			],
			'too_late': [
				"Eman! There you are!",
				"I was getting worried...",
				"",
				"But you got all 3 items! That's what matters!",
				"The party already started in the ice area, but",
				"I saved you a special spot! <3",
				"",
				"Happy Birthday my love.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** TOO LATE ENDING ***",
				"Let's celebrate together!"
			],
			'incomplete': [
				"Eman! You found the ice area party!",
				"But... you're missing some items!",
				"",
				"I need you to bring:",
				"[*] Gift (if you don't have it)",
				"[*] Flowers (if you don't have it)",
				"[*] Cake (if you don't have it)",
				"",
				"Don't worry, the party will wait!",
				"Go back and collect all 3 items!",
				"",
				"The ice area entrance will stay open for you.",
				"I'll be waiting right here! <3"
			]
		},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest',
		'is_party_npc': True  # Special flag for ending detection
		},
	'o6': {
		'monsters': {0: ('Finsta', 15)},  # Birthday NPC: Quiz #4
		'dialog': {
			'default': [
				"Another birthday question!",
				"This one's about a special moment...",
				"Can you remember?"
			],
			'correct': [
				"December 3rd 2019! What a magical day!",
				"That first kiss was unforgettable!",
				"Here are 5 more flowers!"
			],
			'wrong': [
				"Not quite! It was December 3rd 2019!",
				"But that's okay, memories can blur!",
				"No flowers, but keep going!",
				"(+15 minutes time penalty)"
			]
		},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice',
		'question': "What day was your first kiss with Haider?",
		'options': ['A) December 10th 2019', 'B) December 3rd 2019', 'C) December 5th 2019', 'D) December 1st 2019'],
		'quiz_answer': 'B',
		'flowers_reward': 5,
		'time_cost': 30,
		'wrong_penalty': 15
		},
	'o7': {
		'monsters': {0: ('Friolera', 18)},  # Birthday NPC: Quiz #5 (Joke Question)
		'dialog': {
			'default': [
				"Haha! This question is a funny one...",
				"Haider says he can't remember!",
				"But let's see what you say..."
			],
			'correct': [
				"Haha! Haider told me he actually has no idea",
				"so you pass! All answers were correct!",
				"Here are 5 flowers anyway!"
			],
			'wrong': [
				"Wait... Haider told me he actually has no idea",
				"so you pass! All answers were correct!",
				"Here are 5 flowers anyway!"
			]
		},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice',
		'question': "What is the word Haider secretly told you to remember in Dubai?",
		'options': ['A) Skibidyblumpkin', 'B) ShipidyDipidyBooty', 'C) Lilimunchinmcgee', 'D) All of the above'],
		'quiz_answer': 'ALL',  # Special: all answers correct
		'flowers_reward': 5,
		'time_cost': 30,
		'wrong_penalty': 0  # No penalty - it's a joke question
		},
	'p1': {
		'monsters': {0: ('Atrox', 20)},  # Birthday NPC: Quiz #6
		'dialog': {
			'default': [
				"One more question!",
				"This one's about food...",
				"What does Haider cook best for you?"
			],
			'correct': [
				"Gochujang pasta! Absolutely delicious!",
				"He really knows how to cook for you!",
				"Here are your final 5 flowers!"
			],
			'wrong': [
				"Nope! It's the Gochujang pasta!",
				"That's his specialty for you!",
				"No flowers, but you tried!",
				"(+15 minutes time penalty)"
			]
		},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest',
		'question': "What's your favorite meal Haider cooks?",
		'options': ['A) Gochujang pasta', 'B) Fried calamari', 'C) Mushroom Pie', 'D) Sushi'],
		'quiz_answer': 'A',
		'flowers_reward': 5,
		'time_cost': 30,
		'wrong_penalty': 15
		},
	'p2': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'p3': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'p4': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Atrox',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['I love trees', 'and fights'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'px': {
		# ARENA.TMX boss - awards Arena Badge upon defeat (plant arena)
		'monsters': {0: ('Draem', 30), 1: ('Gulfin', 32), 2: ('Finiette', 34)},
		'dialog': {
			'default': [
				"Welcome to the Arena of Nature!",
				"Win to earn the ARENA BADGE!"
			], 
			'defeated': [
				"You proved your strength! ARENA BADGE awarded!",
				"The Water Arena awaits for the final celebration."
			]},
		'battle_reward': 'arena_badge',
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
		},
	'w1': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w2': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w3': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w4': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'w5': {
		'monsters': {0: ('Friolera', 25), 1: ('Gulfin', 20), 2: ('Draem',24), 3: ('Finiette', 30)},
		'dialog': {
			'default': ['It\'s so cold in here', 'maybe a fight will warm me up'], 
			'defeated': ['Good luck with the boss!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'ice'
		},
	'wx': {
		# Final party NPC (Haider) in water.tmx
		'monsters': {},
		'dialog': {
			'default': [
				"Eman! You're here at the water arena!",
				"Do you have everything for the party?"
			],
			'perfect': [
				"Eman! You made it with time to spare!",
				"And you brought everything for our party!",
				"",
				"Welcome to your birthday party!",
				"",
				"Happy Birthday my love.",
				"Congrats on beating all the challenges today.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day",
				"and wonderful time.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** PERFECT ENDING ***",
				"Now let's celebrate by the water!"
			],
			'good': [
				"Eman! You made it just in time!",
				"That was close! But you got everything!",
				"",
				"Welcome to the party!",
				"",
				"Happy Birthday my love.",
				"You did it! I knew you could!",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** GOOD ENDING ***",
				"The party is just beginning!"
			],
			'late': [
				"Eman! You're here!",
				"A bit late, but you got everything!",
				"Fashionably late, as always!",
				"",
				"Welcome to the party!",
				"",
				"Happy Birthday my love.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year,",
				"but I hope you have an amazing day.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** LATE ENDING ***",
				"Better late than never! Let's party!"
			],
			'too_late': [
				"Eman! There you are!",
				"I was getting worried...",
				"",
				"But you got all the items! That's what matters!",
				"The party already started by the water, but",
				"I saved you a special spot! <3",
				"",
				"Happy Birthday my love.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"*** TOO LATE ENDING ***",
				"Let's celebrate together!"
			],
			'incomplete': [
				"Eman! You found the final party!",
				"But... you're missing some items!",
				"",
				"Bring: Gift, Cake, 15 Flowers, Fire Badge, Arena Badge",
				"",
				"Don't worry, the party will wait!",
				"I'll be right here by the water! <3"
			]
		},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'ice',
		'is_party_npc': True
		},
	'f1': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f2': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['right', 'left'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
		},
	'f3': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['right', 'left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f4': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['up', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f5': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['left'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'f6': {
		'monsters': {0: ('Cindrill', 15), 1: ('Jacana', 20), 2: ('Draem',24), 3: ('Atrox', 30)},
		'dialog': {
			'default': ['This place feels kinda warm...', 'fight!'], 
			'defeated': ['Congratultion!']},
		'directions': ['right'],
		'look_around': True,
		'defeated': False,
		'biome': 'sand'
		},
	'fx': {
		# FIRE.TMX boss - awards Fire Badge upon defeat
		'monsters': {0: ('Cindrill', 32), 1: ('Atrox', 34), 2: ('Charmadillo', 36)},
		'dialog': {
			'default': [
				"Welcome to the Fire Arena!",
				"Defeat me and earn the FIRE BADGE!"
			], 
			'defeated': [
				"You bested the flames! FIRE BADGE awarded!",
				"Head to the Arena next for the ARENA BADGE."
			]},
		'battle_reward': 'fire_badge',
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand'
		},
	'Nurse': {
		'direction': 'down',
		'radius': 0,
		'look_around': False,
		'dialog': {
			'default': ['Welcome to the hospital', 'Your monsters have been healed'], 
			'defeated': None},
		'directions': ['down'],
		'defeated': False,
		'biome': None
		},
	'NoteKeeper': {
		'direction': 'down',
		'radius': 0,
		'look_around': False,
		'dialog': {
			'default': [
				'Hey Eman! Happy Birthday!',
				'',
				'I heard you were looking for something?',
				'',
				'Haider dropped off a note for you earlier!',
				'Said it was super important...',
				'',
				'Here, let me read it to you:',
				'',
				'===============================',
				'',
				'*** HAPPY BIRTHDAY EMAN! ***',
				'',
				'Welcome to your 25th birthday adventure!',
				'',
				'I have planned something special, but',
				'you will have to work for it!',
				'',
				'YOUR MISSION:',
				'Collect 3 special items and reach the',
				'party venue by MIDNIGHT (12:00 AM)',
				'',
				'THE ITEMS YOU NEED:',
				'[*] A perfect birthday gift',
				'[*] Beautiful flowers',
				'[*] Your birthday cake',
				'',
				'THE JOURNEY:',
				'[1] Shopping District - Get the gift',
				'[2] Flower Garden - Pick flowers',
				'[3] Bakery - Collect your cake',
				'[4] Party Venue - Find me!',
				'',
				'IMPORTANT:',
				'>> Time: 6:00 PM -> Deadline: 12:00 AM',
				'>> Answer questions correctly to save time!',
				'>> Each wrong answer = 15 min penalty',
				'',
				'I believe in you! Now go! The clock',
				'is ticking...',
				'',
				'With all my love,',
				'- Haider <3',
				'',
				'===============================',
				'',
				'Wow! That sounds exciting!',
				'',
				'You better get going, Eman!',
				'Time is ticking!',
				'',
				'Good luck on your adventure!',
				'',
				'[QUEST STARTED! Check top-right for time]'
			],
			'defeated': None
		},
		'directions': ['down'],
		'defeated': False,
		'biome': None,
		'is_birthday_note': True
		}
}

MONSTER_DATA = {
	'Plumette': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 4, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Ivieron', 15)},
	'Ivieron': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 5, 'defense': 10, 'recovery': 1.2, 'speed': 1.2},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Pluma', 32)},
	'Pluma': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 26, 'attack': 6, 'defense': 12, 'recovery': 1.8, 'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': None},
	'Sparchu': {
		'stats': {'element': 'fire', 'max_health': 15, 'max_energy': 7, 'attack': 3, 'defense': 8, 'recovery': 1.1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26:'explosion'},
		'evolve': ('Cindrill', 15)},
	'Cindrill': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 10, 'attack': 3.5, 'defense': 10, 'recovery': 1.2, 'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26:'explosion'},
		'evolve': ('Charmadillo', 33)},
	'Charmadillo': {
		'stats': {'element': 'fire', 'max_health': 29, 'max_energy': 12, 'attack': 4, 'defense': 17, 'recovery': 1.35, 'speed': 1.1},
		'abilities': {0: 'scratch', 5: 'fire', 15: 'battlecry', 26:'explosion', 45: 'annihilate'},
		'evolve': None},
	'Finsta': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 17, 'attack': 2, 'defense': 8, 'recovery': 1.5, 'speed': 1.8},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Gulfin', 34)},
	'Gulfin': {
		'stats': {'element': 'water', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.8, 'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': ('Finiette', 45)},
	'Finiette': {
		'stats': {'element': 'water', 'max_health': 27, 'max_energy': 23, 'attack': 4, 'defense': 17, 'recovery': 2, 'speed': 2.5},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
	'Atrox': {
		'stats': {'element': 'fire', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.3, 'speed': 1.9},
		'abilities': {0: 'scratch', 5: 'spark', 30: 'fire'},
		'evolve': None},
	'Pouch': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1, 'speed': 1.5},
		'abilities': {0: 'scratch', 5: 'spark', 25: 'heal'},
		'evolve': None},
	'Draem': {
		'stats': {'element': 'plant', 'max_health': 23, 'max_energy': 25, 'attack': 4, 'defense': 12, 'recovery': 1.2, 'speed': 1.4},
		'abilities': {0: 'scratch', 5: 'heal', 20: 'explosion', 25: 'splash'},
		'evolve': None},
	'Larvea': {
		'stats': {'element': 'plant', 'max_health': 15, 'max_energy': 17, 'attack': 1, 'defense': 8, 'recovery': 1, 'speed': 1},
		'abilities': {0: 'scratch', 5: 'spark'},
		'evolve': ('Cleaf', 4)},
	'Cleaf': {
		'stats': {'element': 'plant', 'max_health': 18, 'max_energy': 20, 'attack': 3, 'defense': 10, 'recovery': 1.7, 'speed': 1.6},
		'abilities': {0: 'scratch', 5: 'heal'},
		'evolve': None},
	'Jacana': {
		'stats': {'element': 'fire', 'max_health': 12, 'max_energy': 19, 'attack': 3, 'defense': 10, 'recovery': 2.1, 'speed': 2.6},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'burn', 20: 'explosion', 25: 'heal'},
		'evolve': None},
	'Friolera': {
		'stats': {'element': 'water', 'max_health': 13, 'max_energy': 20, 'attack': 4, 'defense': 6, 'recovery': 1.3, 'speed': 2},
		'abilities': {0: 'scratch', 5: 'spark', 15: 'splash', 20: 'ice', 25: 'heal'},
		'evolve': None},
}

ATTACK_DATA = {
	'burn':       {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'fire',   'animation': 'fire'},
	'heal':       {'target': 'player',   'amount': -1.2, 'cost': 600, 'element': 'plant',  'animation': 'green'},
	'battlecry':  {'target': 'player',   'amount': -1.4, 'cost': 20, 'element': 'normal', 'animation': 'green'},
	'spark':      {'target': 'opponent', 'amount': 1.1,  'cost': 20, 'element': 'fire',   'animation': 'fire'},
	'scratch':    {'target': 'opponent', 'amount': 1.2,  'cost': 20, 'element': 'normal', 'animation': 'scratch'},
	'splash':     {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'water',  'animation': 'splash'},
	'fire':       {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'fire',   'animation': 'fire'},
	'explosion':  {'target': 'opponent', 'amount': 2,    'cost': 90, 'element': 'fire',   'animation': 'explosion'},
	'annihilate': {'target': 'opponent', 'amount': 3,    'cost': 30, 'element': 'fire',   'animation': 'explosion'},
	'ice':        {'target': 'opponent', 'amount': 2,    'cost': 15, 'element': 'water',  'animation': 'ice'},
}