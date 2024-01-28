from django.db import models


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название населенного пункта', unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = 'Название населенного пункта'
        verbose_name_plural = 'Название населенных пунктов'

    def __str__(self):
        return self.name

    #def save(self, *args, **kwargs):
    #    if not self.slug:
    #        self.slug = from_cyrillic_to_eng(str(self.name))
    #    super().save(*args, **kwargs)
