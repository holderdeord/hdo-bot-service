from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class ReactAppView(TemplateView):
    # TODO: copy index.html from static/botadmin/public
    template_name = 'botadmin/index.html'
