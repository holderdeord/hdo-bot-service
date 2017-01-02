from django.contrib import admin

# Register your models here.
from quiz.models import Promise, Category, Party


class PromiseAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'body', 'status', 'testable']
    list_filter = ['status', 'testable', 'categories']


admin.site.register(Promise, PromiseAdmin)


class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


admin.site.register(Party, PartyAdmin)
admin.site.register(Category)
