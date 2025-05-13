import statsapi
import json
from datetime import datetime

def get_today_matchups():
    today = datetime.now().strftime('%Y-%m-%d')
    schedule = statsapi.schedule(start_date=today, end_date=today)
    matchups = []

    for game in schedule:
        if 'awayProbablePitcher' in game and 'homeProbablePitcher' in game:
            matchup = {
                'game_date': game['game_date'],
                'away_team': game['away_name'],
                'home_team': game['home_name'],
                'away_pitcher': game['awayProbablePitcher']['fullName'],
                'home_pitcher': game['homeProbablePitcher']['fullName'],
                'venue': game['venue_name']
            }
            matchups.append(matchup)

    return matchups

matchups = get_today_matchups()

with open('matchup_results.json', 'w') as f:
    json.dump(matchups, f, indent=4)

print(f"Saved {len(matchups)} matchups to matchup_results.json")
