import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

URL = 'amqps://daaddtwr:c4lzIyQHZN_nzNqX3pKNqDWCjsVPZKfy@woodpecker.rmq.cloudamqp.com/daaddtwr'
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)


channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print("received in admin")
    
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    if properties.content_type == 'product_liked':
        product.likes = product.likes + 1
    elif properties.content_type == 'product_unliked':
        product.likes = product.likes - 1
    
    product.save()
    print(product.id, product.likes)
    print("product likes updated")


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print("Started Consuming")
channel.start_consuming()
channel.close()