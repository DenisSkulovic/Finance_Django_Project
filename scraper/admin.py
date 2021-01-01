from django.contrib import admin
from scraper.models import Text, Link, Date, Title, Pending

admin.site.register(Text)
admin.site.register(Link)
admin.site.register(Date)
admin.site.register(Title)
admin.site.register(Pending)


