from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from .models import Property
from .services import property_services
from django.shortcuts import get_object_or_404
from .selectors import property_selectors
from core.pagination import get_paginated_response, LimitOffsetPagination
# For our APIs we use the following naming convention: <Entity><Action>Api


class PropertyListAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = '__all__'
    # class InputSerializer(serializers.Serializer):
    #     title = serializers.CharField()
    #     price = serializers.IntegerField()
    #     nick_name = serializers.CharField()

    def get(self, request):
        properties = property_selectors.property_list()
        return Response(data=self.InputSerializer(properties, many=True).data, status=status.HTTP_200_OK)

# Pagination Filter List API


class PropertyPFListAPI(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 1

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        # Important: If we use BooleanField, it will default to False
        is_active = serializers.NullBooleanField(required=False, default=None)

    class OutputSerializer(serializers.Serializer):
        id = serializers.CharField()
        title = serializers.CharField()
        price = serializers.IntegerField()
        is_active = serializers.BooleanField()

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        properties = property_selectors.property_fplist(
            filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=properties,
            request=request,
            view=self
        )


class PropertyFetchAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = '__all__'

    def get(self, request, id):
        property = get_object_or_404(Property, pk=id)
        return Response(data=self.InputSerializer(property).data, status=status.HTTP_200_OK)


class PropertyCreateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = '__all__'

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        property = property_services.property_create(
            **serializer.validated_data,
        )
        return Response(data=self.InputSerializer(property).data, status=status.HTTP_201_CREATED)


class PropertyImageCreateAPI(APIView):

    def post(self, request, id):
        property = get_object_or_404(Property, pk=id)
        file_objs = request.FILES.getlist('file')

        property = property_services.property_image_create(
            property=property,
            file_objs=file_objs
        )
        return Response(status=status.HTTP_201_CREATED)


class PropertyUpdateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Property
            fields = '__all__'

    def put(self, request, id):
        property = get_object_or_404(Property, pk=id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        property = property_services.property_update(
            property=property, data={**serializer.validated_data})
        return Response(data=self.InputSerializer(property).data, status=status.HTTP_204_NO_CONTENT)


class PropertyDeleteAPI(APIView):

    def delete(self, request, id):
        property = get_object_or_404(Property, pk=id)

        property_services.property_delete(property=property)
        return Response(status=status.HTTP_204_NO_CONTENT)
