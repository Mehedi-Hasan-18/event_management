from django.urls import path
from events.views import dashboard,eventform,event,updatetask,delete_event


urlpatterns = [
    path('dashboard/',dashboard, name='dashboard'),
    path('forms/',eventform , name="form"),
    path('event/',event, name='event'),
    path('update-event/<int:id>/',updatetask, name='update-event'),
    path('delete-event/<int:id>/',delete_event, name='delete-event')
    
] 