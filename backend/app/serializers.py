from rest_framework import serializers

class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

class TwoFileSerializer(serializers.Serializer):
    file1 = serializers.FileField()
    file2 = serializers.FileField()
