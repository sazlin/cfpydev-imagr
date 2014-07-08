from django.contrib import admin
from models import Photo, Album
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'date_uploaded', 'date_modified',)
    readonly_fields = ('date_uploaded', 'date_modified',)
    list_display = ('title', 'owner', 'created', 'size')
    list_display_links = ('owner',)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album)
