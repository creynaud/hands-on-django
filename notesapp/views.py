from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from .models import Note


class UserNotesInContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserNotesInContextMixin, self).get_context_data(**kwargs)
        context['notes'] = Note.objects.filter(owner=self.request.user)
        return context


class MyNotes(UserNotesInContextMixin, ListView):
    model = Note
    template_name = 'notesapp/my_notes.html'
    context_object_name = 'notes'

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
my_notes = login_required(MyNotes.as_view())


class NoteDetail(UserNotesInContextMixin, DetailView):
    model = Note
    template_name = 'notesapp/note_detail.html'
    context_object_name = 'note'
note_detail = login_required(NoteDetail.as_view())


class EditNote(UserNotesInContextMixin, UpdateView):
    model = Note
    template_name = 'notesapp/edit_note.html'
    fields = ['title', 'content']
edit_note = login_required(EditNote.as_view())

