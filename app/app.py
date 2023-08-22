from flask import Flask,request,jsonify,json
from flask_cors import CORS
import os
import threading
import time
from confluent_kafka import Producer, Consumer
from app.methods import get_confluent_config
from app.methods import kafka_consumer

app = Flask(__name__)
CORS(app)

app.config["DEBUG"] = True

producer = Producer(get_confluent_config.get_config()[0])

def kafka_consumer_thread():
    kafka_consumer.main()

with app.app_context():
    thread = threading.Thread(target=kafka_consumer_thread)
    thread.start()

@app.route('/get_sentiment', methods=['POST'])
def sentiment_analysis():
    if request.method == 'POST':
        video_id = request.form['video_id']
        print(video_id)
        producer.produce('youtube-urls', key=video_id, value=video_id)
        producer.flush()
        consumer = Consumer(get_confluent_config.get_config()[1])
        consumer.subscribe(['sentiment-results'])

        # Poll the result topic for the specific video ID with a timeout
        timeout = 10  # Example: 10 seconds, adjust as needed
        start_time = time.time()

        try:
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= timeout:
                    # If timeout is reached, break the loop
                    break

                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                if msg.key().decode('utf-8') == video_id:
                    sentiment_result = msg.value().decode('utf-8')
                    return jsonify({'result': sentiment_result})

        finally:
            # Always close the consumer, regardless of how the loop exits
            consumer.close()

    return jsonify({'error': 'Method not supported'})

        


@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
