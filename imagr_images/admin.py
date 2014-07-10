from django.contrib import admin
from django.contrib.admin import SimpleListFilter, DateFieldListFilter
from models import Photo, Album


class ImageSizeListFilter(SimpleListFilter):
    title = 'Image Size'
    parameter_name = 'size'

    def lookups(self, request, model_admin):
        return (
            ('<= 1MB', '< 1MB'),
            ('<= 10MB', '1MB < size <= 10MB'),
            ('<= 100MB', '10MB < size <= 100MB'),
            ('> 100MB', '> 100MB'), )

    def queryset(self, request, queryset):
        if self.value() == '<= 1MB':
            return queryset.filter(image_size__lte=1024 * 1024)
        if self.value() == '<= 10MB':
            return queryset.filter(
                image_size__gt=1024 * 1024,
                image_size__lte=10 * 1024 * 1024, )
        if self.value() == '<= 100MB':
            return queryset.filter(
                image_size__gt=10 * 1024 * 1024,
                image_size__lte=100 * 1024 * 1024, )
        if self.value() == '> 100MB':
            return queryset.filter(image_size__gt=100 * 1024 * 1024)


class PhotoAdmin(admin.ModelAdmin):

    def owner_link(self, photo):
        return u"<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(photo.owner.id, photo.owner)

    owner_link.short_description = ''
    owner_link.allow_tags = True

    fields = ('title',
              'description',
              'date_uploaded',
              'date_modified',
              'image',
              'owner',
              'published')
    readonly_fields = ('date_uploaded',
                               'date_modified',)
    list_display = ('title',
                    'owner_link',
                    'date_uploaded',
                    'date_modified',
                    'image_size')
    #list_display_links = (owner_link,)
    search_fields = ['owner__username',
                            'owner__email',
                            'owner__first_name',
                            'owner__last_name', ]
    # attribute_of_class must be in db, cannot be function
    list_filter = (('date_uploaded', DateFieldListFilter),
                      (ImageSizeListFilter),)


class AlbumAdmin(admin.ModelAdmin):

    def owner_link(self, album):
        return u"<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(album.owner.id, album.owner)

    owner_link.short_description = ''
    owner_link.allow_tags = True

    fields = ('title',
              'description',
              'photos',
              'owner',
              'date_created',
              'date_modified',
              'cover_photo')
    readonly_fields = ('date_created', 'date_modified',)
    list_display = ('title',
                         'description',
                         'owner_link',
                         'date_created',
                         'date_modified',
                    )
    list_display_links = ('date_created',)
    search_fields = ['owner__username',
                     'owner__email',
                     'owner__first_name',
                     'owner__last_name']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
