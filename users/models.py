from django.db import models
from django.contrib.auth.models import AbstractUser
from selling.models import Post

class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class ReportUser(models.Model):
    reporting = models.ForeignKey(User, on_delete=models.CASCADE)
    reported = models.ForeignKey(Post, on_delete=models.CASCADE)

    REPORT_CHOICES = [
        ('inappropriate','It contains offensive and/or inappropriate language and/or content.'),
        ('spam', 'It is spam'),
        ('laws', "It doesn't conform to laws"),
        ('false_info', 'It contains false information'),
        ('irrelevant', 'It is irrelevant'),
        ('other', 'Other'),
    ]

    category = models.CharField(max_length=70,choices=REPORT_CHOICES, default='spam')