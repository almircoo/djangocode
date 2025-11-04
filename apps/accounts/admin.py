from django.contrib import admin
from .models import Ouser


# Register your models here.
@admin.register(Ouser)
class OuserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "date_joined")
    list_filter = ("is_active", "is_staff", "is_active", "groups")
    filter_horizontal = ("groups", "user_permissions")
    search_fields = ("username", "email")
