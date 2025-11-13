#!/usr/bin/env python3
"""
DJ Set Song Recognizer
Identifies all songs in a DJ mix or set from YouTube videos using Shazam
"""

import asyncio
from shazamio import Shazam
import subprocess
import json
import os
import sys
from pathlib import Path

def get_audio_duration(audio_file):
    """Get audio duration using ffprobe"""
    cmd = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
        audio_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def extract_audio_chunk(input_file, start_time, duration, output_file):
    """Extract a chunk of audio using ffmpeg"""
    cmd = [
        'ffmpeg', '-y', '-ss', str(start_time), '-i', input_file,
        '-t', str(duration), '-acodec', 'libmp3lame', '-q:a', '2',
        output_file
    ]
    subprocess.run(cmd, capture_output=True, stderr=subprocess.DEVNULL)

async def recognize_chunk(shazam, chunk_file, chunk_number, timestamp):
    """Recognize a single audio chunk"""
    try:
        result = await shazam.recognize(chunk_file)

        if result and 'track' in result:
            track = result['track']

            # Extract metadata
            title = track.get('title', 'Unknown')
            artist = track.get('subtitle', 'Unknown')

            # Get album from metadata sections
            album = 'Unknown'
            if 'sections' in track and len(track['sections']) > 0:
                for section in track['sections']:
                    if 'metadata' in section:
                        for meta in section['metadata']:
                            if meta.get('title') == 'Album':
                                album = meta.get('text', 'Unknown')
                                break

            return {
                'timestamp': timestamp,
                'title': title,
                'artist': artist,
                'album': album,
                'shazam_url': track.get('url', ''),
                'raw_data': track
            }
    except Exception as e:
        pass

    return None

def format_timestamp(seconds):
    """Convert seconds to MM:SS or HH:MM:SS format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

async def recognize_dj_set(audio_file, chunk_duration=12, skip_seconds=30, output_dir=None):
    """
    Recognize songs in a DJ set by processing it in chunks

    Args:
        audio_file: Path to the audio file
        chunk_duration: Duration of each chunk in seconds (default 12)
        skip_seconds: Seconds to skip between chunks (default 30)
        output_dir: Directory to save results (default: same as audio file)

    Returns:
        List of recognized songs with timestamps
    """

    print(f"Loading audio file: {audio_file}")
    duration = get_audio_duration(audio_file)

    print(f"Audio duration: {format_timestamp(duration)} ({duration:.0f} seconds)")
    print(f"Scanning every {skip_seconds} seconds with {chunk_duration}s samples")
    print(f"Estimated scan time: ~{int((duration / skip_seconds) * 3 / 60)} minutes")
    print(f"This may take a while...\n")

    shazam = Shazam()
    results = []
    chunk_number = 0
    current_pos = 0

    # Create temp directory
    temp_dir = "/tmp/dj_set_chunks"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        while current_pos < duration:
            chunk_number += 1
            chunk_file = f"{temp_dir}/chunk_{chunk_number:04d}.mp3"

            # Extract chunk
            extract_audio_chunk(audio_file, current_pos, chunk_duration, chunk_file)

            # Check if chunk was created
            if not os.path.exists(chunk_file) or os.path.getsize(chunk_file) < 1000:
                break

            time_str = format_timestamp(current_pos)
            print(f"[{time_str}] Chunk {chunk_number}...", end=" ", flush=True)

            result = await recognize_chunk(shazam, chunk_file, chunk_number, current_pos)

            if result:
                print(f"✓ {result['artist']} - {result['title']}")
                results.append(result)
            else:
                print("✗ No match")

            # Cleanup chunk file
            try:
                os.remove(chunk_file)
            except:
                pass

            current_pos += skip_seconds

            # Rate limiting - Shazam allows ~20 requests per minute
            await asyncio.sleep(3)

    finally:
        # Cleanup temp directory
        try:
            os.rmdir(temp_dir)
        except:
            pass

    return results

def save_results(results, audio_file, output_dir=None):
    """Save results to JSON and text files"""

    if output_dir is None:
        output_dir = os.path.dirname(audio_file)

    base_name = Path(audio_file).stem

    # Save raw JSON results
    json_file = os.path.join(output_dir, f"{base_name}_results.json")
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nRaw results saved to: {json_file}")

    # Create simple tracklist
    tracklist_file = os.path.join(output_dir, f"{base_name}_tracklist.txt")
    with open(tracklist_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("DJ SET TRACKLIST\n")
        f.write("=" * 80 + "\n\n")

        unique_tracks = []
        last_song = None
        track_number = 0

        for result in results:
            song_id = f"{result['artist']} - {result['title']}"
            if song_id != last_song:
                track_number += 1
                time_str = format_timestamp(result['timestamp'])
                f.write(f"{track_number:2d}. [{time_str}] {result['artist']} - {result['title']}\n")
                if result.get('album') and result['album'] != 'Unknown':
                    f.write(f"    Album: {result['album']}\n")
                if result.get('shazam_url'):
                    f.write(f"    Shazam: {result['shazam_url']}\n")
                f.write("\n")
                last_song = song_id

        f.write("=" * 80 + "\n")
        f.write(f"Total unique tracks: {track_number}\n")
        f.write(f"Total scans: {len(results)}\n")
        f.write("=" * 80 + "\n")

    print(f"Tracklist saved to: {tracklist_file}")

    return json_file, tracklist_file

def display_results(results):
    """Display the recognized songs in a formatted way"""
    if not results:
        print("\nNo songs were recognized in the audio file")
        return

    print(f"\n{'='*80}")
    print(f"DJ SET TRACKLIST")
    print(f"{'='*80}\n")

    # Remove duplicates - only show when song changes
    unique_tracks = []
    last_song = None

    for result in results:
        song_id = f"{result['artist']} - {result['title']}"
        if song_id != last_song:
            unique_tracks.append(result)
            last_song = song_id

    track_number = 0
    for result in unique_tracks:
        track_number += 1
        time_str = format_timestamp(result['timestamp'])

        print(f"{track_number:2d}. [{time_str}] {result['artist']} - {result['title']}")

        if result.get('album') and result['album'] != 'Unknown':
            print(f"    Album: {result['album']}")

        if result.get('shazam_url'):
            print(f"    Shazam: {result['shazam_url']}")
        print()

    print(f"{'='*80}")
    print(f"Total unique tracks identified: {track_number}")
    print(f"Total scans performed: {len(results)}")
    print(f"{'='*80}")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 recognize_dj_set.py <audio_file> [skip_seconds]")
        print("\nExample:")
        print("  python3 recognize_dj_set.py my_dj_set.mp3")
        print("  python3 recognize_dj_set.py my_dj_set.mp3 20  # Scan every 20 seconds")
        sys.exit(1)

    audio_file = sys.argv[1]
    skip_seconds = int(sys.argv[2]) if len(sys.argv) > 2 else 30

    if not os.path.exists(audio_file):
        print(f"Error: File not found: {audio_file}")
        sys.exit(1)

    print("="*80)
    print("DJ SET SONG RECOGNIZER")
    print("="*80)
    print(f"\nScanning every {skip_seconds} seconds")
    print("Note: Rate limited to ~20 requests/minute (Shazam API)")
    print("="*80 + "\n")

    # Recognize the set
    results = await recognize_dj_set(audio_file, chunk_duration=12, skip_seconds=skip_seconds)

    if results:
        # Save results
        save_results(results, audio_file)

        # Display formatted results
        display_results(results)
    else:
        print("\nFailed to recognize any songs in the DJ set")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
