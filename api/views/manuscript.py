from django.shortcuts import redirect
from quiz.models import Manuscript
from rest_framework import exceptions, permissions, views, reverse

from rest_framework.generics import get_object_or_404


class ManuscriptView(views.APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, category_id):
        return Manuscript.objects.filter(category_id=category_id).orderby('?')

    def redirect(self, request, category_id, format=None, queryset=None):
        queryset = queryset or self.get_queryset(category_id)

        if len(queryset) > 0:
            return redirect(reverse.reverse('api:manuscript', request=request, format=format, kwargs={
                'category_id': category_id,
                'manuscript_id': queryset[0].pk,
            }))
        else:
            raise exceptions.NotFound()

    def get(self, request, category_id, manuscript_id=None, format=None):
        queryset = self.get_queryset(category_id)

        if manuscript_id:
            manuscript = get_object_or_404(queryset, pk=manuscript_id)
        else:
            return self.redirect(request, category_id)



