from kafka import KafkaConsumer, KafkaProducer
import json

MAIN_TOPIC = "lab8-topic"
DLQ_TOPIC = "lab8-dlq"   # Dead Letter Queue

# Консюмер
consumer = KafkaConsumer(
    MAIN_TOPIC,
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id="lab8-dlq-group",
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Продюсер до DLQ
dlq_producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("DLQ consumer started. Waiting for messages...\n")

for msg in consumer:
    data = msg.value
    try:
        print("Получено сообщение:", data)

        # Пример ошибки: деление на 0
        # Если в сообщении есть поле "error" — вызовем ошибку
        if "error" in data:
            raise ValueError("Ошибка обработки сообщения!")

        # Здесь была бы реальная логика обработки
        print("Сообщение обработано успешно.\n")

    except Exception as e:
        print("Ошибка при обработке:", e)
        print("Отправляем в DLQ:", data, "\n")

        dlq_producer.send(DLQ_TOPIC, {
            "original_message": data,
            "error": str(e)
        })
        dlq_producer.flush()