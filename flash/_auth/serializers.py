from rest_framework import serializers

from flash._auth.models import MyUser


# Indeed not necessary because Django's native validator
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
