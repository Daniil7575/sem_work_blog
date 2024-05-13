from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth.models import User

from account.models import Profile
from .models import Post


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers)


def title_len(value):
    if len(value) < 5:
        raise serializers.ValidationError('Title is too short')
    return value


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'profile')


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[title_len])
    author = UserSerializer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'published', 'body')
        read_only_fields = ('author', 'published')

    def validate_slug(self, value):
        if 'slug' in value:
            raise serializers.ValidationError('Forbidden word in the slug')
        return value
