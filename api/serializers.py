from rest_framework import serializers

from notesapp.models import Note


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Note
        fields = ('creation_date', 'title', 'content', 'url')
