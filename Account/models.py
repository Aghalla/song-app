from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin # تغییر این خط
from django.utils import timezone
from django_resized import ResizedImageField
from django.urls import reverse
# Create your models here.

#BaseUserManager for create user admin

def user_upload_pic(instance, filename):
    return f'{instance.username}/pic/profile/{filename}'



class User(AbstractUser):
    email = models.EmailField(blank=False, null=False)
    # phone = models.CharField(max_length=11, blank=True, null=True)  # COMMENTED: phone feature disabled per request (kept for future)
    phone = models.CharField(max_length=11, blank=True, null=True)  # kept but not used - logic commented elsewhere
    profile_pic = ResizedImageField(upload_to=user_upload_pic, blank=True, null=True)
    bio = models.CharField(max_length=259, blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')


    joined_at = models.DateTimeField(default=timezone.now)


    def save(self, *args, **kwargs):
        try:
            old_img = User.objects.get(pk=self.pk)
            if old_img.profile_pic and old_img.profile_pic != self.profile_pic:
                old_img.profile_pic.delete(save=False)
        except User.DoesNotExist:
            pass
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"

    def get_absolute_url(self):
        return reverse("Music:profile-username", args=[self.username])
