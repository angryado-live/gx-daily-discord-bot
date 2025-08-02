import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

RAWG_API_KEY = os.getenv("RAWG_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def fetch_today_games():
    today = datetime.today().strftime('%Y-%m-%d')
    url = f"https://api.rawg.io/api/games?dates={today},{today}&ordering=-added&page_size=10&key={RAWG_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    games = response.json().get("results", [])
    return [f"{game['name']} ({game.get('released', 'N/A')})" for game in games]

def post_to_discord(games):
    if not games:
        content = "No new game releases today."
    else:
        content = "**🎮 New Game Releases Today:**\n" + "\n".join(f"• {g}" for g in games)

    data = {"content": content}
    requests.post(DISCORD_WEBHOOK, json=data)

if __name__ == "__main__":
    games = fetch_today_games()
    post_to_discord(games)
