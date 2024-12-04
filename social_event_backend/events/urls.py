from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet)
router.register(r'events', EventViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'invitations', InvitationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('categories/<int:category_id>/events/', EventsByCategoryView.as_view(), name='events-by-category'),
    path('users/<int:user_id>/subscriptions/', UserSubscriptionsView.as_view(), name='user-subscriptions'),
    path('users/<int:user_id>/invitations/', UserInvitationsView.as_view(), name='user-invitations'),
    path('events/<int:event_id>/subscribers/', EventSubscribersView.as_view(), name='event-subscribers'),
]

urlpatterns += router.urls
