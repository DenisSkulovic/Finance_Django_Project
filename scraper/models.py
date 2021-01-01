from django.db import models


class Pending(models.Model):
    date = models.DateField()
    link = models.URLField()


class Title(models.Model):
    title = models.TextField()

class Date(models.Model):
    date = models.DateField()

class Link(models.Model):
    link = models.URLField()
    date = models.ForeignKey(Date, on_delete=models.CASCADE)

class Text(models.Model):
    text = models.TextField()
    tag = models.CharField(max_length=55)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    position = models.IntegerField()

