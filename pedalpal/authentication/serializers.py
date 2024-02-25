from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "is_subscribed",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_subscribed": {"read_only": True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "email", "first_name", "last_name", "phone", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = Profile.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return user
                else:
                    raise serializers.ValidationError("Incorrect password.")
            else:
                raise serializers.ValidationError("User does not exist.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")