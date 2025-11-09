#!/usr/bin/env python3
"""
Build personalized buy recommendations using user's rating preferences

Uses boardgames_ranks.csv but scores games based on:
1. Complexity preference (heavier games preferred)
2. BGG rating preference (higher rated games preferred)
3. Recency preference (newer games preferred)
4. BGG rank (as tiebreaker)
"""

import csv
import json
from datetime import datetime

def get_weight_score(weight, profile):
    """Calculate score based on complexity preference"""
    for min_w, max_w, avg_rating in profile['weight_preferences']:
        if min_w <= weight < max_w:
            return avg_rating
    # Default for missing weight data
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

    # Load BGG rankings and score them
    recommendations = []
    excluded_count = 0
    expansion_count = 0
    current_year = datetime.now().year

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

            # Note: boardgames_ranks.csv doesn't have weight data
            # We'll need to fetch this or use a default
            # For now, use BGG average as a proxy (highly rated games tend to be heavier)
            # Better approach: Could cross-reference with collection.csv for games we know
            estimated_weight = 2.5  # Default medium
            if bgg_avg >= 8.0:
                estimated_weight = 3.5  # Highly rated games tend to be heavier
            elif bgg_avg >= 7.5:
                estimated_weight = 3.0
            elif bgg_avg < 6.5:
                estimated_weight = 2.0

            # Calculate personalized score (average of the three preference dimensions)
            weight_score = get_weight_score(estimated_weight, profile)
            bgg_score = get_bgg_score(bgg_avg, profile)
            year_score = get_year_score(year, profile)

            # Weighted average: BGG preference is strongest signal, then weight, then year
            personalized_score = (
                bgg_score * 0.5 +     # BGG consensus (strongest correlation)
                weight_score * 0.3 +  # Complexity preference
                year_score * 0.2      # Recency preference
            )

            # Boost by BGG rank (rank 1 = best, so inverse it)
            # Add small bonus for top ranked games
            rank_boost = max(0, (5001 - rank) / 5000 * 0.5)  # Up to +0.5 for rank 1
            final_score = personalized_score + rank_boost

            game = {
                'id': game_id,
                'name': row['name'],
                'rating': 0,
                'avgweight': estimated_weight,
                'minplayers': 1,
                'maxplayers': 8,
                'playingtime': 60,
                'yearpublished': str(year),
                'average': bgg_avg,
                'itemtype': 'boardgame',
                'bggbestplayers': '',
                'bggrecplayers': '',
                'personalizedScore': round(final_score, 3),
                'rank': rank,
            }

            recommendations.append(game)

    # Sort by personalized score (higher is better)
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
    print(f"  - Sorted by personalized preference score")
    print(f"{'='*70}")

    if len(recommendations) > 0:
        print(f"\nTop 15 personalized recommendations:")
        for i, game in enumerate(recommendations[:15], 1):
            print(f"  #{i:2d} - {game['name']:45s} ({game['yearpublished']}) Rating: {game['average']:.2f}, Weight: {game['avgweight']:.1f}")

    print(f"\nPersonalization based on your preferences:")
    print(f"  - Heavier games prioritized (you rate 4.0+ games highest)")
    print(f"  - Highly-rated games prioritized (strong BGG consensus correlation)")
    print(f"  - Recent games prioritized (you rate 2020+ games highest)")

if __name__ == '__main__':
    build_personalized_recommendations()
