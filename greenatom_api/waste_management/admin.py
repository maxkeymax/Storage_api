from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Storage)
admin.site.register(Factory)
admin.site.register(FromFactoryToStorageDistance)
