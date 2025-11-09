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
- **Personalized** based on your rating preferences:
  - Prioritizes heavier games (you rate 4.0+ complexity highest: 8.55 avg)
  - Prioritizes highly-rated games (strong correlation with BGG consensus)
  - Prioritizes recent games (you rate 2020+ games highest: 7.19 avg)
- Excludes all owned and previously owned games from your collection
- Excludes expansions (base games only)
- Filters by the same criteria (player count, complexity, duration)
- Automatically syncs filters with Section 1
- All links verified correct (using BGG game database)

## Data Files

- `owned-games.json` - 277 games from your collection (where own=1)
- `bgg-recommendations.json` - 4,822 personalized buy recommendations
- `preference_profile.json` - Your rating preferences (auto-generated from collection)
- `collection.csv` - Original CSV export from BoardGameGeek
- `boardgames_ranks.csv` - Complete BGG game database with rankings (170,000+ games)
- `excluded-game-ids.json` - IDs to exclude (owned + previously owned)

## Personalization

The buy recommendations are personalized based on your rating history (361 rated games):

### Your Preference Profile
- **Complexity**: You strongly prefer heavier games
  - Very Heavy (4.0+): 8.55 avg rating ⭐
  - Heavy (3.5-4.0): 7.82 avg rating
  - Very Light (1.0-1.5): 6.13 avg rating
- **BGG Consensus**: You tend to agree with highly-rated games
  - BGG 8.0+: 7.90 avg rating ⭐
  - BGG <6.0: 4.04 avg rating
- **Recency**: You prefer newer games
  - 2020+: 7.19 avg rating ⭐
  - Pre-2000: 5.25 avg rating

### How It Works
1. Analyzes your 361 rated games to identify patterns
2. Calculates preference scores for complexity, BGG rating, and recency
3. Scores each game from the BGG database based on these preferences
4. Prioritizes games matching your preferences (recent, heavy, highly-rated)

This means you'll see more games like **Ark Nova** (2021, 8.54, heavy) and fewer like **Brass: Birmingham** (2018, 8.57, older).

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

### Update Buy Recommendations (Personalized)
1. Run `python3 analyze_preferences.py` to analyze your ratings and create `preference_profile.json`
2. Run `python3 build_personalized_recommendations.py` to regenerate `bgg-recommendations.json`
3. This uses `boardgames_ranks.csv`, your preference profile, and excludes games in `excluded-game-ids.json`
4. Automatically personalizes based on your complexity, recency, and BGG rating preferences

### Update Buy Recommendations (Non-Personalized)
1. Run `python3 build_from_all_bgg_games.py` to regenerate `bgg-recommendations.json`
2. This uses only BGG rank (no personalization)

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
- `analyze_preferences.py` - Analyze your ratings to create preference profile
- `build_personalized_recommendations.py` - Build personalized buy recommendations (CURRENT)
- `test_filters.js` - Filter logic tests

### Alternative Scripts
- `build_from_all_bgg_games.py` - Build recommendations without personalization (rank-based only)

### Legacy Scripts (No Longer Used)
- `build_comprehensive_recommendations.py` - Old wishlist-based approach (147 games)
- `build_wishlist_recommendations.py` - Old wishlist-only approach (25 games)
- `apply_id_corrections.py` - Manual ID correction workflow
- `bgg-id-corrections.csv` - Manual ID corrections template
