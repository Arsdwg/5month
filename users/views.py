from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserCreateSerializer, UserAuthSerializer
from .models import UserIsActiveCode
import random
from rest_framework.views import APIView


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.create_user(username=username, password=password, is_active=False)

        confirmation_code = random.randint(100000, 999999)
        UserIsActiveCode.objects.create(user=user, code=confirmation_code)

        print(f"Код подтверждения: {confirmation_code}")

        return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(status=status.HTTP_401_UNAUTHORIZED,
                        data={'error': 'User credentials are wrong!'})


class ConfirmationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        confirmation_code = request.data.get('code')

        try:
            user = User.objects.get(username=username)
            user_confirmation_code = UserIsActiveCode.objects.get(user=user, code=confirmation_code)

            if user_confirmation_code.code == confirmation_code:
                user.is_active = True
                user.save()
                return Response(status=status.HTTP_200_OK, data={'message': 'User confirmed successfully'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
        except UserIsActiveCode.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})









# from rest_framework.decorators import api_view
# from rest_framework import status
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from .serializers import UserCreateSerializer, UserAuthSerializer
# from .models import UserIsActiveCode
# import random
#
#
# @api_view(['POST'])
# def registration_api_view(request):
#     serializer = UserCreateSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#
#     username = request.data.get('username')
#     password = request.data.get('password')
#
#     user = User.objects.create_user(username=username, password=password, is_active=False)
#
#     confirmation_code = random.randint(100000, 999999)
#     UserIsActiveCode.objects.create(user=user, code=confirmation_code)
#
#     print(f"Код подтверждения: {confirmation_code}")
#
#     return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)
#
#
# @api_view(['POST'])
# def authorization_api_view(request):
#     if request.method == 'POST':
#         serializer = UserAuthSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         username = serializer.validated_data.get('username')
#         password = serializer.validated_data.get('password')
#
#         user = authenticate(username=username, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(data={'key': token.key})
#         return Response(status=status.HTTP_401_UNAUTHORIZED,
#                         data={'error': 'User credentials are wrong!'})
#
#
# @api_view(['POST'])
# def confirm_user_api_view(request):
#     if request.method == 'POST':
#         username = request.data.get('username')
#         confirmation_code = request.data.get('code')
#
#         try:
#             user = User.objects.get(username=username)
#             user_confirmation_code = UserIsActiveCode.objects.get(user=user, code=confirmation_code)
#
#             if user_confirmation_code.code == confirmation_code:
#                 user.is_active = True
#                 user.save()
#                 return Response(status=status.HTTP_200_OK, data={'message': 'User confirmed successfully'})
#             else:
#                 return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})
#         except User.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND, data={'error': 'User not found'})
#         except UserIsActiveCode.DoesNotExist:
#             return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Invalid confirmation code'})