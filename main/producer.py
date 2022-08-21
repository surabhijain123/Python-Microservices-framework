import pika
import json
params = pika.URLParameters('amqps://zazqnjsw:ETiBRwrreiVmXaNedN53-Oe7jfFptrDG@beaver.rmq.cloudamqp.com/zazqnjsw')
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)


