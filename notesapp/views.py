from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Note


class MyNotes(ListView):
    model = Note
    template_name = 'notesapp/my_notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
my_notes = login_required(MyNotes.as_view())


class NoteDetail(DetailView):
    model = Note
    template_name = 'notesapp/note_detail.html'
    context_object_name = 'note'
note_detail = login_required(NoteDetail.as_view())
