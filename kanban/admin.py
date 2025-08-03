from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Board, List, Card, Comment, UserProfile, Label, CardActivity


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_name', 'created_at']
    search_fields = ['user__username', 'user__email', 'display_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'user', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at', 'is_active', 'is_template']
    list_filter = ['is_active', 'is_template', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'position', 'created_at']
    list_filter = ['board', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['board', 'position']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['title', 'list', 'assignee', 'priority', 'position', 'completed', 'due_date']
    list_filter = ['priority', 'completed', 'list__board', 'created_at', 'labels']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'created_at'
    filter_horizontal = ['labels']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['card', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CardActivity)
class CardActivityAdmin(admin.ModelAdmin):
    list_display = ['card', 'user', 'activity_type', 'created_at']
    list_filter = ['activity_type', 'created_at']
    search_fields = ['card__title', 'user__username', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
