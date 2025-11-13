#!/usr/bin/env python3
"""
Post tracklist comment to YouTube video programmatically
Requires: pip install google-api-python-client google-auth-oauthlib
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Video ID from URL: https://www.youtube.com/watch?v=93ZGx5wjRdo
VIDEO_ID = '93ZGx5wjRdo'

def authenticate():
    """Authenticate with YouTube API using OAuth2"""
    creds = None
    token_file = 'youtube_token.json'
    credentials_file = 'client_secret.json'

    # Check if we have a saved token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_file):
                print("❌ Error: client_secret.json not found!")
                print("\nTo get your credentials:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project or select existing one")
                print("3. Enable YouTube Data API v3")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download as 'client_secret.json' to this directory")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next time
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds

def post_comment(youtube, video_id, comment_text):
    """Post a comment to a YouTube video"""
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        )
        response = request.execute()

        print(f"✓ Comment posted successfully!")
        print(f"  Comment ID: {response['id']}")
        print(f"  View at: https://www.youtube.com/watch?v={video_id}")

        return response

    except HttpError as e:
        print(f"❌ Error posting comment: {e}")
        if e.resp.status == 403:
            print("\nPossible reasons:")
            print("- Comments are disabled on this video")
            print("- You don't have permission to comment")
            print("- The video owner blocked comments from your account")
        return None

def load_tracklist(filename):
    """Load tracklist from text file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("YouTube Comment Poster")
    print("=" * 50)

    # Authenticate
    print("\n1. Authenticating with YouTube...")
    creds = authenticate()
    if not creds:
        return

    # Build YouTube API client
    youtube = build('youtube', 'v3', credentials=creds)

    # Load tracklist
    print("2. Loading tracklist...")
    tracklist_file = 'youtube_tracklist_comment.txt'
    if not os.path.exists(tracklist_file):
        print(f"❌ Error: {tracklist_file} not found!")
        return

    comment_text = load_tracklist(tracklist_file)
    print(f"   Loaded {len(comment_text)} characters")

    # Post comment
    print("3. Posting comment to video...")
    post_comment(youtube, VIDEO_ID, comment_text)

if __name__ == '__main__':
    main()
