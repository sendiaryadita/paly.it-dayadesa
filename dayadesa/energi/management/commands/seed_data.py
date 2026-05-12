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
            {
                "nama_desa": "Desa Karang Sari",
                "kecamatan": "Ketapang",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.6840,
                "longitude": 105.7420,
                "ketersediaan_energi": 72,
                "keterjangkauan_energi": 68,
                "keberlanjutan_energi": 70,
                "keandalan_energi": 75,
            },
            {
                "nama_desa": "Desa Sumber Jaya",
                "kecamatan": "Merbau Mataram",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.5290,
                "longitude": 105.3920,
                "ketersediaan_energi": 45,
                "keterjangkauan_energi": 50,
                "keberlanjutan_energi": 42,
                "keandalan_energi": 48,
            },
            {
                "nama_desa": "Desa Way Galih",
                "kecamatan": "Tanjung Bintang",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.4010,
                "longitude": 105.3070,
                "ketersediaan_energi": 78,
                "keterjangkauan_energi": 74,
                "keberlanjutan_energi": 69,
                "keandalan_energi": 76,
            },
            {
                "nama_desa": "Desa Rejomulyo",
                "kecamatan": "Jati Agung",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.3510,
                "longitude": 105.2410,
                "ketersediaan_energi": 58,
                "keterjangkauan_energi": 55,
                "keberlanjutan_energi": 45,
                "keandalan_energi": 52,
            },
            {
                "nama_desa": "Desa Candimas",
                "kecamatan": "Natar",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.2940,
                "longitude": 105.2070,
                "ketersediaan_energi": 88,
                "keterjangkauan_energi": 83,
                "keberlanjutan_energi": 79,
                "keandalan_energi": 86,
            },
            {
                "nama_desa": "Desa Purwodadi",
                "kecamatan": "Tanjung Sari",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.4650,
                "longitude": 105.4020,
                "ketersediaan_energi": 32,
                "keterjangkauan_energi": 38,
                "keberlanjutan_energi": 28,
                "keandalan_energi": 34,
            },
            {
                "nama_desa": "Desa Sidomulyo",
                "kecamatan": "Sidomulyo",
                "kabupaten": "Lampung Selatan",
                "provinsi": "Lampung",
                "latitude": -5.5640,
                "longitude": 105.5800,
                "ketersediaan_energi": 69,
                "keterjangkauan_energi": 66,
                "keberlanjutan_energi": 61,
                "keandalan_energi": 64,
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
            {
                "desa": desa_objects["Desa Sumber Jaya"],
                "nama_pelapor": "Rina",
                "kategori_laporan": "Biaya Energi Mahal",
                "isi_laporan": "Sebagian warga merasa biaya energi masih cukup tinggi.",
                "status": "Baru",
            },
            {
                "desa": desa_objects["Desa Karang Sari"],
                "nama_pelapor": "Dewi",
                "kategori_laporan": "Energi Terbarukan",
                "isi_laporan": "Warga mulai tertarik menggunakan lampu tenaga surya untuk area jalan desa.",
                "status": "Selesai",
            },
            {
                "desa": desa_objects["Desa Way Galih"],
                "nama_pelapor": "Hendra",
                "kategori_laporan": "Gangguan Listrik",
                "isi_laporan": "Tegangan listrik terkadang turun pada malam hari ketika pemakaian meningkat.",
                "status": "Diproses",
            },
            {
                "desa": desa_objects["Desa Rejomulyo"],
                "nama_pelapor": "Nadia",
                "kategori_laporan": "Akses Energi Terbatas",
                "isi_laporan": "Beberapa titik rumah warga masih membutuhkan penerangan tambahan di malam hari.",
                "status": "Baru",
            },
            {
                "desa": desa_objects["Desa Candimas"],
                "nama_pelapor": "Fajar",
                "kategori_laporan": "Energi Terbarukan",
                "isi_laporan": "Fasilitas umum desa sudah memiliki penerangan yang cukup stabil.",
                "status": "Selesai",
            },
            {
                "desa": desa_objects["Desa Purwodadi"],
                "nama_pelapor": "Lestari",
                "kategori_laporan": "Gangguan Listrik",
                "isi_laporan": "Listrik sering padam saat hujan deras dan mengganggu aktivitas warga.",
                "status": "Diproses",
            },
            {
                "desa": desa_objects["Desa Sidomulyo"],
                "nama_pelapor": "Rangga",
                "kategori_laporan": "Biaya Energi Mahal",
                "isi_laporan": "Sebagian warga berharap ada solusi energi alternatif yang lebih hemat.",
                "status": "Baru",
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
