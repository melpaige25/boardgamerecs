#!/usr/bin/env python3
"""
Build buy recommendations from user's BGG wishlist/want list
This ensures all IDs are correct since they come from the user's own BGG data
"""

import csv
import json

def build_from_wishlist():
    wishlist_games = []

    with open('collection.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Check if game is wanted but not owned/previously owned
            want = int(row['want']) if row['want'] else 0
            wanttobuy = int(row['wanttobuy']) if row['wanttobuy'] else 0
            wanttoplay = int(row['wanttoplay']) if row['wanttoplay'] else 0
            wishlist = int(row['wishlist']) if row['wishlist'] else 0
            own = int(row['own']) if row['own'] else 0
            prevowned = int(row['prevowned']) if row['prevowned'] else 0

            # Only include if wanted and NOT owned/previously owned
            if (want or wanttobuy or wanttoplay or wishlist) and not own and not prevowned:
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
                wishlist_games.append(game)

    # Sort by BGG average rating
    wishlist_games.sort(key=lambda x: x['average'], reverse=True)

    # Save to JSON
    with open('bgg-recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(wishlist_games, f, indent=2)

    print(f"✓ Created bgg-recommendations.json with {len(wishlist_games)} games from your wishlist")
    print(f"✓ All game IDs are correct (from your BGG collection)")

    if len(wishlist_games) > 0:
        print(f"\nTop 5 recommendations:")
        for game in wishlist_games[:5]:
            print(f"  - {game['name']} (Rating: {game['average']:.1f})")
    else:
        print("\n⚠ No wishlist games found!")
        print("  Make sure you have games marked as 'want', 'wanttobuy', 'wanttoplay', or 'wishlist' in BGG")

if __name__ == '__main__':
    build_from_wishlist()
