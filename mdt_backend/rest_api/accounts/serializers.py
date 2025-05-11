from rest_framework import serializers
from apps.accounts.models import User, BotUser, UserType
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True, write_only=True)
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    user_type = serializers.ChoiceField(choices=UserType.choices(), default='USER')
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        fields = ['name', 'username', 'email', 'user_type', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        # Split name into first_name and last_name (optional logic)
        name = validated_data.pop('name')
        first_name, last_name = name.split(' ', 1) if ' ' in name else (name, '')

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=last_name
        )

        # Create the user profile with user_type
        BotUser.objects.create(
            user=user,
            user_type=validated_data['user_type']
        )

        # Create token
        Token.objects.create(user=user)

        return user

    def to_representation(self, instance):
        # Return the response data
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'name': f"{instance.first_name} {instance.last_name}".strip(),
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},  # Ensure ID is not required in input
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        fields = ['username', 'password']