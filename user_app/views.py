from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .caching import get_cached_user_by_id
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    queryset = User.objects.all()
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