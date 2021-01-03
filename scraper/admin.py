from django.contrib import admin
from scraper.models import Text, Article, Request

admin.site.register(Text)
admin.site.register(Article)
admin.site.register(Request)