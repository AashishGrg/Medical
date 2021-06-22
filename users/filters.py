import django_filters

from users.models import Doctor


class DoctorFilter(django_filters.filterset.FilterSet):
    class Meta:
        model = Doctor
        fields = ('is_active',)
