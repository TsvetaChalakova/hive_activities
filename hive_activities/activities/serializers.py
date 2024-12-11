from rest_framework import serializers
from hive_activities.activities.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        read_only_fields = ['created_by', 'assigned_to']
