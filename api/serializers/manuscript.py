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
        fields = ('type', 'order', 'text', 'button_text')


class ManuscriptImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.get_url()

    class Meta:
        model = ManuscriptImage
        fields = ('url', 'type',)


class ManuscriptSerializer(serializers.ModelSerializer):
    items = ManuscriptItemSerializer(many=True)
    promises = PromiseSerializer(many=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        return list(ManuscriptImageSerializer(ManuscriptImage.objects.all(), many=True).data)

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'category', 'items', 'promises', 'images')


class ManuscriptListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'category')
