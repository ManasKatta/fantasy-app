import requests
import json

user_response = requests.get("https://api.sleeper.app/v1/user/monkeyfire2987")
print(f"User ID: {user_response.json()['user_id']}")

league_response = requests.get(f"https://api.sleeper.app/v1/user/{user_response.json()['user_id']}/leagues/nfl/2023")
print(f"League ID: {league_response.json()[0]['league_id']}")

league_users_response = requests.get(f"https://api.sleeper.app/v1/league/{league_response.json()[0]['league_id']}/users")
rosters_response = requests.get(f"https://api.sleeper.app/v1/league/{league_response.json()[0]['league_id']}/rosters")
players_response = requests.get("https://api.sleeper.app/v1/players/nfl")

print()

for x in range(len(rosters_response.json())):
    print(f"{league_users_response.json()[x]['display_name']}:", end = " ")
    for y in rosters_response.json()[x]['starters']:
        try:
            print(f"{players_response.json()[y]['full_name']} ", end = " ")
        except:
            print(y)