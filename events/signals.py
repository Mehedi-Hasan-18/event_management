from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from events.models import Event,Participant,EventParticipant


@receiver(m2m_changed, sender=Event.participant.through)
def handle_participant_added(sender, instance, action, pk_set, **kwargs):
    print("Action:", action)
    print("Instance (Event):", instance)
    print("Participants Added:", pk_set)
    if action == "post_add":
        for participant_id in pk_set:
            # Get through the intermediate model
            relation = EventParticipant.objects.get(
                event=instance,
                participant_id=participant_id
            )
            send_mail(
                "Event Registration",
                f"You've been added",
                "from@example.com",
                [relation.participant.email],
                fail_silently=False,
            )