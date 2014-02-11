from django.http.response import HttpResponse

# Create your views here.
from django.template import loader
from django.template.context import RequestContext

from .models import Note


def notes(request):
    template = loader.get_template('notesapp/notes.html')
    context = RequestContext(request, {'notes': Note.objects.all()})
    return HttpResponse(template.render(context))
