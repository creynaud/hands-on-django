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

    def test_edit_note_not_authenticated(self):
        note = NoteFactory()

        url = reverse('edit_note', args=[note.id])
        response = self.app.get(url, user=note.owner)

        form = response.forms['edit-note-form']
        new_title = 'Updated Title'
        form['title'] = new_title
        new_content = 'Updated content.'
        form['content'] = new_content

        response = form.submit().follow()
        self.assertContains(response, new_title)
        self.assertContains(response, new_content)

    def test_edit_note_not_authenticated(self):
        note = NoteFactory()

        url = reverse('edit_note', args=[note.id])
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_add_note_authenticated(self):
        user = UserFactory()

        url = reverse('add_note')
        response = self.app.get(url, user=user)

        form = response.forms['add-note-form']
        title = 'New Note Title'
        form['title'] = title
        content = 'New Note Content'
        form['content'] = content

        response = form.submit().follow()
        self.assertContains(response, title)
        self.assertContains(response, content)

    def test_add_note_authenticated_no_content(self):
        user = UserFactory()

        url = reverse('add_note')
        response = self.app.get(url, user=user)

        form = response.forms['add-note-form']
        title = 'New Note Title'
        form['title'] = title

        response = form.submit().follow()
        self.assertIsNotNone(Note.objects.get(title=title))
        self.assertContains(response, title)

    def test_add_note_authenticated_no_title(self):
        user = UserFactory()

        url = reverse('add_note')
        response = self.app.get(url, user=user)

        form = response.forms['add-note-form']
        content = 'New Note Content'
        form['content'] = content

        response = form.submit()
        self.assertContains(response, 'This field is required')

    def test_add_note_not_authenticated(self):
        url = reverse('add_note')
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_note_authenticated(self):
        note = NoteFactory(title='Note to delete',
                           content='Note to delete content')

        url = reverse('delete_note', args=[note.id])
        response = self.app.get(url, user=note.owner)

        form = response.forms['delete-note-form']
        response = form.submit().follow()

        self.assertNotContains(response, note.title)
        self.assertNotContains(response, note.content)

    def test_delete_note_not_authenticated(self):
        note = NoteFactory()
        url = reverse('delete_note', args=[note.id])
        response = self.app.get(url)
        self.assertNotEqual(response.status_code, 200)
