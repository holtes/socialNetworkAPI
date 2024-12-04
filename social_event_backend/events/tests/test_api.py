from django.utils import timezone
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ..models import EventCategory, Event, Subscription, Invitation


class APITestCaseWithAuthentication(APITestCase):
    def setUp(self):
        # Создание пользователя и получение токена
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.user1 = User.objects.create_user(username="testuser1", password="password1234")
        self.client = APIClient()
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'password123'})
        self.access_token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Создание тестовых данных
        self.category = EventCategory.objects.create(name="Test Category")
        self.event = Event.objects.create(title="Test Event", description="Description", category=self.category,
                                          date=timezone.now(), location="Moscow", creator=self.user)
        self.event.attendees.set([self.user, self.user1])
        self.invitation = Invitation.objects.create(event=self.event, sender=self.user, recipient=self.user1,
                                                    is_accepted=False, sent_at=timezone.now())
        self.subscription = Subscription.objects.create(event=self.event, user=self.user, subscribed_at=timezone.now())


class TestEventCategoryAPI(APITestCaseWithAuthentication):
    def test_get_event_categories(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Category", str(response.data))

    def test_create_event_category(self):
        data = {"name": "New Category"}
        response = self.client.post('/api/categories/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventCategory.objects.count(), 2)


class TestEventAPI(APITestCaseWithAuthentication):
    def test_get_events_by_category(self):
        url = f'/api/categories/{self.category.id}/events/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Event", str(response.data))

    def test_create_event(self):
        data = {
          "category": {
              "name": "string",
              "description": "string"
          },
          "title": "Test event",
          "description": "Test event description",
          "date": "2024-12-04T10:36:36.446Z",
          "location": "Test location"
        }
        response = self.client.post('/api/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)


class TestSubscriptionAPI(APITestCaseWithAuthentication):
    def test_get_user_subscriptions(self):
        url = f'/api/users/{self.user.id}/subscriptions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("testuser", str(response.data))


class TestInvitationAPI(APITestCaseWithAuthentication):
    def test_get_user_invitations(self):
        url = f'/api/users/{self.user1.id}/invitations/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("testuser", str(response.data))


class TestEventSubscribersAPI(APITestCaseWithAuthentication):
    def test_get_event_subscribers(self):
        url = f'/api/events/{self.event.id}/subscribers/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("testuser", str(response.data))
