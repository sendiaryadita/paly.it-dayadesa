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

        widgets = {
            "desa": forms.Select(attrs={
                "class": "input-soft w-full"
            }),

            "nama_pelapor": forms.TextInput(attrs={
                "class": "input-soft w-full",
                "placeholder": "Nama Anda"
            }),

            "kategori_laporan": forms.Select(attrs={
                "class": "input-soft w-full"
            }),

            "isi_laporan": forms.Textarea(attrs={
                "class": "input-soft w-full",
                "rows": 5,
                "placeholder": "Tulis laporan Anda..."
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # desa jadi OPTIONAL
        self.fields["desa"].required = False