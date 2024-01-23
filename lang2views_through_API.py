#!/usr/bin/env python
# coding=utf-8

import os
import io
import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import json
import ffmpeg
from mutagen.mp3 import MP3

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
        "dropbox_path": "/home/santiago/Dropbox/Lang2views/Client Projects/TheFireArmGuy/",
        "trello_board_id": "64c709c04259bef49a00c5de",
        "trello_dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
        "trello_longformat_list_id": "64baa956447059d528377b87",
        "trello_longformat_script_field_ID": "64ca69028b331b036679c2ab",
        "trello_shorts_list_id": "64c709c04259bef49a00c5df",
        "trello_short_script_field_id": "6537d7173e68b703e6327632",
        "trello_short_tamplate_id": "64ca6c0f94fc3cee563f130b",
        "trello_longformat_template_id": "",
        "trello_new_card_id": "",
    },
    "prank_me_later": {
        "trello_board_id": "64c709c04259bef49a00c5de",
        "trello_longformat_list_id": "64baa956447059d528377b87",
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
    "storage_location": "",
    "video_url": "",
    "script_url": "",
    "new_trello_card_id": "",
    "video_length": "",
    "thumbnail_path": "",
}


# channel
# channel RangeOfVideos=[4,14] month="jan" samescript="yes/no" script="script ID if not new doc" chat_gpt="instructions"


# options to have
# link month

# list of differente videos from differente channels
# link link link link month


class Lang2views:
    def __init__(self, video_links, creator_name):
        self.video_links = video_links
        self.creator_name = creator_name
        yt_video["video_url"] = video_links

        # authenticate for youtube.com
        yt_video["id"] = extract.video_id(yt_video["video_url"])
        self.youtube_auth = build("youtube", "v3", developerKey=keys["youtube_api_key"])
        self.youtube_auth = self.youtube_auth.videos().list(
            part="snippet", id=yt_video["id"]
        )
        self.youtube_auth = self.youtube_auth.execute()

        # authenticate for google docs
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        self.gdocs_auth = build("docs", "v1", credentials=creds)

    def set_video_title(self):
        yt_video["title"] = self.youtube_auth["items"][0]["snippet"]["title"]

    def set_video_description(self):
        yt_video["description"] = self.youtube_auth["items"][0]["snippet"][
            "description"
        ]

    def set_video_tags(self):
        yt_video["tags"] = self.youtube_auth["items"][0]["snippet"]["tags"]

    def set_video_number(self, video_type):
        print(video_type)
        shorts_folders = os.listdir(
            creator[self.creator_name]["dropbox_path"] + video_type
        )
        shorts_folders = sorted(shorts_folders)
        video_number = str(shorts_folders[-1][0:2])
        yt_video["video_number"] = video_number

    def create_dropbox_video_folder(self, video_type):
        # if (
        #     os.listdir(
        #         creator[self.creator_name]["dropbox_path"]
        #         + yt_video["video_number"]
        #         + ". "
        #         + yt_video["title"]
        #     )
        #     == None
        # ):
        os.mkdir(
            creator[self.creator_name]["dropbox_path"]
            + video_type
            + "/"
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
        )
        print(yt_video)

    def download_video(self, video_type):
        output_path = (
            creator[self.creator_name]["dropbox_path"]
            + video_type
            + "/"
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
            + "/"
        )

        yt = YouTube(yt_video["video_url"])
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)

    def convert_video_to_audio(self, video_type):
        input_file = ffmpeg.input(
            creator[self.creator_name]["dropbox_path"]
            + video_type
            + "/"
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
            + "/"
            + yt_video["title"]
            + ".mp4"
        )

        # Extract the audio and save it as an MP3 file
        input_file.output(
            creator[self.creator_name]["dropbox_path"]
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
            + "/"
            + yt_video["title"]
            + ".mp3",
            acodec="mp3",
        ).run()

    def transcribe_video(self):
        model = whisper.load_model("base")
        result = model.transcribe(
            creator[self.creator_name]["dropbox_path"]
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
            + "/"
            + yt_video["title"]
            + ".mp3"
        )
        yt_video["script"] = result["text"]

    def count_video_length(self):
        audio = MP3(
            yt_video["shorts_path"]
            + yt_video["video_number"]
            + ". "
            + yt_video["title"]
            + "/"
            + yt_video["title"]
            + ".mp3"
        )
        yt_video["length"] = audio.info.length

    def gdoc_set_doc_title(self):
        body = {"title": yt_video["video_number"] + yt_video["title"] + " - Script"}
        doc = self.gdocs_auth.documents().create(body=body).execute()
        title = doc.get("title")
        self.video_script_doc_id = doc.get("documentId")
        yt_video[
            "script_url"
        ] = "https://docs.google.com/document/d/video_script_doc_id/edit"

    def gdoc_set_script(self):
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
            self.gdocs_auth.documents()
            .batchUpdate(
                documentId=self.video_script_doc_id, body={"requests": gdoc_text}
            )
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

    def trello_create_from_template():
        # def clone_trello_card(name, list_id, card_id):
        url = "https://api.trello.com/1/cards"

        headers = {"Accept": "application/json"}

        query = {
            "key": keys["trello_api_key"],
            "token": keys["trello_token"],
            "dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
            "idCardSource": creator["thefirearmguy"]["trello_short_tamplate_id"],
            "idList": creator["thefirearmguy"]["trello_shorts_list_id"],
            "keepFromSource": "checklists,attachments,stickers,members,labels,customFields",
            "name": yt_video["title"],
        }

        response = requests.request("POST", url, headers=headers, params=query)
        creator["thefirearmguy"]["trello_new_card_id"] = json.loads(response.text)["id"]

    def trello_update_custom_field():
        url = (
            "https://api.trello.com/1/cards/"
            + creator["thefirearmguy"]["trello_new_card_id"]
            + "/customField/64ca69028b331b036679c2ab/item"
        )

        headers = {"Content-Type": "application/json"}

        query = {
            "key": "507e54976cbef96c4b8e1b5b883f4639",
            "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
        }

        payload = json.dumps({"value": {"text": yt_video["script_url"]}})

        response = requests.request(
            "PUT", url, data=payload, headers=headers, params=query
        )
        print(response.text)


def main():
    month = "01"
    creator = "thefirearmguy"
    video_type = "Shorts"

    translated_video = Lang2views(
        "https://www.youtube.com/shorts/g7QtnCEWhfE", "thefirearmguy"
    )
    translated_video.set_video_title()
    translated_video.set_video_description()
    translated_video.set_video_tags()
    translated_video.set_video_number(video_type)
    translated_video.create_dropbox_video_folder(video_type)
    translated_video.download_video(video_type)
    translated_video.convert_video_to_audio(video_type)
    # translated_video.transcribe_video()
    # translated_video.count_video_length()
    # translated_video.count_video_length()
    # translated_video.gdoc_set_doc_title()
    # translated_video.gdoc_set_script()
    # print(yt_video)


if __name__ == "__main__":
    main()
