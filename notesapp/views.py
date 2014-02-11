from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView

from .models import Note
from .forms import NoteCreationForm


class UserNotesInContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserNotesInContextMixin, self).get_context_data(
            **kwargs)
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


class AddNote(UserNotesInContextMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    form_class = NoteCreationForm
    template_name = 'notesapp/add_note.html'

    def form_valid(self, form):
        self.object = form.save(owner=self.request.user)
        return redirect(self.object.get_absolute_url())
add_note = login_required(AddNote.as_view())


class DeleteNote(UserNotesInContextMixin, DeleteView):
    model = Note
    template_name = 'notesapp/delete_note.html'

    def get_success_url(self):
        return reverse('my_notes')
delete_note = login_required(DeleteNote.as_view())
