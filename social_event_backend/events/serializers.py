from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventCategory, Comment, Invitation, Message, Subscription

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    attendees = UserSerializer(many=True, read_only=True)
    category = EventCategorySerializer()

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        # Извлекаем данные для вложенного объекта (категории)
        category_data = validated_data.pop('category')
        # Создаем или находим категорию
        category, _ = EventCategory.objects.get_or_create(**category_data)
        # Создаем событие, связывая его с категорией
        event = Event.objects.create(category=category, **validated_data)
        return event

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer()

    class Meta:
        model = Invitation
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer()

    class Meta:
        model = Message
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'
