from django.db import models


class douban_book(models.Model):
    title = models.CharField(max_length=50)
    info = models.CharField(max_length=200)
    rating = models.FloatField()
    link = models.CharField(max_length=100)
    author = models.CharField(max_length=10)

    def __str__(self):
        return self.title