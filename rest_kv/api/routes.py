import json

from flask import Blueprint, Response, current_app, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException

api_bp = Blueprint("api", __name__)


@api_bp.errorhandler(HTTPException)
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


@api_bp.route("/all", methods=["GET"])
def get_all_pairs():
    resp = {}
    keys = current_app.redis_client.keys()
    for key in keys:
        key_type = current_app.redis_client.type(key)
        if key_type == "hash":
            value = current_app.redis_client.hgetall(key)
        else:
            value = current_app.redis_client.get(key)
        resp[key] = value
    return jsonify(resp)


@api_bp.route("/get", methods=["GET"])
def get_keys():
    keys = request.args.get("keys")
    if not keys:
        payload = {"error": "No keys provided", "status_code": "400"}
        return jsonify(payload), 400
    keys = keys.split(",")
    values = []
    for key in keys:
        key_type = current_app.redis_client.type(key)
        if key_type == "hash":
            value = current_app.redis_client.hgetall(key)
        else:
            value = current_app.redis_client.get(key)
        if value:
            values.append(value)
        else:
            values.append(None)

    payload = {k: v for k, v in zip(keys, values)}
    return jsonify(payload)


@api_bp.route("/set", methods=["POST"])
def set_keys():
    try:
        data = request.get_json()

        if not data:
            payload = {"error": "No key values pairs provided", "status_code": 400}
            return jsonify(payload), 400

        resp = {}

        for key, value in data.items():
            if type(value) == dict:
                status = current_app.redis_client.hset(key, mapping=value)
            else:
                status = current_app.redis_client.set(key, value)
            resp[key] = status

        return jsonify(resp)

    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400


@api_bp.route("/delete", methods=["POST"])
def delete_keys():
    try:
        data = request.get_json()
        keys = data.get("keys")

        if not keys:
            return Response("No keys provided to delete", status=400)

        resp = {}
        for key in keys:
            status = current_app.redis_client.delete(key)
            resp[key] = bool(status)

        return jsonify(resp)

    except BadRequest as e:
        print(e)
        payload = {"error": e.description, "status_code": 400}
        return jsonify(payload), 400
