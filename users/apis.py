from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from users.services import user_services
from users.selectors import user_selectors
from rest_framework.permissions import IsAuthenticated

class GetUsersAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    def get(self, request):
        users = user_selectors.get_users()
        data = self.OutputSerializer(users, many=True).data
        
        return Response(data, status=status.HTTP_200_OK)


class GetUserByIdAPI(APIView):
    permission_classes = [IsAuthenticated]

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = '__all__'
    
    def get(self, request, id):
        user = user_selectors.get_user_by_id(id=id)
        data = self.OutputSerializer(user).data
        
        return Response(data, status=status.HTTP_200_OK)
    
    
class CreateUserAPI(APIView):
    
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField()
        mobile = serializers.CharField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_services.create_user(**serializer.validated_data)
        return Response(data = { "id":user.id }, status=status.HTTP_201_CREATED)

class Send_OTP_API(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        user = user_selectors.get_user_by_id(id=id)
        user_services.send_OTP(user=user)

        return Response(status=status.HTTP_200_OK)

class verify_OTP_API(APIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        code = serializers.CharField()
    
    def post(self, request, id):
        user = user_selectors.get_user_by_id(id)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_services.verify_OTP(user=user, **serializer.validated_data)
        return Response(data = { "id":user.id }, status=status.HTTP_200_OK)


class CreateSuperUserAPI(APIView):
    
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField()
        username = serializers.CharField()
        password = serializers.CharField()
    
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = user_services.create_superuser(**serializer.validated_data)
        return Response(data = { "id":user.id }, status=status.HTTP_201_CREATED)


class UpdateUserAPI(APIView):
    permission_classes = [IsAuthenticated]
    
    class InputSerializer(serializers.Serializer):
        email = serializers.CharField(allow_blank=True)
        username = serializers.CharField(allow_blank=True)
        first_name = serializers.CharField(allow_blank=True)
        last_name = serializers.CharField(allow_blank=True)
        bio = serializers.CharField(allow_blank=True)
        birthdate = serializers.DateField(allow_null=True)
        password = serializers.CharField(allow_blank=True)
    
    def post(self, request, id):
        try:
            user = user_selectors.get_user_by_id(id)
        except :
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_services.update_user(user=user, data=serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
