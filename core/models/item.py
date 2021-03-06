from django.db import models
from django.conf import settings
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('S', "Длинные"),
    ('SW', "Спортивные"),
    ('OW', 'Уличные'),
)

LABEL_CHOICES = (
    ('P', "primary"),
    ('S', "secondary"),
    ('D', 'danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(blank=True, null=True)
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)

    @property
    def is_discount(self):
        if self.discount_price is None:
            return False
        else:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            "slug": self.slug
        })