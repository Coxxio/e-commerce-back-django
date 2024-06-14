from rest_framework import serializers

from src.apps.users.api.serializers.PersonSerializer import PersonSerializer
from src.apps.users.models import UserModel
from src.apps.users.api.validations.passwordValidator import ValidatePassword


class UpdatePass(serializers.ModelSerializer):
    person = PersonSerializer()
    password = serializers.CharField(
        validators=[ValidatePassword()])

    class Meta:
        model = UserModel
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'role': instance.role,
            'createdAt': instance.createdAt,
            'updatedAt': instance.updatedAt,
            'person': PersonSerializer(instance.person).data
        }


class UserSerializer(serializers.ModelSerializer):
    # person = PersonSerializer()
    password = serializers.CharField(
        validators=[ValidatePassword()])

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'role',
                  'createdAt', 'updatedAt', 'person')

    def create(self, validated_data):
        user = UserModel(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {
            'id': str(instance.id),
            'email': instance.email,
            'role': instance.role,
            'createdAt': instance.createdAt,
            'updatedAt': instance.updatedAt,
            'person': PersonSerializer(instance.person).data

        }
