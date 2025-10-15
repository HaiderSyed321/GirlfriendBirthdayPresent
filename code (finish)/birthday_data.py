# Birthday Adventure Story Data
# Custom story for Eman's 25th Birthday

BIRTHDAY_STORY_DATA = {
	# Starting note at home
	'home_note': {
		'dialog': {
			'default': [
				"Happy Birthday, Eman!",
				"I've planned something special for your 25th birthday,",
				"but you'll have to work for it!",
				"",
				"Collect 3 items and reach the party venue by midnight:",
				"[*] A special gift",
				"[*] Beautiful flowers", 
				"[*] Your birthday cake",
				"",
				"Your journey begins now...",
				"Time: 6:00 PM | Deadline: 12:00 AM",
				"",
				"First stop: The Shopping District",
				"- Love, Haider <3"
			]
		}
	},
	
	# Shop Owner - Gift Challenge
	'shop_owner': {
		'monsters': {0: ('Jacana', 14)},  # 1v1 battle then quiz
		'dialog': {
			'default': [
				"Welcome! Looking for the perfect gift?",
				"I have something special, but first...",
				"Let me test if you really know Haider!",
			],
			'correct': [
				"Excellent! You know him well!",
				"Here's the perfect gift for the party.",
				"Haider will love that you remembered!",
				"",
				"*** GIFT COLLECTED! ***",
				"Next stop: The Flower Garden"
			],
			'wrong': [
				"Hmm, not quite right...",
				"But I'll give you the gift anyway!",
				"Just remember: Pad Thai with Beef!",
				"",
				"(+15 minutes time penalty)",
				"*** GIFT COLLECTED! ***",
				"Next stop: The Flower Garden"
			]
		},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest',
		'question': "What's Haider's favorite food?",
		'options': ['A) Sushi', 'B) Pad Thai with Beef', 'C) Pizza', 'D) Burgers'],
		'quiz_answer': 'B',
		'item_reward': 'gift',
		'time_cost': 30,
		'wrong_penalty': 15
	},
	
	# Gardener - Flowers Challenge
	'gardener': {
		'monsters': {0: ('Pluma', 20)},  # 1v1 battle then quiz
		'dialog': {
			'default': [
				"Ah, looking for flowers for someone special?",
				"These blooms are precious - only for true love!"
			],
			'correct': [
				"Beautiful! The Woodsworth water fountain!",
				"That's where your story began...",
				"These flowers are perfect for you!",
				"",
				"*** FLOWERS COLLECTED! ***",
				"Next stop: The Bakery"
			],
			'wrong': [
				"Not quite, but close!",
				"It was at the Woodsworth water fountain!",
				"Take these flowers anyway!",
				"",
				"(+15 minutes time penalty)",
				"*** FLOWERS COLLECTED! ***",
				"Next stop: The Bakery"
			]
		},
		'directions': ['right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest',
		'question': "Where did you and Haider first meet?",
		'options': ['A) At a coffee shop', 'B) At Woodsworth College water fountain', 'C) At the library', 'D) At a party'],
		'quiz_answer': 'B',
		'item_reward': 'flowers',
		'time_cost': 30,
		'wrong_penalty': 15
	},
	
	# Baker - Cake Challenge
	'baker': {
		'monsters': {0: ('Charmadillo', 25)},  # 1v1 battle then quiz
		'dialog': {
			'default': [
				"A birthday cake? How wonderful!",
				"This is a special order from Haider himself!",
				"But I need to make sure you're the right person..."
			],
			'correct': [
				"December 2019! Almost 6 years together!",
				"Here's your beautiful birthday cake!",
				"Haider ordered it specially for you.",
				"",
				"*** CAKE COLLECTED! ***",
				"Now hurry to the party venue!",
				"You have everything you need!"
			],
			'wrong': [
				"Hmm, let me check my notes...",
				"Ah yes! December 2019!",
				"Here's your cake anyway!",
				"",
				"(+15 minutes time penalty)",
				"*** CAKE COLLECTED! ***",
				"Now hurry to the party venue!"
			]
		},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'sand',
		'question': "When did you two start dating?",
		'options': ['A) November 2019', 'B) December 2019', 'C) January 2020', 'D) December 2018'],
		'quiz_answer': 'B',
		'item_reward': 'cake',
		'time_cost': 30,
		'wrong_penalty': 15
	},
	
	# Friend - Helpful NPC
	'friend_helper': {
		'monsters': {},
		'dialog': {
			'default': [
				"Hey Eman! Happy Birthday!",
				"Haider told me about his surprise!",
				"You're doing great - keep going!",
				"",
				"Tip: Answer the questions correctly",
				"to save time! Every minute counts!"
			],
			'defeated': [
				"Good luck! You've got this!"
			]
		},
		'directions': ['down', 'right'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	
	# Time Waster - Obstacle NPC
	'procrastination': {
		'monsters': {},
		'dialog': {
			'default': [
				"Hey! Want to chat for a bit?",
				"No rush, right? The party can wait...",
				"Let me tell you about my day..."
			],
			'defeated': [
				"Oh, you're in a hurry? Okay then!",
				"",
				"(+10 minutes wasted)"
			]
		},
		'directions': ['left', 'right'],
		'look_around': True,
		'defeated': False,
		'biome': 'forest',
		'time_cost': 10
	},
	
	# Haider - Final NPC at Party
	'haider_party': {
		'monsters': {},
		'dialog': {
			'perfect': [
				"Eman! You made it with time to spare!",
				"And you brought everything!",
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
				"Now let's celebrate!"
			],
			'good': [
				"Eman! You made it just in time!",
				"That was close!",
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
				"The party is just beginning!"
			],
			'late': [
				"Eman! You're here!",
				"A bit late, but that's okay!",
				"Fashionably late, as always!",
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
				"Better late than never! Let's party!"
			],
			'too_late': [
				"Eman! There you are!",
				"I was getting worried...",
				"",
				"The party already started, but",
				"I saved you a seat! <3",
				"",
				"Happy Birthday my love.",
				"",
				"I'm so sorry I was not there to help you",
				"celebrate your birthday this year.",
				"",
				"Happy 25th Birthday.",
				"I love you more than you can ever imagine. <3",
				"",
				"Let's celebrate together!"
			],
			'incomplete': [
				"Eman! You're here!",
				"But... where are the items?",
				"",
				"Don't worry, the party can wait!",
				"Go back and collect:",
				"[*] Gift (if missing)",
				"[*] Flowers (if missing)",
				"[*] Cake (if missing)",
				"",
				"I'll be waiting right here! <3"
			]
		},
		'directions': ['down'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest'
	},
	
	# Memory Challenge - Optional
	'memory_challenge': {
		'monsters': {},
		'dialog': {
			'default': [
				"Hey! Want to test your memory?",
				"",
				"QUESTION: Where was your first date?",
				"A) ROM Museum in Toronto",
				"B) CN Tower",
				"C) Ripley's Aquarium",
				"D) Casa Loma"
			],
			'correct': [
				"Perfect! The ROM Museum!",
				"What a special first date that was!",
				"",
				"Here's a shortcut for you!",
				"(-15 minutes saved!)"
			],
			'wrong': [
				"Not quite! It was the ROM Museum!",
				"But nice try!",
				"Keep going!"
			]
		},
		'directions': ['up', 'down'],
		'look_around': False,
		'defeated': False,
		'biome': 'forest',
		'quiz_answer': 'A',
		'time_bonus': -15  # Negative = saves time!
	}
}

# Quiz Questions Bank (for variety)
QUIZ_QUESTIONS = [
	{
		'question': "What's Haider's favorite food?",
		'options': ['A) Sushi', 'B) Pad Thai with Beef', 'C) Pizza', 'D) Burgers'],
		'answer': 'B',
		'hint': "It's Thai food with beef!"
	},
	{
		'question': "Where did you first meet?",
		'options': ['A) Coffee shop', 'B) Woodsworth College water fountain', 'C) Library', 'D) Party'],
		'answer': 'B',
		'hint': "At a water fountain on campus!"
	},
	{
		'question': "When did you start dating?",
		'options': ['A) November 2019', 'B) December 2019', 'C) January 2020', 'D) December 2018'],
		'answer': 'B',
		'hint': "Almost 6 years ago, in winter!"
	},
	{
		'question': "Where was your first date?",
		'options': ['A) ROM Museum', 'B) CN Tower', 'C) Aquarium', 'D) Casa Loma'],
		'answer': 'A',
		'hint': "A museum in Toronto!"
	},
	{
		'question': "What's Eman's favorite food?",
		'options': ['A) Italian', 'B) Korean Barbecue', 'C) Mexican', 'D) Chinese'],
		'answer': 'B',
		'hint': "Grilled meat, Korean style!"
	}
]

