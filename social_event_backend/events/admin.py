from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id' ,'title', 'date', 'location', 'category')
    search_fields = ('title', 'description')
    list_filter = ('location', 'category')

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('event', 'author', 'created_at')
    search_fields = ('event__title', 'author__username')
    list_filter = ('created_at',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'subscribed_at')
    search_fields = ('user__username', 'event__title')
    list_filter = ('subscribed_at',)

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'event', 'is_accepted', 'sent_at')
    search_fields = ('inviter__username', 'invitee__username', 'event__title')
    list_filter = ('is_accepted', 'sent_at')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'event__title')
    list_filter = ('created_at',)
