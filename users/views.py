from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from users.services import users_service
from users.selectors import users_selectors
from rest_framework.permissions import IsAuthenticated

class GetUsersAPI(APIView):
    
    permission_classes = [IsAuthenticated]
    
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    def get(self, request):
        users = users_selectors.get_users()
        data = self.OutputSerializer(users, many=True).data
        
        return Response(data, status=status.HTTP_200_OK)


class GetUserByIdAPI(APIView):

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    def get(self, request, id):
        user = users_selectors.get_user_by_id(id=id)
        data = self.OutputSerializer(user).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    
class CreateUserAPI(APIView):
    
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField()
        username = serializers.CharField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        users_service.create_user(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class CreateSuperUserAPI(APIView):
    
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField()
        username = serializers.CharField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        users_service.create_superuser(**serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)


class UpdateUserAPI(APIView):
    
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField(allow_blank=True)
        username = serializers.CharField(allow_blank=True)
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        bio = serializers.CharField(allow_blank=True)
        birthdate = serializers.DateField(allow_null=True)
        password = serializers.CharField(allow_blank=True)
    
    def post(self, request, id):
        User =  get_user_model()
        user = User.objects.get(pk=id)

        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        users_service.update_user(user=user, data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
