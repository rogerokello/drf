from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
    # The source argument controls which attribute is used to populate
    # a field, and can point at any attribute on the serialized instance.
    # It can also take the dotted notation shown below, in which case 
    # it will traverse the given attributes, in a similar way as it is
    # used with Django's template language.
    # The untyped ReadOnlyField is always read-only, and will be used for
    # serialized representations, but will not be used for updating model
    # instances when they are deserialized.
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style', 'owner')


class UserSerializer(serializers.ModelSerializer):
    # Because 'snippets' is a reverse relationship on the User model, it will not be included
    # by default when using the ModelSerializer class, so we needed to add an explicit field
    # for it.
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
