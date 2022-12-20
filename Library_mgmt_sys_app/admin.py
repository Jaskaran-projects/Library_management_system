from django.contrib import admin
from .models import *

admin.site.register(Authors)
admin.site.register(Languages)
admin.site.register(Publishers)
admin.site.register(Books)
admin.site.register(Ebooks)
admin.site.register(HardCopys)