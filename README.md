# 🎵 DJ Set Song Recognizer

Automatically identify all songs in a DJ mix or set from YouTube videos using Shazam's music recognition API.

Perfect for:
- Creating tracklists for DJ sets
- Identifying songs in long mixes
- Music discovery from YouTube DJ performances
- Archiving setlists with timestamps

## ✨ Features

- 🎯 **Accurate Song Recognition** - Uses Shazam's powerful music recognition API
- ⏱️ **Timestamped Tracklists** - Every song identified with its exact start time
- 📝 **Multiple Output Formats** - JSON for data processing, TXT for human reading
- 🚀 **Easy to Use** - Simple command-line interface
- 🎬 **YouTube Integration** - Download audio directly from YouTube videos
- 🔄 **Configurable Scanning** - Adjust scan frequency for speed vs. accuracy

## 📋 Prerequisites

- **Python 3.11+** (Python 3.14 has compatibility issues with pydub)
- **ffmpeg** - For audio processing
- **yt-dlp** - For downloading YouTube videos

## 🚀 Quick Start

### 1. Install Dependencies

**macOS:**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required tools
brew install python@3.11 ffmpeg yt-dlp

# Install Python packages
python3.11 -m pip install --user shazamio
```

**Linux (Ubuntu/Debian):**
```bash
# Install required tools
sudo apt update
sudo apt install python3.11 python3-pip ffmpeg

# Install yt-dlp
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Install Python packages
python3.11 -m pip install --user shazamio
```

**Windows:**
```powershell
# Install Python 3.11 from https://www.python.org/downloads/
# Install ffmpeg from https://www.gyan.dev/ffmpeg/builds/
# Install yt-dlp from https://github.com/yt-dlp/yt-dlp/releases

# Install Python packages
python -m pip install shazamio
```

### 2. Download the Tool

```bash
git clone https://github.com/YOUR_USERNAME/dj-set-song-recognizer.git
cd dj-set-song-recognizer
```

### 3. Download a DJ Set from YouTube

```bash
./download_youtube.sh 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'
```

Or with a custom output name:
```bash
./download_youtube.sh 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID' my_favorite_set
```

### 4. Recognize Songs

```bash
python3.11 recognize_dj_set.py dj_set_YOUR_VIDEO_ID.mp3
```

**Customize scan frequency:**
```bash
# Scan every 20 seconds (faster but might miss some songs)
python3.11 recognize_dj_set.py dj_set_YOUR_VIDEO_ID.mp3 20

# Scan every 45 seconds (slower but saves API calls)
python3.11 recognize_dj_set.py dj_set_YOUR_VIDEO_ID.mp3 45
```

## 📊 Output Files

The tool generates two output files:

### 1. JSON Results (`*_results.json`)
Complete data including:
- Song title and artist
- Timestamp of each detection
- Album information
- Shazam URL
- Full Shazam API response

### 2. Human-Readable Tracklist (`*_tracklist.txt`)
Clean, formatted tracklist with:
- Track numbers
- Timestamps in MM:SS or HH:MM:SS format
- Artist and song names
- Album information (when available)
- Shazam links

Example output:
```
================================================================================
DJ SET TRACKLIST
================================================================================

 1. [05:00] Rex the Dog - Hold It / Control It
    Shazam: https://www.shazam.com/track/12345678

 2. [14:00] Rex the Dog - Vortex
    Shazam: https://www.shazam.com/track/87654321

 3. [23:30] Donna Summer - Bad Girls (Gigamesh Remix)
    Shazam: https://www.shazam.com/track/11223344

================================================================================
Total unique tracks identified: 30
Total scans performed: 174
================================================================================
```

## 🎛️ How It Works

1. **Audio Extraction**: Downloads or loads the audio file
2. **Chunking**: Splits the audio into 12-second samples at regular intervals
3. **Recognition**: Sends each chunk to Shazam's recognition API
4. **Deduplication**: Removes duplicate detections of the same song
5. **Output**: Generates timestamped tracklist files

## ⚙️ Configuration

### Scan Interval
- **Default**: 30 seconds (balanced speed and accuracy)
- **Fast**: 15-20 seconds (faster but may miss songs during transitions)
- **Thorough**: 45-60 seconds (slower but fewer API calls)

### Rate Limits
- Shazam API: ~20 requests per minute
- The tool automatically adds 3-second delays between requests

## 📝 Example Workflow

```bash
# 1. Download a Boiler Room set
./download_youtube.sh 'https://www.youtube.com/watch?v=93ZGx5wjRdo' boiler_room_set

# 2. Recognize songs (scan every 30 seconds)
python3.11 recognize_dj_set.py boiler_room_set.mp3

# 3. View the tracklist
cat boiler_room_set_tracklist.txt

# 4. Process the JSON data (optional)
python3 -m json.tool boiler_room_set_results.json
```

## 🐛 Troubleshooting

### Python Version Issues
```bash
# Check your Python version
python3.11 --version

# If python3.11 is not found, install it:
brew install python@3.11  # macOS
sudo apt install python3.11  # Linux
```

### Missing Dependencies
```bash
# Reinstall Python packages
python3.11 -m pip install --user --upgrade shazamio

# Check if ffmpeg is installed
ffmpeg -version

# Check if yt-dlp is installed
yt-dlp --version
```

### No Songs Recognized
- Try scanning more frequently (e.g., every 15 seconds)
- Ensure the audio quality is good
- Some songs might not be in Shazam's database
- DJ transitions can make recognition difficult

### Python 3.14 Compatibility
If you get `ModuleNotFoundError: No module named 'audioop'`, use Python 3.11 or 3.12:
```bash
python3.11 recognize_dj_set.py your_file.mp3
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

MIT License - feel free to use this tool for any purpose.

## 🙏 Acknowledgments

- [Shazamio](https://github.com/shazamio/ShazamIO) - Python library for Shazam API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Audio processing

## ⚠️ Disclaimer

This tool is for personal use only. Please respect copyright laws and the terms of service of YouTube and Shazam. Do not use this tool to infringe on the rights of content creators.

## 📧 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/YOUR_USERNAME/dj-set-song-recognizer/issues) on GitHub.

---

**Made with ❤️ for music lovers and DJ enthusiasts**
