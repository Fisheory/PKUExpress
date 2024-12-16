from django.db import models

from accounts.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_messages"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.CharField(
        max_length=10, choices=[("text", "text"), ("image", "image")]
    )

    # content: text or image url
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="message_images", null=True, blank=True)

    def __str__(self):
        if self.content_type == "text":
            return f"{self.sender.username} -> {self.receiver.username}: {self.text}"
        else:
            return f"{self.sender.username} -> {self.receiver.username}: image"
