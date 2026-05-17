from django.contrib import admin

from .models import CitizenReport, Desa, TopikForum, BalasanForum


@admin.register(Desa)
class DesaAdmin(admin.ModelAdmin):
    list_display = (
        "nama_desa",
        "kecamatan",
        "kabupaten",
        "provinsi",
        "esi_score",
        "kategori_esi",
    )
    search_fields = (
        "nama_desa",
        "kecamatan",
        "kabupaten",
        "provinsi",
    )
    list_filter = (
        "provinsi",
        "kabupaten",
    )
    readonly_fields = (
        "esi_score",
        "created_at",
        "updated_at",
    )


@admin.register(CitizenReport)
class CitizenReportAdmin(admin.ModelAdmin):
    list_display = (
        "nama_pelapor",
        "desa",
        "kategori_laporan",
        "status",
        "tanggal_laporan",
    )
    search_fields = (
        "nama_pelapor",
        "desa__nama_desa",
        "kategori_laporan",
    )
    list_filter = (
        "kategori_laporan",
        "status",
        "tanggal_laporan",
    )
    readonly_fields = (
        "tanggal_laporan",
    )

@admin.register(TopikForum)
class TopikForumAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "penulis", "pinned", "dibuat_pada")
    list_filter = ("kategori", "pinned")
    search_fields = ("judul", "isi", "penulis__username")
    list_editable = ("pinned",)


@admin.register(BalasanForum)
class BalasanForumAdmin(admin.ModelAdmin):
    list_display = ("topik", "penulis", "dibuat_pada")
    search_fields = ("isi", "penulis__username", "topik__judul")
