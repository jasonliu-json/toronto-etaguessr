# ETA Guesser - Toronto

A guessing game where you estimate the location of a destination based on travel times from Toronto Union Station.

## Features

- **Auto-start**: Automatically picks a destination when you open the page
- **Smart filtering**: Only chooses destinations accessible by all 4 transport modes (no dead-ends!)
- **10km radius**: Destinations within 10km of Union Station for fair gameplay
- **No ferries**: Ferry routes are automatically excluded for better gameplay
- **Directional compass**: Shows which direction the destination is (without revealing distance)
- **Left-side UI**: Clean interface with map on the right, controls on the left
- **Real-time ETAs**:
  - 🚗 Driving
  - 🚇 Public Transit
  - 🚴 Cycling
  - 🚶 Walking
- **Interactive guessing**: Click on the map to place your guess
- **Accuracy scoring**: Get rated on how close your guess was
- **Visual feedback**: Red line shows the distance between your guess and actual location

## Setup

### 1. Prerequisites

- Python 3.7+
- Google Maps API Key with the following APIs enabled:
  - Maps JavaScript API
  - Distance Matrix API
  - Geocoding API

### 2. Get Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/google/maps-apis/)
2. Create a new project or select an existing one
3. Enable these APIs:
   - Maps JavaScript API
   - Distance Matrix API
   - Geocoding API
4. Create credentials (API Key)
5. Copy your API key

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Flask flask-cors googlemaps
```

### 4. Configure API Keys

**Backend:**
1. Copy the example file: `cp .env.example .env`
2. Edit `.env` and add your API key:
   ```
   GOOGLE_MAPS_API_KEY=your_api_key_here
   ```

**Frontend:**
1. Copy the example file: `cp config.example.js config.js`
2. Edit `config.js` and add your API key:
   ```javascript
   const CONFIG = {
       GOOGLE_MAPS_API_KEY: 'your_api_key_here'
   };
   ```

**Security Note:** Never commit `.env` or `config.js` files - they're already in `.gitignore`

### 5. Run the Application

**Terminal 1 - Start the Python backend:**
```bash
python3 app.py
```

The backend will start on `http://localhost:5001`

**Terminal 2 - Start the frontend:**
```bash
python3 -m http.server 8000
```

Then open your browser to `http://localhost:8000`

## How to Play

1. **Open** the web interface at `http://localhost:8000`
   - A destination is automatically selected when you load the page!

2. **Study the clues**:
   - Look at the travel times for all 4 transport modes
   - A single directional compass arrow (↑) shows which direction the destination is
   - The destination is hidden - you have to guess where it is!

3. **Make your guess**:
   - Click anywhere on the map to place your guess marker (orange with "?")
   - You can click again to move your guess

4. **Submit**:
   - Click "Submit My Guess" button

5. **See results**:
   - Your score (0-5000) appears in the center of the screen with an animation
   - The actual destination appears (marker 'B')
   - Your guess is shown (marker 'G')
   - A red line connects your guess to the actual location
   - Scoring works like Geoguessr:
     - Perfect guess (0km) = 5000 points
     - ~1km away = ~4500 points
     - ~5km away = ~3000 points
     - ~10km away = ~1500 points
     - ~25km away = ~100 points

6. **Play again**:
   - Click "New Game" to start a new round
   - Old markers and lines are automatically cleared

## Project Structure

```
etaGuessr/
├── index.html          # Frontend web interface
├── app.py             # Python Flask backend
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## API Endpoints

### GET /random-destination

Returns a random destination within 30 miles of Union Station with ETAs.

**Response:**
```json
{
  "origin": {
    "lat": 43.6452,
    "lng": -79.3806
  },
  "destination": {
    "lat": 43.7234,
    "lng": -79.4567
  },
  "destination_address": "123 Example St, Toronto, ON",
  "etas": {
    "driving": {
      "duration": "25 mins",
      "distance": "15.2 km"
    },
    "transit": {
      "duration": "38 mins",
      "distance": "16.1 km"
    },
    "bicycling": {
      "duration": "52 mins",
      "distance": "15.8 km"
    },
    "walking": {
      "duration": "3 hours 10 mins",
      "distance": "15.5 km"
    }
  }
}
```

## Console Output

The backend prints formatted ETA information to the console:

```
================================================================================
ROUTE: Union Station → Destination
Origin: 43.6452, -79.3806
Destination: 43.7234, -79.4567
================================================================================
🚗 DRIVING       - 25 mins         (15.2 km)
🚇 TRANSIT       - 38 mins         (16.1 km)
🚴 BICYCLING     - 52 mins         (15.8 km)
🚶 WALKING       - 3 hours 10 mins (15.5 km)
================================================================================
```

## Troubleshooting

**CORS Errors:**
- Make sure the Flask backend is running on port 5001
- The flask-cors package should handle cross-origin requests

**Port 5000 Already in Use:**
- On macOS, AirPlay Receiver uses port 5000 by default
- This app uses port 5001 to avoid conflicts
- If port 5001 is also in use, update both `app.py` (line 179) and `index.html` (line 289) to use a different port

**API Key Issues:**
- Verify all required APIs are enabled in Google Cloud Console
- Check that billing is enabled on your Google Cloud project
- Ensure the API key is correctly configured in both files

**Transit Routes Not Available:**
- Some random destinations may not have public transit routes available
- The app will show "N/A" for unavailable routes

## Deployment

**Important:** GitHub Pages only hosts static files and cannot run the Python backend.

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options including:
- Heroku (free backend hosting)
- Vercel (full-stack serverless)
- Railway (easy deployment)
- VPS setup

Quick option: Deploy backend on Heroku, frontend on GitHub Pages.
