import re

from shorturl import models

from rest_framework import serializers


class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Protocol
        fields = '__all__'
        read_only_fields = '__all__'


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    protocol = ProtocolSerializer()

    class Meta:
        model = models.Url
        fields = '__all__'
        read_only_fields = ['url_short']
