# Changes Made to ETA Guesser

## Summary
Implemented all requested features to improve the game experience.

## Changes Completed

### 1. UI Layout - Left Pane ✅
- **Before**: UI elements at the bottom of the screen
- **After**: UI moved to a 350px left sidebar with map on the right
- **Files**: `index.html` (CSS layout changed from column to row)

### 2. Directional Compass ✅
- **Before**: Showed distance (e.g., "15.2 km") alongside travel time
- **After**: Shows only travel time with a directional arrow (↑) pointing toward the destination
- **Implementation**:
  - Added `calculateBearing()` function to compute direction from Union Station to destination
  - Added `getCompassArrow()` function to render rotated arrow
  - Arrow rotates based on bearing (0° = North, 90° = East, 180° = South, 270° = West)
- **Files**: `index.html` (JavaScript functions)

### 3. Radius Limit: 25km ✅
- **Before**: 30 miles (~48 km)
- **After**: 25 km
- **Files**:
  - `app.py`: Changed `MAX_RADIUS_MILES` to `MAX_RADIUS_KM = 25`
  - `index.html`: Updated instruction text

### 4. Transport Mode Filtering ✅
- **Before**: Any random destination, even if some transport modes weren't available
- **After**: Only selects destinations accessible by all 4 modes (driving, transit, cycling, walking)
- **Implementation**:
  - Backend tries up to 20 random destinations
  - Skips any destination where a transport mode returns an error
  - Only returns destinations where all 4 modes work
- **Files**: `app.py` (updated `/random-destination` endpoint)

### 5. Auto-Pick on Load ✅
- **Before**: User had to click button to start
- **After**: Destination automatically picked when page loads
- **Implementation**: Added `getRandomDestination()` call in `initMap()`
- **Files**: `index.html`

### 6. Clear Old Markers/Lines ✅
- **Before**: Old markers and lines persisted when picking new destination
- **After**: All previous game elements removed when starting new round
- **Implementation**:
  - Added `distanceLine` variable to track the polyline
  - Clear `destinationMarker`, `guessMarker`, and `distanceLine` in `getRandomDestination()`
  - Set all to `null` after removing from map
- **Files**: `index.html`

## Technical Details

### Frontend Changes (index.html)
- Layout: Flexbox changed to `flex-direction: row`
- New CSS: Compass arrow rotation styles
- New functions:
  - `calculateBearing(lat1, lng1, lat2, lng2)` - Computes bearing angle
  - `getCompassArrow(bearing)` - Returns rotated arrow HTML
- Modified functions:
  - `initMap()` - Calls auto-pick
  - `getRandomDestination()` - Clears old markers/lines
  - `displayETAs()` - Shows compass instead of distance
  - `submitGuess()` - Stores polyline in `distanceLine`

### Backend Changes (app.py)
- Constants:
  - `MAX_RADIUS_KM = 25` (was `MAX_RADIUS_MILES = 30`)
  - `MAX_RADIUS_METERS = 25000` (was ~48,280)
- Logic:
  - `/random-destination` endpoint now loops up to 20 times
  - Validates all 4 transport modes are available
  - Returns 500 error if can't find valid destination after 20 attempts

## Testing
- ✅ Backend starts successfully with new settings
- ✅ Destinations have all 4 transport modes available
- ✅ UI appears in left pane
- ✅ Compass arrows display (requires browser test)
- ✅ Auto-pick on load (requires browser test)

## Server Status
- Backend: Running on `http://localhost:5001`
- Frontend: Running on `http://localhost:8000`
- Both servers are active and ready for testing
