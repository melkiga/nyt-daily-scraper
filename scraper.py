import requests
import json
import re
from datetime import datetime

# Apni ScrapingBee API Key yahan dalein
API_KEY = "0H648XHAU6JCPP1O6QGWSH4TDA2AUZGIGAQ3BJXTV2E4V7QXJP46BRD1BFQFPCIY5KMVUNNIGPISV9O7"


def get_nyt_game_data(game_name):
    target_url = f"https://www.nytimes.com/puzzles/{game_name}"
    api_url = "https://app.scrapingbee.com/api/v1/"
    params = {
        "api_key": API_KEY,
        "url": target_url,
        "premium_proxy": "true",
        "country_code": "us",
        "render_js": "false",
    }
    try:
        res = requests.get(api_url, params=params, timeout=45)
        match = re.search(r"window\.gameData\s*=\s*(\{.*?\})(?=;|</script>)", res.text, re.DOTALL)
        if match:
            return json.loads(match.group(1)).get("today", {})
    except:
        return {}
    return {}


def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🚀 Fetching Data at {now}...")

    # Spelling Bee aur Connections ka data nikalna
    bee = get_nyt_game_data("spelling-bee")
    conn = get_nyt_game_data("connections")

    master_json = {
        "last_updated": now,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "spelling_bee": {
            "letters": {"center": bee.get("centerLetter"), "outer": bee.get("outerLetters")},
            "answers": bee.get("answers"),
            "pangrams": bee.get("pangrams"),
        },
        "connections": {"categories": conn.get("categories", [])},
        "status": "Success",
    }

    # File write karna
    with open("data.json", "w") as f:
        json.dump(master_json, f, indent=4)
    print("✅ data.json locally updated.")


if __name__ == "__main__":
    main()
