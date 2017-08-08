from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from quiz.models import Manuscript, ManuscriptItem, Promise, Category, ManuscriptImage, VoterGuideAlternative, \
    HdoCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name')


class HdoCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HdoCategory
        fields = ('pk', 'name')


class PromiseSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return obj.categories.values_list('name', flat=True)

    class Meta:
        model = Promise
        fields = ('pk', 'body', 'status', 'categories',)


class VoterGuideAlternativeSerializer(serializers.ModelSerializer):
    parties = serializers.SerializerMethodField()
    parties_short = serializers.SerializerMethodField()
    full_promises = serializers.SerializerMethodField()
    # FIXME: Use list of parties instead of promisor_name?

    def get_full_promises(self, obj):
        def get_promise(promise):
            return {
                'pk': promise.pk,
                'body': promise.body,
                'promisor_name': promise.promisor_name,
                'parties': list(set(promise.parties.values_list('title', flat=True))),
                'parties_short': list(set(promise.parties.values_list('short_title', flat=True)))
            }

        return list(map(get_promise, obj.promises.all()))

    def get_parties(self, obj):
        return list(set(obj.promises.values_list('parties__title', flat=True)))

    def get_parties_short(self, obj):
        return list(set(obj.promises.values_list('parties__short_title', flat=True)))
    
    class Meta:
        model = VoterGuideAlternative
        fields = ('pk', 'text', 'promises', 'full_promises', 'parties', 'parties_short')


class ManuscriptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptItem
        fields = ('pk', 'type', 'order', 'text',
                  # FIXME: Not very nice
                  'reply_text_1', 'reply_text_2', 'reply_text_3',
                  'reply_action_1', 'reply_action_2', 'reply_action_3')


class ManuscriptImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = ManuscriptImage
        fields = ('url', 'type',)


class BaseManuscriptSerializer(WritableNestedModelSerializer):
    items = ManuscriptItemSerializer(many=True, required=False)
    promises = PromiseSerializer(many=True, required=False)
    images = serializers.SerializerMethodField()
    voter_guide_alternatives = VoterGuideAlternativeSerializer(many=True, required=False)

    def get_images(self, obj):
        return list(ManuscriptImageSerializer(ManuscriptImage.objects.all(), many=True).data)

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'type', 'category', 'hdo_category', 'updated', 'default',
                  'is_first_in_category', 'items', 'promises', 'next', 'images',
                  'voter_guide_alternatives')


class ManuscriptSerializer(BaseManuscriptSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:manuscript-detail')

    class Meta:
        model = Manuscript
        fields = ('pk', 'url', 'name', 'type', 'category', 'hdo_category', 'updated', 'default',
                  'is_first_in_category', 'items', 'promises', 'next', 'images',
                  'voter_guide_alternatives')


class ManuscriptListSerializer(WritableNestedModelSerializer):
    items = ManuscriptItemSerializer(many=True, required=False)
    category = serializers.SerializerMethodField()
    hdo_category = serializers.SerializerMethodField()
    voter_guide_alternatives = VoterGuideAlternativeSerializer(many=True, required=False)
    url = serializers.HyperlinkedIdentityField(view_name='api:manuscript-detail')

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    def get_hdo_category(self, obj):
        return obj.hdo_category.name if obj.hdo_category else None

    class Meta:
        model = Manuscript
        fields = ('pk', 'url', 'name', 'type', 'category', 'hdo_category', 'next', 'updated', 'default',
                  'is_first_in_category', 'items', 'voter_guide_alternatives')
