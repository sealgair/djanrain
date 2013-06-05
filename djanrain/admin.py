from django.contrib import admin
from janrained.models import JanrainedSite, JanrainedAuth

class JanrainedAuthInline(admin.TabularInline):
    model = JanrainedAuth
    fields = ['identifier', 'profile']
    readonly_fields = fields

admin.site.register(JanrainedSite)
