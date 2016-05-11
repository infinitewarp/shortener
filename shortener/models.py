from django.conf import settings
from django.db import models


class Link(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    url = models.URLField(max_length=2000)

    class Meta:
        ordering = ['creation_date']

    @property
    def token(self):
        if not self.id:
            return None
        return settings.CONVERTER.encode(self.id)
