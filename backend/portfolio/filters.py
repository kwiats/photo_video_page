import django_filters

from portfolio.models import MediaPosition


class MediaPositionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    create_date = django_filters.DateFromToRangeFilter(field_name='create_date')

    class Meta:
        model = MediaPosition
        fields = ['name', 'create_date']