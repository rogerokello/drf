# Because we're using ViewSet classes rather than View classes,
# we actually don't need to design the URL conf ourselves. The
# conventions for wiring up resources into views and urls can be
# handled automatically, using a Router class. All we need to do
# is register the appropriate view sets with a router, and let it
# do the rest.

# Registering the viewsets with the router is similar to providing
# a urlpattern. We include two arguments - the URL prefix for the
# views, and the viewset itself.

# The DefaultRouter class we're using also automatically creates the
# API root view for us, so we can now delete the api_root method from
# our views module.
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
