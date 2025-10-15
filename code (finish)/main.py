from settings import *
from game_data import *
from birthday_data import BIRTHDAY_STORY_DATA
from pytmx.util_pygame import load_pygame
from os.path import join
from random import randint

from sprites import Sprite, AnimatedSprite, MonsterPatchSprite, BorderSprite, CollidableSprite, TransitionSprite, CollectibleSprite
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree
from monster_index import MonsterIndex
from battle import Battle
from quiz import Quiz
from timer import Timer
from evolution import Evolution

from support import *
from monster import Monster

class Game:
	# general 
	def __init__(self):
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		pygame.display.set_caption('Birthday Adventure: Race Against Time')
		self.clock = pygame.time.Clock()
		self.encounter_timer = Timer(2000, func = self.monster_encounter)
		
		# key press tracking (compatibility for pygame < 2.8)
		self.keys_just_pressed = set()
		
		# Birthday Game: Time System
		self.current_game_time = GAME_START_TIME  # Start at 6:00 PM
		self.game_over = False
		self.game_won = False
		
		# Birthday Game: Item Collection System (3 items needed)
		self.collected_items = {
			'gift': False,
			'flowers': False,
			'cake': False
		}
		
		# Birthday Game: Quest System
		self.quest_started = False  # Has Eman found the note?
		self.show_intro = True  # Show opening message
		self.intro_dismissed = False
		self.show_journal = False  # Toggle quest journal/inventory
		self.ice_area_unlocked = False  # Ice area locked until all items collected
		self.show_ice_blocked_message = False  # Show message when player tries to enter ice
		self.ice_blocked_timer = 0  # Timer for ice blocked message

		# player monsters 
		self.player_monsters = {
			0: Monster('Ivieron', 32),
			1: Monster('Atrox', 15),
			2: Monster('Cindrill', 16),
			3: Monster('Atrox', 10),
			4: Monster('Sparchu', 11),
			5: Monster('Gulfin', 9),
			6: Monster('Jacana', 10),
		}
		for monster in self.player_monsters.values():
			monster.xp += randint(0,monster.level * 100)
		self.test_monsters = {
			0: Monster('Finsta', 15),
			1: Monster('Pouch', 13),
			2: Monster('Larvea', 12),
		}


		# groups 
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()
		self.monster_sprites = pygame.sprite.Group()
		self.collectible_sprites = pygame.sprite.Group()

		# transition / tint
		self.transition_target = None
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		self.import_assets()
		self.setup(self.tmx_maps['world'], 'house')
		self.audio['overworld'].play(-1)

		# overlays 
		self.dialog_tree = None
		self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
		self.index_open = False
		self.battle = None
		self.quiz = None
		self.evolution = None


	def import_assets(self):
		self.tmx_maps = tmx_importer('..', 'data', 'maps')

		self.overworld_frames = {
			'water': import_folder('..', 'graphics', 'tilesets', 'water'),
			'coast': coast_importer(24, 12, '..', 'graphics', 'tilesets', 'coast'),
			'characters': all_character_import('..', 'graphics', 'characters')
		}

		self.monster_frames = {
			'icons': import_folder_dict('..', 'graphics', 'icons'),
			'monsters': monster_importer(4,2,'..', 'graphics', 'monsters'),
			'ui': import_folder_dict('..', 'graphics', 'ui'),
			'attacks': attack_importer('..', 'graphics', 'attacks')
		}
		self.monster_frames['outlines'] = outline_creator(self.monster_frames['monsters'], 4)

		self.fonts = {
			'dialog': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'regular': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'small': pygame.font.Font(join('..', 'graphics', 'fonts', 'PixeloidSans.ttf'), 14),
			'bold': pygame.font.Font(join('..', 'graphics', 'fonts', 'dogicapixelbold.otf'), 20),
		}
		self.bg_frames = import_folder_dict('..', 'graphics', 'backgrounds')
		self.start_animation_frames = import_folder('..', 'graphics', 'other', 'star animation')
	
		self.audio = audio_importer('..', 'audio')
	
	def format_time(self, minutes):
		"""Convert minutes to 12-hour format string"""
		hours = int(minutes // 60)
		mins = int(minutes % 60)
		
		# Convert to 12-hour format
		if hours == 0:
			display_hour = 12
			period = "AM"
		elif hours < 12:
			display_hour = hours
			period = "AM"
		elif hours == 12:
			display_hour = 12
			period = "PM"
		else:
			display_hour = hours - 12
			period = "PM"
		
		return f"{display_hour}:{mins:02d} {period}"
	
	def get_time_remaining(self):
		"""Get remaining time in minutes"""
		return GAME_END_TIME - self.current_game_time
	
	def draw_ui_overlay(self):
		"""Draw time, collectibles, and other UI elements"""
		# Time display (top-right)
		time_str = self.format_time(self.current_game_time)
		time_remaining = self.get_time_remaining()
		
		# Background panel for time
		time_panel = pygame.Surface((200, 80))
		time_panel.fill(COLORS['dark'])
		time_panel.set_alpha(200)
		self.display_surface.blit(time_panel, (WINDOW_WIDTH - 220, 20))
		
		# Current time
		time_surf = self.fonts['regular'].render(f"Time: {time_str}", False, COLORS['white'])
		self.display_surface.blit(time_surf, (WINDOW_WIDTH - 210, 30))
		
		# Time remaining
		hours_left = int(time_remaining // 60)
		mins_left = int(time_remaining % 60)
		
		# Color code based on urgency
		if time_remaining < 60:  # Less than 1 hour
			time_color = COLORS['red']
		elif time_remaining < 120:  # Less than 2 hours
			time_color = COLORS['gold']
		else:
			time_color = COLORS['white']
		
		remaining_surf = self.fonts['small'].render(f"{hours_left}h {mins_left}m left", False, time_color)
		self.display_surface.blit(remaining_surf, (WINDOW_WIDTH - 210, 60))
		
		# Items display (top-left)
		items_panel = pygame.Surface((220, 100))
		items_panel.fill(COLORS['dark'])
		items_panel.set_alpha(200)
		self.display_surface.blit(items_panel, (20, 20))
		
		items_text = self.fonts['regular'].render("Items Collected:", False, COLORS['white'])
		self.display_surface.blit(items_text, (30, 30))
		
		# Show collected items with checkmarks
		y_offset = 55
		for item_name, collected in self.collected_items.items():
			if collected:
				status = "[X]"
				color = COLORS['green']
			else:
				status = "[ ]"
				color = COLORS['white']
			
			item_display = f"{status} {item_name.title()}"
			item_surf = self.fonts['small'].render(item_display, False, color)
			self.display_surface.blit(item_surf, (30, y_offset))
			y_offset += 20
		
		# Journal hint
		journal_hint = self.fonts['small'].render("Press J for Journal", False, COLORS['white'])
		self.display_surface.blit(journal_hint, (20, 85))
	
	def draw_intro_screen(self):
		"""Draw the opening intro message"""
		if not self.show_intro or self.intro_dismissed:
			return
		
		# Semi-transparent overlay
		overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		overlay.fill((0, 0, 0))
		overlay.set_alpha(180)
		self.display_surface.blit(overlay, (0, 0))
		
		# Main message box
		box_width, box_height = 900, 500
		box_x = (WINDOW_WIDTH - box_width) // 2
		box_y = (WINDOW_HEIGHT - box_height) // 2
		
		message_box = pygame.Surface((box_width, box_height))
		message_box.fill(COLORS['white'])
		pygame.draw.rect(message_box, COLORS['gold'], message_box.get_rect(), 5)
		
		# Title
		title = self.fonts['bold'].render("*** HAPPY BIRTHDAY EMAN! ***", False, COLORS['gold'])
		title_rect = title.get_rect(center = (box_width // 2, 40))
		message_box.blit(title, title_rect)
		
		# Message lines
		messages = [
			"",
			"It's your 25th birthday, and something special awaits!",
			"",
			"But first, you need to find a mysterious note...",
			"",
			">> Go inside YOUR HOUSE (the one on the right)",
			"",
			">> Find and read the birthday note",
			"",
			">> Once you read it, your adventure begins!",
			"",
			"You'll have until MIDNIGHT to complete your quest.",
			"",
			"",
			"Press SPACE to begin your birthday adventure!"
		]
		
		y_offset = 100
		for line in messages:
			if line:
				if ">>" in line:
					text_surf = self.fonts['regular'].render(line, False, COLORS['red'])
				else:
					text_surf = self.fonts['regular'].render(line, False, COLORS['black'])
				text_rect = text_surf.get_rect(center = (box_width // 2, y_offset))
				message_box.blit(text_surf, text_rect)
			y_offset += 28
		
		self.display_surface.blit(message_box, (box_x, box_y))
		
		# Handle input to dismiss
		if pygame.K_SPACE in self.keys_just_pressed:
			self.intro_dismissed = True
			self.show_intro = False
	
	def draw_quest_reminder(self):
		"""Show a small reminder if quest hasn't started"""
		if not self.quest_started and self.intro_dismissed:
			reminder_box = pygame.Surface((350, 80))
			reminder_box.fill(COLORS['gold'])
			reminder_box.set_alpha(220)
			
			text1 = self.fonts['small'].render(">> Find the note in your house!", False, COLORS['black'])
			text2 = self.fonts['small'].render("(The house on the right)", False, COLORS['black'])
			
			reminder_box.blit(text1, (20, 20))
			reminder_box.blit(text2, (20, 45))
			
			self.display_surface.blit(reminder_box, (WINDOW_WIDTH // 2 - 175, WINDOW_HEIGHT - 120))
	
	def draw_quest_journal(self):
		"""Show the quest journal/inventory with quest details and collected items"""
		if not self.show_journal:
			return
		
		# Create semi-transparent overlay
		overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		overlay.fill((0, 0, 0))
		overlay.set_alpha(150)
		self.display_surface.blit(overlay, (0, 0))
		
		# Create journal window
		journal_width = 700
		journal_height = 500
		journal_x = (WINDOW_WIDTH - journal_width) // 2
		journal_y = (WINDOW_HEIGHT - journal_height) // 2
		
		journal = pygame.Surface((journal_width, journal_height))
		journal.fill(COLORS['white'])
		pygame.draw.rect(journal, COLORS['gold'], journal.get_rect(), 5)
		
		# Title
		title = self.fonts['bold'].render("QUEST JOURNAL", False, COLORS['gold'])
		journal.blit(title, (journal_width // 2 - title.get_width() // 2, 20))
		
		y_pos = 70
		
		# Quest Status
		if self.quest_started:
			status_text = self.fonts['regular'].render("STATUS: Active", False, COLORS['green'])
		else:
			status_text = self.fonts['regular'].render("STATUS: Not Started", False, COLORS['red'])
		journal.blit(status_text, (30, y_pos))
		y_pos += 40
		
		# Mission Brief
		mission_title = self.fonts['bold'].render("MISSION:", False, COLORS['black'])
		journal.blit(mission_title, (30, y_pos))
		y_pos += 30
		
		mission_lines = [
			"Collect 3 special items for the party:",
			"GIFT, FLOWERS, and CAKE",
			"",
			"Find NPCs around town who will challenge you!",
			"Win battles and answer quiz questions correctly.",
			"",
			"Once you have all 3 items, head to the",
			"ICE AREA (top-left) to find Haider's party!",
			"",
			"Reach the party by MIDNIGHT (12:00 AM)!"
		]
		
		for line in mission_lines:
			text = self.fonts['small'].render(line, False, COLORS['black'])
			journal.blit(text, (50, y_pos))
			y_pos += 25
		
		y_pos += 10
		
		# Items Needed
		items_title = self.fonts['bold'].render("ITEMS TO COLLECT:", False, COLORS['black'])
		journal.blit(items_title, (30, y_pos))
		y_pos += 30
		
		items_info = [
			('Gift', self.collected_items['gift'], 'o2 - Shop Owner'),
			('Flowers', self.collected_items['flowers'], 'o3 - Gardener'),
			('Cake', self.collected_items['cake'], 'o4 - Baker')
		]
		
		for item_name, collected, npc_hint in items_info:
			if collected:
				status = "[X] COLLECTED"
				color = COLORS['green']
			else:
				status = "[ ] Not collected"
				color = COLORS['red']
			
			item_text = self.fonts['regular'].render(f"{item_name}: {status}", False, color)
			journal.blit(item_text, (50, y_pos))
			y_pos += 25
			
			hint_text = self.fonts['small'].render(f"    (From: {npc_hint})", False, COLORS['dark gray'])
			journal.blit(hint_text, (50, y_pos))
			y_pos += 25
		
		y_pos += 10
		
		y_pos += 10
		
		# Hints
		hints_title = self.fonts['bold'].render("HINTS:", False, COLORS['black'])
		journal.blit(hints_title, (30, y_pos))
		y_pos += 30
		
		hint_lines = [
			"- Find o2 (Shop Owner) for the GIFT",
			"- Find o3 (Gardener) for the FLOWERS",
			"- Find o4 (Baker) for the CAKE",
			"- Each NPC will challenge you with battles and quizzes",
			"- Wrong answers add 20 minute time penalty",
			"- Ice area (top-left) is LOCKED until you have all 3 items",
			"- Haider is waiting at the party in the ice area!"
		]
		
		for line in hint_lines:
			text = self.fonts['small'].render(line, False, COLORS['dark gray'])
			journal.blit(text, (50, y_pos))
			y_pos += 22
		
		# Close instruction
		close_text = self.fonts['regular'].render("Press J to close", False, COLORS['gold'])
		journal.blit(close_text, (journal_width // 2 - close_text.get_width() // 2, journal_height - 40))
		
		self.display_surface.blit(journal, (journal_x, journal_y))

	def setup(self, tmx_map, player_start_pos):
		# clear the map
		for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites, self.collectible_sprites):
			group.empty()
		
		# Store current map name for special spawns
		self.current_map = player_start_pos

		# terrain
		for layer in ['Terrain', 'Terrain Top']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])

		# water 
		for obj in tmx_map.get_layer_by_name('Water'):
			for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
				for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
					AnimatedSprite((x,y), self.overworld_frames['water'], self.all_sprites, WORLD_LAYERS['water'])

		# coast
		for obj in tmx_map.get_layer_by_name('Coast'):
			terrain = obj.properties['terrain']
			side = obj.properties['side']
			AnimatedSprite((obj.x, obj.y), self.overworld_frames['coast'][terrain][side], self.all_sprites, WORLD_LAYERS['bg'])
		
		# objects 
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.name == 'top':
				Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
			else:
				CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

		# transition objects
		for obj in tmx_map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

		# collision objects 
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# grass patches 
		for obj in tmx_map.get_layer_by_name('Monsters'):
			MonsterPatchSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.monster_sprites), obj.properties['biome'], obj.properties['monsters'], obj.properties['level'])

		# entities 
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				if obj.properties['pos'] == player_start_pos:
					self.player = Player(
						pos = (obj.x, obj.y), 
						frames = self.overworld_frames['characters']['player'], 
						groups = self.all_sprites,
						facing_direction = obj.properties['direction'], 
						collision_sprites = self.collision_sprites)
					# Add reference to game for party ending logic
					self.player.game = self
			else:
				Character(
					pos = (obj.x, obj.y), 
					frames = self.overworld_frames['characters'][obj.properties['graphic']], 
					groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
					facing_direction = obj.properties['direction'],
					character_data = TRAINER_DATA[obj.properties['character_id']],
					player = self.player,
					create_dialog = self.create_dialog,
					collision_sprites = self.collision_sprites,
					radius = obj.properties['radius'],
					nurse = obj.properties['character_id'] == 'Nurse',
					notice_sound = self.audio['notice'])
		
		# Spawn collectibles based on map and quest status
		self.spawn_collectibles()

	def spawn_collectibles(self):
		"""Spawn collectibles on specific maps if not yet collected"""
		# Define spawn positions for each collectible on specific maps
		collectible_spawns = {
			'world': [
				{'type': 'gift', 'pos': (800, 400)},
				{'type': 'flowers', 'pos': (1200, 600)},
				{'type': 'cake', 'pos': (400, 800)}
			]
		}
		
		# Spawn collectibles for current map if quest is started
		if self.quest_started and self.current_map in collectible_spawns:
			for spawn in collectible_spawns[self.current_map]:
				item_type = spawn['type']
				# Only spawn if not yet collected
				if not self.collected_items[item_type]:
					CollectibleSprite(spawn['pos'], item_type, (self.all_sprites, self.collectible_sprites))
	
	def check_collectibles(self):
		"""Check if player collided with any collectibles"""
		if not self.quest_started:
			return
		
		for collectible in self.collectible_sprites:
			if not collectible.collected and collectible.rect.colliderect(self.player.hitbox):
				# Collect the item
				self.collected_items[collectible.item_type] = True
				collectible.collected = True
				collectible.kill()
				
				# Play sound effect
				self.audio['notice'].play()
	
	# dialog system
	def input(self):
		# Toggle quest journal with J key
		if pygame.K_j in self.keys_just_pressed and self.quest_started:
			self.show_journal = not self.show_journal
			self.player.blocked = self.show_journal
		
		if not self.dialog_tree and not self.battle and not self.quiz and not self.show_journal:
			if pygame.K_SPACE in self.keys_just_pressed:
				for character in self.character_sprites:
					if check_connections(100, self.player, character):
						self.player.block()
						character.change_facing_direction(self.player.rect.center)
						self.create_dialog(character)
						character.can_rotate = False

			if pygame.K_RETURN in self.keys_just_pressed:
				self.index_open = not self.index_open
				self.player.blocked = not self.player.blocked

	def create_dialog(self, character):
		if not self.dialog_tree:
			self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

	def end_dialog(self, character):
		self.dialog_tree = None
		
		# Birthday Game: Check if this is the birthday note
		if character.character_data.get('is_birthday_note', False):
			self.quest_started = True
			self.player.unblock()
			return
		
		if character.nurse:
			for monster in self.player_monsters.values():
				monster.health = monster.get_stat('max_health')
				monster.energy = monster.get_stat('max_energy')

			self.player.unblock()
		elif not character.character_data['defeated']:
			self.audio['overworld'].stop()
			self.audio['battle'].play(-1)
			
			# For birthday game: limit to 1v1 battles
			if self.quest_started and character.monsters:
				# Take only first monster from each side
				player_first = {0: list(self.player_monsters.values())[0]}
				opponent_first = {0: list(character.monsters.values())[0]}
			else:
				# Normal battles for non-quest NPCs
				player_first = self.player_monsters
				opponent_first = character.monsters
			
			self.transition_target = Battle(
				player_monsters = player_first, 
				opponent_monsters = opponent_first, 
				monster_frames = self.monster_frames, 
				bg_surf = self.bg_frames[character.character_data['biome']], 
				fonts = self.fonts, 
				end_battle = self.end_battle,
				character = character, 
				sounds = self.audio)
			self.tint_mode = 'tint'
		else:
			self.player.unblock()
			self.check_evolution()

	# transition system
	def transition_check(self):
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			self.player.block()
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				if type(self.transition_target) == Battle:
					self.battle = self.transition_target
				elif self.transition_target == 'level':
					self.battle = None
				else:
					self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0,0))
	
	def end_battle(self, character):
		self.audio['battle'].stop()
		self.transition_target = 'level'
		self.tint_mode = 'tint'
		
		if character:
			# Check if this character has quiz data (question and options fields)
			has_quiz = ('question' in character.character_data and 
			           'options' in character.character_data and 
			           self.quest_started)
			
			if has_quiz:
				# Start quiz after battle for birthday NPCs
				self.start_quiz(character, None)
			else:
				# Normal flow: mark defeated and show dialog
				character.character_data['defeated'] = True
				self.create_dialog(character)
		elif not self.evolution:
			self.player.unblock()
			self.check_evolution()
	
	def start_quiz(self, character, char_id):
		"""Start a quiz for birthday NPCs after battle"""
		# Use character data directly (from TRAINER_DATA in game_data.py)
		quiz_data = character.character_data
		
		# Create quiz with question from character data
		self.quiz = Quiz(
			question_data=quiz_data,
			fonts=self.fonts,
			end_quiz=self.end_quiz,
			character=character,
			game=self
		)
	
	def end_quiz(self, character):
		"""Called when quiz is complete"""
		self.quiz = None
		character.character_data['defeated'] = True
		
		# Show the result dialog (correct/wrong was already set in quiz)
		self.create_dialog(character)
		
		if not self.evolution:
			self.audio['overworld'].play(-1)

	def check_evolution(self):
		for index, monster in self.player_monsters.items():
			if monster.evolution:
				if monster.level == monster.evolution[1]:
					self.audio['evolution'].play()
					self.player.block()
					self.evolution = Evolution(self.monster_frames['monsters'], monster.name, monster.evolution[0], self.fonts['bold'], self.end_evolution, self.start_animation_frames)
					self.player_monsters[index] = Monster(monster.evolution[0], monster.level)
		if not self.evolution:
			self.audio['overworld'].play(-1)

	def end_evolution(self):
		self.evolution = None
		self.player.unblock()
		self.audio['evolution'].stop()
		self.audio['overworld'].play(-1)

	# monster encounters 
	def check_ice_area_blocking(self):
		"""Block access to ice area until all items are collected"""
		if not self.quest_started:
			return
		
		has_all_items = all(self.collected_items.values())
		
		if not has_all_items:
			player_x = self.player.rect.centerx
			player_y = self.player.rect.centery
			
			# Ice area is in top-left corner
			is_near_ice = player_y < 600 and player_x < 900
			
			if is_near_ice:
				# Push player back
				if self.player.direction.y < 0:
					self.player.rect.y += 3
				if self.player.direction.x < 0:
					self.player.rect.x += 3
				self.ice_blocked_timer = 60
		else:
			self.ice_area_unlocked = True
	
	def draw_ice_blocked_message(self):
		"""Show message when ice area is blocked"""
		if self.ice_blocked_timer > 0:
			box_width, box_height = 600, 120
			box_x = (WINDOW_WIDTH - box_width) // 2
			box_y = WINDOW_HEIGHT - box_height - 50
			
			message_box = pygame.Surface((box_width, box_height))
			message_box.fill(COLORS['red'])
			pygame.draw.rect(message_box, COLORS['white'], message_box.get_rect(), 3)
			
			title = self.fonts['bold'].render("ICE AREA LOCKED!", False, COLORS['white'])
			msg1 = self.fonts['regular'].render("You need all 3 items to enter!", False, COLORS['white'])
			msg2 = self.fonts['small'].render("Collect: Gift, Flowers, and Cake", False, COLORS['white'])
			
			message_box.blit(title, (box_width//2 - title.get_width()//2, 15))
			message_box.blit(msg1, (box_width//2 - msg1.get_width()//2, 50))
			message_box.blit(msg2, (box_width//2 - msg2.get_width()//2, 85))
			
			self.display_surface.blit(message_box, (box_x, box_y))
			self.ice_blocked_timer -= 1
	
	def check_monster(self):
		# Birthday Game: Block encounters until quest starts
		if not self.quest_started:
			return
			
		if [sprite for sprite in self.monster_sprites if sprite.rect.colliderect(self.player.hitbox)] and not self.battle and self.player.direction:
			if not self.encounter_timer.active:
				self.encounter_timer.activate()

	def monster_encounter(self):
		sprites = [sprite for sprite in self.monster_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites and self.player.direction:
			self.encounter_timer.duration = randint(800, 2500)
			self.player.block()
			self.audio['overworld'].stop()
			self.audio['battle'].play(-1)
			self.transition_target = Battle(
				player_monsters = self.player_monsters, 
				opponent_monsters = {index:Monster(monster, sprites[0].level + randint(-3,3)) for index, monster in enumerate(sprites[0].monsters)}, 
				monster_frames = self.monster_frames, 
				bg_surf = self.bg_frames[sprites[0].biome], 
				fonts = self.fonts, 
				end_battle = self.end_battle,
				character = None, 
				sounds = self.audio)
			self.tint_mode = 'tint'

	def run(self):
		while True:
			dt = self.clock.tick() / 1000
			self.display_surface.fill('black')

			# event loop 
			self.keys_just_pressed.clear()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN:
					self.keys_just_pressed.add(event.key)

			# update 
			self.encounter_timer.update()
			self.input()
			self.transition_check()
			self.all_sprites.update(dt)
			self.check_monster()
			self.check_collectibles()
			
			# Birthday Game: Check ice area blocking
			if self.quest_started:
				self.check_ice_area_blocking()
			
			# drawing
			self.all_sprites.draw(self.player)
			
			# Birthday Game: Draw UI overlay
			if self.quest_started:  # Only show time/items after quest starts
				self.draw_ui_overlay()
			
			# Birthday Game: Draw ice blocked message
			if self.ice_blocked_timer > 0:
				self.draw_ice_blocked_message()
			
			# Birthday Game: Draw quest reminder
			self.draw_quest_reminder()
			
			# overlays 
			if self.dialog_tree: self.dialog_tree.update(self.keys_just_pressed)
			if self.index_open:  self.monster_index.update(dt, self.keys_just_pressed)
			if self.battle:      self.battle.update(dt, self.keys_just_pressed)
			if self.quiz:        self.quiz.update(dt, self.keys_just_pressed)
			if self.evolution:   self.evolution.update(dt)

			# Birthday Game: Draw intro screen (on top of everything)
			self.draw_intro_screen()
			
			# Birthday Game: Draw quest journal (on top of everything when open)
			self.draw_quest_journal()

			self.tint_screen(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()