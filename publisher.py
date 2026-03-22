import pika
import json

class RabbitMQPublisher:
  def __init__(self) -> None:
    self.__host = "localhost"
    self.__port = 5672
    self.__username = "guest"
    self.__password = "guest"
    self.__exchange = "my_exchange"
    self.__routing_key = ""
    self.__channel = None
    
  def create_channel(self):
    connection_parameters = pika.ConnectionParameters(
      host = self.__host,
      port = self.__port,
      credentials=pika.PlainCredentials(
        username=self.__username,
        password=self.__password
      )
    )

    self.__channel = pika.BlockingConnection(connection_parameters).channel()
    print(self.__channel)
  
  def send_message(self, body: dict):
    self.__channel.basic_publish(
      exchange = self.__exchange,
      routing_key = self.__routing_key,
      body = json.dumps(body),
      properties  = pika.BasicProperties(
        delivery_mode=2
      )
    )
  
rabbit_mq_publisher = RabbitMQPublisher()
rabbit_mq_publisher.create_channel()
rabbit_mq_publisher.send_message({"msg": "Im in Publisher"})