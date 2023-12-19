#!/usr/bin/env python
# coding=utf-8

# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import io
import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import json
import ffmpeg

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pytube import YouTube

from googleapiclient.http import MediaIoBaseDownload

import whisper
from stable_whisper import modify_model
from stable_whisper import load_model
import json
import whisper
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube, Caption, captions, CaptionQuery
import pytube
from pytube import extract


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


keys = {
    "trello_api_key": "507e54976cbef96c4b8e1b5b883f4639",
    "trello_token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
    "youtube_api_key": "AIzaSyDf5sAydLvEi-skWyH5AeiX4g5GP6kHilo",
}


scopes = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

# # If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

creator = {
    "thefirearmguy": {
        "trello_board_id": "64c709c04259bef49a00c5de",
        "trello_longformat_list_ID": "64baa956447059d528377b87",
        "trello_longformat_script_field_ID": "64ca69028b331b036679c2ab",
        "trello_shorts_list_ID": "64c709c04259bef49a00c5df",
        "trello_short_script_field_ID": "6537d7173e68b703e6327632",
        "trello_short_tamplate_id": "64ca6c0f94fc3cee563f130b",
        "trello_longformat_template_id": "",
    },
    "prank_me_later": {
        "trello_board_id": "64c709c04259bef49a00c5de",
        "trello_longformat_list_ID": "64baa956447059d528377b87",
        "trello_longformat_script_field_ID": "64ca69028b331b036679c2ab",
        "trello_shorts_list_ID": "64c709c04259bef49a00c5df",
        "trello_short_script_field_ID": "6537d7173e68b703e6327632",
    },
}

yt_video = {
    "title": "",
    "video_number": "",
    "id": "",
    "description": "",
    "tags": "",
    "script": "",
    "storage_location": "",
    "video_url": "",
    "script_url": "",
    "shorts_path": "/home/santiago/Dropbox/Lang2views/Client Projects/TheFireArmGuy/Shorts/",
    "long_format_path": "/home/santiago/Dropbox/Lang2views/Client Projects/TheFireArmGuy/Long Format/",
}


def main():

    yt_video["video_url"] = "https://youtube.com/shorts/giid2QYVKo0"
    yt_video["id"] = extract.video_id(yt_video["video_url"])

    youtube = build("youtube", "v3", developerKey=keys["youtube_api_key"])
    video_request = youtube.videos().list(part="snippet", id=yt_video["id"])
    video_response = video_request.execute()

    yt_video["title"] = video_response["items"][0]["snippet"]["title"]
    yt_video["description"] = video_response["items"][0]["snippet"]["description"]
    yt_video["tags"] = video_response["items"][0]["snippet"]["tags"]

    shorts_folders = os.listdir(yt_video["shorts_path"])
    shorts_folders = sorted(shorts_folders)
    video_number = str(shorts_folders[-1][0:2])
    yt_video["video_number"] = video_number

    print(yt_video)

    if (
        os.listdir(
            yt_video["shorts_path"]
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
        )
        == None
    ):
        os.mkdir(
            yt_video["shorts_path"]
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
        )

    # Example usage
    output_path = (
        yt_video["shorts_path"]
        + yt_video["video_number"]
        + ". "
        + yt_video["title"]
        + "/"
    )

    yt = YouTube(yt_video["video_url"])
    video_stream = yt.streams.get_highest_resolution()
    video_stream.download(output_path)

    # Load the video file
    input_file = ffmpeg.input(
        yt_video["shorts_path"]
        + yt_video["video_number"]
        + ". "
        + yt_video["title"]
        + "/"
        + yt_video["title"]
        + ".mp4"
    )

    # Extract the audio and save it as an MP3 file
    input_file.output(
        yt_video["shorts_path"]
        + yt_video["video_number"]
        + ". "
        + yt_video["title"]
        + "/"
        + yt_video["title"]
        + ".mp3",
        acodec="mp3",
    ).run()

    model = whisper.load_model("base")
    result = model.transcribe(
        yt_video["shorts_path"]
        + yt_video["video_number"]
        + ". "
        + yt_video["title"]
        + "/"
        + yt_video["title"]
        + ".mp3"
    )
    yt_video["script"] = result["text"]

    print(yt_video)

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    service = build("docs", "v1", credentials=creds)

    body = {"title": video_title + " - Script"}
    doc = service.documents().create(body=body).execute()
    title = doc.get("title")
    _id = doc.get("documentId")
    print(f"Created document with title: {title}, id: {_id}")

    # Text insertion
    gdoc_text = [
        {
            "insertText": {
                "location": {
                    "index": 1,
                },
                "text": yt_video["script"],
            }
        }
    ]
    result = (
        service.documents()
        .batchUpdate(documentId=_id, body={"requests": gdoc_text})
        .execute()
    )

    def create_new_trello_list(name, board):
        url = "https://api.trello.com/1/lists"

        query = {
            "name": "{test}",
            "idBoard": thefirearmguy_data["trello_board_id"],
            "key": keys["trello_api_key"],
            "token": keys["trello_token"],
        }

        response = requests.request("POST", url, params=query)

        print(response.text)

    # def clone_trello_card(name, list_id, card_id):
    url = "https://api.trello.com/1/cards"

    headers = {"Accept": "application/json"}

    query = {
        "key": keys["trello_api_key"],
        "token": keys["trello_token"],
        "dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
        "idCardSource": "64ca6c0f94fc3cee563f130b",
        "idList": "64baa956447059d528377b87",
        "keepFromSource": "checklists,attachments,stickers,members,labels,customFields",
        "name": yt_video["title"],
    }

    response = requests.request("POST", url, headers=headers, params=query)

    print(
        json.dumps(
            json.loads(response.text),
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )
    )

    def update_customefield_from_card(value, custom_field_id, card_id):
        url = "https://api.trello.com/1/cards/6580684b86c5ca371989af23/customField/64ca69028b331b036679c2ab/item"

        headers = {"Content-Type": "application/json"}

        query = {
            "key": "507e54976cbef96c4b8e1b5b883f4639",
            "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
        }

        payload = json.dumps({"value": {"text": "Update custom field test"}})

        response = requests.request(
            "PUT", url, data=payload, headers=headers, params=query
        )
        print(response.text)


if __name__ == "__main__":
    main()
