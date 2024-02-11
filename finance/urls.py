from django.urls import path
from . import views

urlpatterns = [
    path(
        "financial_records_per_proj/<str:ref>/",
        views.financial_records_per_proj,
        name="financial_records_per_proj",
    ),
    path(
        "financial_records_list/",
        views.financial_records_list,
        name="financial_records_list",
    ),
]
