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
            "desa": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-slate-50 p-2 text-slate-900 focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100",
                }
            ),
            "nama_pelapor": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-slate-50 p-2 text-slate-900 placeholder-slate-400 focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100 dark:placeholder-slate-500",
                    "placeholder": "Masukkan nama pelapor",
                }
            ),
            "kategori_laporan": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-slate-50 p-2 text-slate-900 focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100",
                }
            ),
            "isi_laporan": forms.Textarea(
                attrs={
                    "class": "w-full rounded-xl border border-slate-200 bg-slate-50 p-2 text-slate-900 placeholder-slate-400 focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 dark:border-slate-600 dark:bg-slate-900 dark:text-slate-100 dark:placeholder-slate-500",
                    "rows": 5,
                    "placeholder": "Tuliskan kondisi energi yang terjadi di desa",
                }
            ),
        }
