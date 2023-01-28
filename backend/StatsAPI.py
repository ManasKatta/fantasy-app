import pymysql
from flask import Flask, request, jsonify
#from markupsafe import Markup
import json
from flaskext.mysql import MySQL

host = 'playerstats2022.cdwkaxkzcufq.us-east-2.rds.amazonaws.com'
user = 'admin'
password = 'Manas135'
database = 'fantasyapp'




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


if __name__ == '__main__':
    app.run(debug=True)