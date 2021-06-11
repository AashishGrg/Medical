from django.contrib import admin

# Register your models here.
from users.models import PortalUser

admin.site.register(PortalUser)
