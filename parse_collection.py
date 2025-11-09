#!/usr/bin/env python3
"""
Parse the board game collection CSV and create JSON files for:
1. Owned games (for recommendations)
2. List of owned/previously owned game IDs (for filtering BGG recommendations)
"""

import csv
import json

def parse_csv_to_json():
    owned_games = []
    excluded_game_ids = set()

    with open('collection.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            game_id = row['objectid']
            own = int(row['own']) if row['own'] else 0
            prevowned = int(row['prevowned']) if row['prevowned'] else 0

            # Track all owned and previously owned games to exclude from recommendations
            if own == 1 or prevowned == 1:
                excluded_game_ids.add(game_id)

            # Only include currently owned games for "What Should We Play" section
            if own == 1:
                game = {
                    'id': game_id,
                    'name': row['objectname'],
                    'rating': float(row['rating']) if row['rating'] else 0,
                    'numplays': int(row['numplays']) if row['numplays'] else 0,
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
                owned_games.append(game)

    # Save owned games to JSON
    with open('owned-games.json', 'w', encoding='utf-8') as f:
        json.dump(owned_games, f, indent=2)

    # Save excluded game IDs to JSON (for filtering BGG recommendations)
    with open('excluded-game-ids.json', 'w', encoding='utf-8') as f:
        json.dump(list(excluded_game_ids), f, indent=2)

    print(f"✓ Created owned-games.json with {len(owned_games)} games")
    print(f"✓ Created excluded-game-ids.json with {len(excluded_game_ids)} excluded games")

if __name__ == '__main__':
    parse_csv_to_json()
