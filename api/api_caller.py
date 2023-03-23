import requests
import sys

username = input("Please enter your username: ")

try:
    user_response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
except:
    print("Error!")
    sys.exit()

league_response = requests.get(f"https://api.sleeper.app/v1/user/{user_response.json()['user_id']}/leagues/nfl/2023")

league_name = input("Please enter the name of your league: ")

i = -1
for league in league_response.json():
    if league['name'] == league_name:
        i = league_response.json().index(league)

if i == -1:
    print("Error!")
    sys.exit()

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