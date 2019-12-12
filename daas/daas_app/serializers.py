from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin

from .models import Sample, Result


class ResultSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    # fixme: add URL to download compressed code

    class Meta:
        model = Result
        fields = ('timeout', 'elapsed_time', 'exit_status', 'status', 'decompiler',
                  'processed_on', 'version')


class SampleSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    download_url = serializers.CharField()

    class Meta:
        model = Sample
        fields = ('md5', 'sha1', 'sha2', 'name', 'size', 'uploaded_on', 'file_type',
                  'seaweedfs_file_id')
