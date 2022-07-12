from django.db import models


class File(models.Model):
    file_name = models.CharField(max_length=255)
    sqlite = models.FileField(upload_to='uploaded/', max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'File'
        verbose_name_plural = 'Files'