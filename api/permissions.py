from django.conf import settings
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


class AllowAnyOrDjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissionsOrAnonReadOnly):
    def has_permission(self, request, view):
        if settings.MANUSCRIPT_API_ALLOW_ANY:
            return True

        return super().has_permission(request, view)
