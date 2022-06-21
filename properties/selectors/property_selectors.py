from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from properties.models import Property
import django_filters


class BasePropertyFilter(django_filters.FilterSet):
    class Meta:
        model = Property
        fields = ('id', 'is_active')


def property_fplist(*, filters=None):
    filters = filters or {}
    qs = Property.objects.all()

    return BasePropertyFilter(filters, qs).qs


def property_list():
    return Property.objects.all()

    # return Property.objects.filter(price__gt=350000).all()

    # filter = Q(price__gt=350000)
    # filter.add(
    #     Q(price__lte=400000),
    #     Q.AND # Q.OR
    # )
    # return Property.objects.filter(filter).all()

    # return Property.objects.annotate(nick_name=F('title')).values('nick_name')

    # return Property.objects.annotate(nick_name=Concat('title', Value(' '), Value('yey'))).all()
