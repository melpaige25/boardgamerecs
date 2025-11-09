# Board Game Recommender

A clean, modern web application to recommend board games from your collection and discover new games to buy.

## Features

### Section 1: What Should We Play Today?
- Recommends 3 random games from your owned collection
- Filters by player count, complexity, and game duration
- Allows repeating recommendations (cycles through all matching games)
- Direct links to BoardGameGeek for each game

### Section 2: What Games Should We Buy?
- Recommends 3 random games from your BGG collection (wishlist + rated/tracked games)
- Prioritizes wishlist games, includes games you've rated but don't own
- Filters by the same criteria (player count, complexity, duration)
- Automatically syncs filters with Section 1
- All links verified correct (using your actual BGG data)

## Data Files

- `owned-games.json` - 277 games from your collection (where own=1)
- `bgg-recommendations.json` - 147 games (25 wishlist + 122 rated/tracked games)
- `collection.csv` - Original CSV export from BoardGameGeek

## Filter Options

### Player Count
- Any
- 1 Player
- 2 Players
- 3 Players
- 4 Players
- 5 Players
- 6+ Players

### Complexity
- Light (1-2)
- Medium (2-3.5)
- Heavy (3.5-5)

### Duration
- Quick (0-30 min)
- Medium (30-60 min)
- Long (60-90 min)
- Very Long (90+ min)

## Usage

Simply open `index.html` in a web browser. The app will:
1. Load your owned games and BGG recommendations
2. Allow you to filter by preferences
3. Generate personalized recommendations

### Section 1 Usage
1. Select your filters (optional)
2. Click "Recommend" to get 3 game suggestions
3. Click again to get new recommendations

### Section 2 Usage
1. Filters automatically sync from Section 1
2. Click "Recommend" to get 3 game suggestions from your wishlist
3. Click again to see different games from your wishlist

## Technical Details

- Pure vanilla JavaScript (no frameworks)
- Mobile-friendly responsive design
- Subtle dark theme with clean card-based layout
- All data pre-fetched in JSON format for fast performance
- Single recommend button updates both sections simultaneously

## Updating Data

To update the game data:

1. Export your collection from BoardGameGeek as CSV (replace `collection.csv`)
2. Run `python3 parse_collection.py` to regenerate `owned-games.json`
3. Run `python3 build_comprehensive_recommendations.py` to regenerate `bgg-recommendations.json`

## Files

- `index.html` - Main application
- `owned-games.json` - Your owned games (277 games)
- `bgg-recommendations.json` - Buy recommendations (147 games)
- `collection.csv` - BGG collection export
- `parse_collection.py` - Script to parse owned games from CSV
- `build_comprehensive_recommendations.py` - Script to build buy recommendations (wishlist + rated games)
- `test_filters.js` - Filter logic tests
