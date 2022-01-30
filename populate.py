import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','fist_project.settings')

import django
django.setup()

import random
from fist_app.models import AccessRecord, Webpage, Topic
from faker import Faker

fakegen = Faker()

topic = ['penjual sayur','mebel','berdagang','penyanyi']

def addTopic():
    t = Topic.objects.get_or_create(top_name=random.choice(topic))[0]
    t.save()
    return t

def populate(n=5):
    for x in range(n):

        top = addTopic()

        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]
        acc_r = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]

if __name__ == '__main__':
    print("populate scrript")
    populate(10)
    print("populate done")
