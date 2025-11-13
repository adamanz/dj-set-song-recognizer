# Rekordbox & CDJ-2000 USB Setup Guide

Once you've identified songs in a DJ set, you'll want to download high-quality versions and prepare them for your CDJ-2000. This guide covers everything you need.

## Table of Contents
1. [Where to Download High-Quality Music](#where-to-download-high-quality-music)
2. [Rekordbox Setup](#rekordbox-setup)
3. [Preparing USB for CDJ-2000](#preparing-usb-for-cdj-2000)
4. [Rekordbox CLI Tools](#rekordbox-cli-tools)
5. [Automated Workflows](#automated-workflows)

---

## Where to Download High-Quality Music

### 🏆 Top Platforms for Professional DJs

#### **1. Beatport** ⭐ #1 for Electronic Music
- **Website:** https://www.beatport.com/
- **Formats:** WAV (lossless), AIFF, MP3 320kbps
- **Best for:** Electronic, House, Techno, Trance
- **Price:** ~$1.50-$2.50 per track
- **Pros:** Largest electronic catalog, best metadata, BPM/key info
- **Streaming:** Beatport Professional Streaming available (FLAC)

#### **2. Traxsource**
- **Website:** https://www.traxsource.com/
- **Formats:** WAV, AIFF, MP3 320kbps
- **Best for:** House, Deep House, Soulful House
- **Price:** ~$1.49-$2.49 per track
- **Pros:** Excellent house music selection, high quality

#### **3. Juno Download**
- **Website:** https://www.junodownload.com/
- **Formats:** WAV, FLAC, AIFF, MP3 320kbps
- **Best for:** All electronic genres, vinyl also available
- **Price:** ~$1.50-$2.50 per track
- **Pros:** Huge catalog, competitive prices

#### **4. Bandcamp**
- **Website:** https://bandcamp.com/
- **Formats:** FLAC, WAV, AIFF, MP3 320kbps, more
- **Best for:** Independent artists, underground music
- **Price:** Artist-set pricing (often $1-$7 per track)
- **Pros:** Supports artists directly, often includes album art

### 🎵 DJ Record Pools (Subscription Services)

**Best Value for Working DJs:**

#### **1. BPM Supreme**
- **Price:** ~$19.99/month
- **Downloads:** Unlimited
- **Best for:** Open format, Top 40, Hip-Hop, EDM

#### **2. DJcity**
- **Price:** ~$45/month
- **Downloads:** Unlimited
- **Best for:** Club DJs, Top 40, remixes

#### **3. ZipDJ**
- **Price:** ~$15-40/month
- **Downloads:** 200-1000 per month
- **Best for:** Mobile DJs, multi-genre

### 💎 Lossless/Hi-Res Options

#### **7digital**
- **Website:** https://www.7digital.com/
- **Formats:** FLAC, MP3 320kbps
- **Best for:** Popular music, not DJ-focused

#### **Qobuz**
- **Website:** https://www.qobuz.com/
- **Formats:** Up to 24-bit/192kHz FLAC
- **Best for:** Audiophile quality

### 📊 Format Recommendations for CDJ-2000

| Format | Quality | File Size | Recommended? |
|--------|---------|-----------|--------------|
| **WAV** | Lossless | Large (~50MB/track) | ✅ **Best** |
| **AIFF** | Lossless | Large (~50MB/track) | ✅ **Best** |
| **FLAC** | Lossless | Medium (~30MB/track) | ✅ Good (not all CDJs) |
| **MP3 320kbps** | Lossy | Small (~8MB/track) | ✅ Acceptable |
| **MP3 256kbps** | Lossy | Small (~6MB/track) | ⚠️ OK for practice |
| **MP3 128kbps** | Lossy | Small (~3MB/track) | ❌ Avoid |

**For CDJ-2000:** WAV or AIFF preferred, MP3 320kbps minimum for gigs.

---

## Rekordbox Setup

### Installation

1. **Download Rekordbox**
   - Free version: https://rekordbox.com/en/download/
   - Supports CDJ-2000 without subscription

2. **Import Your Music**
   ```
   File > Import Music > Select folders containing your downloaded tracks
   ```

3. **Analyze Tracks**
   - Right-click tracks → Analyze
   - Rekordbox will detect BPM, key, and create waveforms
   - **Essential for beatgrid and hot cues**

### Organizing Your Library

1. **Create Playlists**
   - Click "+" under Playlists
   - Organize by genre, energy level, or gig
   - Example: "High Energy Techno", "Warm-Up House"

2. **Tag Your Tracks**
   - Add ratings (1-5 stars)
   - Use My Tags for custom organization
   - Add comments (e.g., "Works well with Track X")

3. **Set Cue Points & Hot Cues**
   - Essential for performance
   - Set Memory Cues at intro/outro points
   - Set Hot Cues for drops, breaks, vocal sections

---

## Preparing USB for CDJ-2000

### USB Requirements

- **Format:** FAT32 or exFAT
- **Size:** 32GB+ recommended
- **Speed:** USB 3.0 for faster loading
- **Structure:** Rekordbox creates proper folder structure

### Step-by-Step Export Process

#### 1. Format USB Drive (if new)

**macOS:**
```bash
# Insert USB, then:
diskutil list  # Find your USB (usually disk2)
sudo diskutil eraseDisk FAT32 REKORDBOX /dev/diskX
```

**Windows:**
- Right-click USB drive → Format
- File System: exFAT (for files >4GB) or FAT32
- Volume Label: REKORDBOX

#### 2. Export from Rekordbox

1. Insert USB drive
2. Device appears in Rekordbox sidebar
3. **Drag playlists** to your USB device
4. Rekordbox copies tracks and creates database
5. Wait for "Export Complete" message

**⚠️ Important:**
- **Don't manually copy files** - use Rekordbox export
- **Don't edit files on USB** - always re-export from Rekordbox
- **Safely eject** before unplugging

#### 3. Verify on CDJ-2000

1. Insert USB into CDJ
2. Press "MENU/UTILITY"
3. Navigate to "Link"
4. Your playlists should appear
5. Browse and load tracks to test

### USB Best Practices

✅ **DO:**
- Keep master library on computer
- Export specific playlists for each gig
- Have backup USB with same content
- Regularly update and re-export
- Keep USB in protective case

❌ **DON'T:**
- Drag files directly to USB in Finder/Explorer
- Edit track tags on USB
- Use USB without proper Rekordbox export
- Forget to eject safely
- Share USB without cleaning (can spread corruption)

---

## Rekordbox CLI Tools

### Python Libraries for Rekordbox

#### **1. pyrekordbox** ⭐ Recommended
```bash
# Install
pip install pyrekordbox

# Basic usage
from pyrekordbox import Rekordbox6Database

db = Rekordbox6Database()
tracks = db.get_tracks()

for track in tracks:
    print(f"{track.Title} - {track.Artist}")
    print(f"BPM: {track.Tempo}, Key: {track.Key}")
```

**GitHub:** https://github.com/dylanljones/pyrekordbox

#### **2. rbox**
```bash
pip install rbox
```
Minimal library for reading Rekordbox settings.

### Rekordbox XML Export

Rekordbox can export library as XML for scripting:

```python
import xml.etree.ElementTree as ET

tree = ET.parse('rekordbox.xml')
root = tree.getroot()

for track in root.findall('.//TRACK'):
    title = track.get('Name')
    artist = track.get('Artist')
    location = track.get('Location')
    print(f"{artist} - {title}")
    print(f"File: {location}")
```

**Export XML:**
1. Rekordbox → File → Export Collection
2. Choose XML format
3. Save to desired location

### Automated Workflow: Tracklist to USB

Here's a Python script to automate finding and adding recognized songs to Rekordbox:

```python
#!/usr/bin/env python3
"""
Auto-add tracks from DJ set tracklist to Rekordbox playlist
"""
import json
import os
from pathlib import Path

def create_search_list(tracklist_json):
    """Create search list from recognized songs"""
    with open(tracklist_json, 'r') as f:
        results = json.load(f)

    search_list = []
    for item in results:
        artist = item['artist']
        title = item['title']
        search_list.append(f"{artist} - {title}")

    return search_list

def export_search_list(search_list, output_file):
    """Export as text file for manual searching"""
    with open(output_file, 'w') as f:
        f.write("# DJ Set Tracklist for Download\n")
        f.write("# Search these tracks on Beatport/Traxsource\n\n")
        for i, track in enumerate(search_list, 1):
            f.write(f"{i}. {track}\n")

    print(f"Search list saved to: {output_file}")

def main():
    tracklist = "dj_set_shazam_results.json"
    output = "tracks_to_download.txt"

    search_list = create_search_list(tracklist)
    export_search_list(search_list, output)

    # Remove duplicates
    unique_tracks = list(dict.fromkeys(search_list))

    print(f"\nTotal unique tracks to search: {len(unique_tracks)}")
    print("\nNext steps:")
    print("1. Open tracks_to_download.txt")
    print("2. Search and download each track from Beatport/Traxsource")
    print("3. Import downloads to Rekordbox")
    print("4. Create playlist and export to USB")

if __name__ == "__main__":
    main()
```

---

## Automated Workflows

### Complete Workflow: YouTube → USB

```bash
#!/bin/bash
# Complete workflow script

echo "Step 1: Download DJ set from YouTube"
./download_youtube.sh "$YOUTUBE_URL" dj_set

echo "Step 2: Recognize all songs"
python3.11 recognize_dj_set.py dj_set.mp3

echo "Step 3: Create download list"
python3 create_rekordbox_list.py

echo "Step 4: Manual step - Download tracks from Beatport"
echo "  → Open tracks_to_download.txt"
echo "  → Search and buy/download each track"
echo "  → Save to ~/Music/DJ Music/"

read -p "Press enter when downloads are complete..."

echo "Step 5: Import to Rekordbox"
echo "  → Open Rekordbox"
echo "  → File → Import → Select ~/Music/DJ Music/"
echo "  → Wait for analysis to complete"

read -p "Press enter when import is complete..."

echo "Step 6: Create playlist and export to USB"
echo "  → Create new playlist 'DJ Set - [Date]'"
echo "  → Add imported tracks"
echo "  → Drag playlist to USB device in Rekordbox"
echo "  → Wait for export to complete"

echo "✓ Complete! USB is ready for CDJ-2000"
```

### Batch Download Helper

For Beatport (manual process):
1. Use recognized tracklist
2. Search each track on Beatport
3. Add to cart
4. Download WAV versions
5. Move to dedicated folder
6. Import to Rekordbox

**Pro tip:** Beatport allows bulk cart actions - add multiple tracks before downloading.

---

## Rekordbox Tips for CDJ-2000

### Essential Settings

**Preferences → Analysis:**
- ✅ Auto-analyze new tracks
- ✅ Write analysis to file tags
- ✅ Create beatgrid
- ✅ Detect key

**Preferences → CDJ:**
- ✅ Link tracks automatically
- ✅ Display artwork on CDJ
- ⚠️ For CDJ-2000: use "CDJ-2000" mode, not newer models

### Metadata Best Practices

**Essential Tags:**
- Title, Artist, Album
- Genre (for sorting)
- BPM and Key (auto-detected)
- Comments (for notes)
- Artwork (shows on CDJ screen)

**File Naming:**
```
Artist - Track Title (Remix).wav
Artist - Track Title.wav
```

**Folder Structure:**
```
DJ Music/
  ├── House/
  ├── Techno/
  ├── Deep House/
  └── Gig - 2025-01-13/
```

---

## Troubleshooting

### USB Not Recognized on CDJ

1. Check format (FAT32 or exFAT)
2. Re-export from Rekordbox
3. Try different USB port on CDJ
4. Update Rekordbox firmware

### Tracks Missing After Export

1. Ensure tracks were fully analyzed
2. Check that tracks are in playlist before export
3. Verify USB has enough space
4. Try export again

### Beatgrid Issues

1. Re-analyze in Rekordbox
2. Manually adjust beatgrid
3. Set first beat marker correctly
4. Save and re-export to USB

---

## Resources

### Official Documentation
- [Rekordbox Manual](https://rekordbox.com/en/support/manual/)
- [CDJ-2000 Manual](https://www.pioneerdj.com/en-us/support/documents/)

### Python Tools
- [pyrekordbox GitHub](https://github.com/dylanljones/pyrekordbox)
- [DJ Tools Python Library](https://github.com/a-rich/DJ-Tools)

### Communities
- r/DJs on Reddit
- r/Beatmatch (for beginners)
- Rekordbox Forums

---

**Ready to go pro? 🎧**

With high-quality downloads and properly prepared USB drives, your CDJ-2000 performances will be rock solid!
