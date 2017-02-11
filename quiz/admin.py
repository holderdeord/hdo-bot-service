from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea

from quiz.models import Promise, Category, Party, GoogleProfile, Manuscript, ManuscriptItem


class PromiseAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'body', 'status', 'testable']
    list_filter = ['status', 'testable', 'categories']


class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


class GoogleProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


class ManuscriptItemInline(admin.StackedInline):
    model = ManuscriptItem
    ordering = ('order', )
    extra = 0
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        js = [
            'quiz/jquery-ui.js',
            'quiz/inline_ordering.js'
        ]


class ManuscriptAdmin(admin.ModelAdmin):
    filter_horizontal = ['promises']
    inlines = [ManuscriptItemInline]


class ManuscriptItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'manuscript', 'type', 'text', 'order']
    list_filter = ['type']
    ordering = ['manuscript', 'order']


admin.site.register(Promise, PromiseAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Category)
admin.site.register(ManuscriptItem, ManuscriptItemAdmin)
admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(GoogleProfile, GoogleProfileAdmin)
