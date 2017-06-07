from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from quiz.models import Manuscript, ManuscriptItem, Promise, Category, ManuscriptImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name',)


class PromiseSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    def get_categories(self, obj):
        return obj.categories.values_list('name', flat=True)

    class Meta:
        model = Promise
        fields = ('pk', 'body', 'status', 'categories',)


class ManuscriptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManuscriptItem
        fields = ('pk', 'type', 'order', 'text', 'button_text')


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

    def get_images(self, obj):
        return list(ManuscriptImageSerializer(ManuscriptImage.objects.all(), many=True).data)

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'category', 'updated', 'items', 'promises', 'images',)


class ManuscriptSerializer(BaseManuscriptSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:manuscript-detail')

    class Meta:
        model = Manuscript
        fields = ('pk', 'url', 'name', 'type', 'category', 'updated', 'items', 'promises', 'images',)


class ManuscriptListSerializer(WritableNestedModelSerializer):
    items = ManuscriptItemSerializer(many=True, required=False)
    category = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='api:manuscript-detail')

    def get_category(self, obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = Manuscript
        fields = ('pk', 'url', 'name', 'type', 'category', 'updated', 'items')
