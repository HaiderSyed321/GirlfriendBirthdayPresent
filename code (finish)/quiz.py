from settings import *
from timer import Timer

class Quiz:
	def __init__(self, question_data, fonts, end_quiz, character, game):
		"""
		question_data: Dictionary with 'question', 'options', 'answer', 'item_reward', 'time_cost', 'wrong_penalty'
		"""
		self.question_data = question_data
		self.fonts = fonts
		self.end_quiz = end_quiz
		self.character = character
		self.game = game
		
		self.selected_option = 0  # A, B, C, or D (0-3)
		self.answered = False
		self.correct = False
		self.display_result = False
		self.result_timer = Timer(2000, func=self.finish_quiz)
		
		# Prevent immediate input (wait for dialog key release)
		self.input_delay_timer = Timer(300)  # 300ms delay before accepting input
		self.input_delay_timer.activate()
		
	def input(self, keys_just_pressed):
		# Don't process input during result display or input delay
		if self.display_result or self.input_delay_timer.active:
			return
		
		# Navigate options with arrow keys AND WASD
		if pygame.K_DOWN in keys_just_pressed or pygame.K_s in keys_just_pressed:
			self.selected_option = min(3, self.selected_option + 1)
		if pygame.K_UP in keys_just_pressed or pygame.K_w in keys_just_pressed:
			self.selected_option = max(0, self.selected_option - 1)
		
		# Confirm answer with SPACE or RETURN
		if pygame.K_SPACE in keys_just_pressed or pygame.K_RETURN in keys_just_pressed:
			self.check_answer()
	
	def check_answer(self):
		if self.answered:
			return
		
		self.answered = True
		
		# Check if answer is correct (with safe defaults)
		correct_answer = self.question_data.get('quiz_answer', 'B')  # Default to B if not specified
		
		# Make sure selected_option is within valid range
		self.selected_option = max(0, min(3, self.selected_option))
		player_answer = ['A', 'B', 'C', 'D'][self.selected_option]
		
		# Special case: 'ALL' means all answers are correct (joke question)
		if correct_answer == 'ALL':
			self.correct = True
		else:
			self.correct = (player_answer == correct_answer)
		
		# Add base time cost for attempting quiz
		time_cost = self.question_data.get('time_cost', 45)
		self.game.current_game_time += time_cost
		
		# Only award item and mark as defeated if CORRECT
		if self.correct:
			# Flowers reward (adds to counter)
			flowers_amount = self.question_data.get('flowers_reward')
			if flowers_amount:
				if hasattr(self.game, 'award_item'):
					self.game.award_item('flowers_count', flowers_amount)
			# Boolean item reward
			item_reward = self.question_data.get('item_reward')
			if item_reward:
				if hasattr(self.game, 'award_item'):
					self.game.award_item(item_reward)
			# Mark character as defeated (quest complete)
			if hasattr(self.character, 'character_data'):
				self.character.character_data['defeated'] = True
			# Play collection sound
			if hasattr(self.game, 'audio') and 'notice' in self.game.audio:
				self.game.audio['notice'].play()
		else:
			# Wrong answer - apply time penalty and keep defeated as False
			penalty = self.question_data.get('wrong_penalty', 20)
			if hasattr(self.game, 'current_game_time'):
				self.game.current_game_time += penalty
			# Explicitly keep defeated as False so they can battle again
			if hasattr(self.character, 'character_data'):
				self.character.character_data['defeated'] = False
		
		self.display_result = True
		self.result_timer.activate()
	
	def finish_quiz(self):
		# defeated flag is already set in check_answer() based on correct/wrong
		# Don't set it again here!
		
		# Just end the quiz - defeated status is already correct
		self.end_quiz(self.character)
	
	def draw_quiz(self, display_surface):
		# Semi-transparent overlay
		overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		overlay.fill((0, 0, 0))
		overlay.set_alpha(180)
		display_surface.blit(overlay, (0, 0))
		
		# Quiz box
		box_width, box_height = 900, 500
		box_x = (WINDOW_WIDTH - box_width) // 2
		box_y = (WINDOW_HEIGHT - box_height) // 2
		
		quiz_box = pygame.Surface((box_width, box_height))
		quiz_box.fill(COLORS['white'])
		pygame.draw.rect(quiz_box, COLORS['gold'], quiz_box.get_rect(), 5)
		
		if not self.display_result:
			# Display question
			y_offset = 30
			
			title = self.fonts['bold'].render("RELATIONSHIP QUIZ", False, COLORS['gold'])
			quiz_box.blit(title, (box_width // 2 - title.get_width() // 2, y_offset))
			y_offset += 60
			
			# Question text
			question_lines = self.split_text(self.question_data.get('question', 'Question?'), box_width - 60)
			for line in question_lines:
				text = self.fonts['regular'].render(line, False, COLORS['black'])
				quiz_box.blit(text, (30, y_offset))
				y_offset += 30
			
			y_offset += 20
			
			# Options
			options = self.question_data.get('options', ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'])
			for i, option in enumerate(options):
				# Highlight selected option
				if i == self.selected_option:
					color = COLORS['gold']
					prefix = ">> "
				else:
					color = COLORS['black']
					prefix = "   "
				
				text = self.fonts['regular'].render(f"{prefix}{option}", False, color)
				quiz_box.blit(text, (50, y_offset))
				y_offset += 40
			
			# Instructions
			y_offset += 20
			instruction = self.fonts['small'].render("Use UP/DOWN to select, SPACE to confirm", False, COLORS['dark gray'])
			quiz_box.blit(instruction, (box_width // 2 - instruction.get_width() // 2, y_offset))
		else:
			# Display result
			y_offset = 150
			
			if self.correct:
				result_text = "CORRECT!"
				result_color = COLORS['green']
				message = "Great job! You know your stuff!"
			else:
				result_text = "INCORRECT"
				result_color = COLORS['red']
				penalty = self.question_data.get('wrong_penalty', 20)
				message = f"Not quite right... +{penalty} minutes penalty"
			
			title = self.fonts['bold'].render(result_text, False, result_color)
			quiz_box.blit(title, (box_width // 2 - title.get_width() // 2, y_offset))
			y_offset += 60
			
			msg = self.fonts['regular'].render(message, False, COLORS['black'])
			quiz_box.blit(msg, (box_width // 2 - msg.get_width() // 2, y_offset))
			y_offset += 40
			
			# Show item reward ONLY if actually collected (correct answer)
			if self.correct:
				flowers_amount = self.question_data.get('flowers_reward')
				if flowers_amount:
					item_msg = self.fonts['bold'].render(f"*** +{flowers_amount} FLOWERS! ***", False, COLORS['gold'])
					quiz_box.blit(item_msg, (box_width // 2 - item_msg.get_width() // 2, y_offset))
				else:
					item_reward = self.question_data.get('item_reward')
					if item_reward:
						item_msg = self.fonts['bold'].render(f"*** {item_reward.upper()} COLLECTED! ***", False, COLORS['gold'])
						quiz_box.blit(item_msg, (box_width // 2 - item_msg.get_width() // 2, y_offset))
		
		display_surface.blit(quiz_box, (box_x, box_y))
	
	def split_text(self, text, max_width):
		"""Split text into multiple lines if too long"""
		words = text.split(' ')
		lines = []
		current_line = []
		
		for word in words:
			test_line = ' '.join(current_line + [word])
			test_surf = self.fonts['regular'].render(test_line, False, COLORS['black'])
			if test_surf.get_width() <= max_width:
				current_line.append(word)
			else:
				if current_line:
					lines.append(' '.join(current_line))
				current_line = [word]
		
		if current_line:
			lines.append(' '.join(current_line))
		
		return lines
	
	def update(self, dt, keys_just_pressed):
		self.result_timer.update()
		self.input_delay_timer.update()
		self.input(keys_just_pressed)
		self.draw_quiz(pygame.display.get_surface())

