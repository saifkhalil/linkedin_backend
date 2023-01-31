from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django_countries.fields import CountryField
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email,firstName,lastName, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have an First name')
        if not lastName:
            raise ValueError('Users must have an Last name')
        user = self.model(
            email=self.normalize_email(email),
            firstName = firstName,
            lastName = lastName
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,firstName,lastName, password):
        user = self.create_user(
            email=self.normalize_email(email),
            firstName = firstName,
            lastName = lastName,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    phone = PhoneNumberField(verbose_name="Phone Number",blank=True, null=True)
    firstName = models.CharField(verbose_name="First name", max_length=30,blank=True, null=True)
    lastName = models.CharField(verbose_name="Last name", max_length=30,blank=True, null=True)
    job_title = models.CharField(verbose_name="Job title", max_length=30,blank=False, null=False)
    country = CountryField(default='IQ', blank_label=
        '(select country)', verbose_name='Country',blank=False, null=False)
    city = models.CharField(verbose_name="City", max_length=30,blank=True, null=True)   
    email = models.EmailField(verbose_name="Email", max_length=60, unique=True,blank=False, null=False)
    photo = models.ImageField(verbose_name="Avatar",
                              upload_to='avatars', default='photos/default.jpg')
    thumbnail = models.ImageField(verbose_name="Thumbnail image",
                                  upload_to='thumbnail', editable=False, blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User', related_name='%(class)s_createdby', on_delete=models.CASCADE, blank=True, null=True)
    modified_by = models.ForeignKey(
        'User', related_name='%(class)s_modifiedby', null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName','lastName']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.make_thumbnail():
            raise Exception(
                'Could not create thumbnail - is the file type valid?')
        super(User, self).save(*args, **kwargs)

    def make_thumbnail(self):
        image = Image.open(self.photo)
        image.thumbnail((100, 100), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

    # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

    # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(
            temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def __str__(self):
        string = f"{self.firstName} {self.lastName}" if self.firstName and self.lastName else self.email
        return string

    # For checking permissions. to keep it simple all admin have ALL permissons

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)

    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
