from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .caching import get_cached_user_by_id
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.cache import cache

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.filter(is_active=True, is_superuser=False)
    serializer_class = UserSerializer
    
    def retrieve(self, request, pk=None):
        user = get_cached_user_by_id(pk)

        if not user:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                cache.delete(f"user_{user.id}")
                return Response(
                    {"id": user.id, **serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        cache.delete(f"user_{user.id}")  
        return Response({'message': 'User deleted successfully.'}, status=status.HTTP_200_OK)