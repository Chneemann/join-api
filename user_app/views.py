from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from .caching import get_cached_user, cache_user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        cached_user = get_cached_user(user_id)
        
        if cached_user:
            return Response(cached_user)

        user = self.get_object()
        serialized_user = UserSerializer(user).data
        cache_user(user_id, serialized_user)

        return Response(serialized_user)