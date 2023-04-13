import requests
import sys


"""def call_api(username, league_name):
    try:
        user_response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
        league_response = requests.get(f"https://api.sleeper.app/v1/user/{user_response.json()['user_id']}/leagues/nfl/2023")
    except:
        print("Error!")
        sys.exit()

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
        for y in rosters_response.json()[x]['players']:
            try:
                print(f"{players_response.json()[y]['full_name']}({players_response.json()[y]['player_id']}) ", end = " ")
            except:
                print(y)"""

def call_api(username, league_name):
    id_arr = []
    try:
        user_response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
        league_response = requests.get(f"https://api.sleeper.app/v1/user/{user_response.json()['user_id']}/leagues/nfl/2023")
    except:
        print("Error!")
        sys.exit()

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


    for x in range(len(rosters_response.json())):
        if league_users_response.json()[x]['display_name'] == username:
            for y in range(len(rosters_response.json())):
                if(league_users_response.json()[x]['user_id'] == rosters_response.json()[y]['owner_id']):
                    for z in rosters_response.json()[y]['players']:
                        id_arr.append(players_response.json()[z]['player_id'])
    
    return id_arr

result = call_api("monkeyfire2987", "Capstone league")
print(result)