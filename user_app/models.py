import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

def generate_uuid_without_dashes():
    return uuid.uuid4().hex

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None):
        user = self.create_user(email, first_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    uId = models.UUIDField(default=uuid.uuid4, unique=True, editable=False) 
    id = models.CharField(primary_key=True, default=generate_uuid_without_dashes, max_length=32,editable=False, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    initials = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=20, blank=True)
    is_online = models.BooleanField(default=False)
    is_contact_only = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(Permission, related_name="user_app_users_permissions", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email