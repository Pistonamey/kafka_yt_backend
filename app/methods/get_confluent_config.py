import sys
import os

def get_config():
    p_conf = {
        'bootstrap.servers': os.getenv("CONFLUENT_BOOTSTRAP_SERVER_ADDRESS"),
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': os.getenv("CONFLUENT_CLUSTER_KEY"),
        'sasl.password': os.getenv("CONFLUENT_CLUSTER_SECRET")
    }
    c_conf = {
            'bootstrap.servers': os.getenv("CONFLUENT_BOOTSTRAP_SERVER_ADDRESS"),
            'group.id': 'frontend-sentiment-group',
            'auto.offset.reset': 'earliest',
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': os.getenv("CONFLUENT_CLUSTER_KEY"),
            'sasl.password': os.getenv("CONFLUENT_CLUSTER_SECRET")
        }

    return (p_conf,c_conf)



if __name__ == "__main__":
    sys.exit(get_config())