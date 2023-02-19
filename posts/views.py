from rest_framework import viewsets,status
from rest_framework import permissions
from rest_framework.response import Response
from posts.models import post,documents
from posts.serializers import PostsSerializer,documentsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_tracking.mixins import LoggingMixin


class documentsViewSet(viewsets.ModelViewSet):

    queryset = documents.objects.all().order_by('-created_by')
    serializer_class = documentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        ]
    filterset_fields = ['id',]
    ordering_fields = ['created_at', 'id','modified_at']


class PostsViewSet(viewsets.ModelViewSet):
    
    

    model = post
    queryset = post.objects.all().order_by('-created_by')
    serializer_class = PostsSerializer
    permission_classes = [
        permissions.IsAuthenticated,
         ]

    filter_backends = [
        DjangoFilterBackend,
         SearchFilter,
          OrderingFilter,
          ]
    filterset_fields = ['id', 'created_by','created_at']
    search_fields = ['@text','=id']
    ordering_fields = ['created_at', 'id','modified_at']
    ordering = ['-id']


    def create(self, request):
        req_text = request.data.get('text')
        req_documents = request.FILES.getlist('documents')
        req_post_type = request.FILES.getlist('post_type')
        if req_text in ('',None) and req_documents  == []:
            return Response(data={"error":'There are no text or images for this post'}, status=status.HTTP_400_BAD_REQUEST) 
        req_created_by = request.user
        posts = post(text=req_text,post_type=req_post_type,created_by=req_created_by)
        posts.save()
        if req_documents: 
            for document in req_documents:
                doc = documents(attachment=document,post_type=req_post_type,created_by=req_created_by)
                doc.save()
                posts.documents.add(doc)
        serializer = self.get_serializer(posts)
        return Response(serializer.data, status=status.HTTP_201_CREATED) 