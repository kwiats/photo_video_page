from rest_framework import serializers


class CommonSerializer(serializers.ModelSerializer):
    createDate = serializers.DateTimeField(source='create_date', format='%Y-%m-%d %H:%M:%S', read_only=True)
    updateDate = serializers.DateTimeField(source='update_date', format='%Y-%m-%d %H:%M:%S', read_only=True)
    isDeleted = serializers.BooleanField(source='is_deleted', read_only=True)
