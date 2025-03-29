from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    exclude = ('uId',)
    list_display = ('first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'is_online', 'is_contact_only', 'last_login', 'is_active')
    list_filter = ('is_contact_only', 'is_online', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {
            'fields': ['first_name', 'last_name', 'email', 'phone', 'password']
        }),
        ('Additional Info', {
            'fields': ['initials', 'color', 'is_online', 'is_contact_only', 'last_login']
        }),
        ('Permissions', {
            'fields': ['is_active'] 
        }),
    )

    list_editable = ('is_active', 'is_online', 'is_contact_only')
    ordering = ('last_name',)

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)