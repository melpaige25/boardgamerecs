# Board Game Recommender

A clean, modern web application to recommend board games from your collection and discover new games to buy.

## Features

### Section 1: What Should We Play Today?
- Recommends 3 games from your owned collection
- Filters by player count, complexity, and game duration
- Smart recommendation cycling - avoids showing the same games repeatedly until all options are shown
- Green accent theme
- Direct links to BoardGameGeek for each game

### Section 2: What Games Should We Buy?
- Shows top-rated games from BoardGameGeek that you don't own
- Filters by the same criteria (player count, complexity, duration)
- Automatically syncs filters with Section 1
- Red accent theme
- Games sorted by BGG rating

## Data Files

- `owned-games.json` - 277 games from your collection (where own=1)
- `bgg-recommendations.json` - 99 top-rated games from BGG (excluding owned and previously owned)
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
1. Select your filters (or use the synced filters from Section 1)
2. Click "Show Recommendations" to see all matching games
3. Games are automatically sorted by rating

## Technical Details

- Pure vanilla JavaScript (no frameworks)
- Mobile-friendly responsive design
- Black background with green (owned) and red (buy) accents
- All data pre-fetched in JSON format for fast performance

## Updating Data

To update the game data:

1. Export your collection from BoardGameGeek as CSV
2. Run `python3 parse_collection.py` to regenerate `owned-games.json`
3. Manually update `bgg-recommendations.json` with new top-rated games (or modify the fetch script)

## Files

- `index.html` - Main application
- `owned-games.json` - Your owned games
- `bgg-recommendations.json` - Games to buy
- `parse_collection.py` - Script to parse CSV into JSON
- `test_filters.js` - Filter logic tests
