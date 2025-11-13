# YouTube Comment Posting Guide

Complete guide to programmatically post your tracklist to YouTube.

## Prerequisites

1. **Python 3.11+** (you already have this)
2. **Google Cloud Project** with YouTube Data API enabled
3. **OAuth2 Credentials** from Google

## Setup Steps

### Step 1: Install Required Libraries

```bash
cd ~/Downloads
pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

### Step 2: Get YouTube API Credentials

1. **Go to Google Cloud Console**:
   ```bash
   open https://console.cloud.google.com/
   ```

2. **Create or select a project**:
   - Click "Select a project" → "New Project"
   - Name it: "YouTube Tracklist Poster"
   - Click "Create"

3. **Enable YouTube Data API v3**:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search for "YouTube Data API v3"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure consent screen:
     - User Type: External
     - App name: "YouTube Tracklist Poster"
     - User support email: Your email
     - Developer contact: Your email
     - Save and continue through all steps
   - Back to "Create OAuth client ID":
     - Application type: "Desktop app"
     - Name: "Tracklist Poster"
     - Click "Create"
   - Click "Download JSON"
   - Save as `client_secret.json` in `~/Downloads/`

### Step 3: Run the Script

```bash
cd ~/Downloads
python3 post_youtube_comment.py
```

**First run:**
- Browser will open automatically
- Sign in with your Google account
- Click "Allow" when asked for YouTube permissions
- Token will be saved to `youtube_token.json` for future use

**Subsequent runs:**
- No browser needed (uses saved token)
- Comment posts immediately

## Script Features

✓ OAuth2 authentication with token caching
✓ Automatic browser-based login flow
✓ Error handling for disabled comments
✓ Comment ID and URL returned on success

## Troubleshooting

### Error: "Comments are disabled"
- Check if the video allows comments
- Only the video owner can disable comments

### Error: "Insufficient permissions"
- Delete `youtube_token.json`
- Run script again to re-authenticate
- Make sure you grant all requested permissions

### Error: "API quota exceeded"
- YouTube API has daily quota limits (10,000 units/day)
- Posting a comment costs 50 units
- Wait until next day or request quota increase

## Alternative: Node.js Version

If you prefer JavaScript:

```bash
npm install googleapis
```

```javascript
const {google} = require('googleapis');
const fs = require('fs');

// Similar implementation to Python version
// See: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps
```

## API Documentation

- **YouTube Data API v3**: https://developers.google.com/youtube/v3/docs
- **CommentThreads.insert**: https://developers.google.com/youtube/v3/docs/commentThreads/insert
- **OAuth2 for Web Apps**: https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps

## Video Info

- **Video ID**: 93ZGx5wjRdo
- **URL**: https://www.youtube.com/watch?v=93ZGx5wjRdo
- **Tracklist File**: `youtube_tracklist_comment.txt` (35 unique tracks)

## Cost

**Free Tier:**
- 10,000 quota units per day
- Posting 1 comment = 50 units
- You can post ~200 comments/day

**No credit card required** for basic usage.

## Security Notes

- ⚠️ Keep `client_secret.json` private (don't commit to git)
- ⚠️ Keep `youtube_token.json` private (contains your access token)
- ✓ Token expires after 7 days of inactivity
- ✓ Script automatically refreshes expired tokens

## Quick Start Commands

```bash
# 1. Install dependencies
pip install google-api-python-client google-auth-oauthlib

# 2. Get credentials from Google Cloud Console
open https://console.cloud.google.com/

# 3. Download client_secret.json to ~/Downloads/

# 4. Run script
cd ~/Downloads
python3 post_youtube_comment.py

# 5. Follow browser authentication flow (first time only)
```

That's it! Your tracklist will be posted to the YouTube video automatically.
