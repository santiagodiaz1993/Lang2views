#!/usr/bin/env python
# coding=utf-8


# Video
#     Video meta information
#     translation
#     file_managment
#
#
# Tiketing


import os
import io
import re
import shutil
from urllib.parse import urlparse
from urllib.parse import parse_qs
import requests
import json
import ffmpeg
from mutagen.mp3 import MP3
import moviepy.editor as mp
import time

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


youtube_scopes = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

# # If modifying these scopes, delete the file token.json.
gdocs_scopes = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

creator = {
    "TheFireArmGuy": {
        "monthly_shorts": "",
        "monthly_long_format": "",
        "Shorts": "/home/santiago/Dropbox/Lang2views/Client Projects/TheFireArmGuy/Shorts/",
        "Long_Format": "/home/santiago/Dropbox/Lang2views/Client Projects/Long Format/",
        "trello_board_id": "64c709c04259bef49a00c5de",
        "trello_dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
        "trello_longformat_list_id": "65b7c56bbbbb8c9b0bff06a5",
        "trello_longformat_script_field_ID": "64ca69028b331b036679c2ab",
        "trello_shorts_list_id": "65b7c56bbbbb8c9b0bff06a5",
        "trello_short_script_field_id": "6537d7173e68b703e6327632",
        "trello_short_tamplate_id": "64ca6c0f94fc3cee563f130b",
        "trello_longformat_template_id": "",
        "trello_new_card_id": "",
    },
}

yt_video = {
    "YouTubeVideoInfo": {
        "title": "",
        "video_type": "",
        "channel_name": "",
        "downloaded_video_name": "",
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
    },
    "VideoTrelloInfo": {
        "DatePublished": "",
        "OriginalVideoLink": "",
        "VideoLength": "",
        "TranslatedScript": "",
    },
}


def convert_YouTube_duration_to_seconds(duration):
    day_time = duration.split("T")
    day_duration = day_time[0].replace("P", "")
    day_list = day_duration.split("D")
    if len(day_list) == 2:
        day = int(day_list[0]) * 60 * 60 * 24
        day_list = day_list[1]
    else:
        day = 0
        day_list = day_list[0]
    hour_list = day_time[1].split("H")
    if len(hour_list) == 2:
        hour = int(hour_list[0]) * 60 * 60
        hour_list = hour_list[1]
    else:
        hour = 0
        hour_list = hour_list[0]
    minute_list = hour_list.split("M")
    if len(minute_list) == 2:
        minute = int(minute_list[0]) * 60
        minute_list = minute_list[1]
    else:
        minute = 0
        minute_list = minute_list[0]
    second_list = minute_list.split("S")
    if len(second_list) == 2:
        second = int(second_list[0])
    else:
        second = 0
    return day + hour + minute + second


class Lang2views:
    def __init__(self, video_link):
        self.video_link = video_link
        yt_video["YouTubeVideoInfo"]["video_url"] = video_link

        # authenticate for youtube.com
        yt_video["YouTubeVideoInfo"]["id"] = extract.video_id(
            yt_video["YouTubeVideoInfo"]["video_url"]
        )
        self.youtube_auth = build("youtube", "v3", developerKey=keys["youtube_api_key"])
        self.youtube_auth = self.youtube_auth.videos().list(
            part="snippet", id=yt_video["YouTubeVideoInfo"]["id"]
        )
        self.youtube_auth = self.youtube_auth.execute()

        # authenticate for google docs
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", gdocs_scopes)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", gdocs_scopes
            )
            creds = flow.run_local_server(port=0)

        self.gdocs_auth = build("docs", "v1", credentials=creds)

    def check_video_type(self):
        self.youtube_auth_content_det = build(
            "youtube", "v3", developerKey=keys["youtube_api_key"]
        )
        self.youtube_auth_content_det = self.youtube_auth_content_det.videos().list(
            part="contentDetails", id=yt_video["YouTubeVideoInfo"]["id"]
        )
        self.youtube_auth_content_det = self.youtube_auth_content_det.execute()

        dur = self.youtube_auth_content_det["items"][0]["contentDetails"]["duration"]

        if convert_YouTube_duration_to_seconds(dur) >= 60:
            yt_video["YouTubeVideoInfo"]["video_type"] = "Long_Format"
            self.video_type = "Long_Format"
        else:
            self.video_type = "Shorts"
            yt_video["YouTubeVideoInfo"]["video_type"] = "Shorts"

    def get_channel_name(self):
        self.youtube_auth_content_det = build(
            "youtube", "v3", developerKey=keys["youtube_api_key"]
        )
        self.youtube_auth_content_det = self.youtube_auth_content_det.videos().list(
            part="snippet", id=yt_video["YouTubeVideoInfo"]["id"]
        )

        yt_video["YouTubeVideoInfo"][
            "channel_name"
        ] = self.youtube_auth_content_det.execute()["items"][0]["snippet"][
            "channelTitle"
        ]

        self.creator_name = self.youtube_auth_content_det.execute()["items"][0][
            "snippet"
        ]["channelTitle"]

    def set_video_title(self):
        yt_video["YouTubeVideoInfo"]["title"] = self.youtube_auth["items"][0][
            "snippet"
        ]["title"]

    def set_video_description(self):
        yt_video["YouTubeVideoInfo"]["description"] = self.youtube_auth["items"][0][
            "snippet"
        ]["description"]

    def set_video_tags(self):
        yt_video["YouTubeVideoInfo"]["tags"] = self.youtube_auth["items"][0]["snippet"][
            "tags"
        ]

    def set_video_number(self):
        shorts_folders = os.listdir(creator[self.creator_name][self.video_type])
        shorts_folders = sorted(shorts_folders)
        video_number = str(shorts_folders[-1][0:2])
        yt_video["YouTubeVideoInfo"]["video_number"] = video_number

    def create_dropbox_video_folder(self):
        path = creator[self.creator_name][self.video_type]
        # print(
        #     'cp -r "'
        #     + path
        #     + '00. Template Folder"'
        #     + ' "'
        #     + path
        #     + yt_video["video_number"]
        #     + ". "
        #     + yt_video["title"]
        #     + '"'
        # )
        shutil.copytree(
            path + "00. Template Folder",
            path
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["title"],
        )
        # os.popen(
        #     'cp -r "'
        #     + path
        #     + '00. Template Folder"'
        #     + ' "'
        #     + path
        #     + yt_video["video_number"]
        #     + ". "
        #     + yt_video["title"]
        #     + '"'
        # )

    def download_video(self):
        output_path = (
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/"
            + "Original Video"
        )

        yt = YouTube(yt_video["YouTubeVideoInfo"]["video_url"])
        video_stream = yt.streams.get_highest_resolution()
        video_stream.download(output_path)

    def convert_video_to_audio(self):
        yt_video["YouTubeVideoInfo"]["downloaded_video_name"] = os.listdir(
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/"
            + "Original Video"
        )[0]

        clip = mp.VideoFileClip(
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/"
            + "Original Video/"
            + yt_video["YouTubeVideoInfo"]["downloaded_video_name"]
        )
        clip.audio.write_audiofile(
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/Sound Design/Background/"
            + yt_video["YouTubeVideoInfo"]["downloaded_video_name"]
            + "_audio_only.mp3"
        )

    def transcribe_video(self):
        model = whisper.load_model("base")
        result = model.transcribe(
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/Sound Design/Background/"
            + yt_video["YouTubeVideoInfo"]["downloaded_video_name"]
            + "_audio_only.mp3"
        )
        yt_video["YouTubeVideoInfo"]["script"] = result["text"]

    def count_video_length(self):
        audio = MP3(
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/Sound Design/Background/"
            + yt_video["YouTubeVideoInfo"]["downloaded_video_name"]
            + "_audio_only.mp3"
        )
        yt_video["length"] = audio.info.length

    def save_video_info(self):
        path = (
            creator[self.creator_name][self.video_type]
            + yt_video["YouTubeVideoInfo"]["video_number"]
            + ". "
            + yt_video["YouTubeVideoInfo"]["title"]
            + "/"
        )
        with open(path + "video_info.json", "w") as outfile:
            json.dump(yt_video, outfile)

    def gdoc_set_doc_title(self):
        body = {
            "title": yt_video["YouTubeVideoInfo"]["video_number"]
            + yt_video["YouTubeVideoInfo"]["title"]
            + " - Script"
        }
        doc = self.gdocs_auth.documents().create(body=body).execute()
        title = doc.get("title")
        self.video_script_doc_id = doc.get("documentId")
        yt_video["YouTubeVideoInfo"][
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
                    "text": yt_video["YouTubeVideoInfo"]["script"],
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

    def trello_create_from_template(self):
        # def clone_trello_card(name, list_id, card_id):
        url = "https://api.trello.com/1/cards"

        headers = {"Accept": "application/json"}

        query = {
            "key": keys["trello_api_key"],
            "token": keys["trello_token"],
            "dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
            "idCardSource": creator[self.creator_name]["trello_short_tamplate_id"],
            "idList": creator[self.creator_name]["trello_shorts_list_id"],
            "keepFromSource": "checklists,attachments,stickers,members,labels,customFields",
            "name": yt_video["YouTubeVideoInfo"]["title"],
        }

        response = requests.request("POST", url, headers=headers, params=query)
        print(json.loads(response.text))
        yt_video["YouTubeVideoInfo"]["trello_card_id"] = json.loads(response.text)["id"]

    def trello_get_card_info(self):
        # This code sample uses the 'requests' library:
        # http://docs.python-requests.org
        import requests
        import json

        url = (
            "https://api.trello.com/1/cards/"
            + yt_video["YouTubeVideoInfo"]["trello_card_id"]
        )

        headers = {"Accept": "application/json"}

        query = {
            "key": keys["trello_api_key"],
            "token": keys["trello_token"],
            "customFieldItems": "true",
        }

        response = requests.request("GET", url, headers=headers, params=query)

        print(
            json.dumps(
                json.loads(response.text),
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
            )
        )

    def trello_update_custom_field():
        url = (
            "https://api.trello.com/1/cards/"
            + yt_video["YouTubeVideoInfo"]["trello_card_id"]
            + "/customField/64ca69028b331b036679c2ab/item"
        )

        headers = {"Content-Type": "application/json"}

        query = {
            "key": "507e54976cbef96c4b8e1b5b883f4639",
            "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
        }

        payload = json.dumps(
            {"value": {"text": yt_video["YouTubeVideoInfo"]["script_url"]}}
        )

        response = requests.request(
            "PUT", url, data=payload, headers=headers, params=query
        )
        print(response.text)


def main():

    document_id = ""
    all_in_same_socument = ""
    translated_video = Lang2views("https://www.youtube.com/shorts/9NfoKkcYoaE")

    translated_video.check_video_type()
    translated_video.get_channel_name()
    # translated_video.set_video_title()
    # translated_video.set_video_description()
    # translated_video.set_video_tags()
    # translated_video.set_video_number()
    # translated_video.create_dropbox_video_folder()
    # translated_video.download_video()
    # translated_video.convert_video_to_audio()
    # translated_video.transcribe_video()
    # translated_video.count_video_length()
    # translated_video.save_video_info()
    # translated_video.gdoc_set_doc_title()
    # translated_video.gdoc_set_script()
    # translated_video.check_video_type()
    translated_video.trello_create_from_template()
    translated_video.trello_get_card_info()
    # print(yt_video)


if __name__ == "__main__":
    main()
