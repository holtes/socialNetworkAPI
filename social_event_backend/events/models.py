from django.db import models
from django.contrib.auth.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name='events')

    def __str__(self):
        return self.title

class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.event.title}"

class Invitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    is_accepted = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invitation to {self.event.title} from {self.sender.username} to {self.recipient.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.event.title}"

