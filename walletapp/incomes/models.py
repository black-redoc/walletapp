from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Income(models.Model):
    concept = models.CharField(_("Concept"), max_length=80)
    amount = models.BigIntegerField(_("Amount"))
    slug = models.SlugField(_("Slug"), unique=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.concept)
        super(Income, self).save(*args, **kwargs)
