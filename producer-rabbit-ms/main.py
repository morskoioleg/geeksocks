from flask import Flask, request, abort, make_response, jsonify
import pika
import os
import json
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
            jsonify(error=f"error")
            , 403
    )

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["3 per minute"],
    storage_uri="memory://",
)

@limiter.exempt
@app.route("/mail")
def index():
    return "", 200


@app.route("/mail/send", methods=["POST"])
def send():
    if not all(i in request.form for i in ("message","email","phone","name")):
        return abort(400)
    context = {k: request.form[k] for k in request.form if request.form[k] and k in ("message","email","phone","name") }
    context["to"]="oleg.intax@gmail.com"
    context["subject"]="Запрос с сайта"
    context["template"]="verify"
    credentials = pika.PlainCredentials(os.getenv('RMQ_LOGIN'), os.getenv('RMQ_PASSWORD'))
    parameters = pika.ConnectionParameters('hello-world.default.svc.root.local',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    print(json.dumps(context))
    channel.basic_publish(exchange='', routing_key='hello', body=json.dumps(context))
    print(" [x] Sent !'")
    connection.close()
    return "Sent", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

