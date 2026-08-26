from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Colleur, Myuser


class InlineColleur(admin.StackedInline):
	model = Colleur
	can_delete = False


class UserAdmin(BaseUserAdmin):
	inlines = [InlineColleur]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)