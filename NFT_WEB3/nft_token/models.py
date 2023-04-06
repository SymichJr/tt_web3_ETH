from django.db import models

class Token(models.Model):
    id = models.AutoField(primary_key=True)
    unique_hash = models.CharField(max_length=255, unique=True)
    tx_hash = models.CharField(max_length=255)
    media_url = models.URLField()
    owner = models.CharField(max_length=42)

    def __str__(self):
        return self.unique_hash
