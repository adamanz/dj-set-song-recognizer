#!/bin/bash
# Download audio from YouTube video

if [ $# -eq 0 ]; then
    echo "Usage: ./download_youtube.sh <youtube_url> [output_name]"
    echo ""
    echo "Example:"
    echo "  ./download_youtube.sh 'https://www.youtube.com/watch?v=93ZGx5wjRdo'"
    echo "  ./download_youtube.sh 'https://www.youtube.com/watch?v=93ZGx5wjRdo' my_dj_set"
    exit 1
fi

YOUTUBE_URL="$1"
OUTPUT_NAME="${2:-dj_set_%(id)s}"

echo "Downloading audio from: $YOUTUBE_URL"
echo "Output filename: ${OUTPUT_NAME}.mp3"
echo ""

yt-dlp -x --audio-format mp3 --audio-quality 0 -o "${OUTPUT_NAME}.%(ext)s" "$YOUTUBE_URL"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Download complete!"
    echo ""
    echo "Next step: Run song recognition"
    echo "  python3 recognize_dj_set.py ${OUTPUT_NAME}.mp3"
else
    echo ""
    echo "✗ Download failed"
    exit 1
fi
