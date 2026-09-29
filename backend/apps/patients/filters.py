import django_filters
from .models import Patient


class PatientFilter(django_filters.FilterSet):
    full_name = django_filters.CharFilter(lookup_expr="icontains")
    patient_code = django_filters.CharFilter(lookup_expr="icontains")
    age_min = django_filters.NumberFilter(method="filter_age_min")
    age_max = django_filters.NumberFilter(method="filter_age_max")

    class Meta:
        model = Patient
        fields = ["gender", "is_active"]

    def filter_age_min(self, queryset, name, value):
        from datetime import date
        from dateutil.relativedelta import relativedelta
        cutoff_date = date.today() - relativedelta(years=int(value))
        return queryset.filter(date_of_birth__lte=cutoff_date)

    def filter_age_max(self, queryset, name, value):
        from datetime import date
        from dateutil.relativedelta import relativedelta
        cutoff_date = date.today() - relativedelta(years=int(value))
        return queryset.filter(date_of_birth__gte=cutoff_date)