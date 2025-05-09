from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from events.models import Event,Participant


@receiver(m2m_changed, sender=Participant.event.through)
def add_participant(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for participant_id in pk_set:
                participant = Participant.objects.get(pk=participant_id)
                send_mail(
                    "New Participant Assignment",
                    f"You have been added to the event: {instance.title}",  # instance is Event
                    "mdmehedihasanroby@gmail.com",
                    [participant.email],
                    fail_silently=False,
                )