from django.urls import path
from . import views

urlpatterns = [
    path("api", views.chart_data, name="chart_data"),
]
