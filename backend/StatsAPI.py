from flask import Flask, request, jsonify
#from markupsafe import Markup
import json
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Manas135'
app.config['MYSQL_DATABASE_DB'] = 'capstone'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'



mysql.init_app(app)
# conn = mysql.connect()
#mycursor = conn.cursor()

@app.route('/getPlayerStats/<string:name>', methods=['GET'])
def get_player_stats(name):
    query_parameter = '%' + name + '%'
    conn = mysql.connect()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM playerstats2022 WHERE Player LIKE %s", (query_parameter)) 
    result = mycursor.fetchall()
    mycursor.close()
    conn.close()
    return (jsonify(result))


if __name__ == '__main__':
    app.run(debug=True)