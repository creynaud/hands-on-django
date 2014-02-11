from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notesapp.models import Note

from .factories import NoteFactory, UserFactory


class APITestNotAuthenticated(APITestCase):
    def test_get_notes_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_note_not_authenticated(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_note_not_authenticated(self):
        url = reverse('note-list')
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class APITestAuthenticated(APITestCase):
    def test_get_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-detail', args=['dummy'])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_note_not_found(self):
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        url = reverse('note-list', args=['dummy'])
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_notes(self):
        user1 = UserFactory.create()
        note1 = NoteFactory.create(title='Note 1 title',
                                   content='Note 1 content', owner=user1)

        user2 = UserFactory.create()
        note2 = NoteFactory.create(title='Note 2 title',
                                   content='Note 2 content', owner=user2)

        url = reverse('note-list')
        self.client.force_authenticate(user=user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, note1.title)
        self.assertContains(response, note1.content)
        self.assertNotContains(response, note2.title)
        self.assertNotContains(response, note2.content)

    def test_get_note(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.id])
        self.client.force_authenticate(user=note.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictContainsSubset({'title': note.title}, response.data)
        self.assertDictContainsSubset({'content': note.content}, response.data)
        self.assertDictContainsSubset({'creation_date': note.creation_date}, response.data)

    def test_delete_note(self):
        note = NoteFactory.create()
        self.client.force_authenticate(user=note.owner)
        url = reverse('note-detail', args=[note.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_new_note(self):
        user = UserFactory.create()
        url = reverse('note-list')
        data = {
            "title": "New Note Title",
            "content": "This is te note content",
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        note = Note.objects.get(title=data['title'])
        self.assertEqual(note.content, data['content'])
        self.assertEqual(note.title, data['title'])
        self.assertIsNotNone(note.creation_date)
        self.assertEqual(note.owner.email, user.email)

    def test_put_note(self):
        note = NoteFactory.create()
        url = reverse('note-detail', args=[note.id])
        data = {
            "title": "Updated Note Title",
            "content": "This is an updated content",
        }
        self.client.force_authenticate(user=note.owner)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        note = Note.objects.get(id=note.id)
        self.assertEqual(note.content, data['content'])
        self.assertEqual(note.title, data['title'])
        self.assertIsNotNone(note.creation_date)
