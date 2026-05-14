from django.contrib import messages
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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


def tentang(request):
    return render(request, "energi/tentang.html")


def api_data_desa(request):
    desa_list = Desa.objects.all().order_by("nama_desa")

    data_desa = []

    for desa in desa_list:
        data_desa.append(
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

    return JsonResponse(
        {
            "status": "success",
            "total_desa": len(data_desa),
            "data": data_desa,
        }
    )


def peta_energi(request):
    desa_list = Desa.objects.all().order_by("nama_desa")

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
    q = request.GET.get("q", "").strip()
    kategori = request.GET.get("kategori", "").strip()
    status = request.GET.get("status", "").strip()

    laporan_list = CitizenReport.objects.select_related("desa").order_by(
        "-tanggal_laporan"
    )

    if q:
        laporan_list = laporan_list.filter(
            Q(nama_pelapor__icontains=q)
            | Q(isi_laporan__icontains=q)
            | Q(desa__nama_desa__icontains=q)
            | Q(desa__kecamatan__icontains=q)
            | Q(desa__kabupaten__icontains=q)
        )

    if kategori:
        laporan_list = laporan_list.filter(kategori_laporan=kategori)

    if status:
        laporan_list = laporan_list.filter(status=status)

    context = {
        "laporan_list": laporan_list,
        "q": q,
        "kategori": kategori,
        "status": status,
        "kategori_choices": CitizenReport.KATEGORI_CHOICES,
        "status_choices": CitizenReport.STATUS_CHOICES,
    }

    return render(request, "energi/daftar_laporan.html", context)

def login_anggota(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login berhasil.")
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "energi/login.html", {"form": form})


def daftar_anggota(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Akun berhasil dibuat.")
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "energi/daftar_anggota.html", {"form": form})


def logout_anggota(request):
    logout(request)
    messages.success(request, "Berhasil logout.")
    return redirect("dashboard")
