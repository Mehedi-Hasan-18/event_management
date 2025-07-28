from django.urls import path
from events.views import dashboard,eventform,event,updatetask,delete_event,add_category,join_event
from core.views import home


urlpatterns = [
    path('dashboard/',dashboard, name='dashboard'),
    path('', home, name="home"),
    path('forms/',eventform , name="form"),
    path('event/',event, name='event'),
    path('add-category/', add_category, name='add_category'),
    path('update-event/<int:id>/',updatetask, name='update-event'),
    path('delete-event/<int:id>/',delete_event, name='delete-event'),
    path('event/<int:event_id>/join/', join_event, name='join_event')
    
] 