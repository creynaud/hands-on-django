from django import forms

from .models import Note


class NoteCreationForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def save(self, owner=None, commit=True):
        note = super(NoteCreationForm, self).save(commit=False)
        note.owner = owner
        note.save()
        return note
