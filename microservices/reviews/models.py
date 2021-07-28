from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..titles.models import Title
from ..users.models import User


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'reviews'
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['title', 'author']
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'comments'
