from django import forms
from django.forms import ModelForm
from .models import Event,Participant

class styleMixin():
    
    
    
    default_class = 'block w-full border-2 border-gray-300 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500 mt2 mb-3'
    
    def add_style(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget,forms.TextInput):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder':f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class':self.default_class,
                    'placeholder':f'Enter {field.label.lower()}',
                    'rows': '4'
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': self.default_class
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': self.default_class
                })
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_class
                })
                
    

class EventForm(styleMixin,forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_style()

class CreateParticipant(styleMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name','email']
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.add_style()