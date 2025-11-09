# Board Game Recommender

A clean, modern web application to recommend board games from your collection and discover new games to buy.

## Features

### Section 1: What Should We Play Today?
- Recommends 3 random games from your owned collection
- Filters by player count, complexity, and game duration
- Allows repeating recommendations (cycles through all matching games)
- Direct links to BoardGameGeek for each game

### Section 2: What Games Should We Buy?
- Recommends 3 random games from the top 5,000 BGG-ranked games
- Excludes all owned and previously owned games from your collection
- Excludes expansions (base games only)
- Weighted by BGG rank (higher-ranked games prioritized)
- Filters by the same criteria (player count, complexity, duration)
- Automatically syncs filters with Section 1
- All links verified correct (using BGG game database)

## Data Files

- `owned-games.json` - 277 games from your collection (where own=1)
- `bgg-recommendations.json` - 4,822 games from top 5,000 BGG rankings (excluding owned/previously owned)
- `collection.csv` - Original CSV export from BoardGameGeek
- `boardgames_ranks.csv` - Complete BGG game database with rankings (170,000+ games)

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

### Update Owned Games
1. Export your collection from BoardGameGeek as CSV (replace `collection.csv`)
2. Run `python3 parse_collection.py` to regenerate `owned-games.json` and `excluded-game-ids.json`

### Update Buy Recommendations
1. Run `python3 build_from_all_bgg_games.py` to regenerate `bgg-recommendations.json`
2. This uses `boardgames_ranks.csv` and excludes all games in `excluded-game-ids.json`
3. Automatically filters out expansions and prioritizes top-ranked games

### Update BGG Database (Optional)
1. Replace `boardgames_ranks.csv` with latest BGG rankings export
2. Run `python3 build_from_all_bgg_games.py` to rebuild recommendations

## Files

### Application
- `index.html` - Main web application

### Data Files
- `owned-games.json` - Your owned games (277 games)
- `bgg-recommendations.json` - Buy recommendations (4,822 games)
- `collection.csv` - BGG collection export
- `boardgames_ranks.csv` - Complete BGG game database
- `excluded-game-ids.json` - IDs to exclude (owned + previously owned)

### Scripts
- `parse_collection.py` - Parse owned games from CSV
- `build_from_all_bgg_games.py` - Build buy recommendations from BGG database
- `test_filters.js` - Filter logic tests

### Legacy Scripts (No Longer Used)
- `build_comprehensive_recommendations.py` - Old wishlist-based approach (147 games)
- `build_wishlist_recommendations.py` - Old wishlist-only approach (25 games)
- `apply_id_corrections.py` - Manual ID correction workflow
- `bgg-id-corrections.csv` - Manual ID corrections template
