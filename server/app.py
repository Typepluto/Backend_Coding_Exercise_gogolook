import flask
from flask import request, jsonify, Response
import os
from tempdb import TempDB

temp_db = TempDB()
app = flask.Flask(import_name=__name__)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    r = {"result": temp_db.read_all()}
    return jsonify(r)


@app.route('/task', methods=['POST'])
def post_task():
    data = request.json
    r = {"result": temp_db.create(data)}
    return jsonify(r), 201


@app.route('/task/<int:primary_key>', methods=['PUT'])
def put_task(primary_key):
    data = request.json
    r = temp_db.update(data, primary_key)
    return jsonify(r), 200


@app.route('/task/<int:primary_key>', methods=['DELETE'])
def delete_task(primary_key):
    temp_db.delete(primary_key)
    return Response(status=200, mimetype='application/json')


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = True if os.environ.get("APP_DEBUG") else False
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 80)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
