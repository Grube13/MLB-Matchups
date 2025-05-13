import statsapi
import json
from datetime import date

def get_team_stats(team_id):
    try:
        stats = statsapi.team_stats(team_id, group="hitting", type="season")
        hitting_stats = stats[0]['stats']['stats']
        pitching_stats = statsapi.team_stats(team_id, group="pitching", type="season")[0]['stats']['stats']
        return {
            "obp": float(hitting_stats.get('onBasePercentage', 0)),
            "slg": float(hitting_stats.get('sluggingPercentage', 0)),
            "era": float(pitching_stats.get('era', 4.5))
        }
    except Exception:
        return {"obp": 0.320, "slg": 0.410, "era": 4.25}

def get_top_batters(team_id):
    try:
        roster = statsapi.roster(team_id)
        player_ids = [p['person']['id'] for p in roster]
        batters = []
        for pid in player_ids:
            data = statsapi.player_stat_data(pid, group='hitting', type='season')
            ops = data['stats'].get('ops', '0.700')
            name = data['stats'].get('name', 'Unknown')
            batters.append({"name": name, "OPS": float(ops)})
        batters.sort(key=lambda x: x['OPS'], reverse=True)
        return batters[:3]
    except Exception:
        return [{"name": "Unknown", "OPS": 0.700}]

def calculate_score(team_stats, player_stats):
    obp = team_stats.get('obp', 0)
    slg = team_stats.get('slg', 0)
    era = team_stats.get('era', 4.5)
    avg_ops = sum([p['OPS'] for p in player_stats]) / len(player_stats) if player_stats else 0.7
    batting_power = (obp + slg) / 2
    pitching_quality = 1 / (era + 1)
    return round((batting_power * 0.4) + (pitching_quality * 0.3) + (avg_ops * 0.3), 3)

def main():
    games = statsapi.schedule(date=str(date.today()), sportId=1)
    results = []

    for g in games:
        home_id = g['home_id']
        away_id = g['away_id']
        home_name = g['home_name']
        away_name = g['away_name']

        home_stats = get_team_stats(home_id)
        away_stats = get_team_stats(away_id)

        home_batters = get_top_batters(home_id)
        away_batters = get_top_batters(away_id)

        home_score = calculate_score(home_stats, home_batters)
        away_score = calculate_score(away_stats, away_batters)

        favored = home_name if home_score > away_score else away_name

        results.append({
            "home": home_name,
            "away": away_name,
            "home_score": home_score,
            "away_score": away_score,
            "favored": favored
        })

    with open("matchup_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved matchup_results.json with {len(results)} games.")

if __name__ == "__main__":
    main()
