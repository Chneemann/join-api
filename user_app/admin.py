from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ('uId',)
    list_display = ('first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'status', 'last_login', 'is_active', 'is_staff')
    list_filter = ('status', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Additional Info', {
            'fields': ('initials', 'color', 'status', 'last_login')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff')
        }),
    )

    list_editable = ('is_active', 'is_staff', 'status')
    ordering = ('last_name',)

admin.site.register(User, UserAdmin)