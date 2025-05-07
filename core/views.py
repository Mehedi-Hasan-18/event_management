from django.shortcuts import render
from events.models import Event

# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})