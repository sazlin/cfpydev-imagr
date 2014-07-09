from django.contrib import admin
from models import ImagrUser, Relationship
# Register your models here.


class ImagrUserAdmin(admin.ModelAdmin):

    fields = ('username',
              'first_name',
              'last_name',
              'email',
              )

    search_fields = ['username',
                     'email',
                     'first_name',
                     'last_name']

admin.site.register(ImagrUser, ImagrUserAdmin)
admin.site.register(Relationship)
