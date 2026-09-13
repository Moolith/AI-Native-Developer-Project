from django.contrib import admin

from .models import Chore, Household, Partner

admin.site.register(Household)
admin.site.register(Partner)
admin.site.register(Chore)
