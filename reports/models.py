from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class ReportRecipient(models.Model):
    email = models.EmailField(unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})