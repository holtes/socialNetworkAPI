from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import *
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description="Получить список всех событий."),
    create=extend_schema(description="Создать новое событие."),
    retrieve=extend_schema(description="Получить информацию о конкретном событии."),
    update=extend_schema(description="Обновить информацию о событии."),
    partial_update=extend_schema(description="Частично обновить информацию о событии."),
    destroy=extend_schema(description="Удалить событие."),
)

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventsByCategoryView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Event.objects.filter(category_id=category_id)

class UserSubscriptionsView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Subscription.objects.filter(user_id=user_id)

class UserInvitationsView(ListAPIView):
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Invitation.objects.filter(recipient_id=user_id)

class EventSubscribersView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        user_ids = Subscription.objects.filter(event_id=event_id).values_list('user', flat=True)
        return User.objects.filter(id__in=user_ids)



