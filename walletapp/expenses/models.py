from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Expense(models.Model):
    concept = models.CharField(_("Concept"), max_length=80)
    amount = models.BigIntegerField(_("Amount"))
    slug = models.SlugField(_("Slug"), unique=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.concept)
        super(Expense, self).save(*args, **kwargs)

    @property
    def get_created_at(self) -> str:
        return f"{self.created_at.year}-{self.created_at.month}-{self.created_at.day}"

    @property
    def get_full_created_at(self) -> str:
        return f"{self.created_at.day}/{self.created_at.month}/{self.created_at.year}"

    @property
    def get_full_updated_at(self) -> str:
        return f"{self.updated_at.day}/{self.updated_at.month}/{self.updated_at.year}"
