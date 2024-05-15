from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    category_img = models.ImageField(upload_to='pics', null=True, blank=True)  # Allow nulls
    slug = models.SlugField(max_length=100, unique=True)
    desc = models.TextField(max_length=500, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name
