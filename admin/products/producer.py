import pika, json


URL = 'amqps://daaddtwr:c4lzIyQHZN_nzNqX3pKNqDWCjsVPZKfy@woodpecker.rmq.cloudamqp.com/daaddtwr'
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)


channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='adminapp', body=json.dumps(body), properties=properties)

