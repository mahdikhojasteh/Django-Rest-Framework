from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from files.services import file_services


class CreateFileAPI(APIView):

    class InputSerializer(serializers.Serializer):
        extension = serializers.CharField()
        original_name = serializers.CharField()
        generated_name = serializers.CharField()
        entity_id = serializers.IntegerField()
        entity_type = serializers.IntegerField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = file_services.createFile(**serializer.validated_data)
        return Response(data={'id': file.id}, status=status.HTTP_201_CREATED)
