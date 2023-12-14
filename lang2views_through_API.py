#!/usr/bin/env python
# coding=utf-8

# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import io

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pytube import YouTube

from googleapiclient.http import MediaIoBaseDownload

scopes = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]


def main():
    # # Disable OAuthlib's HTTPS verification when running locally.
    # # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # api_service_name = "youtube"
    # api_version = "v3"
    # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

    # # Get credentials and create an API client
    # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    #     client_secrets_file, scopes
    # )
    # credentials = flow.run_local_server(port=0)

    # youtube = googleapiclient.discovery.build(
    #     api_service_name, api_version, credentials=credentials
    # )

    # request = youtube.videos().list(part="snippet", id="MUDNnIbwSNo")
    # response = request.execute()

    # print("This is the whole response")
    # print(response["items"][0]["snippet"]["tags"])

    # print("this is the title")
    # print(response["items"][0]["snippet"]["title"])

    # print("this is the description")
    # print(response["items"][0]["snippet"]["description"])

    # print("these is the tags")
    # print(response["items"][0]["snippet"]["tags"])

    # # print("the captions are being downloaded")
    # # request = youtube.captions().download(id="yNhJTXABEg0", tfmt="srt")

    # # fh = io.FileIO("YOUR_FILE", "wb")

    # # download = MediaIoBaseDownload(fh, request)
    # # complete = False
    # # while not complete:
    # #     status, complete = download.next_chunk()

    # from pytube import YouTube

    # def download_youtube_video(url, output_path="."):
    #     try:
    #         # Create a YouTube object
    #         yt = YouTube(url)

    #         # Get the highest resolution stream
    #         video_stream = yt.streams.get_highest_resolution()

    #         # Download the video
    #         print(f"Downloading: {yt.title}")
    #         video_stream.download(output_path)
    #         print("Download complete!")

    #     except Exception as e:
    #         print(f"Error: {str(e)}")

    # # Example usage
    # url = "https://www.youtube.com/shorts/FBk36cXzkOU"
    # output_path = "/home/santiago/Documents/lang2views_project"
    # download_youtube_video(url, output_path)

    #     import whisper
    #     from stable_whisper import modify_model
    #     from stable_whisper import load_model
    #     import json
    #     import whisper
    #     from youtube_transcript_api import YouTubeTranscriptApi
    #     from pytube import YouTube, Caption, captions, CaptionQuery
    #     import pytube
    #
    #     model = whisper.load_model("base")
    #     result = model.transcribe("angelito.mp4")
    #     translate = model.transcribe("angelito.mp4", task="translate")
    #     print(result["text"])
    #     text = result["text"]
    #

    # import os.path

    # from google.auth.transport.requests import Request
    # from google.oauth2.credentials import Credentials
    # from google_auth_oauthlib.flow import InstalledAppFlow
    # from googleapiclient.discovery import build
    # from googleapiclient.errors import HttpError

    # # If modifying these scopes, delete the file token.json.
    # SCOPES = ["https://www.googleapis.com/auth/documents.readonly"]

    # # The ID of a sample document.
    # DOCUMENT_ID = "195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE"

    # """Shows basic usage of the Docs API.
    #   Prints the title of a sample document.
    #   """
    # creds = None
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists("token.json"):
    #     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open("token.json", "w") as token:
    #         token.write(creds.to_json())

    # try:
    #     service = build("docs", "v1", credentials=creds)

    #     # Retrieve the documents contents from the Docs service.
    #     document = service.documents().get(documentId=DOCUMENT_ID).execute()

    #     print(f"The title of the document is: {document.get('title')}")
    # except HttpError as err:
    #     print(err)

    # import requests

    # This code sample uses the 'requests' library:
    # http://docs.python-requests.org
    import requests
    import json

    # url = "https://api.trello.com/1/lists"

    # query = {
    #     "name": "{Long Format Video Localization}",
    #     "idBoard": "651200fe3757fd7b8aec8f06",
    #     "key": "507e54976cbef96c4b8e1b5b883f4639",
    #     "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
    # }

    # response = requests.request("POST", url, params=query)

    # print(response.text)

    url = "https://api.trello.com/1/cards"

    headers = {"Accept": "application/json"}

    # query = {
    #     "idList": "657b55f47eb6bf3aede6aa9d",
    #     "key": "507e54976cbef96c4b8e1b5b883f4639",
    #     "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
    # }

    # query = {
    #     "idCardSource": "6371a8b401c60500e4c97a07",
    #     "idList": "637182618bef42008339d7cf",
    #     "name": "Hello",
    #     "keepFromSource": "checklists,attachments,stickers,members,labels,customFields",
    #     "dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
    # }

    # query = {
    #     "key": "507e54976cbef96c4b8e1b5b883f4639",
    #     "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
    #     "dsc": "d6d31c3e05df5ae75e15f18f7fd38a00cc0eff6209a01b43b36fbfd88df3dbac",
    #     "idCardSource": "65121053765103ab051fb04a",
    #     "idList": "657b55f47eb6bf3aede6aa9d",
    #     "keepFromSource": "checklists,attachments,stickers,members,labels,customFields",
    #     "name": "Test Template",
    # }

    # response = requests.request("POST", url, headers=headers, params=query)

    # print(
    #     json.dumps(
    #         json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")
    #     )
    # )

    # url = "https://api.trello.com/1/cards/657b59e05a409420e8685702/customField/65120a445fd7a02ace295fc1/item"

    # headers = {"Content-Type": "application/json"}

    # query = {
    #     "key": "507e54976cbef96c4b8e1b5b883f4639",
    #     "token": "ATTAc46e0dc1e8b73744994a0538e89bf048d7a1ea0f6a515563a839233e7abdeeb7635B82D5",
    # }

    # payload = json.dumps({"value": {"text": "Update custom field test"}})

    # response = requests.request("PUT", url, data=payload, headers=headers, params=query)
    # print(response.text)

    import re

    # prankmelater_parent_dir = "/home/santiago/Dropbox/Lang2views/Client Projects/Adley - Prank Me Later/Shorts/"
    # month_dir = "4. January"
    # os.mkdir(prankmelater_parent_dir + month_dir)
    # print("directory opened")
    video_link = "https://www.youtube.com/watch?v=8P1p7coSVhU&t=94s"
    video_id = video_link.split("v=")
    print(video_id)
    video_id = re.search(
        "/^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/|shorts\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/",
        video_link,
    )
    print(video_id)

    from urllib.parse import urlparse

    url_data = urlparse("http://www.youtube.com/watch?v=z_AbfPXTKms&NR=1")
    query = urlparse.parse_qs(url_data.query)
    video = query["v"][0]
    print(video)


if __name__ == "__main__":
    main()
