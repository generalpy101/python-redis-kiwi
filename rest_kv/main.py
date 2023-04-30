import json

import redis
from flask import Flask, Response, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException

app = Flask(__name__)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.errorhandler(HTTPException)
def handle_http_exceptions(err):
    """
    Custom handler for HTTP exceptions.
    Returns JSON output instead of HTML.
    """
    response = err.get_response()
    payload = {"status_code": err.code, "error": err.name, "message": err.description}
    response.data = json.dumps(payload)
    response.content_type = "application/json"
    return response


class KeyNotFound(HTTPException):
    code = 404
    description = "No such key exists"


@app.route("/get", methods=["GET"])
def get_keys():
    key = request.args.get("key")
    if not key:
        payload = {"error": "No key provided", "status_code": "400"}
        return jsonify(payload), 400
    value = redis_client.get(key)
    if not value:
        raise KeyNotFound
    payload = {f"{key}": value, "status_code": 200}
    return jsonify(payload)


@app.route("/set", methods=["POST"])
def set_keys():
    try:
        data = request.get_json()
        key = data.get("key")
        value = data.get("value")

        if not key or not value:
            payload = {"error": "No key or value provided", "status_code": 400}
            return jsonify(payload), 400

        redis_client.set(key, value)
        return Response(f"{key}:{value}")
    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400


@app.route("/delete", methods=["DELETE"])
def delete_keys():
    try:
        data = request.get_json()
        key = data.get("key")

        if not key:
            return Response("No key provided", status=400)

        status = redis_client.delete(key)
        if not status:
            raise KeyNotFound

        return Response(f"{key} deleted")

    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400


if __name__ == "__main__":
    app.run(port=8000, debug=True)
