from django.db import models


class Desa(models.Model):
    nama_desa = models.CharField(max_length=100)
    kecamatan = models.CharField(max_length=100)
    kabupaten = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=100)

    latitude = models.FloatField()
    longitude = models.FloatField()

    ketersediaan_energi = models.IntegerField()
    keterjangkauan_energi = models.IntegerField()
    keberlanjutan_energi = models.IntegerField()
    keandalan_energi = models.IntegerField()

    esi_score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def hitung_esi(self):
        self.esi_score = (
            self.ketersediaan_energi * 0.30 +
            self.keterjangkauan_energi * 0.25 +
            self.keberlanjutan_energi * 0.25 +
            self.keandalan_energi * 0.20
        )
        return self.esi_score

    def kategori_esi(self):
        if self.esi_score <= 40:
            return "Krisis Energi"
        if self.esi_score <= 70:
            return "Transisi Energi"
        return "Mandiri Energi"

    def warna_esi(self):
        if self.esi_score <= 40:
            return "red"
        if self.esi_score <= 70:
            return "orange"
        return "green"

    def save(self, *args, **kwargs):
        self.hitung_esi()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_desa


class CitizenReport(models.Model):
    KATEGORI_CHOICES = [
        ("Gangguan Listrik", "Gangguan Listrik"),
        ("Akses Energi Terbatas", "Akses Energi Terbatas"),
        ("Biaya Energi Mahal", "Biaya Energi Mahal"),
        ("Energi Terbarukan", "Energi Terbarukan"),
        ("Lainnya", "Lainnya"),
    ]

    STATUS_CHOICES = [
        ("Baru", "Baru"),
        ("Diproses", "Diproses"),
        ("Selesai", "Selesai"),
    ]

    desa = models.ForeignKey(
        Desa,
        on_delete=models.CASCADE,
        related_name="laporan_warga"
    )
    nama_pelapor = models.CharField(max_length=100)
    kategori_laporan = models.CharField(
        max_length=100,
        choices=KATEGORI_CHOICES
    )
    isi_laporan = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Baru"
    )
    tanggal_laporan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pelapor} - {self.desa.nama_desa}"