from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea

from quiz.models import Promise, Category, Party, GoogleProfile, Manuscript, ManuscriptItem, ManuscriptImage


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


class ManuscriptImageAdmin(admin.ModelAdmin):
    list_display = ['admin_thumbnail', 'type']
    list_filter = ['type']

    def admin_thumbnail(self, obj):
        url = obj.get_url()

        if not url:
            return ''

        return '<img src="{}" width=250 />'.format(url)

    admin_thumbnail.short_description = 'Thumbnail'
    admin_thumbnail.allow_tags = True

admin.site.register(Promise, PromiseAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Category)
admin.site.register(ManuscriptItem, ManuscriptItemAdmin)
admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(ManuscriptImage, ManuscriptImageAdmin)
admin.site.register(GoogleProfile, GoogleProfileAdmin)
