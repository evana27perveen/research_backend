from django.contrib.auth.models import Group
from rest_framework import serializers
from App_auth.models import CustomUser, ProfileModel


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        grp_name = self.context.get('group_name')
        user.save()
        group = Group.objects.get_or_create(
            name=grp_name
        )
        group[0].user_set.add(user)
        return user


class ProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProfileModel
        fields = '__all__'
