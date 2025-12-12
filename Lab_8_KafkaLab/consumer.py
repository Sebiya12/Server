from kafka import KafkaConsumer
import json

def safe_deserializer(m):
    text = m.decode('utf-8')
    try:
        return json.loads(text)   # пробуем как JSON
    except Exception:
        return text               # если не JSON — вернем просто строку

consumer = KafkaConsumer(
    'lab8-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="lab8-group",
    value_deserializer=safe_deserializer
)

print("Python consumer started. Waiting for messages...\n")

for message in consumer:
    print("Получено сообщение:", message.value)