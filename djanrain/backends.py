import json
import urllib2
import urllib
from django.contrib.auth.models import User
from djanrain.models import DjanrainAuth, DjanrainSite


class DjanrainAuthBackend(object):

    def authenticate(self, janrain_token=None):
        post_data = urllib.urlencode({
            'apiKey': str(DjanrainSite.objects.get_current().secret_key),
            'token': str(janrain_token)
        })
        api_response = urllib2.urlopen("https://rpxnow.com/api/v2/auth_info", data=post_data)
        data = json.load(api_response)
        if data.get('stat') == 'ok':
            jauth, created = DjanrainAuth.objects.get_or_create_from_profile(data['profile'])
            return jauth.user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None