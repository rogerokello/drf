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

from rest_framework import generics

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


# The generics.ListCreateAPIView class provides the core functionality for the
# list and create operations
class SnippetList(generics.ListCreateAPIView):
    """
    List all code snippets, or create a new snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


# The generics.RetrieveUpdateDestroyAPIView class provides the functionality for
# the retrieval of an item, Update of an item and Deleting of an item.
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

