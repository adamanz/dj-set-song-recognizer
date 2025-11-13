#!/usr/bin/env python3
"""
Rekordbox Helper - CLI tool for working with Rekordbox
Uses pyrekordbox library to interact with Rekordbox 6 database

Installation:
    pip install pyrekordbox
"""

import json
import argparse
from pathlib import Path

try:
    from pyrekordbox import Rekordbox6Database
    from pyrekordbox.db6 import tables
except ImportError:
    print("Error: pyrekordbox not installed")
    print("Install with: pip install pyrekordbox")
    exit(1)

def list_playlists(db):
    """List all playlists in Rekordbox"""
    playlists = db.get_playlist()

    print("\nRekordbox Playlists:")
    print("=" * 80)

    for pl in playlists:
        track_count = len(db.get_playlist_tracks(pl.ID)) if pl.ID else 0
        print(f"ID: {pl.ID:4d} | {pl.Name:50s} | {track_count:4d} tracks")

    print("=" * 80)
    print(f"Total: {len(playlists)} playlists")

def search_tracks(db, query):
    """Search for tracks in Rekordbox library"""
    all_tracks = db.get_track()
    query_lower = query.lower()

    matches = []
    for track in all_tracks:
        # Search in title, artist, album
        if (query_lower in str(track.Title).lower() or
            query_lower in str(track.Artist).lower() or
            query_lower in str(track.Album).lower()):
            matches.append(track)

    print(f"\nSearch Results for '{query}':")
    print("=" * 80)

    for track in matches:
        print(f"{track.Artist} - {track.Title}")
        print(f"  Album: {track.Album}")
        print(f"  BPM: {track.Tempo:.1f}, Key: {track.Key}")
        print(f"  File: {track.FolderPath}")
        print()

    print("=" * 80)
    print(f"Found {len(matches)} matching tracks")

def export_playlist_csv(db, playlist_name, output_file):
    """Export playlist to CSV format"""
    import csv

    playlists = db.get_playlist()
    target_playlist = None

    for pl in playlists:
        if pl.Name == playlist_name:
            target_playlist = pl
            break

    if not target_playlist:
        print(f"Error: Playlist '{playlist_name}' not found")
        return

    tracks = db.get_playlist_tracks(target_playlist.ID)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Artist', 'Title', 'Album', 'BPM', 'Key', 'Genre', 'File Path'])

        for track_entry in tracks:
            track = db.get_track(id=track_entry.TrackID)[0]
            writer.writerow([
                track.Artist,
                track.Title,
                track.Album,
                track.Tempo,
                track.Key,
                track.Genre,
                track.FolderPath
            ])

    print(f"✓ Exported {len(tracks)} tracks to {output_file}")

def create_shopping_list(tracklist_json, output_file):
    """Create a shopping list from recognized tracks"""
    with open(tracklist_json, 'r') as f:
        results = json.load(f)

    # Remove duplicates
    seen = set()
    unique_tracks = []

    for item in results:
        track_id = f"{item['artist']} - {item['title']}"
        if track_id not in seen:
            seen.add(track_id)
            unique_tracks.append(item)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# DJ Set Track Shopping List\n")
        f.write("# Generated from Shazam recognition\n")
        f.write("=" * 80 + "\n\n")
        f.write("## Search these tracks on:\n")
        f.write("- Beatport: https://www.beatport.com/\n")
        f.write("- Traxsource: https://www.traxsource.com/\n")
        f.write("- Juno Download: https://www.junodownload.com/\n\n")
        f.write("## Tracks:\n\n")

        for i, track in enumerate(unique_tracks, 1):
            f.write(f"{i:2d}. [{track.get('timestamp', 0) // 60:02d}:{track.get('timestamp', 0) % 60:02d}] "
                   f"{track['artist']} - {track['title']}\n")

            if track.get('album'):
                f.write(f"    Album: {track['album']}\n")

            if track.get('shazam_url'):
                f.write(f"    Shazam: {track['shazam_url']}\n")

            f.write("\n")

        f.write("=" * 80 + "\n")
        f.write(f"\nTotal tracks to download: {len(unique_tracks)}\n")
        f.write(f"Estimated cost (@ $2.00/track): ${len(unique_tracks) * 2:.2f}\n")

    print(f"✓ Shopping list saved to {output_file}")
    print(f"  {len(unique_tracks)} unique tracks")

def find_missing_tracks(db, shopping_list):
    """Check which tracks from shopping list are already in Rekordbox"""
    with open(shopping_list, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Parse shopping list
    needed_tracks = []
    for line in lines:
        if line.startswith((' ', '\t')) or not line.strip():
            continue
        if ']' in line:
            # Format: "1. [MM:SS] Artist - Title"
            parts = line.split('] ', 1)
            if len(parts) == 2:
                track_info = parts[1].strip()
                needed_tracks.append(track_info)

    # Check against Rekordbox library
    all_tracks = db.get_track()

    found = []
    missing = []

    for needed in needed_tracks:
        found_match = False
        for rb_track in all_tracks:
            rb_full = f"{rb_track.Artist} - {rb_track.Title}"
            # Fuzzy matching
            if needed.lower().replace(' ', '') in rb_full.lower().replace(' ', ''):
                found.append((needed, rb_full))
                found_match = True
                break

        if not found_match:
            missing.append(needed)

    print(f"\n{'='*80}")
    print("Track Inventory Check")
    print(f"{'='*80}\n")

    print(f"✓ Already in Rekordbox: {len(found)}")
    for needed, found_as in found:
        print(f"  → {needed}")
        print(f"    Found as: {found_as}")
        print()

    print(f"\n✗ Need to download: {len(missing)}")
    for track in missing:
        print(f"  → {track}")

    print(f"\n{'='*80}")
    print(f"Summary: {len(found)} found, {len(missing)} missing")

def main():
    parser = argparse.ArgumentParser(
        description="Rekordbox Helper - CLI tool for Rekordbox operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all playlists
  python rekordbox_helper.py --list-playlists

  # Search for tracks
  python rekordbox_helper.py --search "Rex the Dog"

  # Export playlist to CSV
  python rekordbox_helper.py --export-playlist "My Playlist" -o playlist.csv

  # Create shopping list from recognized DJ set
  python rekordbox_helper.py --shopping-list dj_set_results.json -o shopping.txt

  # Check what you already have
  python rekordbox_helper.py --check-missing shopping.txt
        """
    )

    parser.add_argument('--list-playlists', action='store_true',
                       help='List all Rekordbox playlists')

    parser.add_argument('--search', metavar='QUERY',
                       help='Search for tracks in library')

    parser.add_argument('--export-playlist', metavar='NAME',
                       help='Export playlist to CSV')

    parser.add_argument('--shopping-list', metavar='JSON',
                       help='Create shopping list from recognition results')

    parser.add_argument('--check-missing', metavar='FILE',
                       help='Check which tracks from shopping list are missing')

    parser.add_argument('-o', '--output', metavar='FILE',
                       help='Output file path')

    args = parser.parse_args()

    if not any([args.list_playlists, args.search, args.export_playlist,
                args.shopping_list, args.check_missing]):
        parser.print_help()
        return

    # Commands that don't need Rekordbox database
    if args.shopping_list:
        output = args.output or 'shopping_list.txt'
        create_shopping_list(args.shopping_list, output)
        return

    # Initialize Rekordbox database connection
    try:
        print("Connecting to Rekordbox database...")
        db = Rekordbox6Database()
        print("✓ Connected successfully\n")
    except Exception as e:
        print(f"Error connecting to Rekordbox: {e}")
        print("\nMake sure:")
        print("1. Rekordbox 6 is installed")
        print("2. You have a Rekordbox library")
        print("3. pyrekordbox is installed: pip install pyrekordbox")
        return

    # Execute commands
    if args.list_playlists:
        list_playlists(db)

    if args.search:
        search_tracks(db, args.search)

    if args.export_playlist:
        if not args.output:
            print("Error: --output required for --export-playlist")
            return
        export_playlist_csv(db, args.export_playlist, args.output)

    if args.check_missing:
        find_missing_tracks(db, args.check_missing)

if __name__ == "__main__":
    main()
