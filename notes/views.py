from django.http.response import HttpResponse
from django.template import loader
from django.template.context import RequestContext
from django.utils import timezone


def home(request):
    template = loader.get_template('notes/index.html')
    context = RequestContext(request, {'date': timezone.now()})
    return HttpResponse(template.render(context))
