import re

from shorturl import models

from rest_framework import serializers


class ProtocolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Protocol
        fields = ['id', 'protocol']
        read_only_fields = ['id', 'protocol']


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    protocol = ProtocolSerializer()

    class Meta:
        model = models.Url
        fields = '__all__'
        read_only_fields = ['url', 'url_short', 'creator_ip']
