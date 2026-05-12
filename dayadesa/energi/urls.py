from django.urls import path

from . import views

urlpatterns = [
    path("", views.peta_energi, name="peta_energi"),
]
