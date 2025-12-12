from kafka import KafkaConsumer, KafkaProducer
import json

INPUT_TOPIC = "lab8-topic"
OUTPUT_TOPIC = "lab8-processed"

# Консюмер для чтения из lab8-topic
consumer = KafkaConsumer(
    INPUT_TOPIC,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="stream-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Продюсер для отправки в lab8-processed
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Stream processor started...")

for msg in consumer:
    original = msg.value

    # Пример обработки: добавляем поле
    processed = {
        "original": original,
        "processed": True
    }

    print("Обработано сообщение:", processed)

    # Отправляем в новую тему
    producer.send(OUTPUT_TOPIC, processed)
    producer.flush()