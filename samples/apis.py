from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from .models import Sample
from .services import sample_services
from django.shortcuts import get_object_or_404
from .selectors import sample_selectors
from core.pagination import get_paginated_response, LimitOffsetPagination


# For our APIs we use the following naming convention: <Entity><Action>API


class SampleListAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sample
            fields = '__all__'

    def get(self, request):
        properties = sample_selectors.sample_list()
        return Response(data=self.InputSerializer(properties, many=True).data, status=status.HTTP_200_OK)


# Pagination Filter List API
class SamplePFListAPI(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sample
            fields = '__all__'

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        properties = sample_selectors.sample_fplist(
            filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=properties,
            request=request,
            view=self
        )


class SampleFetchAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sample
            fields = '__all__'

    def get(self, request, id):
        Sample = get_object_or_404(Sample, pk=id)
        return Response(data=self.InputSerializer(Sample).data, status=status.HTTP_200_OK)


class SampleCreateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sample
            fields = '__all__'

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Sample = sample_services.sample_create(
            **serializer.validated_data,
        )
        return Response(data=self.InputSerializer(Sample).data, status=status.HTTP_201_CREATED)


class SampleUpdateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Sample
            fields = '__all__'

    def put(self, request, id):
        Sample = get_object_or_404(Sample, pk=id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        Sample = sample_services.sample_update(
            Sample=Sample, data={**serializer.validated_data})
        return Response(data=self.InputSerializer(Sample).data, status=status.HTTP_204_NO_CONTENT)


class SampleDeleteAPI(APIView):

    def delete(self, request, id):
        Sample = get_object_or_404(Sample, pk=id)

        sample_services.sample_delete(Sample=Sample)
        return Response(status=status.HTTP_204_NO_CONTENT)
