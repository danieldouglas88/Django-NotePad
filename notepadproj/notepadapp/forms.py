from django import forms
from .models import NotePad
import datetime

class NoteForm(forms.ModelForm):
    class Meta:
        model = NotePad
        fields = '__all__'