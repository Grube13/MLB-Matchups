import json

# Dummy matchup data
matchups = [
    {
        "away_team": "Yankees",
        "home_team": "Red Sox",
        "away_pitcher": "Gerrit Cole",
        "home_pitcher": "Chris Sale",
        "venue": "Fenway Park"
    }
]

# Write to JSON file
with open("matchup_results.json", "w") as f:
    json.dump(matchups, f, indent=2)
