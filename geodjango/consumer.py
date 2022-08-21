import ast
import django
import os

import pika
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "geodjango.settings")
django.setup()
from countries.models import Country
from countries.serializers import CountrySerializer

params = pika.URLParameters('amqps://zazqnjsw:ETiBRwrreiVmXaNedN53-Oe7jfFptrDG@beaver.rmq.cloudamqp.com/zazqnjsw')
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in admin 1')
    print(body)
    received = ast.literal_eval(body.decode("UTF-8"))
    added_or_updated = received['changed_data'].get('added_or_updated')
    deleted = received['changed_data'].get('deleted')
    if added_or_updated:
        for key, value in added_or_updated.items():
            country = Country.objects.get(admin=key)
            value_data = {"admin": value['properties']['ADMIN'],
                          "iso_a3": value['properties']['ISO_A3'],
                          "geometry_type": value['geometry']['type'],
                          "coordinates": "MULTIPOLYGON (((0 0, 0 1, 1 1, 1 0, 0 0)))"}
            print(country)
            if country:
                serializer = CountrySerializer(instance=country, data=value_data)
            else:
                serializer = CountrySerializer(data=value_data)
            serializer.is_valid()
            serializer.save()

    if deleted:
        for item in deleted:
            country = Country.objects.filter(admin=item)
            if len(country) != 0:
                country.delete()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
print('Started consuming')
channel.start_consuming()
channel.close()
