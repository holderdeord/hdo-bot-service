from django.contrib import admin

# Register your models here.
from quiz.models import Promise, Category, Party, GoogleProfile


class PromiseAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'body', 'status', 'testable']
    list_filter = ['status', 'testable', 'categories']


class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


class GoogleProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Promise, PromiseAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Category)
admin.site.register(GoogleProfile, GoogleProfileAdmin)
