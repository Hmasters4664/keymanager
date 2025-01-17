import sys

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils import timezone
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
import uuid
from django.db import models
import uuid
from django.template.defaultfilters import slugify


# Create your models here.


class Key(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255,blank=True)
    notes = models.TextField(blank=True)
    group = models.CharField(max_length=255, blank=True)
    date_created = models.DateTimeField(_('Date Created'),auto_now_add=True, blank=True,)
    modified = models.DateTimeField(_('Date Modified'),auto_now_add=True, blank=True,)
    slug = models.SlugField(blank=True, unique=True)

    def save(self, **kwargs):
        if not self.slug:
            slug_str = "%s" % (uuid.uuid4())
            self.slug = slugify(slug_str)
        super(Key, self).save(**kwargs)
