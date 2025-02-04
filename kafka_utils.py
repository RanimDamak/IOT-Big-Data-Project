from pykafka import KafkaClient

def create_producer():
  # Connect to the Kafka cluster and create a producer
  client = KafkaClient(hosts="localhost:9092")
  producer = client.topics[b"vehicle-data"].get_producer()
  return producer

def create_consumer():
  # Connect to the Kafka cluster and create a consumer
  client = KafkaClient(hosts="localhost:9092")
  consumer = client.topics[b"vehicle-data"].get_simple_consumer()
  return consumer

def publish_data(producer, data):
  # Publish data to the topic
  producer.produce(data)

def consume_data(consumer):
  # Consume the next message
  message = consumer.consume()
  return message.value
