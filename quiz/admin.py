from django.contrib import admin
from django.db.models import TextField
from django.forms import Textarea

from quiz.models import (Promise, Category, Party, GoogleProfile, Manuscript, ManuscriptItem, ManuscriptImage, Answer,
                         AnswerSet, VoterGuideAlternative, HdoCategory, VoterGuideAnswer)


class PromiseAdmin(admin.ModelAdmin):
    list_display = ['external_id', 'body', 'status', 'testable']
    list_filter = ['status', 'testable', 'categories']


class PartyAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']


class GoogleProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


class ManuscriptItemInline(admin.StackedInline):
    model = ManuscriptItem
    ordering = ('order',)
    extra = 0
    fk_name = 'manuscript'
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }

    class Media:
        js = [
            'quiz/jquery-ui.js',
            'quiz/inline_ordering.js'
        ]


class VoterGuideAlternativeInline(admin.StackedInline):
    model = VoterGuideAlternative
    extra = 0
    readonly_fields = ['promises']


class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_default', 'is_first_in_category', 'type', 'category', 'hdo_category']
    readonly_fields = ['promises']
    inlines = [ManuscriptItemInline, VoterGuideAlternativeInline]

    # def alternatives_count(self, obj):
    #     # logging.info(obj.voterguidealternative)
    #     logging.info(obj._meta.get_fields())
    #     # return obj.voter_guide_alternative.count()
    #     return 'test'


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


class AnswerInline(admin.TabularInline):
    model = Answer
    readonly_fields = ['promise']
    extra = 0


class VoterGuideAnswerInline(admin.TabularInline):
    model = VoterGuideAnswer
    extra = 0


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['get_promise', 'status']

    def get_promise(self, obj):
        return '[{}] {}'.format(dict(Promise.STATUS_CHOICES).get(obj.status), obj.promise.body[:100])


class AnswerSetAdmin(admin.ModelAdmin):
    list_display = ['pk', 'session', 'updated']
    readonly_fields = ['uuid', 'session']
    inlines = [VoterGuideAnswerInline, AnswerInline]


class VoterGuideAlternativeAdmin(admin.ModelAdmin):
    list_display = ['text', 'manuscript', 'promises_count']

    def promises_count(self, obj):
        return obj.promises.count()


class HdoCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'label']


class VoterGuideAnswerAdmin(admin.ModelAdmin):
    pass



admin.site.register(AnswerSet, AnswerSetAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Category)
admin.site.register(HdoCategory, HdoCategoryAdmin)
admin.site.register(Promise, PromiseAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(ManuscriptItem, ManuscriptItemAdmin)
admin.site.register(Manuscript, ManuscriptAdmin)
admin.site.register(ManuscriptImage, ManuscriptImageAdmin)
admin.site.register(GoogleProfile, GoogleProfileAdmin)
admin.site.register(VoterGuideAlternative, VoterGuideAlternativeAdmin)
admin.site.register(VoterGuideAnswer, VoterGuideAnswerAdmin)
