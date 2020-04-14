from rest_framework import serializers

from flash._auth.models import MyUser
from flash._auth.validators import courier_role_validator, client_role_validator, phone_number_validator, wrong_role


class BaseUserSerializer(serializers.ModelSerializer):

    role = serializers.IntegerField(validators=[wrong_role], default=3)
    phone_number = serializers.CharField(validators=[phone_number_validator])

    class Meta:
        model = MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'role', 'email', 'is_superuser')


class RegisterSerializer(BaseUserSerializer):

    password = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')

        return MyUser.save_user(validated_data, password)


class UsersSerializer(BaseUserSerializer):

    username = serializers.CharField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        pass

    def create(self, validated_data):
        pass


class CourierSerializer(UsersSerializer):

    role = serializers.IntegerField(write_only=True, validators=[courier_role_validator])

    class Meta(UsersSerializer.Meta):
        pass


class ClientSerializer(UsersSerializer):

    role = serializers.IntegerField(write_only=True, validators=[client_role_validator])

    class Meta(UsersSerializer.Meta):
        pass
