from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from english_course.api.views.drf.permissions import CanAccess
from english_course.api.views.drf.serializers import WordSerializer, EditWordSerializer, CreateWordSerializer
from english_course.models import UserWord


class WordsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, CanAccess]
    serializer_class = WordSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WordSerializer
        return CreateWordSerializer
    def get_queryset(self):
        base_qs = UserWord.objects.select_related('user').order_by('-id')
        user = self.request.user

        if user.role == 'admin':
            return base_qs

        if user.role == 'teacher':
            return base_qs.filter(user__teacher=user)
        return base_qs.filter(user=user)




class WordDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserWord.objects.all()
    permission_classes = [IsAuthenticated, CanAccess]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WordSerializer
        if self.request.method == 'PATCH':
            return EditWordSerializer

        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Word deleted successfully'}, status=status.HTTP_200_OK)

    def get_object(self):
        return super().get_object()


class CreateWordView(APIView):
    permission_classes = [IsAuthenticated, CanAccess]
    def post(self, request):
        serializer = CreateWordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            word = serializer.save()
            return Response({'message': 'Word created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

