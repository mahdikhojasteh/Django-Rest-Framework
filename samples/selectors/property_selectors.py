from samples.models import Sample
import django_filters


class BaseSampleFilter(django_filters.FilterSet):
    class Meta:
        model = Sample
        fields = ('id',)


def sample_fplist(*, filters=None):
    filters = filters or {}
    qs = Sample.objects.all()

    return BaseSampleFilter(filters, qs).qs


def sample_list():
    return Sample.objects.all()
