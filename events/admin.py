from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Event,Participant,Category

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Participant)
