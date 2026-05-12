# DayaDesa

DayaDesa adalah sistem informasi geospasial ketahanan energi desa berbasis web yang digunakan untuk memetakan kondisi energi desa, menghitung Energy Security Index (ESI), dan menampung laporan warga melalui fitur Citizen Report.

## Fitur Utama

1. Dashboard ringkasan DayaDesa
2. Peta energi interaktif menggunakan Leaflet.js
3. Pewarnaan desa berdasarkan skor ESI
4. Perhitungan Energy Security Index berdasarkan 4 pilar
5. Halaman indeks desa
6. Halaman detail desa
7. Form Citizen Report
8. Daftar laporan warga
9. Search dan filter data laporan
10. API JSON data desa untuk kebutuhan peta

## Teknologi yang Digunakan

- Python
- Django
- PostgreSQL
- Django Template
- Bootstrap
- Leaflet.js
- Chart.js
- OpenStreetMap

## Struktur Fitur ESI

Energy Security Index dihitung berdasarkan 4 pilar:

1. Ketersediaan energi
2. Keterjangkauan energi
3. Keberlanjutan energi
4. Keandalan energi

Formula sederhana:

```text
ESI = (Ketersediaan x 30%) + (Keterjangkauan x 25%) + (Keberlanjutan x 25%) + (Keandalan x 20%)

Kategori ESI:

0 - 40   = Krisis Energi
41 - 70  = Transisi Energi
71 - 100 = Mandiri Energi
```
