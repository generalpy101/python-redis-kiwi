import json

import redis
from flask import Flask

from rest_kv.api import api_bp


def create_app(redis_client=None):
    app = Flask(__name__)
    if redis_client is None:
        redis_client = redis.Redis(
            host="localhost", port=6379, decode_responses=True, db=0
        )
    app.redis_client = redis_client
    app.register_blueprint(api_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=8000, debug=True)
