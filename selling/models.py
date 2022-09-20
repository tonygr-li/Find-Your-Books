from django.db import models
from django.utils import timezone
from PIL import Image
from django.urls import reverse
from django.conf import settings
import os
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

# For expiry date: add 60 days to date_posted
def two_months_hence():
    return timezone.now() + timezone.timedelta(days=1)

# Post model: for posts (wanted and selling)
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=800)
    date_posted = models.DateTimeField(default=timezone.now)
    expiry_date = models.DateTimeField(default=two_months_hence)
    author = models.ForeignKey(User, on_delete=models.CASCADE) # Author of the post
    book_author = models.CharField(max_length=50) # Author of the book
    phone_contact = models.CharField(max_length=20, blank=True, null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    postal_code = models.CharField(max_length=40)
    isbn = models.DecimalField(max_digits=13, decimal_places=0)
    main_img = models.ImageField(upload_to='product_pics', verbose_name='Image', default='default-img.png')

    SELL_CHOICES = [
        (True, 'Sell'),
        (False, 'Want'),
    ]

    sell = models.BooleanField(default=True, choices=SELL_CHOICES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-info', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img=Image.open(self.main_img.path)

        if img.height > 700 or img.width > 700:
            output_size = (700,700)
            img.thumbnail(output_size)
            img.save(self.main_img.path)

class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_pics', verbose_name='Image', default='default-img.png', blank=True)

@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.main_img:
        if os.path.isfile(instance.main_img.path):
            os.remove(instance.main_img.path)

@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).main_img
    except Post.DoesNotExist:
        return False

    new_file = instance.main_img
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

@receiver(models.signals.post_delete, sender=Images)
def auto_delete_file_on_delete2(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Images)
def auto_delete_file_on_change2(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).image
    except Post.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)