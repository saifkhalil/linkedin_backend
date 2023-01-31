from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','email','firstName','lastName','is_verified')
    list_filter = ('is_verified',)
    search_fields = ('email','firstName','lastName')

admin.site.register(User, UserAdmin)
