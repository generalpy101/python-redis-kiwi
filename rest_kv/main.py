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


if __name__ == "__main__":
    app.run(debug=True)
