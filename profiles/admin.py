from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from profiles.models import Profile, Occupation


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name',
                                      'occupation', 'date_of_birth', 'phone')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser',
                              'groups')}),
        (None, {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name',
                                      'occupation', 'date_of_birth', 'phone')}),
        (None, {'fields': ('groups',)})
    )
    list_display = ('get_full_name', 'occupation', 'username', 'phone',
                    'date_of_birth')
    list_filter = ('occupation',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'username')
    ordering = ('last_name',)


@admin.register(Occupation)
class OccupationAdmin(ModelAdmin):
    list_display = ('title', 'parent')
    search_fields = ('title',)
    ordering = ('title',)
