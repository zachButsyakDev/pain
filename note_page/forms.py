# forms.py
from django import forms
from .models import Note, NoteSection


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'section']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter note title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Type your note here...'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }


class NoteSectionForm(forms.ModelForm):
    class Meta:
        model = NoteSection
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Section name'}),
        }
