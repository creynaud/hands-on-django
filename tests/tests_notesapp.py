from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from notesapp.models import Note
from tests.factories import UserFactory, NoteFactory


class NotesAppTests(WebTest):
    def test_my_notes_authenticated(self):
        guybrush = UserFactory()

        guybrush_note = NoteFactory(title='Title Guybrush', owner=guybrush)

        elaine = UserFactory()

        elaine_note = NoteFactory(title='Title Elaine', owner=elaine)

        url = reverse('my_notes')
        response = self.app.get(url, user=guybrush)
        self.assertContains(response, guybrush_note.title)
        self.assertNotContains(response, elaine_note.title)

    def test_my_notes_not_authenticated(self):
        url = reverse('my_notes')
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_note_detail_authenticated(self):
        note = NoteFactory()

        url = reverse('note_detail', args=[note.id])
        response = self.app.get(url, user=note.owner)
        self.assertContains(response, note.title)
        self.assertContains(response, note.content)

    def test_note_detail_not_authenticated(self):
        note = NoteFactory()

        url = reverse('note_detail', args=[note.id])
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)
