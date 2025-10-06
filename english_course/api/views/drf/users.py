from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from english_course.api.views.drf.serializers import UserCreateSerializer


class UserCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created', 'username': user.username}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=400)


