from rest_framework import serializers
from .models import User, MiniProject

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {
            "email": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
    """Serializer used for read-only APIs (no password field)."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


class MiniProjectSerializer(serializers.ModelSerializer):
    trainee_name = serializers.CharField(source="trainee.username", read_only=True)
    trainer_name = serializers.CharField(source="trainer.username", read_only=True)

    class Meta:
        model = MiniProject
        fields = [
            "id", "title", "description", "trainee", "trainee_name",
            "trainer", "trainer_name", "progress", "created_at", "updated_at"
        ]
        extra_kwargs = {"trainer": {"read_only": True}}

    def validate_trainee(self, value):
        if value.role != "trainee":
            raise serializers.ValidationError("Selected user is not a trainee.")
        return value

