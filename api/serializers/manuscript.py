from rest_framework import serializers

from quiz.models import Manuscript, ManuscriptItem, Promise, Category


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
        fields = ('type', 'order', 'text',)


class ManuscriptSerializer(serializers.ModelSerializer):
    items = ManuscriptItemSerializer(many=True)
    promises = PromiseSerializer(many=True)

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'category', 'items', 'promises',)


class ManuscriptListSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Manuscript
        fields = ('pk', 'name', 'category')
