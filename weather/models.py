from django.db import models


class DayForecast(models.Model):
    weather = models.TextField()
    url     = models.TextField()

    def __str__(self):
        return self.weather
