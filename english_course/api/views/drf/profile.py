from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from english_course.api.views.drf.permissions import CanAccess
from english_course.api.views.drf.serializers import UserProfileSerializer, EditUserProfileSerializer
from english_course.models import User


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, CanAccess]


    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    def patch(self, request):
        serializer = EditUserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, CanAccess]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        if self.request.method == 'PATCH':
            return EditUserProfileSerializer
        return super().get_serializer_class()




