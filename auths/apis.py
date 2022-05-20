from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from rest_framework_jwt.views import ObtainJSONWebTokenView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token

from auths.mixins import ApiAuthMixin

from auths.services import auth_logout

from users.selectors.user_selectors import user_get_login_data


class UserSessionLoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """
    class InputSerializer(serializers.Serializer):
        mobile = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({
            'session': session_key,
            'data': data
        })


class UserSessionLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()


class UserJwtLoginApi(ObtainJSONWebTokenView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user') or request.user
        if not user.is_active:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        token = serializer.validated_data.get('token')
        issued_at = serializer.validated_data.get('issued_at')
        response_data = JSONWebTokenAuthentication. \
            jwt_create_response_payload(token, user, request, issued_at)

        response = Response(response_data, status=status.HTTP_200_OK)

        if api_settings.JWT_AUTH_COOKIE:
            set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

        return response


class UserJwtLogoutApi(ApiAuthMixin, APIView):
    def post(self, request):
        auth_logout(request.user)

        response = Response()

        if settings.JWT_AUTH['JWT_AUTH_COOKIE'] is not None:
            response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response


class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)
