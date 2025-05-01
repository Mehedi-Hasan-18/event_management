import os
import django
import random
from faker import Faker
from datetime import timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventmanagement.settings')
django.setup()

from events.models import Category, Event, Participant

def populate_event_db():
    fake = Faker()

    # Create Categories
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.paragraph()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = []
    for _ in range(10):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(),
            date=fake.date_this_year(),
            time=fake.time(),
            location=fake.address(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(20):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        # Assign random 1–3 events to each participant
        participant.event.set(random.sample(events, random.randint(1, 3)))
        participants.append(participant)
    print(f"Created {len(participants)} participants and assigned events.")

    print("Database populated successfully!")

# Run the function
populate_event_db()