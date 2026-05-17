from django.contrib import messages
from django.db.models import Avg, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import CitizenReportForm
from .models import CitizenReport, Desa, TopikForum, BalasanForum


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

    rata_rata_esi = desa_list.aggregate(rata_rata=Avg("esi_score"))["rata_rata"]
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
        data_desa.append({
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
        })
    return JsonResponse({"status": "success", "total_desa": len(data_desa), "data": data_desa})


def peta_energi(request):
    desa_list = Desa.objects.all().order_by("nama_desa")
    jumlah_krisis = jumlah_transisi = jumlah_mandiri = 0
    for desa in desa_list:
        k = desa.kategori_esi()
        if k == "Krisis Energi":
            jumlah_krisis += 1
        elif k == "Transisi Energi":
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
            Q(nama_desa__icontains=q) | Q(kecamatan__icontains=q) |
            Q(kabupaten__icontains=q) | Q(provinsi__icontains=q)
        )
    desa_list = list(desa_queryset)
    if kategori:
        desa_list = [d for d in desa_list if d.kategori_esi() == kategori]
    desa_list = sorted(desa_list, key=lambda d: d.esi_score, reverse=True)
    context = {"desa_list": desa_list, "q": q, "kategori": kategori}
    return render(request, "energi/indeks_desa.html", context)


def detail_desa(request, desa_id):
    desa = get_object_or_404(Desa, id=desa_id)
    laporan_list = desa.laporan_warga.all().order_by("-tanggal_laporan")
    context = {"desa": desa, "laporan_list": laporan_list}
    return render(request, "energi/detail_desa.html", context)


def buat_laporan(request):
    desa_id = request.GET.get("desa")
    selected_desa = None
    if desa_id:
        selected_desa = Desa.objects.filter(id=desa_id).first()

    if request.method == "POST":
        nama_desa_manual = request.POST.get("nama_desa_manual", "").strip()
        desa_id_post = request.POST.get("desa", "").strip()

        # Jika desa tidak ada di DB, buat desa baru dengan data minimal
        if not desa_id_post and nama_desa_manual:
            desa_obj, created = Desa.objects.get_or_create(
                nama_desa=nama_desa_manual,
                defaults={
                    "kecamatan": "-",
                    "kabupaten": "-",
                    "provinsi": "-",
                    "latitude": 0,
                    "longitude": 0,
                    "ketersediaan_energi": 50,
                    "keterjangkauan_energi": 50,
                    "keberlanjutan_energi": 50,
                    "keandalan_energi": 50,
                }
            )
            # Inject desa id ke POST data
            post_data = request.POST.copy()
            post_data["desa"] = str(desa_obj.id)
            form = CitizenReportForm(post_data)
        else:
            form = CitizenReportForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Laporan warga berhasil dikirim dan tersimpan di sistem.")
            return redirect("daftar_laporan")
    else:
        initial_data = {}
        if selected_desa:
            initial_data["desa"] = selected_desa
        form = CitizenReportForm(initial=initial_data)

    context = {"form": form, "selected_desa": selected_desa}
    return render(request, "energi/buat_laporan.html", context)


def daftar_laporan(request):
    q = request.GET.get("q", "").strip()
    kategori = request.GET.get("kategori", "").strip()
    status = request.GET.get("status", "").strip()
    laporan_list = CitizenReport.objects.select_related("desa").order_by("-tanggal_laporan")
    if q:
        laporan_list = laporan_list.filter(
            Q(nama_pelapor__icontains=q) | Q(isi_laporan__icontains=q) |
            Q(desa__nama_desa__icontains=q) | Q(desa__kecamatan__icontains=q) |
            Q(desa__kabupaten__icontains=q)
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


def forum(request):
    topik_list = TopikForum.objects.select_related("penulis").prefetch_related("balasan")
    from django.contrib.auth.models import User
    context = {
        "topik_list": topik_list,
        "jumlah_topik": topik_list.count(),
        "jumlah_komentar": BalasanForum.objects.count(),
        "jumlah_anggota_aktif": User.objects.filter(topik_forum__isnull=False).distinct().count(),
    }
    return render(request, "energi/forum.html", context)


def forum_detail(request, topik_id):
    topik = get_object_or_404(TopikForum, id=topik_id)
    return render(request, "energi/forum_detail.html", {"topik": topik})


@login_required
def forum_buat(request):
    if request.method == "POST":
        judul = request.POST.get("judul", "").strip()
        isi = request.POST.get("isi", "").strip()
        kategori = request.POST.get("kategori", "Umum")
        if judul and isi:
            TopikForum.objects.create(judul=judul, isi=isi, kategori=kategori, penulis=request.user)
            messages.success(request, "Topik berhasil dibuat!")
    return redirect("forum")


@login_required
def forum_balas(request, topik_id):
    topik = get_object_or_404(TopikForum, id=topik_id)
    if request.method == "POST":
        isi = request.POST.get("isi", "").strip()
        if isi:
            BalasanForum.objects.create(topik=topik, isi=isi, penulis=request.user)
            messages.success(request, "Balasan berhasil dikirim!")
    return redirect("forum_detail", topik_id=topik_id)