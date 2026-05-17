from django.urls import path

from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("peta/", views.peta_energi, name="peta_energi"),
    path("api/desa/", views.api_data_desa, name="api_data_desa"),
    path("indeks-desa/", views.indeks_desa, name="indeks_desa"),
    path("desa/<int:desa_id>/", views.detail_desa, name="detail_desa"),
    path("lapor/", views.buat_laporan, name="buat_laporan"),
    path("laporan/", views.daftar_laporan, name="daftar_laporan"),
    path("tentang/", views.tentang, name="tentang"),
    path("login/", views.login_anggota, name="login_anggota"),
    path("daftar/", views.daftar_anggota, name="daftar_anggota"),
    path("logout/", views.logout_anggota, name="logout_anggota"),
    # Forum — "forum/buat/" HARUS di atas "forum/<int:topik_id>/"
    path("forum/", views.forum, name="forum"),
    path("forum/buat/", views.forum_buat, name="forum_buat"),
    path("forum/<int:topik_id>/", views.forum_detail, name="forum_detail"),
    path("forum/<int:topik_id>/balas/", views.forum_balas, name="forum_balas"),
]