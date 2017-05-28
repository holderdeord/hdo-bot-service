from django.contrib import admin

from messenger.models import ChatSession


class ChatSessionAdmin(admin.ModelAdmin):
    readonly_fields = ['uuid', 'user_id']
    list_display = ['uuid', 'state', 'user_id']
    list_filter = ['state']

admin.site.register(ChatSession, ChatSessionAdmin)
