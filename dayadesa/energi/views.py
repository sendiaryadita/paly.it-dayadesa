from django.shortcuts import render

from .models import Desa


def peta_energi(request):
    desa_list = Desa.objects.all().order_by("nama_desa")

    desa_data = []

    for desa in desa_list:
        desa_data.append(
            {
                "id": desa.id,
                "nama_desa": desa.nama_desa,
                "kecamatan": desa.kecamatan,
                "kabupaten": desa.kabupaten,
                "provinsi": desa.provinsi,
                "latitude": desa.latitude,
                "longitude": desa.longitude,
                "ketersediaan_energi": desa.ketersediaan_energi,
                "keterjangkauan_energi": desa.keterjangkauan_energi,
                "keberlanjutan_energi": desa.keberlanjutan_energi,
                "keandalan_energi": desa.keandalan_energi,
                "esi_score": round(desa.esi_score, 2),
                "kategori_esi": desa.kategori_esi(),
                "warna_esi": desa.warna_esi(),
                "jumlah_laporan": desa.laporan_warga.count(),
            }
        )

    context = {
        "desa_data": desa_data,
        "jumlah_desa": desa_list.count(),
    }

    return render(request, "energi/peta.html", context)