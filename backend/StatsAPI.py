import pymysql
from flask import Flask, request, jsonify
#from markupsafe import Markup
import json
from flaskext.mysql import MySQL
import requests
import suggestor


host = 'localhost'
user = 'root'
password = 'Manas135'
database = 'capstone'


def call_api(username, league_name):
    try:
        user_response = requests.get(f"https://api.sleeper.app/v1/user/{username}")
        league_response = requests.get(f"https://api.sleeper.app/v1/user/{user_response.json()['user_id']}/leagues/nfl/2023")
    except Exception as e:
        return f"Error: {e}"

    i = -1
    for league in league_response.json():
        if league['name'] == league_name:
            i = league_response.json().index(league)

    if i == -1:
        return "Error: League not found"

    players_dict = {}
    players_dict['roster_positions'] = league_response.json()[i]['roster_positions']
    players_dict['teams'] = []

    league_users_response = requests.get(f"https://api.sleeper.app/v1/league/{league_response.json()[i]['league_id']}/users")
    rosters_response = requests.get(f"https://api.sleeper.app/v1/league/{league_response.json()[i]['league_id']}/rosters")
    #players_response = requests.get("https://api.sleeper.app/v1/players/nfl")

    for x in range(len(league_users_response.json())):
            for y in range(len(rosters_response.json())):
                if(league_users_response.json()[x]['user_id'] == rosters_response.json()[y]['owner_id']):
                    if league_users_response.json()[x]['display_name'] == username:
                        players_dict['teams'].insert(0, rosters_response.json()[y]['players'])
                    else:
                        players_dict['teams'].append(rosters_response.json()[y]['players'])

    return players_dict

app = Flask(__name__)
@app.route('/getPlayerStats/<string:name>', methods=['GET'])
def get_player_stats(name):
    query_parameter = '%' + name + '%'
    connection = pymysql.connect(host= host,
                             user= user,
                             password= password,
                             database= database,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM playerstats2022 WHERE Player LIKE %s", (query_parameter)) 
    result = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return (jsonify(result))

@app.route('/getTop/', methods=['GET'])
def get_top():
    #query_parameter = '%' + name + '%'
    connection = pymysql.connect(host= host,
                             user= user,
                             password= password,
                             database= database,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM playerstats2022 ORDER BY FantPt DESC LIMIT 10") 
    result = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return (jsonify(result))

@app.route('/getUserTeam/<string:name>/<string:league>', methods=['GET'])
def get_player_team(name, league):
    result = call_api(name, league)
    return (jsonify(result['teams'][0]))

@app.route('/getTrades/<string:name>/<string:league>', methods=['GET'])
def get_trades(name, league):
    api_result = call_api(name, league)
    result = suggestor.suggest_trades(api_result['roster_positions'], api_result['teams'])
    return (jsonify(result))


if __name__ == '__main__':
    app.run(debug=True)