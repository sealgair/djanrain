from django.contrib import admin
from djanrain.models import DjanrainSite, DjanrainAuth

class DjanrainAuthInline(admin.TabularInline):
    model = DjanrainAuth
    fields = ['identifier', 'profile']
    readonly_fields = fields

admin.site.register(DjanrainSite)
