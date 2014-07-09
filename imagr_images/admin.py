from django.contrib import admin
from django.core import urlresolvers
from models import Photo, Album

# Register your models here.


class PhotoAdmin(admin.ModelAdmin):

    def owner_link(self):
            return u"<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(self.owner.id, self.owner)

    owner_link.short_description = ''
    owner_link.allow_tags = True

    fields = ('title',
              'description',
              'date_uploaded',
              'date_modified',
              'image',
              'owner',
              'published')
    readonly_fields = ('date_uploaded', 'date_modified',)
    list_display = ('title', owner_link, 'date_uploaded', 'date_modified', 'size')
    list_display_links = (owner_link,)






admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)
