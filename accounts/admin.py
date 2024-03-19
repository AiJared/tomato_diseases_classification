from django.contrib import admin

from django.contrib import admin

from django.contrib.auth.models import Group
from accounts.models import (User, Administrator, Client)

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ["email", "username"]
    list_display = ("username", "first_name", "last_name",
                    "email", "gender", "role", 
                    "is_active", "is_admin",
                    "is_staff", "timestamp")
    
@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    search_fields = ["get_username",]
    list_display = ("get_username",)
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"
    get_username.admin_order_field = "user__username"

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ["get_username",]
    list_display = ("get_username",)
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"
    get_username.admin_order_field = "user__username"
