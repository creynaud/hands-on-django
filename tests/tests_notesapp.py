from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from notesapp.models import Note


class NotesAppTests(WebTest):
    def test_notes(self):
        user = User(username='guybrush', email='guybrush@meleeisland.com')
        user.save()

        note = Note(title='Title', owner=user)
        note.save()

        url = reverse('notes')
        response = self.app.get(url)
        self.assertContains(response, note.title)
