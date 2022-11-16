from flask import Flask, request, abort
import pika
import os

app = Flask(__name__)

@app.route("/mail")
def index():
    return "", 200


@app.route("/mail/send", methods=["POST"])
def send():
    if not all(i in request.form for i in ("message","email","phone","name")):
        return abort(400)
    context = {k: request.form[k] for k in request.form if request.form[k] and k in ("message","email","phone","name") }
    credentials = pika.PlainCredentials(os.getenv('RMQ_LOGIN'), os.getenv('RMQ_PASSWORD'))
    parameters = pika.ConnectionParameters('hello-world.default.svc.root.local',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='', routing_key='hello', body=str(context))
    print(" [x] Sent !'")
    connection.close()    
    return "Sent", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)