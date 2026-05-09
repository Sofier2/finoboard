from django.db import models
from django.contrib.auth.models import User


class Request(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField()

    votes = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    budget = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # 🔥 soft delete
    is_deleted = models.BooleanField(default=False)

    # 🔥 хто видалив
    deleted_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Vote(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='vote_set'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'request')


class CitizenProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    pin_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username