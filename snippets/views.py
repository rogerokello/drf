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
# 1. The @api_view decorator for working with function based views.
# 2. The APIView class for working with class-based views.

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

