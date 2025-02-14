from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, HeritageCard
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ConversationSerializer(serializers.ModelSerializer):
    response = serializers.CharField(read_only=True)  # Make this field read-only so it won't be required

    class Meta:
        model = Conversation
        fields = ['user', 'message', 'response', 'timestamp']

class HeritageCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageCard
        fields = '__all__'

# User Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError("Invalid username")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password")

        refresh = RefreshToken.for_user(user)
        return {'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}