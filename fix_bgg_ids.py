#!/usr/bin/env python3
"""
Fix BGG game IDs by searching for each game name on BoardGameGeek
"""

import json
import time
import xml.etree.ElementTree as ET
try:
    import requests
except ImportError:
    print("Installing requests library...")
    import subprocess
    subprocess.check_call(['pip3', 'install', 'requests'])
    import requests

def search_game_id(game_name, year=None):
    """Search for a game on BGG and return the correct ID"""
    # BGG XML API search endpoint
    url = f"https://boardgamegeek.com/xmlapi2/search?query={requests.utils.quote(game_name)}&type=boardgame&exact=1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        root = ET.fromstring(response.content)
        items = root.findall('item')

        if not items:
            # Try non-exact search
            url = f"https://boardgamegeek.com/xmlapi2/search?query={requests.utils.quote(game_name)}&type=boardgame"
            response = requests.get(url, timeout=10)
            root = ET.fromstring(response.content)
            items = root.findall('item')

        if items:
            # If year provided, try to match it
            if year:
                for item in items:
                    item_year = item.find('yearpublished')
                    if item_year is not None and item_year.get('value') == str(year):
                        return item.get('id')

            # Return first result
            return items[0].get('id')

        return None

    except Exception as e:
        print(f"Error searching for {game_name}: {e}")
        return None

def fix_all_ids():
    """Fix all game IDs in bgg-recommendations.json"""
    print("Loading bgg-recommendations.json...")
    with open('bgg-recommendations.json', 'r') as f:
        games = json.load(f)

    print(f"Found {len(games)} games to fix\n")

    fixed_count = 0
    failed = []

    for i, game in enumerate(games, 1):
        name = game['name']
        year = game.get('yearpublished')
        old_id = game['id']

        print(f"{i}/{len(games)}: Searching for '{name}' ({year})...")

        new_id = search_game_id(name, year)

        if new_id:
            if new_id != old_id:
                print(f"  ✓ Fixed: {old_id} -> {new_id}")
                game['id'] = new_id
                fixed_count += 1
            else:
                print(f"  ✓ Already correct: {new_id}")
        else:
            print(f"  ✗ Could not find ID for {name}")
            failed.append(name)

        # Rate limiting
        time.sleep(1)

    # Save the fixed file
    with open('bgg-recommendations.json', 'w') as f:
        json.dump(games, f, indent=2)

    print("\n" + "=" * 60)
    print(f"✓ Fixed {fixed_count} game IDs")
    print(f"✓ Saved to bgg-recommendations.json")

    if failed:
        print(f"\n⚠ Failed to find {len(failed)} games:")
        for name in failed:
            print(f"  - {name}")

    print("=" * 60)

if __name__ == '__main__':
    fix_all_ids()
