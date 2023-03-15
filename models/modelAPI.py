from flask import Flask, request, jsonify
#from markupsafe import Markup
import json
import xgbmodule

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if(request.method == 'POST'):
        reception = request.get_json()
        return jsonify({'receieved' : reception}), 201
    else:
        return jsonify({"Results" : "Test Success"})

@app.route('/GetValue/<string:name>/<string:pos>', methods=['GET'])
def get_value(name, pos):
    fb = xgbmodule.FantasyBoost(player_name=name, player_pos=pos)
    
    result = fb.predict()
    return (jsonify(result.tolist()))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=7000)