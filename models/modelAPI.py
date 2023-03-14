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
    xgbmodule.fb.change(player_name=name, player_pos=pos)
    result = xgbmodule.fb.predict()
    return (jsonify(result))