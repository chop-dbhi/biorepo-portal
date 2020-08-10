from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.flatpages.models import FlatPage


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    institution = models.CharField(max_length=100, null=True)
    # the user agrees to the End User License Agreement
    eula = models.BooleanField(default=False)
    # reason for using the system
    reason = models.TextField(null=True)
    password_expired = models.BooleanField(default=False)

    institutional_email = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s's Profile" % self.user.get_full_name() or self.user

from accounts.handlers import reset_eula  # noqa

signals.post_save.connect(reset_eula, sender=FlatPage)
