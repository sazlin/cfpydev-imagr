from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from models import Photo, Album

# Register your models here.


# class SizeFilter(SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = _('image size')

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'size'

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('80s', _('in the eighties')),
#             ('90s', _('in the nineties')),
#         )

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value (either '80s' or '90s')
#         # to decide how to filter the queryset.
#         if self.value() == '80s':
#             return queryset.filter(birthday__gte=date(1980, 1, 1),
#                                     birthday__lte=date(1989, 12, 31))
#         if self.value() == '90s':
#             return queryset.filter(birthday__gte=date(1990, 1, 1),
#                                     birthday__lte=date(1999, 12, 31))


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
    readonly_fields = ('date_uploaded',
                       'date_modified',)
    list_display = ('title',
                    owner_link,
                    'date_uploaded',
                    'date_modified',
                    'size')
    list_display_links = (owner_link,)
    search_fields = ['date_uploaded']
    # attribute_of_class must be in db, cannot be function
    list_filter = ['size', ]


class AlbumAdmin(admin.ModelAdmin):

    def owner_link(self):
        return u"<a href='../../imagr_users/imagruser/{}/'>{}</a>".format(self.owner.id, self.owner)

    owner_link.short_description = ''
    owner_link.allow_tags = True

    fields = ('title',
              'description',
              'photos',
              'owner',
              'published',
              'cover_photo')
    list_display = ('title',
                    owner_link,
                    )
    # list_display_links = (owner_link,)
    search_fields = ['owner__username',
                     'owner__email',
                     'owner__first_name',
                     'owner__last_name']


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
