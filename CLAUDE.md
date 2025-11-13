# Claude Code Instructions for DJ Set Song Recognizer

This document provides instructions for Claude Code (or any AI assistant) on how to help users recognize songs in DJ sets from YouTube videos.

## Overview

This tool identifies all songs in a DJ mix or set using Shazam's music recognition API. It processes long audio files by sampling them at regular intervals and creates timestamped tracklists.

## Prerequisites Check

Before starting, verify the user has:

1. **Python 3.11 or 3.12** (NOT 3.14 due to pydub compatibility)
   ```bash
   python3.11 --version
   ```

2. **ffmpeg** for audio processing
   ```bash
   ffmpeg -version
   ```

3. **yt-dlp** for downloading YouTube videos
   ```bash
   yt-dlp --version
   ```

## Installation Steps

### macOS
```bash
brew install python@3.11 ffmpeg yt-dlp
python3.11 -m pip install --user shazamio
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3-pip ffmpeg
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
python3.11 -m pip install --user shazamio
```

### Windows
1. Install Python 3.11 from python.org
2. Install ffmpeg from https://www.gyan.dev/ffmpeg/builds/
3. Install yt-dlp from GitHub releases
4. Run: `python -m pip install shazamio`

## Usage Workflow

### Step 1: Download Repository
```bash
git clone https://github.com/YOUR_USERNAME/dj-set-song-recognizer.git
cd dj-set-song-recognizer
```

### Step 2: Download YouTube Video
```bash
./download_youtube.sh 'https://www.youtube.com/watch?v=VIDEO_ID' output_name
```

### Step 3: Recognize Songs
```bash
python3.11 recognize_dj_set.py audio_file.mp3 [scan_interval_seconds]
```

**Examples:**
```bash
# Default scanning (every 30 seconds)
python3.11 recognize_dj_set.py my_set.mp3

# Fast scanning (every 15 seconds)
python3.11 recognize_dj_set.py my_set.mp3 15

# Slow scanning (every 60 seconds)
python3.11 recognize_dj_set.py my_set.mp3 60
```

## Common Issues and Solutions

### Issue 1: Python 3.14 Compatibility Error
**Error:** `ModuleNotFoundError: No module named 'audioop'`

**Solution:** Use Python 3.11 or 3.12
```bash
python3.11 recognize_dj_set.py audio_file.mp3
```

### Issue 2: No Songs Recognized
**Possible causes:**
- Audio quality is too low
- Songs are obscure/not in Shazam database
- Scanning interval is too long
- Heavy DJ transitions/effects

**Solutions:**
- Decrease scan interval: `python3.11 recognize_dj_set.py file.mp3 15`
- Try different sections of the mix manually
- Ensure audio file is not corrupted

### Issue 3: Rate Limiting
**Error:** Too many requests to Shazam

**Solution:** The tool already includes 3-second delays. For longer sets, consider:
- Increasing scan interval: `python3.11 recognize_dj_set.py file.mp3 45`
- Running the scan during off-peak hours

### Issue 4: Missing Dependencies
```bash
# Reinstall all dependencies
python3.11 -m pip install --user --upgrade shazamio
brew reinstall ffmpeg yt-dlp  # macOS
```

## Output Files

The tool generates two files:

1. **`*_results.json`** - Raw data with full API responses
2. **`*_tracklist.txt`** - Human-readable tracklist with timestamps

## How It Works

1. **Audio Loading**: Loads the MP3 file and gets its duration
2. **Chunking**: Extracts 12-second samples at regular intervals using ffmpeg
3. **Recognition**: Sends each chunk to Shazam API via shazamio library
4. **Processing**: Collects all results with timestamps
5. **Deduplication**: Removes consecutive duplicates (same song playing)
6. **Output**: Saves both JSON and formatted text tracklists

## Performance Considerations

### Scan Interval Selection

| Interval | Speed | Accuracy | Use Case |
|----------|-------|----------|----------|
| 15-20s   | Fast  | Good     | Quick preview, fast-paced mixes |
| 30s      | Balanced | Better | Default, most DJ sets |
| 45-60s   | Slow  | Lower    | Long sets, API conservation |

### Time Estimates

For a 90-minute DJ set:
- 15s interval: ~30 minutes (360 scans)
- 30s interval: ~15 minutes (180 scans)
- 60s interval: ~8 minutes (90 scans)

## Advanced Usage

### Process Multiple Files
```bash
for file in *.mp3; do
    python3.11 recognize_dj_set.py "$file" 30
done
```

### Extract Specific Time Range
```bash
# Extract 10 minutes starting at 30:00
ffmpeg -i full_set.mp3 -ss 00:30:00 -t 00:10:00 excerpt.mp3
python3.11 recognize_dj_set.py excerpt.mp3
```

### Batch Download and Process
```bash
# Create a file with YouTube URLs (one per line)
cat urls.txt | while read url; do
    ./download_youtube.sh "$url"
    python3.11 recognize_dj_set.py dj_set_*.mp3
done
```

## API Information

- **Shazam API**: Free, but rate-limited to ~20 requests per minute
- **No API Key Required**: shazamio uses Shazam's public endpoints
- **Recognition Accuracy**: ~80-90% for well-mixed electronic music

## Code Structure

### `recognize_dj_set.py`
Main script containing:
- `get_audio_duration()`: Uses ffprobe to get audio length
- `extract_audio_chunk()`: Uses ffmpeg to extract samples
- `recognize_chunk()`: Sends audio to Shazam API
- `format_timestamp()`: Converts seconds to readable format
- `recognize_dj_set()`: Main processing loop
- `save_results()`: Generates output files
- `display_results()`: Console output

### `download_youtube.sh`
Simple wrapper for yt-dlp with:
- Audio-only download
- MP3 conversion
- Custom naming
- Error handling

## Troubleshooting Decision Tree

```
No output at all?
├─ Check Python version (must be 3.11 or 3.12)
└─ Verify all dependencies installed

Some songs not detected?
├─ Reduce scan interval (try 15-20 seconds)
└─ Check if songs are in Shazam database (try manually with phone app)

Process too slow?
├─ Increase scan interval (try 45-60 seconds)
└─ Consider running overnight for very long sets

API errors?
├─ Check internet connection
├─ Wait a few minutes (rate limiting)
└─ Try with a shorter test file first
```

## Tips for Best Results

1. **Start with default settings** (30-second interval)
2. **Test on a 5-minute excerpt first** before processing a full 2-hour set
3. **Use higher scan frequency for fast-paced sets** (trap, drum & bass)
4. **Use lower scan frequency for melodic sets** (house, techno)
5. **Cross-reference results** with Shazam mobile app if unsure
6. **Save the JSON output** for later reprocessing

## Extending the Tool

### Add Spotify Integration
```python
# After song recognition, search Spotify API
import spotipy
# ... implementation
```

### Add Beatport Integration
```python
# Search for tracks on Beatport
# Useful for DJ sets
```

### Export to Rekordbox XML
```python
# Convert tracklist to Rekordbox playlist format
# See Rekordbox CLI tools
```

## Contributing

When adding features:
1. Maintain Python 3.11 compatibility
2. Add error handling for all external calls
3. Update README and CLAUDE.md
4. Test with various audio file formats
5. Consider rate limiting implications

## Resources

- [Shazamio Documentation](https://github.com/shazamio/ShazamIO)
- [yt-dlp Documentation](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [Shazam API Unofficial Docs](https://github.com/AudDMusic/audd-go)

## Support Checklist

When helping a user:
- ✅ Verify Python version is 3.11 or 3.12
- ✅ Confirm ffmpeg and yt-dlp are installed
- ✅ Test with a short audio clip first
- ✅ Check internet connection for API calls
- ✅ Explain scan interval trade-offs
- ✅ Show how to interpret output files
- ✅ Suggest rate limiting if processing fails

---

**Last Updated**: 2025-01-13
**Compatible With**: Python 3.11, 3.12 (NOT 3.14)
