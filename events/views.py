
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q,Count
from django.utils import timezone
from datetime import date
from events.models import Event,Participant
from .forms import EventForm,CreateParticipant
from django.db.models import Count, Case, When, BooleanField
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from .forms import CategoryForm
from .models import Event, Participant, EventParticipant

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('signIn')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()
def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_perticipant(user):
    return user.groups.filter(name='Participant').exists()


@permission_required('events.add_event', login_url='signIn')
# def dashboard(request):
    
#     today = timezone.now().date()
    
    
#     counts = Event.objects.aggregate(
#         total_event=Count('id'),
#         upcoming_event=Count('id', filter=Q(date__gte=today)), 
#         past_event=Count('id', filter=Q(date__lt=today)) ,   
#     )
#     total_participant = Participant.objects.aggregate(per_count=Count('id'))
    
    
#     #RETRIVING DATA
#     type = request.GET.get('type','all')
#     base_query = Event.objects.select_related('category').prefetch_related('participant')
#     if type == 'perticipant':
#         participants = Participant.objects.all().order_by('name')
#         event = base_query.annotate(participant_count=Count('participant')).filter(participant_count__gt=0)
#     elif type == 'upcoming':
#         event = base_query.filter(date__gte=timezone.now().date())
#     elif type == 'past':
#         event = base_query.filter(date__lt=timezone.now().date())
#     else:
#         event = base_query.all()
    
    
#     return render(request,'dashboard.html',{'view_type':type,'counts':counts,'total_participant':total_participant,'events':event,'participants':participants})

def dashboard(request):
    
    today = timezone.now().date()
    
    counts = Event.objects.aggregate(
        total_event=Count('id'),
        upcoming_event=Count('id', filter=Q(date__gte=today)), 
        past_event=Count('id', filter=Q(date__lt=today)),   
    )
    total_participant = Participant.objects.aggregate(per_count=Count('id'))
    
    # RETRIEVING DATA
    type = request.GET.get('type', 'all')
    base_query = Event.objects.select_related('category').prefetch_related('participant')
    
    # Initialize both variables
    event = []
    participants = []
    
    if type == 'perticipant':
        participants = Participant.objects.all().order_by('name')
        # Don't set event for participants view, leave it empty
    elif type == 'upcoming':
        event = base_query.filter(date__gte=timezone.now().date())
    elif type == 'past':
        event = base_query.filter(date__lt=timezone.now().date())
    else:
        event = base_query.all()
    
    return render(request, 'dashboard.html', {
        'view_type': type,
        'counts': counts,
        'total_participant': total_participant,
        'events': event,
        'participants': participants
    })



@login_required
def eventform(request):
    form = EventForm()
    par_form = CreateParticipant()
    if request.method == "POST":
        form = EventForm(request.POST)
        par_form = CreateParticipant(request.POST)
        if form.is_valid() and par_form.is_valid():
            event = form.save()
            participant = par_form.save()
            
            # Add the event to the participant
            participant.event.add(event)

            messages.success(request, "Task Created Successfully")
            return redirect('dashboard')
        else:
            messages.error(request, "Form validation failed")
            print(form.errors)
            print(par_form.errors)
    return render(request, "forms.html", {'form': form, 'par_form': par_form})



@permission_required('events.change_event', login_url='signIn')
def updatetask(request,id):
    event = Event.objects.get(id=id)
    participant = Participant.objects.get(id=id)
    form = EventForm(instance=event)
    par_form = CreateParticipant(instance=participant)
    if request.POST:
        form = EventForm(request.POST,instance=event)
        par_form = CreateParticipant(request.POST,instance=participant)
        if par_form.is_valid() and form.is_valid():
            events = form.save()
            participant = par_form.save(commit=False)
            participant.save()
            participant.event.add(events)
            
            messages.success(request,"Task Created Successfull")
            return redirect('dashboard')
    return render(request,"forms.html",{'form':form, 'par_form':par_form})


@permission_required('events.delete_event', login_url='signIn')
@login_required
def delete_event(request,id):
    if request.method == 'POST':
        event = Event.objects.get(id=id)
        event.delete()
        messages.success(request,'Task Delete SuccessFull')
        return redirect('dashboard')
        
        


    
@login_required
def event(request):
    event = Event.objects.all()
    return render(request,'event.html', {'events':event})




def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    try:
        participant = Participant.objects.get(email=request.user.email)
    except Participant.DoesNotExist:
        messages.error(request, "You are not registered as a participant.")
        return redirect('dashboard')

    if EventParticipant.objects.filter(event=event, participant=participant).exists():
        messages.info(request, "This User already joined this event.")
    else:
        EventParticipant.objects.create(event=event, participant=participant)
        messages.success(request, "User Added successfully joined the event.")

    return redirect('dashboard')
