import pika, json

from main import Product, db
URL = 'amqps://daaddtwr:c4lzIyQHZN_nzNqX3pKNqDWCjsVPZKfy@woodpecker.rmq.cloudamqp.com/daaddtwr'
params = pika.URLParameters(URL)

connection = pika.BlockingConnection(params)


channel = connection.channel()

channel.queue_declare(queue='adminapp')

def callback(ch, method, properties, body):
    print("received in adminapp")
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print("Product Created!")
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("Product Updated!")
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        product.session.delete()
        db.session.delete(product)
        db.session.commit()
        print("Product Deleted!")
        

channel.basic_consume(queue='adminapp', on_message_callback=callback, auto_ack=True)
print("Started Consuming")
channel.start_consuming()
channel.close()