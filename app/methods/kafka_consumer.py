from confluent_kafka import Consumer, KafkaError, Producer
from methods import get_confluent_config
from methods import get_sentiment
import sys
import os

def main():
    print("came inside")
    c_conf = {
        'bootstrap.servers': os.getenv("CONFLUENT_BOOTSTRAP_SERVER_ADDRESS"),
        'group.id': 'youtube-sentiment-group',
        'auto.offset.reset': 'earliest',
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': os.getenv("CONFLUENT_CLUSTER_KEY"),
        'sasl.password': os.getenv("CONFLUENT_CLUSTER_SECRET")
    }

    p_conf=get_confluent_config.get_config()[0]

    consumer = Consumer(c_conf)
    consumer.subscribe(['youtube-urls'])
    producer=Producer(p_conf)

    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
        else:
            video_id = msg.value().decode('utf-8')
            sentiment_result = get_sentiment.main(video_id)
            # Here, produce the result to the sentiment-results topic
            # You'll need a producer configuration here too
            producer.produce('sentiment-results', key=video_id, value=str(sentiment_result))
            producer.flush()

if __name__ == "__main__":
    sys.exit(main())
