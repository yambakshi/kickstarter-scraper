from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-popular-campaigns', views.get_popular_campaigns)
]
