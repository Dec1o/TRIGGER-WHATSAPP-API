from rest_framework import serializers
from .models import WhatsAppSession, MessageTemplate, MessageDispatch

class WhatsAppSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppSession
        fields = ['id', 'session_name', 'is_active', 'qr_code_path', 'created_at', 'updated_at']
        read_only_fields = ['id', 'qr_code_path', 'is_active', 'created_at', 'updated_at']

class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = ['id', 'name', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MessageDispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageDispatch
        fields = ['id', 'session', 'phone_number', 'original_message', 'modified_message', 
                 'media_type', 'media_url', 'status', 'scheduled_time', 'sent_time', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'modified_message', 'status', 'sent_time', 'created_at', 'updated_at']

class BulkMessageDispatchSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    phone_numbers = serializers.ListField(child=serializers.CharField(max_length=20))
    message = serializers.CharField()
    media_type = serializers.ChoiceField(choices=MessageDispatch.MEDIA_TYPE_CHOICES, default='none')
    media_url = serializers.CharField(required=False, allow_blank=True)