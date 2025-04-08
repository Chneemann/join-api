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
from django.contrib.auth.tokens import default_token_generator
from .services import create_password_reset_link, send_password_reset_email, verify_password_reset_token, set_user_password

User = get_user_model()

class LoginView(APIView):
    serializer_class = LoginSerializer

    def _create_token_response(self, user):
        now = timezone.now()
        token, created = ExpiringToken.objects.get_or_create(user=user)

        if token.is_expired():
            token.delete()
            token = ExpiringToken.objects.create(user=user)

        token.expires_at = now + TOKEN_EXPIRATION_TIME
        token.save()

        user.last_login = now
        user.save(update_fields=['last_login'])

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
            user.is_active = True
            set_user_password(user, password)
            return Response({'message': 'User created.'}, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            reset_link = create_password_reset_link(request, user, token)
            send_password_reset_email(user, token, reset_link)
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({'error': 'Could not send password reset email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        password = request.data.get('password')
        uidb64 = request.data.get('uid')
        token = request.data.get('token')

        if not password or not uidb64 or not token:
            return Response({'error': 'Missing required parameters.'}, status=status.HTTP_400_BAD_REQUEST)

        user = verify_password_reset_token(uidb64, token)
        if user:
            set_user_password(user, password)
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid reset link.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
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