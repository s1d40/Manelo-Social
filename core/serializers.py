from rest_framework import serializers
from .models import ChatRoom, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_full_name = serializers.SerializerMethodField()
    recipient_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'chat_room', 'sender', 'recipient', 'content', 'sent_at', 'read_at', 'sender_full_name', 'recipient_full_name']
    
    def get_sender_full_name(self, obj):
        return obj.sender.full_name()

    def get_recipient_full_name(self, obj):
        return obj.recipient.full_name()

class ChatRoomSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'members', 'messages']