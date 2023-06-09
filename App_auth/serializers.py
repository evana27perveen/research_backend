from django.contrib.auth.models import Group
from rest_framework import serializers
from App_auth.models import *


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


class AdminProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AdminProfileModel
        fields = '__all__'


class ResearcherProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ResearcherProfileModel
        fields = '__all__'


class ReviewerProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReviewerProfileModel
        fields = '__all__'


class ReaderProfileModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReaderProfileModel
        fields = '__all__'
