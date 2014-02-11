from rest_framework import viewsets, permissions

from notesapp.models import Note

from .serializers import NoteSerializer


class NotesViewSet(viewsets.ModelViewSet):
    model = Note
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def pre_save(self, obj):
        super(NotesViewSet, self).pre_save(obj)
        obj.owner = self.request.user
