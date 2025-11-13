# Claude Code Skill: YouTube DJ Tracklist Recognition

This repository includes a Claude Code skill that automates the entire process of recognizing songs in YouTube DJ sets and posting tracklists as comments.

## What is a Claude Code Skill?

A skill is a specialized instruction set that teaches Claude Code how to perform complex multi-step tasks automatically. This skill handles:

1. ✅ Downloading audio from YouTube
2. ✅ Recognizing all songs using Shazam
3. ✅ Formatting tracklists for YouTube
4. ✅ Posting comments programmatically via YouTube API

## Installation

### Step 1: Install the Skill

```bash
# Copy the skill to your Claude Code skills directory
cp youtube-dj-tracklist.md ~/.claude/skills/
```

Or manually create `~/.claude/skills/youtube-dj-tracklist.md` with the skill content.

### Step 2: Verify Installation

Skills are automatically loaded by Claude Code. Just start a new conversation!

## Usage

Simply ask Claude Code:

> "Find all songs from this YouTube DJ set: https://www.youtube.com/watch?v=93ZGx5wjRdo"

> "Recognize tracks in this mix and post the tracklist to YouTube comments"

> "Download and identify all songs from [YouTube URL]"

Claude will automatically:
1. Download the audio
2. Run song recognition
3. Format the results
4. Post to YouTube (if you have API credentials)

## How It Works

The skill guides Claude Code through a 3-phase workflow:

### Phase 1: Download & Recognize
- Uses `yt-dlp` to extract audio
- Runs `recognize_dj_set.py` with Shazam API
- Samples audio every 30 seconds (configurable)

### Phase 2: Format Output
- Removes duplicate detections
- Creates YouTube-friendly timestamps
- Formats as: `MM:SS Artist - Title`

### Phase 3: Post to YouTube (Optional)
- Authenticates via OAuth2
- Posts formatted tracklist as comment
- Caches token for future use

## Prerequisites

The skill checks for and guides installation of:

- Python 3.11 or 3.12 (NOT 3.14)
- ffmpeg
- yt-dlp
- shazamio Python library
- google-api-python-client (for YouTube posting)

## Example Session

```
User: Find all songs from https://www.youtube.com/watch?v=93ZGx5wjRdo

Claude: I'll use the YouTube DJ Tracklist Recognition skill to:
1. Download the audio from YouTube
2. Recognize all songs using Shazam
3. Format the tracklist with timestamps
4. Post it as a YouTube comment

[Executes workflow automatically]

✓ Downloaded 87.65MB MP3 file
✓ Recognized 44 songs
✓ Created YouTube tracklist with 35 unique tracks
✓ Posted comment to video

View your comment: https://www.youtube.com/watch?v=93ZGx5wjRdo
```

## Skill Features

### Automatic Dependency Management
- Checks for required tools
- Provides installation commands if missing
- Uses correct Python version (3.11 vs 3.14)

### Smart Recognition Parameters
- Adjusts scan interval based on mix type
- Fast mixes (trap/dnb): 15-20s intervals
- Slow mixes (house/techno): 45-60s intervals

### Error Handling
- Handles rate limiting from Shazam API
- Retries failed recognitions
- Provides troubleshooting guidance

### YouTube Integration
- OAuth2 authentication with token caching
- Browser-based login flow (first time only)
- Automatic comment posting

## Output Files

The skill generates:
- `dj_set_VIDEO_ID.mp3` - Downloaded audio
- `dj_set_VIDEO_ID_results.json` - Full Shazam results
- `dj_set_VIDEO_ID_tracklist.txt` - Human-readable tracklist
- `youtube_comment.txt` - Formatted for YouTube

## Performance

For a 90-minute DJ set:
- Download: 1-2 minutes
- Recognition: ~15 minutes
- Format & post: <15 seconds
- **Total: ~20 minutes fully automated**

## Advanced Configuration

### Adjust Recognition Interval

For faster recognition (less accurate):
```bash
python3.11 recognize_dj_set.py audio.mp3 15  # Scan every 15 seconds
```

For slower recognition (more conservative):
```bash
python3.11 recognize_dj_set.py audio.mp3 60  # Scan every 60 seconds
```

### YouTube API Setup

First-time YouTube commenting requires OAuth2 setup:
1. Create Google Cloud Project
2. Enable YouTube Data API v3
3. Create OAuth Desktop credentials
4. Download `client_secret.json`

See `YOUTUBE_COMMENT_SETUP.md` for detailed instructions.

## Troubleshooting

### Skill Not Loading?

```bash
# Check skill exists
ls ~/.claude/skills/youtube-dj-tracklist.md

# Restart Claude Code
# Skills load on session start
```

### Python 3.14 Errors?

Always use Python 3.11 explicitly:
```bash
python3.11 recognize_dj_set.py audio.mp3
```

The skill automatically handles this.

### No Songs Recognized?

The skill will:
1. Try reducing scan interval to 15 seconds
2. Check audio file integrity
3. Suggest manual verification with Shazam app

## Contributing

Found an issue or want to improve the skill?

1. Edit `~/.claude/skills/youtube-dj-tracklist.md`
2. Test with Claude Code
3. Submit improvements to the repository

## Related Documentation

- `README.md` - Main project documentation
- `CLAUDE.md` - AI assistant instructions
- `REKORDBOX_GUIDE.md` - DJ workflow integration
- `YOUTUBE_COMMENT_SETUP.md` - YouTube API setup

## License

This skill is part of the DJ Set Song Recognizer project.
Free to use and modify.

## Credits

- Created for Claude Code
- Uses Shazam API via shazamio library
- YouTube Data API v3 integration
- Audio processing with ffmpeg

---

**Repository**: https://github.com/adamanz/dj-set-song-recognizer

**Skill Location**: `~/.claude/skills/youtube-dj-tracklist.md`
