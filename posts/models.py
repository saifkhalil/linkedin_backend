from email.mime import image
from django.db import models
from accounts.models import User
from django.core.validators import FileExtensionValidator
# Create your models here.

class documents(models.Model):
    id = models.AutoField(primary_key=True,)
    attachment = models.FileField(upload_to='documents/%Y/%m/%d/',verbose_name='Attachment',validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'git'])])
    # post_id = models.IntegerField(blank=True,null=True, verbose_name='Post')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE, editable=False)




class post(models.Model):
    VIDEO = "video"
    IMAGE = 'img'
    URL = 'iframe'
    POST_TYPES =  [
        (IMAGE, 'img'),
        (VIDEO, 'video'),
        (URL, 'iframe'),
    ]

    id = models.AutoField("id",primary_key=True)
    text = models.CharField(verbose_name='Text',null=True,blank=True,max_length=1000)
    documents = models.ManyToManyField(blank=True, related_name='documents', to=documents,verbose_name='Documents')
    post_type = models.CharField(
        max_length=6,
        choices=POST_TYPES,
        default=URL,
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    created_by = models.ForeignKey(
        User, related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True, editable=False)
    modified_by = models.ForeignKey(
        User, related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE, editable=False)


    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural ='Posts'
        indexes = [ models.Index(fields=['id','text']),]