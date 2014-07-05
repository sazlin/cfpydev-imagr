import datetime
from django.conf import settings
from django.db import models
import os.path


PRIVACY_LEVELS = (
    (0, 'Private'),
    (1, 'Public'),
)


def get_file_owner_username(instance, filename):
    "Calculate a storage path for this file instance"
    parts = [instance.owner.username]
    today = datetime.datetime.utcnow()
    parts.extend(map(unicode, [today.year, today.month]))
    parts.append(os.path.basename(filename))
    path = u"/".join(parts)
    return path


class Photo(models.Model):
    """Represent a single photo in a collection of photos
    """
    image = models.ImageField(
        upload_to=get_file_owner_username,
        height_field='height',
        width_field='width',
    )
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    height = models.PositiveSmallIntegerField(default=0, editable=False)
    width = models.PositiveSmallIntegerField(default=0, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published = models.IntegerField(choices=PRIVACY_LEVELS)

    def __unicode__(self):
        return self.title


class Album(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    photos = models.ManyToManyField(
        Photo,
        related_name="albums",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    published = models.IntegerField(choices=PRIVACY_LEVELS)
    cover_photo = models.ManyToManyField(
        Photo,
        related_name="cover_of",
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.title
