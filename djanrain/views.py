from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site
from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from janrained.models import JanrainedSite


class LoginView(TemplateView):
    """
    Janrain-backed login view.  Displays Janrain widget.
    """
    template_name = "janrained/login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get_current()
        context['janrained_site'] = JanrainedSite.objects.get_current()
        return context

login_view = LoginView.as_view()


class GetTokenView(RedirectView):
    """
    View invoked by Janrain to provide authentication information
    """
    http_method_names = ["post"]
    permanent = False

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GetTokenView, self).dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        token = self.request.POST['token']

        if self.request.user.is_authenticated():
            # todo: associate new JanrainedAuth with existing account
            return self.request.path
        else:
            user = authenticate(janrain_token=token)
            if user:
                login(self.request, user)
                return "/"
            else:
                messages.error(self.request, "Authentication Failed")
                return reverse(login_view)

get_token_view = GetTokenView.as_view()
