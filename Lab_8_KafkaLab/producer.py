from kafka import KafkaProducer
from flask import Flask, request, jsonify
import json

# Создаём Flask-приложение
app = Flask(__name__)

# Настраиваем продюсера Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "lab8-topic"

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    # Отправляем сообщение в Kafka
    producer.send(TOPIC, data)
    producer.flush()

    return jsonify({"status": "sent", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)