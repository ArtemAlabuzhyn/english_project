from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from english_course.api.views.drf.serializers import LoginSerializer


# class LoginAPIView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         if not username or not password:
#             return Response({'error': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
#
#
# class LogoutAPIView(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
