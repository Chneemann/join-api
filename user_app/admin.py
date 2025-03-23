from django.contrib import admin
from django import forms
from .models import User

class UserAdmin(admin.ModelAdmin):
    exclude = ('uId',)
    list_display = ('first_name', 'last_name', 'email', 'phone', 'initials', 'color', 'status', 'last_login', 'is_active', 'is_staff')
    list_filter = ('status', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'password') #Passwort hier beibehalten.
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

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)