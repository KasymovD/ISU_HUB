from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            'activity', 'description', 'file_type', 'location',
            'event_type', 'camera_shot', 'camera_angle', 'atmosphere',
            'language', 'race', 'date', 'image',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Добавьте другие виджеты при необходимости
        }