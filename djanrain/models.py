import random
import re
import json
from django.contrib.sites.models import Site
from django.db import models
from django.contrib.auth.models import User
import string


def rand_string(n):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


class JanrainedAuthManager(models.Manager):

    def get_or_create_from_profile(self, profile):
        identifier = profile['identifier']
        try:
            return JanrainedAuth.objects.get(identifier=identifier), False
        except JanrainedAuth.DoesNotExist:
            username_options = [
                'preferredUsername',
                'email',
                'displayName',
            ]
            username = None
            for key in username_options:
                username = profile.get(key)
                if not username:
                    continue
                username = re.sub(r"[^\w\.@+-]+", "", username)
                if len(username) > 30:
                    continue
                if User.objects.filter(username=username).exists():
                    continue
                break

            while username is None:  # still
                attempt = "janrained-{0}".format(rand_string(10))
                if not User.objects.filter(username=attempt).exists():
                    username = attempt

            params = {
                'username': username
            }
            if 'email' in profile:
                params['email'] = profile['email']
            user = User.objects.create(**params)

            return self.create(
                user=user,
                identifier=profile['identifier'],
                profile=profile
            ), True


class JanrainedAuth(models.Model):
    user = models.ForeignKey(User)
    identifier = models.CharField(max_length=256)
    profile_json = models.TextField()

    objects = JanrainedAuthManager()

    @property
    def profile(self):
        return json.loads(self.profile_json)

    @profile.setter
    def profile(self, value):
        self.profile_json = json.dumps(value, indent=2)


JR_SITE_CACHE = {}


class JanrainedSiteManager(models.Manager):
    def get_current(self):
        """
        get the JanrainedSite for the current Site
        """
        site = Site.objects.get_current()
        try:
            current_jrsite = JR_SITE_CACHE[site.id]
        except KeyError:
            current_jrsite = self.get(site=site)
            JR_SITE_CACHE[site.id] = current_jrsite
        return current_jrsite

    def clear_cache(self):
        """
        Clears the ``JanrainedSite`` object cache.
        """
        global JR_SITE_CACHE
        JR_SITE_CACHE = {}


class JanrainedSite(models.Model):
    """
    Stores Janrain settings (including the secret api key) so that they don't have to be hardcoded
    """
    site = models.ForeignKey(Site, unique=True)
    app_name = models.CharField(max_length=64)
    app_id = models.CharField(max_length=64)
    secret_key = models.CharField(max_length=64)

    objects = JanrainedSiteManager()