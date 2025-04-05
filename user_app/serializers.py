import random
from rest_framework import serializers, viewsets
from .models import User
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

def generate_random_color():
    return "#" + "".join(random.choices("0123456789ABCDEF", k=6))

def generate_initials(first_name, last_name):
    return f"{first_name[0].upper()}{last_name[0].upper()}"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'is_online', 'is_contact_only', 'last_login']
    
    def create(self, validated_data):
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        validated_data['initials'] = generate_initials(first_name, last_name)
        
        if 'color' not in validated_data:
            validated_data['color'] = generate_random_color()
        return super().create(validated_data)
    
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    parser_classes = [CamelCaseJSONParser] 
    renderer_classes = [CamelCaseJSONRenderer] 