from rest_framework import serializers


class ManuscriptSerializer(serializers.ModelSerializer):
    

    class Meta:
        fields = ('category', '')

