from rest_framework import serializers,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_dynamic_fields import DynamicFieldsMixin
from accounts.models import User
from posts.models import post,documents
from djoser.serializers import UserSerializer

class documentsSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    attachment = serializers.FileField()
    created_by = UserSerializer(default=serializers.CurrentUserDefault())
    # modified_by = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all(),required=False, allow_null=True)
    # post_text = serializers.SerializerMethodField('get_post_text')

    # def get_post_text(self, obj):
    #     if obj.post_id:
    #         posts = get_object_or_404(post,pk=obj.post_id)
    #         return posts
    #     else:
    #         return None

    class Meta:
        model = documents
        fields = ['id','attachment','created_by','created_at','modified_by','modified_at']
        extra_kwargs = {'created_by': {'required': False},'modified_by': {'required': False}}


class PostsSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    # created_by = serializers.SlugRelatedField(slug_field='username',queryset=User.objects.all())
    documents = documentsSerializer(many=True,required=False)
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = post
#        list_serializer_class = FilteredListSerializer
        fields = [ 'id', 'text','documents','post_type','created_by','created_at','modified_by','modified_at']
        http_method_names = ['get', 'post', 'head','put']
        extra_kwargs = {'created_by': {'required': False},'modified_by': {'required': False},'documents': {'required': False}}