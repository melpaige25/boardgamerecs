#!/usr/bin/env python3
"""
Build buy recommendations from:
1. User's BGG wishlist/want list (highest priority)
2. Games in collection that are rated/tracked but not owned (correct IDs!)
This gives a much larger pool while ensuring all IDs are accurate.
"""

import csv
import json

def build_comprehensive_recommendations():
    wishlist_games = []
    tracked_games = []

    with open('collection.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Parse ownership flags
            want = int(row['want']) if row['want'] else 0
            wanttobuy = int(row['wanttobuy']) if row['wanttobuy'] else 0
            wanttoplay = int(row['wanttoplay']) if row['wanttoplay'] else 0
            wishlist = int(row['wishlist']) if row['wishlist'] else 0
            own = int(row['own']) if row['own'] else 0
            prevowned = int(row['prevowned']) if row['prevowned'] else 0

            # Skip owned/previously owned
            if own or prevowned:
                continue

            game = {
                'id': row['objectid'],
                'name': row['objectname'],
                'rating': float(row['rating']) if row['rating'] else 0,
                'avgweight': float(row['avgweight']) if row['avgweight'] else 0,
                'minplayers': int(row['minplayers']) if row['minplayers'] else 0,
                'maxplayers': int(row['maxplayers']) if row['maxplayers'] else 0,
                'playingtime': int(row['playingtime']) if row['playingtime'] else 0,
                'yearpublished': row['yearpublished'],
                'average': float(row['average']) if row['average'] else 0,
                'itemtype': row['itemtype'],
                'bggbestplayers': row['bggbestplayers'],
                'bggrecplayers': row['bggrecplayers']
            }

            # Prioritize wishlist games
            if want or wanttobuy or wanttoplay or wishlist:
                wishlist_games.append(game)
            else:
                # Other games (rated/tracked but not explicitly wanted)
                tracked_games.append(game)

    # Combine: wishlist first, then tracked games
    all_games = wishlist_games + tracked_games

    # Sort by BGG average rating
    all_games.sort(key=lambda x: x['average'], reverse=True)

    # Save to JSON
    with open('bgg-recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(all_games, f, indent=2)

    print(f"✓ Created bgg-recommendations.json with {len(all_games)} games")
    print(f"  - Wishlist games: {len(wishlist_games)}")
    print(f"  - Rated/tracked games: {len(tracked_games)}")
    print(f"✓ All game IDs are correct (from your BGG collection)")

    if len(all_games) > 0:
        print(f"\nTop 10 recommendations:")
        for game in all_games[:10]:
            priority = "⭐ WISHLIST" if game in wishlist_games else "   Tracked"
            print(f"  {priority} - {game['name']} (Rating: {game['average']:.1f})")

if __name__ == '__main__':
    build_comprehensive_recommendations()
