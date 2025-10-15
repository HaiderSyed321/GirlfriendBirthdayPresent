from settings import *
from game_data import *
from birthday_data import BIRTHDAY_STORY_DATA
from pytmx.util_pygame import load_pygame
from os.path import join
from random import randint
import json

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
		
		# Birthday Game: Item Collection System (5 items total)
		# - gift: boolean
		# - cake: boolean
		# - flowers_count: integer progress toward 15
		# - fire_badge: boolean (earned by defeating FIRE boss)
		# - arena_badge: boolean (earned by defeating ARENA boss)
		self.collected_items = {
			'gift': False,
			'cake': False,
			'flowers_count': 0,
			'fire_badge': False,
			'arena_badge': False
		}
		
		# Birthday Game: Quest System
		self.quest_started = False  # Has Eman found the note?
		self.show_intro = True  # Show opening message
		self.intro_dismissed = False
		self.show_journal = False  # Toggle quest journal/inventory
		self.ice_area_unlocked = False  # Ice area locked until all items collected
		self.show_ice_blocked_message = False  # Show message when player tries to enter ice
		self.ice_blocked_timer = 0  # Timer for ice blocked message
		
		# Music control
		self.music_muted = False

		# Save system
		self.save_file = join('savegame.json')
		self.save_message = None
		self.save_message_timer = Timer(1200)

		# player monsters 
		self.player_monsters = {
			0: Monster('Ivieron', 50),
			1: Monster('Atrox', 42),
			2: Monster('Cindrill', 46),
			3: Monster('Atrox', 40),
			4: Monster('Sparchu', 44),
			5: Monster('Gulfin', 43),
			6: Monster('Jacana', 41),
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
		self.show_final_message = False
		self.show_final_message = False


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
		items_panel = pygame.Surface((260, 160))
		items_panel.fill(COLORS['dark'])
		items_panel.set_alpha(200)
		self.display_surface.blit(items_panel, (20, 20))
		
		items_text = self.fonts['regular'].render("Items Collected:", False, COLORS['white'])
		self.display_surface.blit(items_text, (30, 30))
		
		# Show collected items with checkmarks / progress
		y_offset = 55
		# Gift
		gift_collected = self.collected_items.get('gift', False)
		gift_text = self.fonts['small'].render(f"{'[X]' if gift_collected else '[ ]'} Gift", False, COLORS['green'] if gift_collected else COLORS['white'])
		self.display_surface.blit(gift_text, (30, y_offset)); y_offset += 20
		# Cake
		cake_collected = self.collected_items.get('cake', False)
		cake_text = self.fonts['small'].render(f"{'[X]' if cake_collected else '[ ]'} Cake", False, COLORS['green'] if cake_collected else COLORS['white'])
		self.display_surface.blit(cake_text, (30, y_offset)); y_offset += 20
		# Flowers progress (15 required)
		flowers_count = int(self.collected_items.get('flowers_count', 0))
		flowers_done = flowers_count >= 15
		flowers_text = self.fonts['small'].render(f"{'[X]' if flowers_done else '[ ]'} Flowers {flowers_count}/15", False, COLORS['green'] if flowers_done else COLORS['white'])
		self.display_surface.blit(flowers_text, (30, y_offset)); y_offset += 20
		# Fire badge
		fire_badge = self.collected_items.get('fire_badge', False)
		fire_text = self.fonts['small'].render(f"{'[X]' if fire_badge else '[ ]'} Fire Badge", False, COLORS['green'] if fire_badge else COLORS['white'])
		self.display_surface.blit(fire_text, (30, y_offset)); y_offset += 20
		# Arena badge
		arena_badge = self.collected_items.get('arena_badge', False)
		arena_text = self.fonts['small'].render(f"{'[X]' if arena_badge else '[ ]'} Arena Badge", False, COLORS['green'] if arena_badge else COLORS['white'])
		self.display_surface.blit(arena_text, (30, y_offset)); y_offset += 20
		
		# Journal hint - moved to bottom right to avoid overlap
		journal_hint = self.fonts['small'].render("Press J for Journal", False, COLORS['white'])
		journal_hint_shadow = self.fonts['small'].render("Press J for Journal", False, COLORS['black'])
		hint_x = WINDOW_WIDTH - journal_hint.get_width() - 20
		hint_y = WINDOW_HEIGHT - 40
		self.display_surface.blit(journal_hint_shadow, (hint_x + 2, hint_y + 2))
		self.display_surface.blit(journal_hint, (hint_x, hint_y))
		
		# Music mute hint - below journal hint
		music_status = "MUTED" if self.music_muted else "ON"
		music_hint = self.fonts['small'].render(f"Press M: Music {music_status}", False, COLORS['white'])
		music_hint_shadow = self.fonts['small'].render(f"Press M: Music {music_status}", False, COLORS['black'])
		music_x = WINDOW_WIDTH - music_hint.get_width() - 20
		music_y = WINDOW_HEIGHT - 65
		self.display_surface.blit(music_hint_shadow, (music_x + 2, music_y + 2))
		self.display_surface.blit(music_hint, (music_x, music_y))

		# Save/load hint and transient status
		save_hint = self.fonts['small'].render("F5: Save  F9: Load", False, COLORS['white'])
		save_hint_shadow = self.fonts['small'].render("F5: Save  F9: Load", False, COLORS['black'])
		sh_x = 20
		sh_y = WINDOW_HEIGHT - 40
		self.display_surface.blit(save_hint_shadow, (sh_x + 2, sh_y + 2))
		self.display_surface.blit(save_hint, (sh_x, sh_y))
		if self.save_message and not self.save_message_timer.active:
			status = self.fonts['small'].render(self.save_message, False, COLORS['yellow'])
			status_bg = self.fonts['small'].render(self.save_message, False, COLORS['black'])
			sx = sh_x
			sy = sh_y - 24
			self.display_surface.blit(status_bg, (sx + 2, sy + 2))
			self.display_surface.blit(status, (sx, sy))
	
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
			"Collect 5 special items for the party:",
			"GIFT, CAKE, 15 FLOWERS, FIRE BADGE, ARENA BADGE",
			"",
			"Find NPCs around town who will challenge you!",
			"Win battles and answer quiz questions correctly.",
			"",
			"Once you have all 5 items, head to the",
			"WATER ARENA for the final party with Haider!",
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

		# Gift
		gift_collected = self.collected_items.get('gift', False)
		gift_status = "[X] COLLECTED" if gift_collected else "[ ] Not collected"
		journal.blit(self.fonts['regular'].render(f"Gift: {gift_status}", False, COLORS['green'] if gift_collected else COLORS['red']), (50, y_pos)); y_pos += 25
		journal.blit(self.fonts['small'].render("    (From: o2 - Shop Owner)", False, COLORS['dark gray']), (50, y_pos)); y_pos += 25
		# Cake
		cake_collected = self.collected_items.get('cake', False)
		cake_status = "[X] COLLECTED" if cake_collected else "[ ] Not collected"
		journal.blit(self.fonts['regular'].render(f"Cake: {cake_status}", False, COLORS['green'] if cake_collected else COLORS['red']), (50, y_pos)); y_pos += 25
		journal.blit(self.fonts['small'].render("    (From: o4 - Baker)", False, COLORS['dark gray']), (50, y_pos)); y_pos += 25
		# Flowers
		flowers_count = int(self.collected_items.get('flowers_count', 0))
		flowers_done = flowers_count >= 15
		flowers_status = f"{'[X]' if flowers_done else '[ ]'} {flowers_count}/15 collected"
		journal.blit(self.fonts['regular'].render(f"Flowers: {flowers_status}", False, COLORS['green'] if flowers_done else COLORS['red']), (50, y_pos)); y_pos += 25
		journal.blit(self.fonts['small'].render("    (From: o3/p1/o7 - 5 each via quiz)", False, COLORS['dark gray']), (50, y_pos)); y_pos += 25
		# Fire badge
		fire_badge = self.collected_items.get('fire_badge', False)
		fire_status = "[X] COLLECTED" if fire_badge else "[ ] Not collected"
		journal.blit(self.fonts['regular'].render(f"Fire Badge: {fire_status}", False, COLORS['green'] if fire_badge else COLORS['red']), (50, y_pos)); y_pos += 25
		journal.blit(self.fonts['small'].render("    (From: FIRE.TMX boss)", False, COLORS['dark gray']), (50, y_pos)); y_pos += 25
		# Arena badge
		arena_badge = self.collected_items.get('arena_badge', False)
		arena_status = "[X] COLLECTED" if arena_badge else "[ ] Not collected"
		journal.blit(self.fonts['regular'].render(f"Arena Badge: {arena_status}", False, COLORS['green'] if arena_badge else COLORS['red']), (50, y_pos)); y_pos += 25
		journal.blit(self.fonts['small'].render("    (From: ARENA.TMX boss)", False, COLORS['dark gray']), (50, y_pos)); y_pos += 25
		
		y_pos += 10
		
		y_pos += 10
		
		# Hints
		hints_title = self.fonts['bold'].render("HINTS:", False, COLORS['black'])
		journal.blit(hints_title, (30, y_pos))
		y_pos += 30
		
		hint_lines = [
			"- o2 (Shop Owner) -> Gift",
			"- o4 (Baker) -> Cake",
			"- o3/p1/o7 quizzes -> 5 Flowers each (total 15)",
			"- FIRE boss -> Fire Badge",
			"- ARENA boss -> Arena Badge",
			"- Wrong quiz answers add 20 minute penalty",
			"- WATER arena is LOCKED until you have all 5 items",
			"- Final party with Haider is in WATER.TMX"
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
		
		# Store current map name
		# Determine key name for this tmx map
		for key, value in self.tmx_maps.items():
			if value == tmx_map:
				self.current_map = key
				break

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
		created_player = False
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'Player':
				# Support special 'any' spawn (used by load_game) → use the first player marker
				if player_start_pos == 'any' and not created_player or obj.properties['pos'] == player_start_pos:
					self.player = Player(
						pos = (obj.x, obj.y),
						frames = self.overworld_frames['characters']['player'],
						groups = self.all_sprites,
						facing_direction = obj.properties.get('direction', 'down'),
						collision_sprites = self.collision_sprites)
					self.player.game = self
					created_player = True
			else:
				Character(
					pos = (obj.x, obj.y),
					frames = self.overworld_frames['characters'][obj.properties['graphic']],
					groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
					facing_direction = obj.properties.get('direction', 'down'),  # Safe default
					character_data = TRAINER_DATA[obj.properties['character_id']],
					player = self.player,
					create_dialog = self.create_dialog,
					collision_sprites = self.collision_sprites,
					radius = obj.properties.get('radius', 0),  # Safe default
					nurse = obj.properties['character_id'] == 'Nurse',
					notice_sound = self.audio['notice'])

		# Fallback: ensure a player exists (for maps lacking markers)
		if not created_player:
			self.player = Player(
				pos = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
				frames = self.overworld_frames['characters']['player'],
				groups = self.all_sprites,
				facing_direction = 'down',
				collision_sprites = self.collision_sprites)
			self.player.game = self
		
		# Spawn collectibles based on map and quest status
		self.spawn_collectibles()

	def spawn_collectibles(self):
		"""Spawn collectibles on specific maps if not yet collected"""
		# In the birthday quest, items are obtained via NPCs/bosses & quizzes,
		# so we do not spawn pick-ups on the map anymore. Keep the structure
		# for potential future use, but leave it empty.
		collectible_spawns = {}
		
		# Spawn collectibles for current map if quest is started
		if self.quest_started and self.current_map in collectible_spawns:
			for spawn in collectible_spawns[self.current_map]:
				item_type = spawn['type']
				# Defensive: skip unknown keys (e.g., legacy 'flowers')
				if item_type not in self.collected_items:
					continue
				# Only spawn if not yet collected (boolean items only)
				if isinstance(self.collected_items[item_type], bool) and not self.collected_items[item_type]:
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
			# Mute/Unmute music with M key
			if pygame.K_m in self.keys_just_pressed:
				self.toggle_music()

			# Quick save / load for testing
			if pygame.K_F5 in self.keys_just_pressed:
				self.save_game()
			if pygame.K_F9 in self.keys_just_pressed:
				self.load_game()
			
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

	def create_dialog(self, character, dialog_type='default'):
		try:
			if not self.dialog_tree:
				self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog, dialog_type)
		except Exception as e:
			print(f"ERROR in create_dialog: {e}")
			import traceback
			traceback.print_exc()
			# Recover gracefully
			self.player.unblock()

	def end_dialog(self, character, trigger_quiz=False):
		self.dialog_tree = None
		# Final party ending: after talking to Haider at WATER with all items
		if hasattr(character, 'character_data') and character.character_data.get('is_party_npc', False) and self.current_map == 'water' and self.has_all_party_items():
			self.show_final_message = True
			self.player.block()
			return
		
		# Birthday Game: Check if this is the birthday note
		if character.character_data.get('is_birthday_note', False):
			self.quest_started = True
			self.player.unblock()
			return
		
		# Birthday Game: If this was pre-quiz dialog, now start the quiz
		if trigger_quiz and 'question' in character.character_data:
			# CRITICAL: Unblock player so they can interact with quiz
			self.player.unblock()
			self.start_quiz(character)
			return
		
		if character.nurse:
			for monster in self.player_monsters.values():
				monster.health = monster.get_stat('max_health')
				monster.energy = monster.get_stat('max_energy')

			self.player.unblock()
		elif not character.character_data['defeated']:
			self.audio['overworld'].stop()
			self.audio['battle'].play(-1)
			
			# CRITICAL: Reset character's monsters to full health for retry battles
			if hasattr(character, 'monsters') and character.monsters:
				for monster in character.monsters.values():
					monster.health = monster.get_stat('max_health')
					monster.energy = monster.get_stat('max_energy')
					monster.initiative = 0
					monster.defending = False
					monster.paused = False
			
			# Player uses full roster; NPCs limited to first two for 1v1 cycling
			if hasattr(character, 'monsters') and character.monsters:
				player_roster = self.player_monsters
				opponent_first = {k:v for k,v in list(character.monsters.items())[:2]}
			else:
				# No monsters - shouldn't happen, but handle it gracefully
				self.player.unblock()
				return
			
			self.transition_target = Battle(
				player_monsters = player_roster, 
				opponent_monsters = opponent_first, 
				monster_frames = self.monster_frames, 
				bg_surf = self.bg_frames[character.character_data['biome']], 
				fonts = self.fonts, 
				end_battle = self.end_battle,
				character = character, 
				sounds = self.audio)
			self.tint_mode = 'tint'
		else:
			# If speaking with final party NPC (Haider) at water and all items collected, show final message
			if hasattr(character, 'character_data') and character.character_data.get('is_party_npc', False) and self.current_map == 'water' and self.has_all_party_items():
				self.show_final_message = True
				self.player.block()
			else:
				self.player.unblock()
			self.check_evolution()

	# transition system
	def transition_check(self):
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			# Gate entry to WATER arena until all required items are collected
			target_map, target_pos = sprites[0].target
			if target_map == 'water' and not self.has_all_party_items():
				# Show blocked message and do not transition
				self.player.unblock()
				self.ice_blocked_timer = 90
				return
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
		try:
			self.audio['battle'].stop()
			self.transition_target = 'level'
			self.tint_mode = 'tint'
			# Auto-heal player's monsters after every battle
			for monster in self.player_monsters.values():
				monster.health = monster.get_stat('max_health')
				monster.energy = monster.get_stat('max_energy')
				monster.initiative = 0
				monster.defending = False
				monster.paused = False
			
			if character and hasattr(character, 'character_data'):
				# Check if this character has quiz data (question and options fields)
				has_quiz = (self.quest_started and 
				           'question' in character.character_data and 
				           'options' in character.character_data)
				
				# If a boss grants a battle reward, award it now
				battle_reward = character.character_data.get('battle_reward')
				if battle_reward and not character.character_data.get('defeated', False):
					self.award_item(battle_reward, amount=character.character_data.get('reward_amount'))
					character.character_data['defeated'] = True
					# Play collection sound
					if 'notice' in self.audio:
						self.audio['notice'].play()
					self.create_dialog(character)
				elif has_quiz and not character.character_data.get('defeated', False):
					# Show pre-quiz dialog after battle victory
					character.change_facing_direction(self.player.rect.center)
					self.create_dialog(character, dialog_type='pre_quiz')
				else:
					# Normal flow: mark defeated and show dialog
					character.character_data['defeated'] = True
					self.create_dialog(character)
			elif not self.evolution:
				self.player.unblock()
				self.check_evolution()
		except Exception as e:
			print(f"ERROR in end_battle: {e}")
			import traceback
			traceback.print_exc()
			# Recover gracefully
			self.player.unblock()
			if hasattr(self, 'audio') and 'overworld' in self.audio:
				self.audio['overworld'].play(-1)
		
	def draw_final_message(self):
		"""Show a loving final message after speaking with Haider at the WATER arena."""
		if not self.show_final_message:
			return
		# Semi-transparent overlay
		overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		overlay.fill((0, 0, 0))
		overlay.set_alpha(200)
		self.display_surface.blit(overlay, (0, 0))
		# Message box
		box_width, box_height = 900, 500
		box_x = (WINDOW_WIDTH - box_width) // 2
		box_y = (WINDOW_HEIGHT - box_height) // 2
		message_box = pygame.Surface((box_width, box_height))
		message_box.fill(COLORS['white'])
		pygame.draw.rect(message_box, COLORS['gold'], message_box.get_rect(), 5)
		# Title
		title = self.fonts['bold'].render("THANK YOU FOR PLAYING!", False, COLORS['gold'])
		title_rect = title.get_rect(center = (box_width // 2, 40))
		message_box.blit(title, title_rect)
		# Paragraph
		lines = [
			"Eman, thank you for adventuring through this little world.",
			"I hope you smiled, laughed, and felt loved along the way.",
			"Happy 25th Birthday — you are amazing.",
			"",
			"Thank you for playing the Birthday Adventure.",
			"I love you so much, always and forever. — Haider"
		]
		y = 100
		for line in lines:
			text = self.fonts['regular'].render(line, False, COLORS['black'])
			text_rect = text.get_rect(center = (box_width // 2, y))
			message_box.blit(text, text_rect)
			y += 36
		# Close hint
		close = self.fonts['small'].render("Press SPACE to continue", False, COLORS['red'])
		close_rect = close.get_rect(center = (box_width // 2, box_height - 40))
		message_box.blit(close, close_rect)
		self.display_surface.blit(message_box, (box_x, box_y))
		# Input to dismiss
		if pygame.K_SPACE in self.keys_just_pressed:
			self.show_final_message = False
			self.player.unblock()
	
	def start_quiz(self, character):
		"""Start a quiz for birthday NPCs after battle"""
		# Safety check
		if not hasattr(character, 'character_data'):
			self.player.unblock()
			return
			
		# Use character data directly (from TRAINER_DATA in game_data.py)
		quiz_data = character.character_data
		
		# Verify quiz data exists
		if 'question' not in quiz_data or 'options' not in quiz_data:
			self.player.unblock()
			return
		
		# Ensure player is unblocked and ready for quiz
		self.player.unblock()
		
		# Create quiz with question from character data
		self.quiz = Quiz(
			question_data=quiz_data,
			fonts=self.fonts,
			end_quiz=self.end_quiz,
			character=character,
			game=self
		)
	def has_all_party_items(self):
		"""Return True if all 5 required items are collected."""
		flowers_ok = int(self.collected_items.get('flowers_count', 0)) >= 15
		return bool(self.collected_items.get('gift') and self.collected_items.get('cake') and flowers_ok and self.collected_items.get('fire_badge') and self.collected_items.get('arena_badge'))

	def award_item(self, item_key, amount=None):
		"""Award an item or progress. Supports boolean items and flower counts."""
		if item_key in ('flowers', 'flowers_count'):
			current = int(self.collected_items.get('flowers_count', 0))
			self.collected_items['flowers_count'] = current + int(amount or 0)
		else:
			self.collected_items[item_key] = True
		
		# Block player during quiz so they can't move
		self.player.block()
	
	def end_quiz(self, character):
		"""Called when quiz is complete"""
		# Get result before clearing quiz
		was_correct = self.quiz.correct if self.quiz else False
		self.quiz = None
		
		# Unblock player after quiz
		self.player.unblock()
		
		# DO NOT set defeated here - it's already set correctly in quiz.py
		# defeated = True if correct (has item)
		# defeated = False if wrong (can retry)
		
		# Show the appropriate dialog based on result
		if was_correct:
			# Show success dialog with 'correct' type
			self.create_dialog_for_quiz_result(character, 'correct')
		else:
			# Show failure dialog with 'wrong' type
			self.create_dialog_for_quiz_result(character, 'wrong')
		
		if not self.evolution:
			self.audio['overworld'].play(-1)

	def create_dialog_for_quiz_result(self, character, result_type):
		"""Create dialog showing quiz result (correct or wrong)"""
		if not self.dialog_tree:
			# Get the specific dialog based on result
			if result_type in character.character_data['dialog']:
				dialog_messages = character.character_data['dialog'][result_type]
			else:
				dialog_messages = character.character_data['dialog']['default']
			
			# Temporarily override get_dialog to return specific messages
			original_get_dialog = character.get_dialog
			character.get_dialog = lambda dt='default': dialog_messages
			
			# Create dialog tree
			self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)
			
			# Restore original method
			character.get_dialog = original_get_dialog
	
	def toggle_music(self):
		"""Toggle music mute/unmute"""
		self.music_muted = not self.music_muted
		
		if self.music_muted:
			# Mute all audio
			for sound in self.audio.values():
				if hasattr(sound, 'set_volume'):
					sound.set_volume(0)
		else:
			# Unmute all audio (set to full volume)
			for sound in self.audio.values():
				if hasattr(sound, 'set_volume'):
					sound.set_volume(1.0)
	
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
	
	def save_game(self):
		"""Write a minimal save file for testing convenience"""
		try:
			# Backward-compatible save: include all new keys with defaults
			save_collected = {
				'gift': bool(self.collected_items.get('gift', False)),
				'cake': bool(self.collected_items.get('cake', False)),
				'flowers_count': int(self.collected_items.get('flowers_count', 0)),
				'fire_badge': bool(self.collected_items.get('fire_badge', False)),
				'arena_badge': bool(self.collected_items.get('arena_badge', False))
			}
			save_data = {
				'map': self.current_map,
				'player_pos': [self.player.rect.centerx, self.player.rect.centery],
				'quest_started': self.quest_started,
				'collected_items': save_collected,
				'game_time': self.current_game_time,
			}
			with open(self.save_file, 'w') as f:
				json.dump(save_data, f)
			self.save_message = 'Saved (F9 to Load)'
			self.save_message_timer.activate()
		except Exception as e:
			print('Save failed:', e)

	def load_game(self):
		"""Load saved file if present"""
		try:
			with open(self.save_file, 'r') as f:
				save_data = json.load(f)
			# Restore core state
			self.quest_started = save_data.get('quest_started', False)
			# Merge collected items safely with defaults
			saved_items = save_data.get('collected_items', {})
			self.collected_items['gift'] = bool(saved_items.get('gift', False))
			self.collected_items['cake'] = bool(saved_items.get('cake', False))
			self.collected_items['flowers_count'] = int(saved_items.get('flowers_count', saved_items.get('flowers', 0)))
			self.collected_items['fire_badge'] = bool(saved_items.get('fire_badge', False))
			self.collected_items['arena_badge'] = bool(saved_items.get('arena_badge', False))
			self.current_game_time = save_data.get('game_time', self.current_game_time)
			# Re-setup current map to re-place entities and player
			map_key = save_data.get('map', self.current_map)
			self.setup(self.tmx_maps[map_key], player_start_pos = 'any')
			# Move player to saved position (with clamping)
			px, py = save_data.get('player_pos', [self.player.rect.centerx, self.player.rect.centery])
			self.player.rect.center = (int(px), int(py))
			self.player.hitbox.center = self.player.rect.center
			self.player.unblock()
			self.save_message = 'Loaded'
			self.save_message_timer.activate()
		except FileNotFoundError:
			self.save_message = 'No Save Found'
			self.save_message_timer.activate()
		except Exception as e:
			print('Load failed:', e)

	def end_evolution(self):
		self.evolution = None
		self.player.unblock()
		self.audio['evolution'].stop()
		self.audio['overworld'].play(-1)

	# monster encounters 
	def check_ice_area_blocking(self):
		"""Legacy: previously blocked world ice corner. No-op for WATER gate."""
		return
	
	def draw_ice_blocked_message(self):
		"""Show message when ice area is blocked"""
		if self.ice_blocked_timer > 0:
			box_width, box_height = 600, 120
			box_x = (WINDOW_WIDTH - box_width) // 2
			box_y = WINDOW_HEIGHT - box_height - 50
			
			message_box = pygame.Surface((box_width, box_height))
			message_box.fill(COLORS['red'])
			pygame.draw.rect(message_box, COLORS['white'], message_box.get_rect(), 3)
			
			title = self.fonts['bold'].render("WATER ARENA LOCKED!", False, COLORS['white'])
			msg1 = self.fonts['regular'].render("You need all 5 items to enter!", False, COLORS['white'])
			msg2 = self.fonts['small'].render("Collect: Gift, Cake, 15 Flowers, Fire Badge, Arena Badge", False, COLORS['white'])
			
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
			# Final message overlay on top
			self.draw_final_message()

			# Birthday Game: Draw intro screen (on top of everything)
			self.draw_intro_screen()
			
			# Birthday Game: Draw quest journal (on top of everything when open)
			self.draw_quest_journal()

			self.tint_screen(dt)
			pygame.display.update()

if __name__ == '__main__':
	game = Game()
	game.run()