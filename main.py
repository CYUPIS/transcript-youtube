import argparse
import sys
import os
import re
import time
import random
from typing import Optional, List
from pathlib import Path

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.proxies import GenericProxyConfig
    from youtube_transcript_api._errors import (
        TranscriptsDisabled,
        NoTranscriptFound,
        VideoUnavailable,
        RequestBlocked,
        IpBlocked,
        CouldNotRetrieveTranscript,
    )
except ImportError:
    print("Error: youtube-transcript-api tidak terinstall!")
    print("Install dengan: pip install youtube-transcript-api")
    sys.exit(1)


# ============================================
# CONFIGURATION
# ============================================

# Delay default untuk menghindari spam detection (dalam detik)
DEFAULT_MIN_DELAY = 2
DEFAULT_MAX_DELAY = 5

# Ekstensi file berdasarkan format
FORMAT_EXTENSIONS = {
    "raw": ".txt",
    "timestamp": ".txt",
    "srt": ".srt",
    "json": ".json",
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_video_id(url_or_id: str) -> str:
    """
    Ekstrak video ID dari URL atau ID langsung.
    Support berbagai format URL YouTube.
    """
    url_or_id = url_or_id.strip()
    
    # Jika sudah 11 karakter dan hanya alphanumeric + _-, kemungkinan sudah ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # Pattern untuk berbagai format URL YouTube
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    # Jika tidak match, kembalikan as is (mungkin error nanti)
    return url_or_id


def random_delay(min_delay: float = DEFAULT_MIN_DELAY, max_delay: float = DEFAULT_MAX_DELAY):
    """
    Delay random untuk menghindari spam detection.
    """
    delay = random.uniform(min_delay, max_delay)
    print(f"  ⏳ Menunggu {delay:.1f} detik...", file=sys.stderr)
    time.sleep(delay)


def sanitize_filename(name: str) -> str:
    """
    Bersihkan nama file dari karakter tidak valid.
    """
    # Hapus karakter yang tidak valid untuk nama file
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    # Batas panjang nama file
    return name[:200]


# ============================================
# CORE FUNCTIONS
# ============================================

def get_transcript(
    video_id: str,
    languages: list = None,
    proxy_url: Optional[str] = None,
    preserve_formatting: bool = False,
):
    """
    Mengambil transkrip dari video YouTube.

    Args:
        video_id: ID video YouTube (contoh: ytYpQxHf078)
        languages: List bahasa prioritas (default: ['id', 'en'])
        proxy_url: URL proxy (contoh: http://user:pass@host:port)
        preserve_formatting: Pertahankan format HTML

    Returns:
        FetchedTranscript object (iterable, each entry has .text, .start, .duration)
    """
    if languages is None:
        languages = ['id', 'en']

    # Setup proxy jika ada
    proxy_config = None
    if proxy_url:
        proxy_config = GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )

    # Inisialisasi API
    ytt_api = YouTubeTranscriptApi(proxy_config=proxy_config)

    # Fetch transcript
    transcript = ytt_api.fetch(
        video_id,
        languages=languages,
        preserve_formatting=preserve_formatting
    )

    return transcript


def format_transcript_raw(transcript) -> str:
    """Format transkrip menjadi teks mentah (tanpa timestamp)."""
    return " ".join(entry.text for entry in transcript)


def format_transcript_with_timestamp(transcript) -> str:
    """Format transkrip dengan timestamp."""
    lines = []
    for entry in transcript:
        timestamp = format_seconds(entry.start)
        lines.append(f"[{timestamp}] {entry.text}")
    return "\n".join(lines)


def format_seconds(seconds: float) -> str:
    """Konversi detik ke format MM:SS atau HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_srt(transcript) -> str:
    """Format transkrip ke format SRT (subtitle)."""
    lines = []
    for i, entry in enumerate(transcript, 1):
        start_time = format_srt_time(entry.start)
        end_time = format_srt_time(entry.start + getattr(entry, "duration", 0))
        lines.append(f"{i}")
        lines.append(f"{start_time} --> {end_time}")
        lines.append(entry.text)
        lines.append("")
    return "\n".join(lines)


def format_srt_time(seconds: float) -> str:
    """Format waktu untuk SRT."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def process_transcript(transcript, output_format: str) -> str:
    """
    Format transcript sesuai format yang diminta.
    """
    if output_format == "raw":
        return format_transcript_raw(transcript)
    elif output_format == "timestamp":
        return format_transcript_with_timestamp(transcript)
    elif output_format == "srt":
        return format_srt(transcript)
    elif output_format == "json":
        import json
        transcript_data = [
            {"text": entry.text, "start": entry.start, "duration": getattr(entry, "duration", 0)}
            for entry in transcript
        ]
        return json.dumps(transcript_data, indent=2, ensure_ascii=False)
    return format_transcript_raw(transcript)


# ============================================
# MULTI-VIDEO PROCESSING
# ============================================

def process_single_video(
    video_id: str,
    languages: list,
    output_format: str,
    proxy_url: Optional[str] = None,
    output_file: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> dict:
    """
    Proses single video dan return result dict.
    """
    result = {
        "video_id": video_id,
        "success": False,
        "output_file": None,
        "error": None,
        "segments": 0,
    }
    
    try:
        # Ambil transcript
        transcript = get_transcript(
            video_id,
            languages=languages,
            proxy_url=proxy_url
        )
        
        result["segments"] = len(transcript)
        
        # Format output
        output = process_transcript(transcript, output_format)
        
        # Tentukan output file
        if output_file:
            result["output_file"] = output_file
            filepath = output_file
        elif output_dir:
            ext = FORMAT_EXTENSIONS.get(output_format, ".txt")
            filepath = os.path.join(output_dir, f"{video_id}{ext}")
            result["output_file"] = filepath
        else:
            result["output_file"] = None
            filepath = None
        
        # Tulis ke file atau stdout
        if filepath:
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            # Output ke stdout
            print(output)
        
        result["success"] = True
        
    except Exception as e:
        result["error"] = str(e)
    
    return result


def process_multiple_videos(
    video_ids: List[str],
    languages: list,
    output_format: str,
    proxy_url: Optional[str] = None,
    output_dir: Optional[str] = None,
    min_delay: float = DEFAULT_MIN_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
) -> List[dict]:
    """
    Proses multiple videos dengan delay anti-spam.
    Setiap video otomatis disimpan ke file terpisah.
    """
    results = []
    total = len(video_ids)
    
    # Jika tidak ada output_dir, buat folder default
    if not output_dir:
        output_dir = "./transcripts"
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"📋 Memproses {total} video", file=sys.stderr)
    print(f"📁 Output folder: {output_dir}", file=sys.stderr)
    print(f"⏱️  Delay: {min_delay}-{max_delay} detik antar request", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)
    
    for i, video_id in enumerate(video_ids, 1):
        video_id = extract_video_id(video_id)
        
        print(f"[{i}/{total}] Video: {video_id}", file=sys.stderr)
        
        result = process_single_video(
            video_id=video_id,
            languages=languages,
            output_format=output_format,
            proxy_url=proxy_url,
            output_dir=output_dir,
        )
        
        results.append(result)
        
        if result["success"]:
            print(f"  ✅ Berhasil! {result['segments']} segments → {result['output_file']}", file=sys.stderr)
        else:
            print(f"  ❌ Gagal: {result['error']}", file=sys.stderr)
        
        # Delay sebelum video berikutnya (kecuali video terakhir)
        if i < total:
            random_delay(min_delay, max_delay)
    
    return results


def print_summary(results: List[dict]):
    """
    Print ringkasan hasil processing.
    """
    success = sum(1 for r in results if r["success"])
    failed = len(results) - success
    
    print(f"\n{'='*60}", file=sys.stderr)
    print("📊 RINGKASAN", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print(f"  ✅ Berhasil: {success}", file=sys.stderr)
    print(f"  ❌ Gagal: {failed}", file=sys.stderr)
    
    if failed > 0:
        print("\n❌ Video yang gagal:", file=sys.stderr)
        for r in results:
            if not r["success"]:
                print(f"  - {r['video_id']}: {r['error'][:60]}...", file=sys.stderr)
    
    if success > 0:
        print("\n✅ File yang berhasil disimpan:", file=sys.stderr)
        for r in results:
            if r["success"] and r["output_file"]:
                print(f"  - {r['output_file']}", file=sys.stderr)
    
    print(f"{'='*60}\n", file=sys.stderr)


# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(
        description="Ambil transkrip dari video YouTube (support multi-video)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  # Single video
  %(prog)s ytYpQxHf078

  # Multiple video (auto delay & save terpisah)
  %(prog)s ytYpQxHf078 dQw4w9WgXcQ jNQXAC9IVRw

  # Dari file list
  %(prog)s --file videos.txt

  # Dengan format SRT
  %(prog)s ytYpQxHf078 --format srt --output-dir ./subtitles

  # Dengan custom delay
  %(prog)s ytYpQxHf078 dQw4w9WgXcQ --delay 5 10

  # Dengan proxy
  %(prog)s ytYpQxHf078 --proxy "http://user:pass@host:port"

  # List transcript yang tersedia
  %(prog)s ytYpQxHf078 --list
        """
    )

    parser.add_argument(
        "video_ids",
        nargs="*",
        help="ID atau URL video YouTube (bisa lebih dari satu)"
    )
    parser.add_argument(
        "-f", "--file",
        help="File berisi list video ID/URL (satu per baris)"
    )
    parser.add_argument(
        "-l", "--languages",
        nargs="+",
        default=["id", "en"],
        help="Bahasa prioritas (default: id en)"
    )
    parser.add_argument(
        "--format",
        choices=["raw", "timestamp", "srt", "json"],
        default="raw",
        help="Format output (default: raw)"
    )
    parser.add_argument(
        "-o", "--output",
        help="File output (hanya untuk single video)"
    )
    parser.add_argument(
        "-d", "--output-dir",
        help="Folder output untuk menyimpan file (auto untuk multi-video)"
    )
    parser.add_argument(
        "-p", "--proxy",
        help="URL proxy (contoh: http://user:pass@host:port)"
    )
    parser.add_argument(
        "--delay",
        nargs=2,
        type=float,
        metavar=("MIN", "MAX"),
        default=[DEFAULT_MIN_DELAY, DEFAULT_MAX_DELAY],
        help="Delay antar request dalam detik (default: 2 5)"
    )
    parser.add_argument(
        "--no-delay",
        action="store_true",
        help="Nonaktifkan delay (berisiko terkena spam detection)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List transcript yang tersedia"
    )

    args = parser.parse_args()

    # Validasi input
    video_ids = list(args.video_ids) if args.video_ids else []
    
    # Baca dari file jika ada
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                file_ids = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                video_ids.extend(file_ids)
        except FileNotFoundError:
            print(f"Error: File tidak ditemukan: {args.file}", file=sys.stderr)
            sys.exit(1)
    
    if not video_ids:
        parser.print_help()
        print("\nError: Masukkan minimal satu video ID atau gunakan --file", file=sys.stderr)
        sys.exit(1)

    # Extract video IDs dari URL
    video_ids = [extract_video_id(vid) for vid in video_ids]
    
    # Hapus duplikat sambil preserve order
    seen = set()
    video_ids = [x for x in video_ids if not (x in seen or seen.add(x))]

    # Setup delay
    min_delay, max_delay = args.delay if not args.no_delay else (0, 0)

    try:
        # Mode: List transcripts
        if args.list:
            ytt_api = YouTubeTranscriptApi()
            for video_id in video_ids:
                print(f"\nTranscript untuk video {video_id}:", file=sys.stderr)
                print("-" * 50)
                try:
                    transcript_list = ytt_api.list(video_id)
                    for t in transcript_list:
                        status = "Generated" if t.is_generated else "Manual"
                        print(f"  [{t.language_code}] {t.language} ({status})")
                except Exception as e:
                    print(f"  Error: {e}")
            return

        # Mode: Single video
        if len(video_ids) == 1:
            result = process_single_video(
                video_id=video_ids[0],
                languages=args.languages,
                output_format=args.format,
                proxy_url=args.proxy,
                output_file=args.output,
                output_dir=args.output_dir,
            )
            
            if result["success"]:
                print(f"\n✅ Berhasil! {result['segments']} segments", file=sys.stderr)
                if result["output_file"]:
                    print(f"📁 File: {result['output_file']}", file=sys.stderr)
            else:
                print(f"\n❌ Error: {result['error']}", file=sys.stderr)
                sys.exit(1)

        # Mode: Multiple videos
        else:
            # Override output_dir jika tidak diset
            output_dir = args.output_dir or "./transcripts"
            
            results = process_multiple_videos(
                video_ids=video_ids,
                languages=args.languages,
                output_format=args.format,
                proxy_url=args.proxy,
                output_dir=output_dir,
                min_delay=min_delay,
                max_delay=max_delay,
            )
            
            print_summary(results)
            
            # Exit dengan error code jika ada yang gagal
            if any(not r["success"] for r in results):
                sys.exit(1)

    except RequestBlocked:
        print(f"\n❌ Error: YouTube memblokir request dari IP ini.", file=sys.stderr)
        print("Solusi:", file=sys.stderr)
        print("  1. Gunakan proxy: --proxy 'http://user:pass@host:port'", file=sys.stderr)
        print("  2. Jalankan script dari komputer lokal (bukan server cloud)", file=sys.stderr)
        sys.exit(1)

    except IpBlocked:
        print(f"\n❌ Error: IP diblokir oleh YouTube.", file=sys.stderr)
        print("Solusi: Gunakan rotating residential proxy.", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print(f"\n\n⚠️ Dibatalkan oleh user.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
