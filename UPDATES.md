# Latest Updates to ETA Guesser

## Changes Summary

### 1. Button Naming and Visibility ✅
- **Renamed**: "Pick Random Destination" → "New Game"
- **Button Swapping Logic**:
  - Initially shows "New Game" button (auto-picks destination on load)
  - When user places guess → Shows "Submit My Guess" button
  - After submit → Hides both buttons, shows "New Game" button
  - Clicking "New Game" → Resets and starts new round

### 2. Compass Redesign ✅
- **Before**: Compass arrow appeared next to each transport mode's time
- **After**: Single large compass arrow in dedicated section above ETAs
- **Location**: New "Direction to Destination" section between coordinates and ETAs
- **Design**: Larger (48px) arrow that rotates to point toward destination

### 3. Geoguessr-Style Scoring ✅
- **Replaced**: Accuracy ratings (Perfect/Great/Good/etc.)
- **New System**: Score out of 5000 points
- **Formula**: Exponential decay based on distance
  ```
  Score = 5000 × e^(-0.25 × distance_km)
  ```
- **Examples**:
  - 0 km = 5000 points (perfect)
  - 1 km = 4467 points
  - 5 km = 3543 points
  - 10 km = 2500 points
  - 15 km = 1250 points
  - 25 km = 100 points

### 4. Score Animation ✅
- **Display**: Large score popup in center of screen
- **Styling**:
  - 72px font size for score
  - White background with shadow
  - Blue color (#1a73e8)
- **Animation**:
  - Fades in immediately after submit
  - Shows for 1 second
  - Fades out automatically
  - Does not block interaction

## Technical Implementation

### New CSS Classes
```css
#newGameBtn - Red button for starting new game
#compass-indicator - Container for single compass
.compass-display - Large compass arrow (48px)
#score-popup - Center screen popup
.score-value - 72px score display
.score-label - "points" label
```

### New JavaScript Functions
```javascript
calculateScore(distanceKm) - Exponential scoring formula
showScoreAnimation(score) - Display and fade score popup
startNewGame() - Reset game state and start new round
```

### Modified Functions
- `getRandomDestination()`: Button visibility management
- `displayETAs()`: Shows single compass, removes per-mode arrows
- `submitGuess()`: Calculates score, shows animation, swaps buttons

## UI Flow

### Game Start
1. Page loads → Auto-picks destination
2. Shows: Compass + ETAs + "New Game" button (hidden)
3. User clicks map → Shows "Submit My Guess" button

### After Submit
1. Hides: "New Game" and "Submit" buttons
2. Shows: Center screen score animation (1 second)
3. Reveals: Destination marker, distance line, results
4. Shows: "New Game" button (red)

### New Game
1. User clicks "New Game"
2. Clears: All markers, lines, results
3. Picks: New random destination
4. Shows: New compass + ETAs
5. Ready for next guess

## Testing Checklist

- [x] "New Game" button appears on load
- [x] Single compass shows direction
- [x] Score animation displays on submit
- [x] Score calculation uses exponential formula
- [x] Button visibility swaps correctly
- [x] Old markers/lines clear on new game
- [x] Instructions update appropriately

## Visual Changes

**Before:**
```
🚗 Driving      - 25 mins (15.2 km) ↑
🚇 Transit      - 38 mins (16.1 km) ↑
🚴 Cycling      - 52 mins (15.8 km) ↑
🚶 Walking      - 3 hrs 10 mins (15.5 km) ↑
```

**After:**
```
Direction to Destination
         ↑ (48px, rotated)

🚗 Driving      - 25 mins
🚇 Transit      - 38 mins
🚴 Cycling      - 52 mins
🚶 Walking      - 3 hrs 10 mins
```

**Score Display (center of screen):**
```
┌────────────────────┐
│                    │
│       3543         │
│       points       │
│                    │
└────────────────────┘
```

## Files Modified

- `index.html`: All changes implemented
- `README.md`: Updated documentation
- `UPDATES.md`: This file

## No Backend Changes Required

All changes are frontend-only. The backend continues to:
- Generate random destinations within 25km
- Filter for all 4 transport modes
- Return ETAs and coordinates

The scoring and UI improvements are purely client-side enhancements.
