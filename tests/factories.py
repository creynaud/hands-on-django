from django.contrib.auth.models import User

from factory.declarations import Sequence, SubFactory
from factory.django import DjangoModelFactory
from factory.helpers import lazy_attribute

from notesapp.models import Note


class UserFactory(DjangoModelFactory):
    FACTORY_FOR = User
    username = Sequence(lambda n: 'some_email{0}@acme.com'.format(n))

    @lazy_attribute
    def email(self):
        return self.username

    @lazy_attribute
    def password(self):
        return "123"


class NoteFactory(DjangoModelFactory):
    FACTORY_FOR = Note
    owner = SubFactory(UserFactory)

    @lazy_attribute
    def title(self):
        return "Some Title"

    @lazy_attribute
    def content(self):
        return "Some content."
