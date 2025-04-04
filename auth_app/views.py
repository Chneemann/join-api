from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication
from django.contrib.auth import authenticate
from join.settings import TOKEN_EXPIRATION_TIME
from .serializer import LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import ExpiringToken, ExpiringTokenAuthentication
from django.contrib.auth import get_user_model
from user_app.serializers import UserSerializer

User = get_user_model()

class LoginView(APIView):
    serializer_class = LoginSerializer

    def _create_token_response(self, user):
        token, created = ExpiringToken.objects.get_or_create(user=user)

        if not created and token.is_expired():
            token.delete()
            token = ExpiringToken.objects.create(user=user)

        if created or not token.expires_at:
            token.expires_at = timezone.now() + TOKEN_EXPIRATION_TIME
            token.save()

        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user:
                if not user.is_active:
                    return Response({'error': 'Account is inactive, please check your mails'}, status=status.HTTP_403_FORBIDDEN)
                return self._create_token_response(user)
            return Response({'error': 'Unable to login with provided credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = getattr(request.user, 'auth_token', None)

        if token is None or not isinstance(token, ExpiringToken):
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        if token.is_expired():
            return Response({"error": "No active session or token already expired"}, status=status.HTTP_401_UNAUTHORIZED)
        token.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_409_CONFLICT)

        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = serialized.save()
            user.set_password(password)
            user.is_active = True
            user.save()
            return Response({'message': 'User created.'}, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            token = ExpiringToken.objects.get(user=request.user)
        except ExpiringToken.DoesNotExist:
            return Response({"error": "Token does not exist, please log in again"}, status=status.HTTP_401_UNAUTHORIZED)

        if token.is_expired():
            token.delete()
            return Response({"error": "Token expired, please log in again"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"user_id": request.user.id}, status=status.HTTP_200_OK)