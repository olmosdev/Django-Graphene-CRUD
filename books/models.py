from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # To see this field on admin panel
    def __str__(self) -> str:
        return self.title
