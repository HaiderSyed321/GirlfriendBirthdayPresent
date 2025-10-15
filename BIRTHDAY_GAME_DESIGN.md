# Birthday Adventure Game - Design Document

## 🎉 Concept
A time-based adventure where your girlfriend must navigate through challenges to reach her birthday party hosted by Haider before midnight (12 AM).

## 🎮 Game Modifications Needed

### 1. **Story & Theme**
- **Protagonist**: Your girlfriend (customizable character)
- **Goal**: Reach Haider's party location before 12 AM
- **Antagonists**: Time-themed "obstacles" instead of monsters
  - Examples: "Procrastination", "Traffic", "Lost Keys", "Forgot Gift"
  - Each represents a real-life delay/challenge

### 2. **Time System** ⏰
- **Starting Time**: 6 PM (6 hours to reach party)
- **Time Mechanics**:
  - Each battle/encounter takes 15-30 minutes of in-game time
  - Walking through certain areas takes time
  - Resting/healing takes time
  - Display clock in top-right corner
  - Urgency increases as midnight approaches

### 3. **Map Design** 🗺️
**Journey Stages**:
1. **Home** → Starting point (6:00 PM)
2. **Shopping District** → Get the perfect gift (6:30 PM)
3. **Cafe/Restaurant** → Pick up cake (7:30 PM)
4. **City Streets** → Navigate traffic (8:30 PM)
5. **Park/Shortcut** → Decision point (9:30 PM)
6. **Party Venue** → Haider's location (Goal: Before 12 AM)

### 4. **Battle System Redesign** 🎯
Instead of monster battles, create **"Challenge Encounters"**:

**Challenge Types**:
- **Quiz Battles**: Answer questions about your relationship
  - "What was our first date?"
  - "What's my favorite food?"
  - Correct answers = faster completion
  
- **Memory Games**: Match pairs of your photos/memories
  
- **Decision Battles**: Choose the right path/action
  - "Which gift should I get?"
  - "Which route is faster?"

### 5. **Characters** 👥
Replace NPCs with:
- **Friends**: Give hints and help
- **Family Members**: Provide shortcuts or delays
- **Strangers**: Random encounters (some helpful, some not)
- **Haider** (Final NPC): At the party venue

### 6. **Rewards & Items** 🎁
Instead of monsters, collect:
- **Time Savers**: Shortcuts, taxi rides, bike
- **Party Items**: Gift, cake, flowers, card
- **Memories**: Photos/mementos that unlock special endings
- **Energy**: Coffee, snacks (to move faster)

### 7. **Multiple Endings** 🎬
- **Perfect Ending** (11:00-11:59 PM): Arrives early, surprise party ready
- **Just in Time** (11:59 PM): Dramatic entrance at midnight
- **Fashionably Late** (12:01-12:30 AM): Party started, but still special
- **Too Late** (After 12:30 AM): Heartfelt apology scene, reschedule

### 8. **Special Features** ✨
- **Photo Album**: Collect memories throughout journey
- **Love Meter**: Increases with correct answers/good choices
- **Birthday Messages**: Hidden messages from Haider throughout
- **Final Surprise**: Video message or special scene at the end

## 🔧 Technical Implementation Priority

### Phase 1: Core Changes (Do First)
1. ✅ Fix character sprites (DONE)
2. Add time system and clock display
3. Rename game title and main character
4. Modify dialog system for story

### Phase 2: Content (Do Second)
1. Create new map layout (6 stages)
2. Replace monster data with challenge data
3. Write dialog for each NPC
4. Design quiz questions/challenges

### Phase 3: Polish (Do Last)
1. Add custom graphics (photos, etc.)
2. Record/add custom music
3. Create multiple endings
4. Add birthday surprise elements

## 📝 Quick Start Implementation

### Immediate Changes You Can Make:
1. **Change game title** in `main.py` line 24
2. **Rename player character** in map files
3. **Modify dialog** in `game_data.py`
4. **Add time display** to UI
5. **Change monster names** to challenge names

### Files to Modify:
- `main.py` - Game title, time system
- `game_data.py` - Dialog, character data, "monster" data
- `settings.py` - Add time constants
- `battle.py` - Rename to `challenge.py`, modify mechanics
- `entities.py` - Add time tracking to player
- Map files in `data/maps/` - Redesign layout

## 🎨 Personalization Ideas
- Replace monster sprites with custom images
- Add photos of you two as "collectibles"
- Custom music: her favorite songs
- Inside jokes as easter eggs
- Real locations you've been to as map areas
- Friends/family as NPCs with personalized dialog

## ⏱️ Development Timeline
- **Quick Version** (2-3 hours): Change text, add timer, modify dialog
- **Medium Version** (1-2 days): New maps, challenge system, custom graphics
- **Full Version** (3-5 days): Everything above + polish, testing, surprises

Would you like me to start implementing any specific part of this design?

