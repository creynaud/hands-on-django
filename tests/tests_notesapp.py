from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_webtest import WebTest

from notesapp.models import Note


class NotesAppTests(WebTest):
    def test_my_notes_authenticated(self):
        user = User(username='guybrush', email='guybrush@meleeisland.com')
        user.save()

        note = Note(title='Title', owner=user)
        note.save()

        elaine = User(username='elaine', email='elaine@meleeisland.com')
        elaine.save()

        elaine_note = Note(title='Elaine Note Title', owner=elaine)
        elaine_note.save()

        url = reverse('my_notes')
        response = self.app.get(url, user=user)
        self.assertContains(response, note.title)
        self.assertNotContains(response, elaine_note.title)

    def test_my_notes_not_authenticated(self):
        url = reverse('my_notes')
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)
