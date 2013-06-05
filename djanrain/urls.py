from django.conf.urls import patterns, url
from janrained.views import get_token_view, login_view

urlpatterns = patterns('',
    url(r'^token/', get_token_view, name="login"),
    url(r'^login/', login_view)
)

