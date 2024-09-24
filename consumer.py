import json

import pika
from pika.channel import Channel
from pika.spec import BasicProperties
from pika.spec import Basic

import config
from main import create_shorts_title_gpt
from result_sender import send_fail, send_success

__QUEUE_IP: str = config.get_queue_ip()
__QUEUE_NAME: str = config.get_queue_name()

def callback(ch: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
    data: dict = json.loads(body.decode('utf-8'))

    subscription: str = data['subscription']

    try:
        answer: str = create_shorts_title_gpt(subscription)
    except RuntimeError as e:
        send_fail(e)
    else:
        send_success(answer)
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(__QUEUE_IP))
    channel = connection.channel()

    channel.queue_declare(queue=__QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=__QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()




