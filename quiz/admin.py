from django.contrib import admin

# Register your models here.
from quiz.models import Promise, Category, Party


class PromiseAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'body', 'status']


admin.site.register(Promise, PromiseAdmin)
admin.site.register(Category)
admin.site.register(Party)
