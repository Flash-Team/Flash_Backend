from rest_framework import serializers

from flash._auth.models import MyUser


# Indeed not necessary because Django's native validator
from flash._auth.validators import courier_role_validator, client_role_validator


def wrong_role(value):
    result = False

    for el in MyUser.USER_ROLES:
        if value == el[0]:
            return

    if not result:
        raise serializers.ValidationError('Role not found')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.IntegerField(validators=[wrong_role])

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'is_superuser', 'password', 'role',)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = MyUser.objects.create_user(**validated_data)

        user.set_password(password)

        user.save()

        return user


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'is_superuser', 'password', 'role',)

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        if validated_data.get('is_superuser'):
            instance.is_superuser = validated_data.get('is_superuser')

        if validated_data.get('role'):
            instance.role = validated_data.get('role')

        instance.save()

        return instance


class CourierSerializer(UsersSerializer):
    role = serializers.IntegerField(write_only=True, validators=[courier_role_validator])

    class Meta(UsersSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'role',)


class ClientSerializer(UsersSerializer):
    role = serializers.IntegerField(write_only=True, validators=[client_role_validator])

    class Meta(UsersSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'role',)

