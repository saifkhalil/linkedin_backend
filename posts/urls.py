from django.urls import path, include
from rest_framework import routers
from posts.views import PostsViewSet,documentsViewSet

app_name = 'Posts'

router = routers.DefaultRouter()
router.register(r'posts', PostsViewSet,"Posts")
router.register(r'documents', documentsViewSet,"documents")




urlpatterns = [
    path('', include(router.urls)),
]