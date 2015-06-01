from django.conf.urls import url
from stocks import views

urlpatterns = [
    url(r'^$', views.portfolio, name="portfolio"),
    url(r'^portfolio', views.portfolio, name="portfolio"),
    url(r'^quote', views.quote, name="quote"),
    url(r'^buy', views.buy, name="buy"),
    url(r'^sell', views.sell, name="sell"),
]