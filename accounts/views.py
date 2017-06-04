from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlencode
from django.views.generic import DetailView, RedirectView


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


class LoginSuccessView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # TODO: Add these params from python-social-auth profile
        #self.request.user.
        params = {
            'access_token': 'a',
            'token_type': 'b',
            'expires_in': 'c'
        }

        return settings.PWA_SUCCESS_URL + urlencode(params)
