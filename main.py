import requests
from datetime import datetime
import pytz
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

def fetch_games():
    url = "https://games.api.opera.com/games"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_todays_games(games):
    today = datetime.now(pytz.utc).date()
    return [
        game for game in games
        if 'release_date' in game and
        datetime.strptime(game['release_date'], '%Y-%m-%dT%H:%M:%SZ').date() == today
    ]

def post_to_discord(games):
    if not games:
        return
    message = "**🎮 New Game Releases Today:**\n"
    for game in games:
        title = game.get('title', 'Unknown Title')
        platforms = game.get('platforms', [])
        platform_str = ", ".join(platforms)
        message += f"- **{title}** ({platform_str})\n"
    requests.post(WEBHOOK_URL, json={"content": message})

def main():
    games = fetch_games()
    todays_games = get_todays_games(games)
    post_to_discord(todays_games)

if __name__ == "__main__":
    main()
# test commit
