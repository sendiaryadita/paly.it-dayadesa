from django.core.management.base import BaseCommand

from energi.models import CitizenReport, Desa


class Command(BaseCommand):
    help = "Mengisi data dummy desa dan laporan warga untuk DayaDesa"

    def handle(self, *args, **kwargs):
        desa_data = [
            {
                "nama_desa": "Desa Sukamaju",
                "kecamatan": "Natar",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.3080,
                "longitude": 105.1780,
                "ketersediaan_energi": 85,
                "keterjangkauan_energi": 80,
                "keberlanjutan_energi": 75,
                "keandalan_energi": 82,
            },
            {
                "nama_desa": "Desa Mekarsari",
                "kecamatan": "Jati Agung",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.3720,
                "longitude": 105.2560,
                "ketersediaan_energi": 65,
                "keterjangkauan_energi": 60,
                "keberlanjutan_energi": 55,
                "keandalan_energi": 62,
            },
            {
                "nama_desa": "Desa Harapan",
                "kecamatan": "Tanjung Bintang",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.4440,
                "longitude": 105.3370,
                "ketersediaan_energi": 35,
                "keterjangkauan_energi": 40,
                "keberlanjutan_energi": 30,
                "keandalan_energi": 38,
            },
        ]

        desa_objects = {}

        for data in desa_data:
            desa, created = Desa.objects.update_or_create(
                nama_desa=data["nama_desa"],
                defaults=data,
            )

            desa_objects[desa.nama_desa] = desa

            status = "dibuat" if created else "diperbarui"
            self.stdout.write(
                self.style.SUCCESS(
                    f"Data {desa.nama_desa} berhasil {status}."
                )
            )

        laporan_data = [
            {
                "desa": desa_objects["Desa Sukamaju"],
                "nama_pelapor": "Ahmad",
                "kategori_laporan": "Energi Terbarukan",
                "isi_laporan": "Desa sudah mulai menggunakan panel surya untuk penerangan fasilitas umum.",
                "status": "Baru",
            },
            {
                "desa": desa_objects["Desa Mekarsari"],
                "nama_pelapor": "Siti",
                "kategori_laporan": "Gangguan Listrik",
                "isi_laporan": "Listrik masih beberapa kali padam ketika malam hari.",
                "status": "Baru",
            },
            {
                "desa": desa_objects["Desa Harapan"],
                "nama_pelapor": "Budi",
                "kategori_laporan": "Akses Energi Terbatas",
                "isi_laporan": "Sebagian warga masih mengalami keterbatasan akses listrik stabil.",
                "status": "Diproses",
            },
        ]

        for laporan in laporan_data:
            report, created = CitizenReport.objects.get_or_create(
                desa=laporan["desa"],
                nama_pelapor=laporan["nama_pelapor"],
                kategori_laporan=laporan["kategori_laporan"],
                isi_laporan=laporan["isi_laporan"],
                defaults={
                    "status": laporan["status"],
                },
            )

            status = "dibuat" if created else "sudah ada"
            self.stdout.write(
                self.style.SUCCESS(
                    f"Laporan dari {report.nama_pelapor} berhasil {status}."
                )
            )

        self.stdout.write(
            self.style.SUCCESS("Seeder DayaDesa selesai dijalankan.")
        )
