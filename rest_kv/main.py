import redis
from flask import Flask, Response, request

app = Flask(__name__)
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


@app.route("/get", methods=["GET"])
def get_keys():
    key = request.args.get("key")
    if not key:
        return Response("No key provided", status=400)
    value = redis_client.get(key)
    if not value:
        return Response("No value found", status=404)
    return Response(value, status=200)


@app.route("/set", methods=["POST"])
def set_keys():
    try:
        data = request.get_json()
        key = data.get("key")
        value = data.get("value")

        if not key or not value:
            return Response("No key or value provided", status=400)

        redis_client.set(key, value)
        return Response(f"{key}:{value}")
    except Exception as e:
        print(e)
        return Response(f"Server error occure: {e}", status=500)


@app.route("/delete", methods=["DELETE"])
def delete_keys():
    try:
        data = request.get_json()
        key = data.get("key")

        if not key:
            return Response("No key provided", status=400)

        status = redis_client.delete(key)
        if not status:
            return Response("No such key found", status=404)

        return Response(f"{key} deleted")

    except Exception as e:
        print(e)
        return Response(f"Server error occured: {e}", status=500)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
