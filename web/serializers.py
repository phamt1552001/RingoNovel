from rest_framework import serializers
from .models import Novel

class NovelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = '__all__'
