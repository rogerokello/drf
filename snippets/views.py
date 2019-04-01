# ----------- Request Object -------------
# REST framework introduces a Request object that extends the regular HttpRequest
# and provides more flexible request parsing. The core functionality of the Request
# object is the request.data attribute, which is similar to request.POST, but more
# useful for working with Web APIs.
# request.POST  - Only handles form data.  Only works for 'POST' method.
# request.data  - Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.

# ----------- Response Object -------------
# REST framework also introduces a Response object, which is a type of TemplateResponse
# that takes unrendered content and uses content negotiation to determine the correct
# content type to return to the client.
# return Response(data)  # Renders to content type as requested by the client.

# ----------- Status Codes ----------------
# Using numeric HTTP status codes in your views doesn't always make for obvious reading,
# and it's easy to not notice if you get an error code wrong. REST framework provides more
# explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module.
# It's a good idea to use these throughout rather than using numeric identifiers.

# ----------- Wrapping API views --------------
# The create/retrieve/update/delete operations that we've been using so far are going to be
# pretty similar for any model-backed API views we create. Those bits of common behaviour are
# implemented in REST framework's the generics.ListCreateAPIView class and the 
# generics.RetrieveUpdateDestroyAPIView class

from rest_framework import generics, permissions, renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    # Notice that we've also used the @action decorator to create a
    # custom action, named highlight. This decorator can be used to
    # add any custom endpoints that don't fit into the standard
    # create/update/delete style.
    # Custom actions which use the @action decorator will respond to
    # GET requests by default. We can use the methods argument if we
    # wanted an action that responded to POST requests.
    # The URLs for custom actions by default depend on the method name
    # itself. If you want to change the way url should be constructed,
    # you can include url_path as a decorator keyword argument.
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Here we've used the ReadOnlyModelViewSet class to automatically
# provide the default 'read-only' operations. We're still setting
# the queryset and serializer_class attributes exactly as we did
# when we were using regular views, but we no longer need to provide
# the same information to two separate classes.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
