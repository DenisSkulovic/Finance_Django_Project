from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# the following choices were introduced to restrict the extent of scraping. Free Heroku allows to store only so many rows.
periodicity_choices = (
    ('Daily', '1D'),
    ('Bidaily', '2D'),
    ('3-day', '3D'),
    ('5-day', '5D'),
    ('Weekly', 'W'),
    ('Biweekly', '2W'),
    ('Monthly', 'M'),
    )
periods_choices = (
    (1, 1),
    (2, 2),
    )
google_results_pages_choices = (
    (1, 1),
    (2, 2),
    )

status_choices = (
    ('Unprocessed','Unprocessed'),
    ('Processing','Processing'),
    ('Processed','Processed')
    )

class Request(models.Model):
    keyword = models.CharField(max_length=55)
    search_start_date = models.DateField()
    periods = models.IntegerField(choices=periods_choices)
    periodicity = models.CharField(max_length=55, choices=periodicity_choices)
    google_results_pages = models.IntegerField(choices=google_results_pages_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=55, default='Unprocessed', choices=status_choices)


class Article(models.Model):
    title = models.TextField(default='Queued for scraping.')
    date = models.DateField()
    link = models.URLField()
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=55, default='Unprocessed', choices=status_choices)
    def __str__(self):
        return f'title: {self.title}; date: {self.date}'


class Text(models.Model):
    text = models.TextField()
    tag = models.CharField(max_length=55)
    position = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    sentiment = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=55, default='Unprocessed', choices=status_choices)



# from django.db.models import Count
# Request.objects.annotate(count_articles=Count('article'))