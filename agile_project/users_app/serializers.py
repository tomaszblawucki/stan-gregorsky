from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user_man = User.objects
        print(validated_data)
        user = user_man.create_user(email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name'],
            surname = validated_data['surname'],
            birth_date=validated_data['birth_date'])
        return user

    class Meta:
        model = User
        fields = ('email', 'password', 'name', 'surname', 'birth_date')
        write_only_fields = ('password',)
