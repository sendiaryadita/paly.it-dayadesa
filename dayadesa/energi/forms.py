from django import forms

from .models import CitizenReport


class CitizenReportForm(forms.ModelForm):
    class Meta:
        model = CitizenReport
        fields = [
            "desa",
            "nama_pelapor",
            "kategori_laporan",
            "isi_laporan",
        ]

        labels = {
            "desa": "Pilih Desa",
            "nama_pelapor": "Nama Pelapor",
            "kategori_laporan": "Kategori Laporan",
            "isi_laporan": "Isi Laporan",
        }

        widgets = {
            "desa": forms.Select(attrs={"class": "form-select"}),
            "nama_pelapor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Masukkan nama pelapor",
                }
            ),
            "kategori_laporan": forms.Select(attrs={"class": "form-select"}),
            "isi_laporan": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Tuliskan kondisi energi yang terjadi di desa",
                }
            ),
        }
