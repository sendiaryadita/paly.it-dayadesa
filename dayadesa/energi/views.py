from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitizenReportForm
from .models import CitizenReport, Desa


def dashboard(request):
    desa_list = Desa.objects.all()
    laporan_list = CitizenReport.objects.select_related("desa").order_by(
        "-tanggal_laporan"
    )[:5]

    jumlah_krisis = 0
    jumlah_transisi = 0
    jumlah_mandiri = 0

    for desa in desa_list:
        kategori = desa.kategori_esi()

        if kategori == "Krisis Energi":
            jumlah_krisis += 1
        elif kategori == "Transisi Energi":
            jumlah_transisi += 1
        else:
            jumlah_mandiri += 1

    rata_rata_esi = desa_list.aggregate(
        rata_rata=Avg("esi_score")
    )["rata_rata"]

    desa_prioritas = Desa.objects.all().order_by("esi_score")[:5]

    context = {
        "jumlah_desa": desa_list.count(),
        "jumlah_laporan": CitizenReport.objects.count(),
        "jumlah_krisis": jumlah_krisis,
        "jumlah_transisi": jumlah_transisi,
        "jumlah_mandiri": jumlah_mandiri,
        "rata_rata_esi": rata_rata_esi or 0,
        "desa_prioritas": desa_prioritas,
        "laporan_list": laporan_list,
    }

    return render(request, "energi/dashboard.html", context)


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

    jumlah_krisis = 0
    jumlah_transisi = 0
    jumlah_mandiri = 0

    for desa in desa_list:
        kategori = desa.kategori_esi()

        if kategori == "Krisis Energi":
            jumlah_krisis += 1
        elif kategori == "Transisi Energi":
            jumlah_transisi += 1
        else:
            jumlah_mandiri += 1

    context = {
        "desa_data": desa_data,
        "jumlah_desa": desa_list.count(),
        "jumlah_laporan": CitizenReport.objects.count(),
        "jumlah_krisis": jumlah_krisis,
        "jumlah_transisi": jumlah_transisi,
        "jumlah_mandiri": jumlah_mandiri,
    }

    return render(request, "energi/peta.html", context)


def indeks_desa(request):
    q = request.GET.get("q", "").strip()
    kategori = request.GET.get("kategori", "").strip()

    desa_queryset = Desa.objects.all()

    if q:
        desa_queryset = desa_queryset.filter(
            Q(nama_desa__icontains=q)
            | Q(kecamatan__icontains=q)
            | Q(kabupaten__icontains=q)
            | Q(provinsi__icontains=q)
        )

    desa_list = list(desa_queryset)

    if kategori:
        desa_list = [
            desa for desa in desa_list
            if desa.kategori_esi() == kategori
        ]

    desa_list = sorted(
        desa_list,
        key=lambda desa: desa.esi_score,
        reverse=True,
    )

    context = {
        "desa_list": desa_list,
        "q": q,
        "kategori": kategori,
    }

    return render(request, "energi/indeks_desa.html", context)


def detail_desa(request, desa_id):
    desa = get_object_or_404(Desa, id=desa_id)
    laporan_list = desa.laporan_warga.all().order_by("-tanggal_laporan")

    context = {
        "desa": desa,
        "laporan_list": laporan_list,
    }

    return render(request, "energi/detail_desa.html", context)


def buat_laporan(request):
    desa_id = request.GET.get("desa")
    selected_desa = None

    if desa_id:
        selected_desa = Desa.objects.filter(id=desa_id).first()

    if request.method == "POST":
        form = CitizenReportForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Laporan warga berhasil dikirim dan tersimpan di sistem.",
            )
            return redirect("daftar_laporan")
    else:
        initial_data = {}

        if selected_desa:
            initial_data["desa"] = selected_desa

        form = CitizenReportForm(initial=initial_data)

    context = {
        "form": form,
        "selected_desa": selected_desa,
    }

    return render(request, "energi/buat_laporan.html", context)


def daftar_laporan(request):
    laporan_list = CitizenReport.objects.select_related("desa").order_by(
        "-tanggal_laporan"
    )

    context = {
        "laporan_list": laporan_list,
    }

    return render(request, "energi/daftar_laporan.html", context)
