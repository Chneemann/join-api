from rest_framework import serializers, viewsets
from .models import User
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'status', 'last_login']
        
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [CamelCaseJSONParser] 
    renderer_classes = [CamelCaseJSONRenderer] 