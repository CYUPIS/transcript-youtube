# 📖 BUKU MANUAL
# YouTube Transcript Automation Script
## Versi 2.0

---

## 📋 DAFTAR ISI

1. [Pendahuluan](#1-pendahuluan)
2. [Instalasi](#2-instalasi)
3. [Penggunaan Dasar](#3-penggunaan-dasar)
4. [Penggunaan Multi-Video](#4-penggunaan-multi-video)
5. [Format Output](#5-format-output)
6. [Pengaturan Delay](#6-pengaturan-delay)
7. [Menggunakan Proxy](#7-menggunakan-proxy)
8. [Input dari File](#8-input-dari-file)
9. [Troubleshooting](#9-troubleshooting)
10. [Tips & Best Practices](#10-tips--best-practices)
11. [FAQ](#11-faq)
12. [Changelog](#12-changelog)

---

## 1. PENDAHULUAN

### 1.1 Apa itu YouTube Transcript Automation?

YouTube Transcript Automation adalah script Python untuk mengambil transkrip (teks percakapan) dari video YouTube secara otomatis. Script ini menggunakan library `youtube-transcript-api` untuk mengakses subtitle/caption yang tersedia di video YouTube, baik yang dibuat manual maupun yang di-generate otomatis oleh YouTube.

### 1.2 Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| ✅ Single Video | Ambil transkrip dari satu video |
| ✅ Multi-Video | Ambil transkrip dari banyak video sekaligus |
| ✅ Auto-Save | Simpan otomatis ke file terpisah per video |
| ✅ Anti-Spam | Delay random untuk menghindari blokir |
| ✅ Multiple Format | Raw, Timestamp, SRT, JSON |
| ✅ URL Support | Paste URL lengkap, auto-extract ID |
| ✅ File Input | Baca daftar video dari file |
| ✅ Proxy Support | Gunakan proxy untuk bypass IP block |
| ✅ Multi-Language | Prioritas bahasa yang bisa dikustomisasi |

### 1.3 Kegunaan

- 📝 Membuat subtitle untuk video
- 📊 Analisis konten video
- 📖 Membuat ringkasan/transkrip
- 🔍 Indexing konten video untuk search
- ♿ Aksesibilitas untuk tuna rungu
- 🌐 Terjemahan otomatis

---

## 2. INSTALASI

### 2.1 Requirements

- Python 3.7 atau lebih baru
- pip (Python package manager)
- Koneksi internet

### 2.2 Install Library

```bash
pip install youtube-transcript-api
```

### 2.3 Download Script

Simpan file `youtube_transcript_automation.py` di komputer Anda.

### 2.4 Verifikasi Instalasi

```bash
python youtube_transcript_automation.py --help
```

Jika berhasil, akan muncul pesan help dengan semua opsi yang tersedia.

---

## 3. PENGGUNAAN DASAR

### 3.1 Mengambil Transkrip Single Video

**Cara paling mudah:**

```bash
python youtube_transcript_automation.py ytYpQxHf078
```

Output akan langsung ditampilkan di terminal.

### 3.2 Menyimpan ke File

```bash
python youtube_transcript_automation.py ytYpQxHf078 -o transcript.txt
```

### 3.3 Menggunakan URL Lengkap

Script otomatis mengekstrak video ID dari berbagai format URL:

```bash
# Semua cara ini sama hasilnya
python youtube_transcript_automation.py ytYpQxHf078
python youtube_transcript_automation.py https://www.youtube.com/watch?v=ytYpQxHf078
python youtube_transcript_automation.py https://youtu.be/ytYpQxHf078
python youtube_transcript_automation.py https://www.youtube.com/embed/ytYpQxHf078
python youtube_transcript_automation.py https://www.youtube.com/shorts/ytYpQxHf078
```

### 3.4 Memilih Bahasa

Default: Indonesia (`id`) lalu Inggris (`en`). Jika tidak ada, akan mencoba bahasa lain yang tersedia.

```bash
# Prioritas: Jepang → Inggris
python youtube_transcript_automation.py ytYpQxHf078 -l ja en

# Prioritas: Jawa → Indonesia → Inggris
python youtube_transcript_automation.py ytYpQxHf078 -l jv id en
```

### 3.5 Melihat Bahasa yang Tersedia

```bash
python youtube_transcript_automation.py ytYpQxHf078 --list
```

Output:
```
Transcript untuk video ytYpQxHf078:
--------------------------------------------------
  [id] Indonesian (Generated)
  [en] English (Generated)
```

---

## 4. PENGGUNAAN MULTI-VIDEO

### 4.1 Multiple Video ID

Masukkan beberapa video ID sekaligus:

```bash
python youtube_transcript_automation.py video1 video2 video3
```

Contoh:
```bash
python youtube_transcript_automation.py ytYpQxHf078 dQw4w9WgXcQ jNQXAC9IVRw
```

### 4.2 Output Otomatis

Untuk multi-video, setiap video otomatis disimpan ke file terpisah:

```bash
# Default folder: ./transcripts/
python youtube_transcript_automation.py video1 video2 video3

# Custom folder:
python youtube_transcript_automation.py video1 video2 video3 --output-dir ./my_transcripts
```

### 4.3 Naming File

Format nama file otomatis: `{video_id}.{ekstensi}`

| Format | Ekstensi |
|--------|----------|
| raw | .txt |
| timestamp | .txt |
| srt | .srt |
| json | .json |

Contoh output:
```
./transcripts/
├── ytYpQxHf078.txt
├── dQw4w9WgXcQ.txt
└── jNQXAC9IVRw.txt
```

### 4.4 Ringkasan Hasil

Di akhir proses, akan ditampilkan ringkasan:

```
============================================================
📊 RINGKASAN
============================================================
  ✅ Berhasil: 2
  ❌ Gagal: 1

❌ Video yang gagal:
  - abc123: Transcript tidak tersedia untuk video ini

✅ File yang berhasil disimpan:
  - ./transcripts/ytYpQxHf078.txt
  - ./transcripts/dQw4w9WgXcQ.txt
============================================================
```

---

## 5. FORMAT OUTPUT

### 5.1 Raw (Default)

Transkrip mentah tanpa timestamp:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format raw
```

Output:
```
Selamat datang di Malaka Podcast. Di sini sudah bersama dengan Kania Cita dan Feri Irwandi yang host. Dan kita kedatangan Pak Tom Lembong untuk kali kedua ya...
```

### 5.2 Timestamp

Transkrip dengan timestamp:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format timestamp
```

Output:
```
[00:00] Selamat datang di Malaka Podcast.
[00:05] Di sini sudah bersama dengan Kania Cita dan Feri Irwandi yang host.
[00:12] Dan kita kedatangan Pak Tom Lembong untuk kali kedua ya.
[00:18] Untuk kali kedua tepuk tangan.
```

### 5.3 SRT (Subtitle)

Format standar subtitle:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format srt -o video.srt
```

Output:
```
1
00:00:00,000 --> 00:00:05,000
Selamat datang di Malaka Podcast.

2
00:00:05,000 --> 00:00:12,000
Di sini sudah bersama dengan Kania Cita dan Feri Irwandi yang host.

3
00:00:12,000 --> 00:00:18,000
Dan kita kedatangan Pak Tom Lembong untuk kali kedua ya.
```

### 5.4 JSON

Format JSON untuk processing lanjutan:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format json
```

Output:
```json
[
  {
    "text": "Selamat datang di Malaka Podcast.",
    "start": 0.0,
    "duration": 5.0
  },
  {
    "text": "Di sini sudah bersama dengan Kania Cita dan Feri Irwandi yang host.",
    "start": 5.0,
    "duration": 7.0
  }
]
```

---

## 6. PENGATURAN DELAY

### 6.1 Kenapa Perlu Delay?

YouTube memiliki sistem proteksi terhadap request berlebihan. Jika terlalu banyak request dalam waktu singkat, IP Anda bisa diblokir sementara atau permanen.

### 6.2 Delay Default

- **Minimal**: 2 detik
- **Maksimal**: 5 detik
- **Random**: Setiap delay bernilai random antara min-max

### 6.3 Custom Delay

```bash
# Delay 3-8 detik
python youtube_transcript_automation.py video1 video2 video3 --delay 3 8

# Delay 5-10 detik (lebih aman)
python youtube_transcript_automation.py video1 video2 video3 --delay 5 10

# Delay 1-2 detik (lebih cepat, tapi berisiko)
python youtube_transcript_automation.py video1 video2 video3 --delay 1 2
```

### 6.4 Menonaktifkan Delay

⚠️ **TIDAK DISARANKAN** - Berisiko tinggi terkena spam detection!

```bash
python youtube_transcript_automation.py video1 video2 video3 --no-delay
```

### 6.5 Rekomendasi Delay

| Jumlah Video | Delay | Keterangan |
|--------------|-------|------------|
| 1-10 | 2-5 detik | Default, cukup aman |
| 10-50 | 3-7 detik | Lebih aman |
| 50-100 | 5-10 detik | Sangat aman |
| >100 | 8-15 detik | Aman untuk batch besar |

---

## 7. MENGGUNAKAN PROXY

### 7.1 Kapan Perlu Proxy?

- IP Anda diblokir YouTube
- Menjalankan script dari server cloud (AWS, GCP, Azure, dll)
- Request dalam jumlah sangat besar

### 7.2 Format Proxy

```
http://username:password@host:port
```

### 7.3 Cara Penggunaan

```bash
# HTTP Proxy
python youtube_transcript_automation.py ytYpQxHf078 --proxy "http://user:pass@proxy.example.com:8080"

# SOCKS5 Proxy
python youtube_transcript_automation.py ytYpQxHf078 --proxy "socks5://user:pass@proxy.example.com:1080"
```

### 7.4 Rekomendasi Proxy

| Tipe Proxy | Kelebihan | Kekurangan |
|------------|-----------|------------|
| **Rotating Residential** | Paling aman, IP berubah otomatis | Berbayar |
| **Static Residential** | Lebih murah | IP tetap, bisa diblokir |
| **Datacenter** | Murah, cepat | Mudah diblokir YouTube |
| **Free Proxy** | Gratis | Tidak stabil, tidak aman |

### 7.5 Layanan Proxy Rekomendasi

- **Webshare** - Rotating residential proxy (ada referral di library)
- **Bright Data** - Enterprise grade
- **Smartproxy** - Balance price/quality
- **Oxylabs** - Premium option

---

## 8. INPUT DARI FILE

### 8.1 Format File

Buat file teks dengan satu video ID/URL per baris:

**videos.txt:**
```
# Ini komentar (diabaikan)
ytYpQxHf078
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/jNQXAC9IVRw

# Bisa campur ID dan URL
abc123def45
```

### 8.2 Cara Penggunaan

```bash
python youtube_transcript_automation.py --file videos.txt
```

### 8.3 Kombinasi File + Manual

```bash
# Gabungkan dari file + ID manual
python youtube_transcript_automation.py --file videos.txt video1 video2
```

### 8.4 Contoh Workflow

```bash
# 1. Buat file daftar video
cat > my_videos.txt << EOF
# Daftar video untuk transkrip
ytYpQxHf078
dQw4w9WgXcQ
jNQXAC9IVRw
EOF

# 2. Jalankan script
python youtube_transcript_automation.py --file my_videos.txt --format srt --output-dir ./subtitles

# 3. Hasil
ls ./subtitles/
# ytYpQxHf078.srt
# dQw4w9WgXcQ.srt
# jNQXAC9IVRw.srt
```

---

## 9. TROUBLESHOOTING

### 9.1 Error: "Request blocked by YouTube"

**Penyebab:**
- IP Anda diblokir YouTube
- Menjalankan dari server cloud

**Solusi:**
1. Gunakan proxy: `--proxy "http://..."`
2. Jalankan dari komputer lokal
3. Tunggu beberapa jam dan coba lagi

### 9.2 Error: "IP blocked"

**Penyebab:**
- IP sudah diblokir permanen

**Solusi:**
1. Gunakan rotating residential proxy
2. Ganti IP (restart router jika dynamic IP)
3. Gunakan VPN

### 9.3 Error: "Transcripts disabled"

**Penyebab:**
- Video tidak memiliki subtitle/caption

**Solusi:**
- Tidak ada solusi, video tersebut tidak menyediakan transkrip

### 9.4 Error: "No transcript found"

**Penyebab:**
- Tidak ada transkrip dalam bahasa yang diminta

**Solusi:**
```bash
# Cek bahasa yang tersedia
python youtube_transcript_automation.py VIDEO_ID --list

# Gunakan bahasa yang tersedia
python youtube_transcript_automation.py VIDEO_ID -l en
```

### 9.5 Error: "Video unavailable"

**Penyebab:**
- Video private
- Video dihapus
- Video diblokir di region Anda

**Solusi:**
- Gunakan proxy dari region lain
- Video tidak bisa diakses

### 9.6 Error: "Connection timeout"

**Penyebab:**
- Koneksi lambat
- Proxy tidak responsif

**Solusi:**
1. Periksa koneksi internet
2. Ganti proxy
3. Coba lagi nanti

### 9.7 Output Kosong

**Penyebab:**
- Bahasa tidak sesuai
- Video tanpa audio/speech

**Solusi:**
```bash
# Cek bahasa tersedia
python youtube_transcript_automation.py VIDEO_ID --list
```

---

## 10. TIPS & BEST PRACTICES

### 10.1 Untuk Penggunaan Sekali-sekali

```bash
# Delay default sudah cukup
python youtube_transcript_automation.py video_id
```

### 10.2 Untuk Batch Besar

```bash
# Gunakan delay lebih besar
python youtube_transcript_automation.py --file videos.txt --delay 5 10

# Atau pecah menjadi batch kecil
# batch1.txt (50 video)
python youtube_transcript_automation.py --file batch1.txt --delay 5 8

# batch2.txt (50 video)
python youtube_transcript_automation.py --file batch2.txt --delay 5 8
```

### 10.3 Untuk Server Cloud

```bash
# WAJIB gunakan proxy
python youtube_transcript_automation.py video_id --proxy "http://user:pass@proxy:port"
```

### 10.4 Optimasi Performa

```bash
# Format raw = paling cepat
python youtube_transcript_automation.py video_id --format raw

# Format srt = sedikit lebih lambat karena formatting
python youtube_transcript_automation.py video_id --format srt
```

### 10.5 Backup & Logging

```bash
# Simpan dengan timestamp
python youtube_transcript_automation.py video_id -o "transcript_$(date +%Y%m%d_%H%M%S).txt"

# Redirect stderr untuk logging
python youtube_transcript_automation.py --file videos.txt 2> error.log
```

### 10.6 Validasi Video ID

Script otomatis memvalidasi dan mengekstrak video ID dari berbagai format:
- ✅ `ytYpQxHf078`
- ✅ `https://www.youtube.com/watch?v=ytYpQxHf078`
- ✅ `https://youtu.be/ytYpQxHf078`
- ✅ `https://www.youtube.com/embed/ytYpQxHf078`
- ✅ `https://www.youtube.com/shorts/ytYpQxHf078`

---

## 11. FAQ

### Q1: Apakah script ini legal?

**A:** Ya, script ini hanya mengakses subtitle/caption yang sudah tersedia publik di YouTube. Sama seperti mengklik tombol "Show transcript" di YouTube.

### Q2: Apakah bisa untuk video private?

**A:** Tidak, hanya video publik yang bisa diambil transkripnya.

### Q3: Apakah ada limit request?

**A:** YouTube tidak mempublikasikan limit pasti. Dengan delay 2-5 detik, Anda bisa memproses ratusan video per jam dengan aman.

### Q4: Kenapa transkrip tidak akurat?

**A:** Jika video menggunakan auto-generated caption, akurasi tergantung kualitas audio dan清晰度发音. Untuk akurasi lebih baik, cari video dengan caption manual.

### Q5: Bisakah translate ke bahasa lain?

**A:** Script ini tidak melakukan translate. Gunakan tool terpisah untuk translate, atau manfaatkan fitur YouTube auto-translate yang bisa diakses via browser.

### Q6: Format mana yang terbaik?

**A:** 
- **Raw** → Untuk analisis teks, NLP, summarization
- **Timestamp** → Untuk navigasi, kutipan
- **SRT** → Untuk subtitle video
- **JSON** → Untuk processing programmatic

### Q7: Apakah bisa untuk YouTube Music?

**A:** Tidak, YouTube Music tidak menyediakan transcript. Hanya video YouTube regular.

### Q8: Bagaimana cara mengatasi IP block?

**A:**
1. Gunakan rotating residential proxy
2. Jalankan dari komputer lokal
3. Kurangi frekuensi request (tambah delay)
4. Gunakan VPN

---

## 12. CHANGELOG

### Versi 2.0 (Current)

**Fitur Baru:**
- ✨ Multi-video support
- ✨ Input dari file (`--file`)
- ✨ Auto-save per video
- ✨ Random delay anti-spam
- ✨ Summary report
- ✨ URL auto-extraction

**Perubahan:**
- 🔧 Attribute access (`entry.text`) instead of dict access (`entry['text']`)
- 🔧 Proper handling of `FetchedTranscript` object

### Versi 1.0 (Initial)

- ✅ Single video transcript
- ✅ Multiple output formats
- ✅ Proxy support
- ✅ Language selection

---

## 📞 SUPPORT

Jika menemukan bug atau butuh bantuan:
1. Baca ulang bagian Troubleshooting
2. Cek issue di GitHub repository `youtube-transcript-api`
3. Pastikan menggunakan versi terbaru

---

## 📄 LICENSE

Script ini menggunakan library `youtube-transcript-api` yang dilisensikan under MIT License.

---

**Happy Transcribing! 🎬📝**
