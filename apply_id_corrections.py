#!/usr/bin/env python3
"""
Apply BGG ID corrections from the CSV file to bgg-recommendations.json
"""

import csv
import json

def apply_corrections():
    # Load the corrections CSV
    corrections = {}
    with open('bgg-id-corrections.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            game_name = row['Game Name']
            correct_id = row['Correct ID (fill this in)'].strip()

            if correct_id:  # Only process if correct ID is filled in
                corrections[game_name] = correct_id

    print(f"Found {len(corrections)} corrections in CSV file\n")

    # Load the games JSON
    with open('bgg-recommendations.json', 'r', encoding='utf-8') as f:
        games = json.load(f)

    # Apply corrections
    updated_count = 0
    for game in games:
        if game['name'] in corrections:
            old_id = game['id']
            new_id = corrections[game['name']]

            if old_id != new_id:
                print(f"✓ {game['name']}: {old_id} -> {new_id}")
                game['id'] = new_id
                updated_count += 1
            else:
                print(f"  {game['name']}: Already correct ({old_id})")

    # Save updated JSON
    with open('bgg-recommendations.json', 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✓ Updated {updated_count} game IDs")
    print(f"✓ Saved to bgg-recommendations.json")
    print(f"{'='*60}")

if __name__ == '__main__':
    apply_corrections()
