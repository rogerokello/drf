from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# The HyperlinkedModelSerializer has the following differences from ModelSerializer:
# - It does not include the id field by default.
# - It includes a url field, using HyperlinkedIdentityField.
# - Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # The source argument controls which attribute is used to populate
    # a field, and can point at any attribute on the serialized instance.
    # It can also take the dotted notation shown below, in which case
    # it will traverse the given attributes, in a similar way as it is
    # used with Django's template language.
    # The untyped ReadOnlyField is always read-only, and will be used for
    # serialized representations, but will not be used for updating model
    # instances when they are deserialized.
    owner = serializers.ReadOnlyField(source='owner.username')

    # Notice that we've also added a new 'highlight' field. This field is of
    # the same type as the url field, except that it points to the
    # 'snippet-highlight' url pattern, instead of the 'snippet-detail' url
    # pattern.
    # Because we've included format suffixed URLs such as '.json', we also
    # need to indicate on the highlight field that any format suffixed
    # hyperlinks it returns should use the '.html' suffix.
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'title', 'code', 'linenos',
                  'language', 'style', 'owner')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # Because 'snippets' is a reverse relationship on the User model, it will not be included
    # by default when using the ModelSerializer class, so we needed to add an explicit field
    # for it.
    snippets = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
