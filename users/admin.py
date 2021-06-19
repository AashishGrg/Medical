from django.contrib import admin

# Register your models here.
from users.models import *

admin.site.register(PortalUser)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(DoctorSpeciality)
admin.site.register(Examiner)
