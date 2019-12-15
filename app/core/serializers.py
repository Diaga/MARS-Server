from rest_framework import serializers


class ModelBySerializer(serializers.ModelSerializer):
    """Support for created_by & updated_by"""

    def create(self, validated_data):
        """Support for created_by & updated_by"""
        request = self.context['request']

        user = super(ModelBySerializer, self).create(validated_data)
        user.created_by = request.user
        user.updated_by = request.user
        user.save()

        return user

    def update(self, instance, validated_data):
        """Support for updated_by"""
        request = self.context['request']

        user = super(ModelBySerializer, self).update(instance, validated_data)
        user.updated_by = request.user
        user.save()

        return user
