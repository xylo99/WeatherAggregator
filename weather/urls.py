from django.urls import path
from weather.views import scrape, forecast_list

urlpatterns = [
    path('scrape/', scrape, name="scrape"),
    path('', forecast_list, name="home"),
]
