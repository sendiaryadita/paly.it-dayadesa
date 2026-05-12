from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("peta/", views.peta_energi, name="peta_energi"),
    path("indeks-desa/", views.indeks_desa, name="indeks_desa"),
    path("desa/<int:desa_id>/", views.detail_desa, name="detail_desa"),
    path("lapor/", views.buat_laporan, name="buat_laporan"),
    path("laporan/", views.daftar_laporan, name="daftar_laporan"),
]
