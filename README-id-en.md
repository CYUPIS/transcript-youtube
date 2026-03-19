# 📖 YouTube Transcript Automation

A powerful Python script to automatically extract transcripts from YouTube videos. Support for single and batch processing with anti-spam protection.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✅ **Single Video** | Extract transcript from one video |
| ✅ **Multi-Video** | Process multiple videos at once |
| ✅ **Auto-Save** | Automatically save each video to separate file |
| ✅ **Anti-Spam** | Random delay to avoid being blocked |
| ✅ **Multiple Formats** | Raw, Timestamp, SRT, JSON |
| ✅ **URL Support** | Paste full URL, auto-extract video ID |
| ✅ **File Input** | Read video list from file |
| ✅ **Proxy Support** | Use proxy to bypass IP blocks |
| ✅ **Multi-Language** | Customizable language priority |

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Usage Examples](#usage-examples)
4. [Output Formats](#output-formats)
5. [Multi-Video Processing](#multi-video-processing)
6. [Configuration](#configuration)
7. [Proxy Setup](#proxy-setup)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)
10. [Contributing](#contributing)

---

## 📦 Installation

### Requirements

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install youtube-transcript-api
```

### Download Script

```bash
# Clone the repository
git clone https://github.com/yourusername/youtube-transcript-automation.git

# Or download the script directly
curl -O https://raw.githubusercontent.com/yourusername/youtube-transcript-automation/main/youtube_transcript_automation.py
```

### Verify Installation

```bash
python youtube_transcript_automation.py --help
```

---

## 🚀 Quick Start

### Extract Single Video Transcript

```bash
# Basic usage - outputs to terminal
python youtube_transcript_automation.py ytYpQxHf078

# Save to file
python youtube_transcript_automation.py ytYpQxHf078 -o transcript.txt
```

### Extract Multiple Videos

```bash
# Process multiple videos with auto-save
python youtube_transcript_automation.py video1 video2 video3 --output-dir ./transcripts
```

### Check Available Languages

```bash
python youtube_transcript_automation.py ytYpQxHf078 --list
```

---

## 📖 Usage Examples

### Basic Commands

```bash
# Using video ID
python youtube_transcript_automation.py ytYpQxHf078

# Using full YouTube URL (auto-extracts ID)
python youtube_transcript_automation.py https://www.youtube.com/watch?v=ytYpQxHf078

# Using short URL
python youtube_transcript_automation.py https://youtu.be/ytYpQxHf078

# Using YouTube Shorts URL
python youtube_transcript_automation.py https://www.youtube.com/shorts/ytYpQxHf078
```

### Language Selection

```bash
# Default: Indonesian → English
python youtube_transcript_automation.py ytYpQxHf078

# Custom priority: Japanese → English
python youtube_transcript_automation.py ytYpQxHf078 -l ja en

# Multiple languages: Javanese → Indonesian → English
python youtube_transcript_automation.py ytYpQxHf078 -l jv id en
```

### Save to File

```bash
# Single video
python youtube_transcript_automation.py ytYpQxHf078 -o my_transcript.txt

# Multiple videos with custom folder
python youtube_transcript_automation.py video1 video2 video3 --output-dir ./my_transcripts
```

### From File Input

```bash
# Create a list file
cat > videos.txt << EOF
# This is a comment (ignored)
ytYpQxHf078
https://www.youtube.com/watch?v=dQw4w9WgXcQ
jNQXAC9IVRw
EOF

# Process the list
python youtube_transcript_automation.py --file videos.txt
```

---

## 📄 Output Formats

### 1. Raw Format (Default)

Plain text without timestamps:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format raw
```

**Output:**
```
Welcome to Malaka Podcast. Here with Kania Cita and Feri Irwandi as hosts. And we have Mr. Tom Lembong for the second time...
```

### 2. Timestamp Format

Text with timestamps for easy navigation:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format timestamp
```

**Output:**
```
[00:00] Welcome to Malaka Podcast.
[00:05] Here with Kania Cita and Feri Irwandi as hosts.
[00:12] And we have Mr. Tom Lembong for the second time.
```

### 3. SRT Format (Subtitles)

Standard subtitle format for video players:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format srt -o video.srt
```

**Output:**
```
1
00:00:00,000 --> 00:00:05,000
Welcome to Malaka Podcast.

2
00:00:05,000 --> 00:00:12,000
Here with Kania Cita and Feri Irwandi as hosts.

3
00:00:12,000 --> 00:00:18,000
And we have Mr. Tom Lembong for the second time.
```

### 4. JSON Format

Structured data for programmatic processing:

```bash
python youtube_transcript_automation.py ytYpQxHf078 --format json
```

**Output:**
```json
[
  {
    "text": "Welcome to Malaka Podcast.",
    "start": 0.0,
    "duration": 5.0
  },
  {
    "text": "Here with Kania Cita and Feri Irwandi as hosts.",
    "start": 5.0,
    "duration": 7.0
  }
]
```

---

## 🔄 Multi-Video Processing

### Basic Multi-Video

```bash
python youtube_transcript_automation.py ytYpQxHf078 dQw4w9WgXcQ jNQXAC9IVRw
```

### Output Structure

Each video is automatically saved to a separate file:

```
./transcripts/
├── ytYpQxHf078.txt
├── dQw4w9WgXcQ.txt
└── jNQXAC9IVRw.txt
```

### File Naming Convention

| Format | Extension | Example |
|--------|-----------|---------|
| raw | `.txt` | `ytYpQxHf078.txt` |
| timestamp | `.txt` | `ytYpQxHf078.txt` |
| srt | `.srt` | `ytYpQxHf078.srt` |
| json | `.json` | `ytYpQxHf078.json` |

### Sample Output

```
============================================================
📋 Processing 3 videos
📁 Output folder: ./transcripts
⏱️  Delay: 2-5 seconds between requests
============================================================

[1/3] Video: ytYpQxHf078
  ⏳ Waiting 3.2 seconds...
  ✅ Success! 847 segments → ./transcripts/ytYpQxHf078.txt

[2/3] Video: dQw4w9WgXcQ
  ⏳ Waiting 4.1 seconds...
  ✅ Success! 156 segments → ./transcripts/dQw4w9WgXcQ.txt

[3/3] Video: jNQXAC9IVRw
  ✅ Success! 12 segments → ./transcripts/jNQXAC9IVRw.txt

============================================================
📊 SUMMARY
============================================================
  ✅ Success: 3
  ❌ Failed: 0

✅ Files saved:
  - ./transcripts/ytYpQxHf078.txt
  - ./transcripts/dQw4w9WgXcQ.txt
  - ./transcripts/jNQXAC9IVRw.txt
============================================================
```

---

## ⚙️ Configuration

### Delay Settings

Anti-spam delay between requests:

```bash
# Default: 2-5 seconds random delay
python youtube_transcript_automation.py video1 video2

# Custom delay: 3-8 seconds
python youtube_transcript_automation.py video1 video2 --delay 3 8

# More conservative: 5-10 seconds
python youtube_transcript_automation.py video1 video2 --delay 5 10

# Disable delay (NOT RECOMMENDED - risk of being blocked)
python youtube_transcript_automation.py video1 video2 --no-delay
```

### Recommended Delays

| Number of Videos | Delay | Risk Level |
|------------------|-------|------------|
| 1-10 | 2-5 sec | Low |
| 10-50 | 3-7 sec | Low |
| 50-100 | 5-10 sec | Very Low |
| 100+ | 8-15 sec | Minimal |

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `video_ids` | - | Video IDs or URLs (space-separated) | - |
| `--file` | `-f` | File containing video list | - |
| `--languages` | `-l` | Language priority | `id en` |
| `--format` | - | Output format | `raw` |
| `--output` | `-o` | Output file (single video) | stdout |
| `--output-dir` | `-d` | Output folder (multi-video) | `./transcripts` |
| `--proxy` | `-p` | Proxy URL | - |
| `--delay` | - | Min/max delay in seconds | `2 5` |
| `--no-delay` | - | Disable anti-spam delay | - |
| `--list` | - | List available transcripts | - |

---

## 🌐 Proxy Setup

### When to Use Proxy

- Your IP is blocked by YouTube
- Running from cloud servers (AWS, GCP, Azure, etc.)
- Processing large batches of videos

### Proxy Format

```
http://username:password@host:port
```

### Usage Examples

```bash
# HTTP Proxy
python youtube_transcript_automation.py ytYpQxHf078 --proxy "http://user:pass@proxy.example.com:8080"

# SOCKS5 Proxy
python youtube_transcript_automation.py ytYpQxHf078 --proxy "socks5://user:pass@proxy.example.com:1080"

# With authentication
python youtube_transcript_automation.py video1 video2 --proxy "http://username:password@192.168.1.1:3128"
```

### Recommended Proxy Services

| Service | Type | Best For |
|---------|------|----------|
| **Webshare** | Rotating Residential | Most reliable |
| **Bright Data** | Residential | Enterprise use |
| **Smartproxy** | Mixed | Balance price/quality |
| **Oxylabs** | Premium | Large scale |

---

## 🔧 Troubleshooting

### Error: "Request blocked by YouTube"

**Cause:** Your IP is blocked or you're using a cloud server.

**Solutions:**
1. Use proxy: `--proxy "http://..."`
2. Run from local computer instead of cloud server
3. Wait a few hours and try again

### Error: "IP blocked"

**Cause:** Your IP has been permanently blocked.

**Solutions:**
1. Use rotating residential proxy
2. Change your IP (restart router if dynamic)
3. Use VPN

### Error: "Transcripts disabled"

**Cause:** Video has no subtitles/captions.

**Solution:** No solution - this video doesn't provide transcripts.

### Error: "No transcript found"

**Cause:** No transcript available in requested language.

**Solutions:**
```bash
# Check available languages
python youtube_transcript_automation.py VIDEO_ID --list

# Use available language
python youtube_transcript_automation.py VIDEO_ID -l en
```

### Error: "Video unavailable"

**Cause:** Video is private, deleted, or blocked in your region.

**Solutions:**
- Use proxy from different region
- Video may not be accessible

### Empty Output

**Cause:** Language mismatch or video has no speech.

**Solutions:**
```bash
# Check available languages
python youtube_transcript_automation.py VIDEO_ID --list
```

---

## ❓ FAQ

### Q1: Is this legal?

**A:** Absolutly legal. This script only accesses publicly available subtitles/captions on YouTube. It's equivalent to clicking "Show transcript" on the YouTube website.

### Q2: Can I use this for private videos?

**A:** No. Only public videos with available transcripts can be processed.

### Q3: Are there rate limits?

**A:** YouTube doesn't publish exact limits. With 2-5 second delays, you can safely process hundreds of videos per hour.

### Q4: Why are transcripts inaccurate?

**A:** If the video uses auto-generated captions, accuracy depends on audio quality and speaker clarity. For better accuracy, look for videos with manually created captions.

### Q5: Can I translate transcripts?

**A:** This script doesn't perform translation. Use a separate translation tool, or use YouTube's auto-translate feature in the browser.

### Q6: Which format is best?

**A:**
- **Raw** → Text analysis, NLP, summarization
- **Timestamp** → Navigation, citations
- **SRT** → Video subtitles
- **JSON** → Programmatic processing

### Q7: Does it work with YouTube Music?

**A:** No. YouTube Music doesn't provide transcripts. Only regular YouTube videos.

### Q8: How do I handle IP blocks?

**A:**
1. Use rotating residential proxy
2. Run from local computer
3. Reduce request frequency (increase delay)
4. Use VPN

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/youtube-transcript-automation.git
cd youtube-transcript-automation

# Install dependencies
pip install youtube-transcript-api

# Make your changes and test
python youtube_transcript_automation.py --help
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This script uses the `youtube-transcript-api` library which is also licensed under the MIT License.

---

## 🙏 Acknowledgments

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - The core library that makes this possible

---

## 📊 Project Stats

- **Version:** 2.0
- **Python Support:** 3.7+
- **Output Formats:** 4 (Raw, Timestamp, SRT, JSON)
- **Languages Supported:** All YouTube supported languages

---

**Happy Transcribing! 🎬📝**
