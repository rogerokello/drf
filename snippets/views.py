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

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
