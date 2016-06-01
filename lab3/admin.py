

# Register your models here.
from django.contrib import admin

from lab3.models import airlines, departure, destination, flights, planes

admin.site.register(airlines)
admin.site.register(departure)
admin.site.register(destination)
admin.site.register(planes)
admin.site.register(flights)