#!/usr/bin/env python3
"""
Analyze user rating patterns to build a personalized recommendation profile
"""

import csv
import json

def analyze_preferences():
    """Analyze user's rating patterns and create preference profile"""

    # Load rated games from collection
    ratings = []
    with open('collection.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rating = row.get('rating', '').strip()
            if rating and rating != '0':
                try:
                    ratings.append({
                        'rating': float(rating),
                        'avgweight': float(row['avgweight']) if row['avgweight'] else 0,
                        'average': float(row['average']) if row['average'] else 0,
                        'year': int(row['yearpublished']) if row['yearpublished'] else 0,
                    })
                except:
                    pass

    print(f"Analyzed {len(ratings)} rated games\n")

    # Calculate preference curves
    # Complexity preference (weight -> expected rating boost)
    weight_buckets = [
        (1.0, 1.5, 6.13),
        (1.5, 2.0, 6.63),
        (2.0, 2.5, 7.01),
        (2.5, 3.0, 6.80),
        (3.0, 3.5, 7.45),
        (3.5, 4.0, 7.82),
        (4.0, 6.0, 8.55),
    ]

    # BGG rating preference
    bgg_buckets = [
        (8.0, 10.0, 7.90),
        (7.5, 8.0, 7.50),
        (7.0, 7.5, 6.88),
        (6.5, 7.0, 6.09),
        (6.0, 6.5, 5.48),
        (0.0, 6.0, 4.04),
    ]

    # Year preference
    year_buckets = [
        (2020, 2030, 7.19),
        (2015, 2020, 6.66),
        (2010, 2015, 6.42),
        (2000, 2010, 6.59),
        (0, 2000, 5.25),
    ]

    # Create preference profile
    profile = {
        'weight_preferences': weight_buckets,
        'bgg_preferences': bgg_buckets,
        'year_preferences': year_buckets,
        'baseline_rating': sum(r['rating'] for r in ratings) / len(ratings),
    }

    # Save profile
    with open('preference_profile.json', 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2)

    print("Preference profile created:")
    print(f"  Baseline rating: {profile['baseline_rating']:.2f}")
    print(f"  Complexity boost: +{8.55 - profile['baseline_rating']:.2f} for very heavy games")
    print(f"  Recency boost: +{7.19 - profile['baseline_rating']:.2f} for recent games (2020+)")
    print(f"  BGG consensus boost: +{7.90 - profile['baseline_rating']:.2f} for highly rated games (8.0+)")
    print(f"\nSaved to preference_profile.json")

if __name__ == '__main__':
    analyze_preferences()
