from rest_framework import serializers
from .models import Profile,  User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, min_length = 6)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["username", "email", "avatar_url", "country", "city",
                  "organization", "about", "rating", "max_rating"]
        read_only_fields = ["rating", "max_rating"]