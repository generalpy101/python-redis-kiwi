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
    keys = request.args.get("keys")
    if not keys:
        payload = {"error": "No keys provided", "status_code": "400"}
        return jsonify(payload), 400
    keys = keys.split(",")
    values = []
    for key in keys:
        value = redis_client.get(key)
        if value:
            values.append(value)
        else:
            values.append(None)

    payload = {k: v for k, v in zip(keys, values)}
    return jsonify(payload)


@app.route("/set", methods=["POST"])
def set_keys():
    try:
        data = request.get_json()
        print(data)

        if not data:
            payload = {"error": "No key values pairs provided", "status_code": 400}
            return jsonify(payload), 400

        for key, value in data.items():
            status = redis_client.set(key, value)
            if not status:
                payload = {
                    "error": "Server Error",
                    "description": f"Error while writing pair f{key}:f{value}",
                    "status_code": 500,
                }
                return jsonify(payload), 500

        payload = dict(data)
        payload["status_code"] = 200
        return jsonify(payload)

    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400


@app.route("/delete", methods=["POST"])
def delete_keys():
    try:
        data = request.get_json()
        keys = data.get("keys")

        if not keys:
            return Response("No keys provided to delete", status=400)

        resp = {}
        for key in keys:
            status = redis_client.delete(key)
            resp[key] = bool(status)

        return jsonify(resp)

    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400


if __name__ == "__main__":
    app.run(port=8000, debug=True)
