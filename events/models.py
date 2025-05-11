from django.db import models

class Category(models.Model):
    c_name = models.CharField(max_length=250)
    description = models.TextField()
    
    def __str__(self):
        return self.c_name
    
class Event(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.TextField()
    
    # `````````````````FOREIGN KEY SETUP``````````````````
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1,related_name='category')

    def __str__(self):
        return self.title
    
    

    

class Participant(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    event = models.ManyToManyField(Event,related_name="participant")
    
    def __str__(self):
        return self.name
    
    
class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'participant')