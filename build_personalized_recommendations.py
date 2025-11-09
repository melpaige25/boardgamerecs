#!/usr/bin/env python3
"""
Build personalized buy recommendations with REALISTIC filter values

Key fix: Use game categories to estimate varied complexity and duration
instead of using the same defaults for all games
"""

import csv
import json
from datetime import datetime

# Category-based estimates for complexity, duration, and player count
CATEGORY_ESTIMATES = {
    'wargames': {
        'avgweight': 4.0,
        'playingtime': 180,
        'minplayers': 1,
        'maxplayers': 4,
    },
    'strategygames': {
        'avgweight': 3.0,
        'playingtime': 90,
        'minplayers': 2,
        'maxplayers': 5,
    },
    'thematic': {
        'avgweight': 2.5,
        'playingtime': 90,
        'minplayers': 2,
        'maxplayers': 5,
    },
    'familygames': {
        'avgweight': 2.0,
        'playingtime': 45,
        'minplayers': 2,
        'maxplayers': 6,
    },
    'partygames': {
        'avgweight': 1.5,
        'playingtime': 30,
        'minplayers': 4,
        'maxplayers': 10,
    },
    'childrensgames': {
        'avgweight': 1.3,
        'playingtime': 20,
        'minplayers': 2,
        'maxplayers': 4,
    },
    'abstracts': {
        'avgweight': 2.0,
        'playingtime': 30,
        'minplayers': 2,
        'maxplayers': 2,
    },
    'cgs': {
        'avgweight': 2.5,
        'playingtime': 60,
        'minplayers': 2,
        'maxplayers': 2,
    },
}

# Priority order (based on user preferences for heavier games)
CATEGORY_PRIORITY = [
    'wargames',
    'strategygames',
    'thematic',
    'familygames',
    'cgs',
    'abstracts',
    'partygames',
    'childrensgames',
]

def get_game_estimates(row):
    """Get estimated complexity, duration, and player count from category"""
    # Check categories in priority order
    for category in CATEGORY_PRIORITY:
        rank_field = f'{category}_rank'
        if row.get(rank_field):
            return CATEGORY_ESTIMATES[category]

    # Default for uncategorized games
    return {
        'avgweight': 2.5,
        'playingtime': 60,
        'minplayers': 2,
        'maxplayers': 6,
    }

def load_collection_data():
    """Load actual game data from collection.csv for cross-referencing"""
    collection = {}
    with open('collection.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            game_id = row['objectid']
            try:
                collection[game_id] = {
                    'avgweight': float(row['avgweight']) if row['avgweight'] else None,
                    'playingtime': int(row['playingtime']) if row['playingtime'] else None,
                    'minplayers': int(row['minplayers']) if row['minplayers'] else None,
                    'maxplayers': int(row['maxplayers']) if row['maxplayers'] else None,
                }
            except:
                pass
    return collection

def get_weight_score(weight, profile):
    """Calculate score based on complexity preference"""
    for min_w, max_w, avg_rating in profile['weight_preferences']:
        if min_w <= weight < max_w:
            return avg_rating
    return profile['baseline_rating']

def get_bgg_score(bgg_avg, profile):
    """Calculate score based on BGG rating preference"""
    for min_bgg, max_bgg, avg_rating in profile['bgg_preferences']:
        if min_bgg <= bgg_avg < max_bgg:
            return avg_rating
    return profile['baseline_rating']

def get_year_score(year, profile):
    """Calculate score based on year preference"""
    for min_y, max_y, avg_rating in profile['year_preferences']:
        if min_y <= year < max_y:
            return avg_rating
    return profile['baseline_rating']

def build_personalized_recommendations():
    # Load preference profile
    try:
        with open('preference_profile.json', 'r', encoding='utf-8') as f:
            profile = json.load(f)
        print("✓ Loaded preference profile")
    except FileNotFoundError:
        print("Error: preference_profile.json not found. Run analyze_preferences.py first.")
        return

    # Load excluded game IDs
    with open('excluded-game-ids.json', 'r', encoding='utf-8') as f:
        excluded_ids = set(json.load(f))
    print(f"✓ Loaded {len(excluded_ids)} excluded game IDs")

    # Load collection data for cross-referencing
    collection_data = load_collection_data()
    print(f"✓ Loaded {len(collection_data)} games from collection for cross-reference")

    # Load BGG rankings and score them
    recommendations = []
    excluded_count = 0
    expansion_count = 0
    current_year = datetime.now().year
    crossref_count = 0

    with open('boardgames_ranks.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Only use ranked games in top 5000
            rank_str = row['rank'].strip() if row['rank'] else ''
            if not rank_str or rank_str == '0':
                continue

            rank = int(rank_str)
            if rank > 5000:
                continue

            game_id = row['id']

            # Exclude owned/previously owned
            if game_id in excluded_ids:
                excluded_count += 1
                continue

            # Exclude expansions
            is_expansion = int(row['is_expansion']) if row['is_expansion'] else 0
            if is_expansion == 1:
                expansion_count += 1
                continue

            # Extract game data
            year = int(row['yearpublished']) if row['yearpublished'] else current_year
            bgg_avg = float(row['average']) if row['average'] else 0

            # Get estimates from category or collection data
            if game_id in collection_data:
                # Use actual data from collection
                estimates = collection_data[game_id]
                crossref_count += 1
            else:
                # Use category-based estimates
                estimates = get_game_estimates(row)

            weight = estimates['avgweight'] or 2.5
            playtime = estimates['playingtime'] or 60
            minplayers = estimates['minplayers'] or 2
            maxplayers = estimates['maxplayers'] or 6

            # Calculate personalized score
            weight_score = get_weight_score(weight, profile)
            bgg_score = get_bgg_score(bgg_avg, profile)
            year_score = get_year_score(year, profile)

            # Weighted average: BGG preference is strongest signal
            personalized_score = (
                bgg_score * 0.5 +     # BGG consensus
                weight_score * 0.3 +  # Complexity preference
                year_score * 0.2      # Recency preference
            )

            # Boost by BGG rank
            rank_boost = max(0, (5001 - rank) / 5000 * 0.5)
            final_score = personalized_score + rank_boost

            game = {
                'id': game_id,
                'name': row['name'],
                'rating': 0,
                'avgweight': weight,
                'minplayers': minplayers,
                'maxplayers': maxplayers,
                'playingtime': playtime,
                'yearpublished': str(year),
                'average': bgg_avg,
                'itemtype': 'boardgame',
                'bggbestplayers': '',
                'bggrecplayers': '',
                'personalizedScore': round(final_score, 3),
                'rank': rank,
            }

            recommendations.append(game)

    # Sort by personalized score
    recommendations.sort(key=lambda x: x['personalizedScore'], reverse=True)

    # Remove temporary fields
    for game in recommendations:
        del game['personalizedScore']
        del game['rank']

    # Save recommendations
    with open('bgg-recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(recommendations, f, indent=2)

    print(f"\n{'='*70}")
    print(f"✓ Created personalized bgg-recommendations.json with {len(recommendations)} games")
    print(f"  - Source: Top 5000 ranked BGG games")
    print(f"  - Excluded expansions: {expansion_count}")
    print(f"  - Excluded owned/prev owned: {excluded_count}")
    print(f"  - Cross-referenced with collection: {crossref_count} games")
    print(f"  - Category-based estimates: {len(recommendations) - crossref_count} games")
    print(f"  - Sorted by personalized preference score")
    print(f"{'='*70}")

    # Analyze variety in filter values
    print(f"\n✓ Filter value variety:")

    weight_dist = {}
    for game in recommendations:
        w = game['avgweight']
        bucket = f"{int(w)}.0-{int(w)+1}.0"
        weight_dist[bucket] = weight_dist.get(bucket, 0) + 1
    print(f"  Complexity distribution:")
    for bucket in sorted(weight_dist.keys()):
        print(f"    {bucket}: {weight_dist[bucket]} games")

    time_dist = {}
    for game in recommendations:
        t = game['playingtime']
        if t <= 30: bucket = 'Quick (≤30)'
        elif t <= 60: bucket = 'Medium (31-60)'
        elif t <= 90: bucket = 'Long (61-90)'
        else: bucket = 'Very Long (>90)'
        time_dist[bucket] = time_dist.get(bucket, 0) + 1
    print(f"  Duration distribution:")
    for bucket in ['Quick (≤30)', 'Medium (31-60)', 'Long (61-90)', 'Very Long (>90)']:
        if bucket in time_dist:
            print(f"    {bucket}: {time_dist[bucket]} games")

    print(f"\nTop 10 personalized recommendations:")
    for i, game in enumerate(recommendations[:10], 1):
        print(f"  #{i:2d} - {game['name']:45s} Weight: {game['avgweight']:.1f}, Time: {game['playingtime']}min, Players: {game['minplayers']}-{game['maxplayers']}")

if __name__ == '__main__':
    build_personalized_recommendations()
